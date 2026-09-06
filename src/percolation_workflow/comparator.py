from __future__ import annotations

import re
import json
import hashlib
import subprocess
from dataclasses import dataclass, field
from pathlib import Path
from pathlib import PurePosixPath
from collections.abc import Mapping
from typing import Any


_CANDIDATE_SCHEMA_VERSION = 1
_SHA256 = re.compile(r"^[0-9a-f]{64}$")
_NAME = re.compile(r"^[A-Za-z_][A-Za-z0-9_']*(?:\.[A-Za-z_][A-Za-z0-9_']*)*$")


def normalized_statement(text: str) -> str:
    """Conservative comparator normalization; semantic equality remains Lean's job."""
    return re.sub(r"\s+", " ", text).strip()


def compare_statement(challenge: str | Path, solution: str | Path) -> bool:
    """Compare the declared theorem surface before invoking an external comparator.

    This is intentionally not a parser or proof checker. It only catches accidental drift in the
    statement files; the final result must still come from the project's comparator and Lean build.
    """
    left = normalized_statement(Path(challenge).read_text(encoding="utf-8"))
    right = normalized_statement(Path(solution).read_text(encoding="utf-8"))
    return left == right


def validate_source_files(values) -> tuple[str, ...]:
    """Validate explicit non-Lean inputs that the comparator depends on.

    Globs are deliberately rejected: a receipt must identify a closed set of
    source inputs whose hashes can be replayed by registry freshness checks.
    """
    if values is None:
        return ()
    if not isinstance(values, (list, tuple)):
        raise ValueError('comparator source_files must be a list')
    result = []
    for value in values:
        if not isinstance(value, str) or not value.strip():
            raise ValueError('comparator source_files must contain nonempty strings')
        relative = PurePosixPath(value)
        if (relative.is_absolute() or '..' in relative.parts or '\\' in value
                or relative == PurePosixPath('.') or relative.name != value.split('/')[-1]):
            raise ValueError('comparator source_files contains an unsafe path')
        normalized = relative.as_posix()
        if normalized not in result:
            result.append(normalized)
    return tuple(result)


@dataclass(frozen=True)
class CandidateReceiptAudit:
    """Pure audit result for a sidecar candidate receipt.

    ``accepted`` means only that the candidate contains complete,
    coordinator-bound evidence.  It is deliberately not a registry or
    ``EvidenceStage`` transition.  A legacy receipt normally becomes
    ``pending`` when its missing coordinator bindings are supplied later;
    malformed or stale data is ``rejected``.
    """

    status: str
    reasons: tuple[str, ...] = ()
    receipt: dict[str, Any] = field(default_factory=dict)
    manifest: dict[str, Any] | None = None

    @property
    def accepted(self) -> bool:
        return self.status == "accepted"

    @property
    def pending(self) -> bool:
        return self.status == "pending"

    @property
    def rejected(self) -> bool:
        return self.status == "rejected"

    def __bool__(self) -> bool:
        return self.accepted

    def __getitem__(self, key: str):
        """Small mapping-compatible surface for callers using dict results."""
        return self.to_dict()[key]

    def get(self, key: str, default=None):
        return self.to_dict().get(key, default)

    def to_dict(self) -> dict[str, Any]:
        return {
            "status": self.status,
            "accepted": self.accepted,
            "pending": self.pending,
            "rejected": self.rejected,
            "reasons": list(self.reasons),
            "receipt": dict(self.receipt),
            "manifest": None if self.manifest is None else dict(self.manifest),
        }


def _canonical_json(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True,
                      separators=(",", ":")).encode("utf-8")


def _sha256(value: Any) -> str:
    return hashlib.sha256(_canonical_json(value)).hexdigest()


def _is_sha256(value: Any) -> bool:
    return isinstance(value, str) and bool(_SHA256.fullmatch(value))


def _nonempty_string(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _hash_map(value: Any, field_name: str, reasons: list[str]) -> dict[str, str] | None:
    if not isinstance(value, Mapping) or not value:
        reasons.append(f"{field_name} is missing or not a nonempty object")
        return None
    result: dict[str, str] = {}
    for key, digest in value.items():
        if not _nonempty_string(key) or not _is_sha256(digest):
            reasons.append(f"{field_name} contains an invalid path/hash entry")
            continue
        result[str(key)] = digest
    return result


def _sorted_unique_ids(value: Any, field_name: str, reasons: list[str]) -> list[str] | None:
    if not isinstance(value, list) or any(not _nonempty_string(item) for item in value):
        reasons.append(f"dag_binding.{field_name} must be a list of nonempty IDs")
        return None
    ids = [str(item) for item in value]
    if len(ids) != len(set(ids)):
        reasons.append(f"dag_binding.{field_name} contains duplicate IDs")
    if ids != sorted(ids):
        reasons.append(f"dag_binding.{field_name} must be sorted")
    return ids


def _binding(value: Any, reasons: list[str], *, field_name: str = "dag_binding") -> dict[str, Any] | None:
    if not isinstance(value, Mapping):
        reasons.append(f"{field_name} is missing or not an object")
        return None
    node_id = value.get("node_id")
    parent_id = value.get("parent_id")
    if not _nonempty_string(node_id):
        reasons.append(f"{field_name}.node_id is missing")
    if parent_id is not None and not _nonempty_string(parent_id):
        reasons.append(f"{field_name}.parent_id must be a nonempty ID or null")
    child_ids = _sorted_unique_ids(value.get("child_ids"), "child_ids", reasons)
    dependency_ids = _sorted_unique_ids(value.get("dependency_ids"), "dependency_ids", reasons)
    if child_ids is not None and node_id in child_ids:
        reasons.append(f"{field_name}.child_ids contains its own node_id")
    if dependency_ids is not None and node_id in dependency_ids:
        reasons.append(f"{field_name}.dependency_ids contains its own node_id")
    if parent_id == node_id:
        reasons.append(f"{field_name}.parent_id points to its own node_id")
    if not _nonempty_string(node_id) or child_ids is None or dependency_ids is None:
        return None
    return {"node_id": str(node_id), "parent_id": None if parent_id is None else str(parent_id),
            "child_ids": child_ids, "dependency_ids": dependency_ids}


def _snapshot_nodes(snapshot: Any, reasons: list[str]) -> tuple[dict[str, dict[str, Any]], str | None] | None:
    """Normalize an authoritative DAG snapshot without consulting receipt text."""
    explicit_digest = None
    raw_nodes: Any = snapshot
    if isinstance(snapshot, Mapping):
        explicit_digest = snapshot.get("dag_snapshot_sha256", snapshot.get("sha256"))
        if explicit_digest is not None and not _is_sha256(explicit_digest):
            reasons.append("authoritative DAG snapshot has an invalid sha256")
        if "nodes" in snapshot:
            raw_nodes = snapshot["nodes"]
        elif "node_id" in snapshot:
            raw_nodes = [snapshot]
    if isinstance(raw_nodes, Mapping):
        entries = []
        for key, value in raw_nodes.items():
            if not isinstance(value, Mapping):
                reasons.append("authoritative DAG node is not an object")
                continue
            entry = dict(value)
            entry.setdefault("node_id", key)
            entries.append(entry)
    elif isinstance(raw_nodes, list):
        entries = raw_nodes
    else:
        reasons.append("authoritative DAG snapshot requires a nodes object or list")
        return None
    nodes: dict[str, dict[str, Any]] = {}
    for entry in entries:
        if not isinstance(entry, Mapping):
            reasons.append("authoritative DAG node is not an object")
            continue
        local_reasons: list[str] = []
        normalized = _binding(entry, local_reasons, field_name="DAG node binding")
        reasons.extend(local_reasons)
        if normalized is None:
            continue
        node_id = normalized["node_id"]
        if node_id in nodes:
            reasons.append(f"authoritative DAG has duplicate node_id: {node_id}")
        else:
            nodes[node_id] = normalized
    if not nodes:
        reasons.append("authoritative DAG snapshot has no valid nodes")
        return None
    if explicit_digest is None:
        explicit_digest = _sha256({"nodes": {key: nodes[key] for key in sorted(nodes)}})
    return nodes, explicit_digest


def _receipt_self_hash(receipt: Mapping[str, Any]) -> str:
    unsigned = dict(receipt)
    for key in ("receipt_sha256", "receipt_self_sha256", "self_sha256"):
        unsigned.pop(key, None)
    return _sha256(unsigned)


def _axiom_report(value: Any, field_name: str, reasons: list[str]) -> dict[str, tuple[str, ...]] | None:
    if not isinstance(value, Mapping) or not value:
        reasons.append(f"{field_name} is missing or not a nonempty object")
        return None
    report: dict[str, tuple[str, ...]] = {}
    for theorem, axioms in value.items():
        if not _nonempty_string(theorem) or not isinstance(axioms, (list, tuple)):
            reasons.append(f"{field_name} contains an invalid theorem report")
            continue
        if any(not _nonempty_string(axiom) for axiom in axioms):
            reasons.append(f"{field_name} contains an invalid axiom name")
            continue
        normalized = tuple(str(axiom) for axiom in axioms)
        if len(set(normalized)) != len(normalized):
            reasons.append(f"{field_name} contains duplicate axioms")
            continue
        report[str(theorem)] = normalized
    return report


def _comparator_evidence(candidate: Mapping[str, Any], reasons: list[str],
                         pending: list[str]) -> None:
    """Require the same standalone acceptance line used by ``run_comparator``."""
    status = candidate.get("comparator_status")
    if status is None:
        pending.append("missing comparator_status")
    elif status != "accepted":
        if status == "pending":
            pending.append("comparator acceptance is still pending")
        else:
            reasons.append("comparator_status must be accepted or pending")
        return
    command = candidate.get("comparator_command")
    if not isinstance(command, list) or not command or any(not isinstance(part, str) for part in command):
        if status == "accepted":
            reasons.append("accepted comparator evidence requires comparator_command")
        else:
            pending.append("missing comparator_command")
    stdout = candidate.get("comparator_stdout")
    stderr = candidate.get("comparator_stderr")
    if not isinstance(stdout, str) or not isinstance(stderr, str):
        if status == "accepted":
            reasons.append("accepted comparator evidence requires comparator output")
        else:
            pending.append("missing comparator output")
        return
    if "Your solution is okay!" not in (stdout + "\n" + stderr).splitlines():
        if status == "accepted":
            reasons.append("comparator output lacks the exact acceptance line")
        else:
            pending.append("comparator exact acceptance line is pending")


def validate_candidate_receipt(
    receipt: Mapping[str, Any],
    dag_snapshot: Any = None,
    *,
    expected_statement_identity: Mapping[str, Any] | None = None,
    expected_dag_binding: Mapping[str, Any] | None = None,
    expected_dag_snapshot_sha256: str | None = None,
    expected_source_hashes: Mapping[str, str] | None = None,
    expected_olean_hashes: Mapping[str, str] | None = None,
    expected_lean_toolchain: str | None = None,
    expected_mathlib_commit: str | None = None,
    expected_axioms: Mapping[str, Any] | None = None,
) -> CandidateReceiptAudit:
    """Validate a compiled-candidate sidecar against coordinator-owned bindings.

    This is deliberately pure: it reads no files, updates no workflow state,
    and never calls Lean or a comparator.  Comparator acceptance and registry
    promotion remain separate gates: even an accepted audit result is emitted
    by ``build_comparator_manifest`` as a ``compiled_candidate`` with
    ``registry_status=pending``.

    Missing authoritative context is ``pending``.  Explicit malformed data,
    stale hashes, duplicate/unsorted edges, and dangling DAG references are
    ``rejected``.  This makes legacy receipts safe to retain without treating
    their absent fields as proof of validity.
    """
    if not isinstance(receipt, Mapping):
        return CandidateReceiptAudit("rejected", ("candidate receipt must be an object",))
    candidate = dict(receipt)
    reasons: list[str] = []
    pending: list[str] = []

    schema = candidate.get("schema_version")
    if schema is None:
        pending.append("missing schema_version")
    elif schema != _CANDIDATE_SCHEMA_VERSION:
        reasons.append("unsupported candidate receipt schema_version")
    if candidate.get("status") != "compiled_candidate":
        if "status" not in candidate:
            pending.append("missing compiled candidate status")
        else:
            reasons.append("candidate receipt status must be compiled_candidate")

    identity = candidate.get("statement_identity")
    if not isinstance(identity, Mapping):
        pending.append("missing statement_identity")
    else:
        required_identity = ("module", "name", "statement_sha256")
        if any(not _nonempty_string(identity.get(key)) for key in required_identity):
            reasons.append("statement_identity is incomplete")
        elif not _NAME.fullmatch(identity["module"]):
            reasons.append("statement_identity.module is invalid")
        elif not _NAME.fullmatch(identity["name"]):
            reasons.append("statement_identity.name is not fully qualified")
        if not _is_sha256(identity.get("statement_sha256")):
            reasons.append("statement_identity.statement_sha256 is invalid")
        if "challenge_sha256" in identity and not _is_sha256(identity["challenge_sha256"]):
            reasons.append("statement_identity.challenge_sha256 is invalid")
        if expected_statement_identity is None:
            pending.append("statement_identity is not bound to an authoritative statement")
        else:
            for key, expected in expected_statement_identity.items():
                if identity.get(key) != expected:
                    reasons.append(f"statement_identity mismatch: {key}")

    if "dag_binding" not in candidate:
        binding = None
        pending.append("missing dag_binding")
    else:
        binding = _binding(candidate.get("dag_binding"), reasons)
    if binding is not None:
        if expected_dag_binding is not None:
            expected_reasons: list[str] = []
            normalized_expected = _binding(expected_dag_binding, expected_reasons,
                                           field_name="expected_dag_binding")
            reasons.extend(expected_reasons)
            if normalized_expected is not None and binding != normalized_expected:
                reasons.append("dag_binding mismatch")
        elif dag_snapshot is None:
            pending.append("dag_binding is not bound to an authoritative DAG snapshot")

    dag_digest = candidate.get("dag_snapshot_sha256")
    if dag_digest is None:
        pending.append("missing dag_snapshot_sha256")
    elif not _is_sha256(dag_digest):
        reasons.append("dag_snapshot_sha256 is invalid")

    snapshot_nodes = None
    snapshot_digest = expected_dag_snapshot_sha256
    if dag_snapshot is not None:
        parsed_snapshot = _snapshot_nodes(dag_snapshot, reasons)
        if parsed_snapshot is not None:
            snapshot_nodes, parsed_digest = parsed_snapshot
            if snapshot_digest is None:
                snapshot_digest = parsed_digest
            elif parsed_digest != snapshot_digest:
                reasons.append("authoritative DAG snapshot hash disagrees with expected hash")
    elif snapshot_digest is None:
        pending.append("missing authoritative DAG snapshot hash")
    if snapshot_digest is not None and not _is_sha256(snapshot_digest):
        reasons.append("expected DAG snapshot hash is invalid")
    if dag_digest is not None and snapshot_digest is not None and dag_digest != snapshot_digest:
        reasons.append("dag_snapshot_sha256 mismatch")

    if binding is not None and snapshot_nodes is not None:
        if binding["node_id"] not in snapshot_nodes:
            reasons.append("dag_binding has a dangling node_id")
        else:
            authoritative = snapshot_nodes[binding["node_id"]]
            if binding != authoritative:
                reasons.append("dag_binding does not match authoritative DAG node")
        universe = set(snapshot_nodes)
        refs = ([binding["parent_id"]] if binding["parent_id"] is not None else [])
        refs += binding["child_ids"] + binding["dependency_ids"]
        dangling = sorted(set(refs) - universe)
        if dangling:
            reasons.append("dag_binding has dangling references: " + ", ".join(dangling))
    elif binding is not None and snapshot_nodes is None:
        pending.append("DAG node universe is unavailable for dangling-reference checks")

    if "source_hashes" not in candidate:
        pending.append("missing source_hashes")
        source_hashes = None
    else:
        source_hashes = _hash_map(candidate.get("source_hashes"), "source_hashes", reasons)
    if "olean_hashes" not in candidate:
        pending.append("missing olean_hashes")
        olean_hashes = None
    else:
        olean_hashes = _hash_map(candidate.get("olean_hashes"), "olean_hashes", reasons)
    if source_hashes is not None:
        if expected_source_hashes is None:
            pending.append("source_hashes are not bound to an authoritative source snapshot")
        elif dict(expected_source_hashes) != source_hashes:
            reasons.append("source_hashes mismatch")
    if olean_hashes is not None:
        if expected_olean_hashes is None:
            pending.append("olean_hashes are not bound to an authoritative OLean snapshot")
        elif dict(expected_olean_hashes) != olean_hashes:
            reasons.append("olean_hashes mismatch")

    lean_toolchain = candidate.get("lean_toolchain", candidate.get("toolchain"))
    if not _nonempty_string(lean_toolchain):
        pending.append("missing lean_toolchain pin")
    elif expected_lean_toolchain is None:
        pending.append("lean_toolchain is not bound to the expected pin")
    elif lean_toolchain != expected_lean_toolchain:
        reasons.append("lean_toolchain mismatch")

    mathlib_commit = candidate.get("mathlib_commit")
    if not _nonempty_string(mathlib_commit):
        pending.append("missing mathlib_commit pin")
    elif expected_mathlib_commit is None:
        pending.append("mathlib_commit is not bound to the expected pin")
    elif mathlib_commit != expected_mathlib_commit:
        reasons.append("mathlib_commit mismatch")

    if "axioms" not in candidate:
        axioms = None
        pending.append("missing axiom report")
    else:
        axioms = _axiom_report(candidate.get("axioms"), "axioms", reasons)
    strict = candidate.get("strict_admission")
    if not isinstance(strict, Mapping):
        pending.append("missing strict_admission report")
    else:
        if strict.get("accepted") is not True:
            reasons.append("strict_admission was not accepted")
        if "axioms" not in strict:
            strict_axioms = None
            pending.append("missing strict_admission.axioms report")
        else:
            strict_axioms = _axiom_report(strict.get("axioms"), "strict_admission.axioms", reasons)
        if axioms is not None and strict_axioms is not None and axioms != strict_axioms:
            reasons.append("axiom report disagrees with strict_admission")
        strict_toolchain = strict.get("toolchain")
        if strict_toolchain is not None and strict_toolchain != lean_toolchain:
            reasons.append("strict_admission toolchain mismatch")
    if axioms is not None:
        if expected_axioms is None:
            pending.append("axiom report is not bound to expected axioms")
        else:
            expected_reasons: list[str] = []
            normalized_expected_axioms = _axiom_report(expected_axioms, "expected_axioms", expected_reasons)
            reasons.extend(expected_reasons)
            if normalized_expected_axioms is not None and axioms != normalized_expected_axioms:
                reasons.append("axiom report mismatch")

    _comparator_evidence(candidate, reasons, pending)

    self_hashes = [candidate.get(key) for key in
                   ("receipt_sha256", "receipt_self_sha256", "self_sha256")
                   if candidate.get(key) is not None]
    if not self_hashes:
        pending.append("missing receipt self-hash")
    elif len(set(self_hashes)) != 1 or not _is_sha256(self_hashes[0]):
        reasons.append("receipt self-hash is invalid or inconsistent")
    elif self_hashes[0] != _receipt_self_hash(candidate):
        reasons.append("receipt self-hash mismatch")

    if reasons:
        return CandidateReceiptAudit("rejected", tuple(dict.fromkeys(reasons)), candidate)
    if pending:
        return CandidateReceiptAudit("pending", tuple(dict.fromkeys(pending)), candidate)
    return CandidateReceiptAudit("accepted", (), candidate)


def build_comparator_manifest(
    receipt: Mapping[str, Any],
    dag_snapshot: Any = None,
    *,
    expected_statement_identity: Mapping[str, Any] | None = None,
    expected_dag_binding: Mapping[str, Any] | None = None,
    expected_dag_snapshot_sha256: str | None = None,
    expected_source_hashes: Mapping[str, str] | None = None,
    expected_olean_hashes: Mapping[str, str] | None = None,
    expected_lean_toolchain: str | None = None,
    expected_mathlib_commit: str | None = None,
    expected_axioms: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    """Return a normalized comparator candidate manifest, or explicit pending/rejected data."""
    audit = validate_candidate_receipt(
        receipt, dag_snapshot,
        expected_statement_identity=expected_statement_identity,
        expected_dag_binding=expected_dag_binding,
        expected_dag_snapshot_sha256=expected_dag_snapshot_sha256,
        expected_source_hashes=expected_source_hashes,
        expected_olean_hashes=expected_olean_hashes,
        expected_lean_toolchain=expected_lean_toolchain,
        expected_mathlib_commit=expected_mathlib_commit,
        expected_axioms=expected_axioms,
    )
    if not audit.accepted:
        return {
            "schema_version": _CANDIDATE_SCHEMA_VERSION,
            "status": audit.status,
            "candidate_status": receipt.get("status") if isinstance(receipt, Mapping) else None,
            "comparator_status": "pending",
            "registry_status": "pending",
            "reasons": list(audit.reasons),
            "receipt": dict(receipt) if isinstance(receipt, Mapping) else None,
        }
    candidate = audit.receipt
    return {
        "schema_version": _CANDIDATE_SCHEMA_VERSION,
        "status": "compiled_candidate",
        "candidate_status": "compiled_candidate",
        "comparator_status": candidate.get("comparator_status", "pending"),
        "registry_status": "pending",
        "statement_identity": dict(candidate["statement_identity"]),
        "dag_binding": dict(candidate["dag_binding"]),
        "dag_snapshot_sha256": candidate["dag_snapshot_sha256"],
        "source_hashes": dict(candidate["source_hashes"]),
        "olean_hashes": dict(candidate["olean_hashes"]),
        "receipt_sha256": next(candidate[key] for key in
                               ("receipt_sha256", "receipt_self_sha256", "self_sha256")
                               if key in candidate),
        "lean_toolchain": candidate["lean_toolchain"],
        "mathlib_commit": candidate["mathlib_commit"],
        "axioms": dict(candidate["axioms"]),
        "strict_admission": dict(candidate["strict_admission"]),
        "comparator_command": list(candidate["comparator_command"]),
        "comparator_stdout": candidate["comparator_stdout"],
        "comparator_stderr": candidate["comparator_stderr"],
    }


@dataclass(frozen=True)
class ComparatorConfig:
    challenge_module: str
    solution_module: str
    theorem_names: tuple[str, ...]
    permitted_axioms: tuple[str, ...] = ()
    enable_nanoda: bool = False
    source_files: tuple[str, ...] = ()
    strict_admission: bool = False


def load_config(path: str | Path) -> ComparatorConfig:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    required = {"challenge_module", "solution_module", "theorem_names"}
    missing = required - data.keys()
    if missing:
        raise ValueError(f"comparator config missing: {sorted(missing)}")
    return ComparatorConfig(data["challenge_module"], data["solution_module"],
                            tuple(data["theorem_names"]), tuple(data.get("permitted_axioms", ())),
                            bool(data.get("enable_nanoda", False)),
                            validate_source_files(data.get('source_files', [])),
                            bool(data.get('strict_admission', False)))


def run_comparator(project_dir: str | Path, command: list[str], *, timeout: float = 3600) -> tuple[bool, str, str]:
    """Require comparator's exact acceptance line as well as exit zero, matching upstream CI.

    The caller must supply the trusted pinned comparator executable and config. This command
    runner does not authenticate arbitrary executables or issue a registry receipt.
    """
    try:
        proc = subprocess.run(command, cwd=project_dir, text=True, encoding="utf-8", errors="replace",
                              capture_output=True, timeout=timeout)
    except OSError as exc:
        return False, '', str(exc)
    except subprocess.TimeoutExpired as exc:
        def decoded(value):
            return value.decode('utf-8', errors='replace') if isinstance(value, bytes) else (value or '')
        return False, decoded(exc.stdout), decoded(exc.stderr) + '\nComparator timed out'
    accepted = 'Your solution is okay!' in (proc.stdout + '\n' + proc.stderr).splitlines()
    return proc.returncode == 0 and accepted, proc.stdout, proc.stderr
