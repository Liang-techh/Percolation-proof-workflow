"""Fail-closed intake and execution for non-Lean research projects.

The Route-B robot project is a useful first external target for the
percolation-style workflow: it already has staged obligations, independent
checkers, historical negatives, and a final fail-closed gate.  This module
adapts that evidence into the persistent DAG without pretending that a Julia,
Python, MATLAB, SOS, or interval result is a Lean theorem.

The only status that can populate ``WorkflowState.registry`` remains
``VERIFIED``.  ``EVIDENCE_COMPLETE`` is a separate dependency-closing status
for an explicitly engineering/audit checker scope, with receipt and source hashes.
Successful mathematical diagnostics never discharge the mathematical obligation.
"""
from __future__ import annotations

import hashlib
import json
import os
import shutil
import sys
from pathlib import Path, PurePosixPath
import subprocess
from typing import Any, Iterable

from .model import NodeStatus, WorkflowState, node_is_closed
from .store import StateStore


EXTERNAL_DOMAIN = "external-research"
INTAKE_SCHEMA = "routeb-6dof-intake-v1"

# These are the research stages from the supplied Route-B brief.  P7 is an
# explicit conditional fallback and is intentionally not on the default
# certificate path; this keeps a failed/obsolete fallback from blocking the
# primary theorem route.
ROUTEB_STAGES: tuple[dict[str, Any], ...] = (
    {
        "name": "P0.reproducibility_baseline",
        "statement": "The Route-B target is reproducible and all selected artifact provenance checks pass.",
        "proof_sketch": "Run robot_final/verify_all.py and retain stdout, stderr, exit code, and source snapshot.",
        "dependencies": [],
        "evidence_level": "engineering_gate",
        "closure_scope": "engineering",
        "claim_status": "open",
        "artifacts": [
            "PROJECT_REFORM_TARGET.md", "PROJECT_REFORM_AUDIT.md",
            "robot_formal_v1/manifest.json", "robot_formal_v1/README.md",
            "robot_final/verify_all.py", "robot_final/routeB_certificate_manifest.toml",
        ],
        "command": ["python", "robot_final/verify_all.py"],
    },
    {
        "name": "P1.bracket_decision",
        "statement": "The selected bracket row is classified by a fail-closed quantified decision gate.",
        "proof_sketch": "Separate falsification candidates from coverage-complete acceptance; preserve negative boxes.",
        "dependencies": ["P0.reproducibility_baseline"],
        "evidence_level": "rigorous_numerical_candidate",
        "claim_status": "unknown_needs_coverage",
        "artifacts": [
            "robot_final/routeB_bracket_decision_gate.csv", "robot_final/P1_BRACKET_DECISION_GATE.md",
            "routeB_dense_Mq/routeB_bracket_decision_gate.csv", "routeB_dense_Mq/P1_BRACKET_DECISION_GATE.md",
        ],
        "command": ["python", "robot_final/verify_solver_metadata.py"],
    },
    {
        "name": "P2.spectral_partition",
        "statement": "The spectral decomposition and partition prioritization are checked against the true target semantics.",
        "proof_sketch": "Use spectral structure only to prioritize boxes; no sampled eigenvalue is a global bound.",
        "dependencies": ["P1.bracket_decision"],
        "evidence_level": "sampled_structure_discovery",
        "claim_status": "diagnostic_only",
        "artifacts": [
            "robot_final/P2_SPECTRAL_ANALYSIS.md", "robot_final/routeB_spectral_summary.csv",
            "routeB_dense_Mq/P2_SPECTRAL_ANALYSIS.md", "routeB_dense_Mq/routeB_spectral_summary.csv",
        ],
        "command": ["python", "robot_final/verify_spectral_analysis.py"],
    },
    {
        "name": "P3.strict_true_dh_bounds",
        "statement": "Strict interval/Taylor enclosures cover the selected true-DH domain, including inverse and C/G guards.",
        "proof_sketch": "Branch boxes until every cell is resolved or fail closed; record unknown and boundary cells.",
        "dependencies": ["P2.spectral_partition"],
        "evidence_level": "rigorous_numerical_local_candidate",
        "claim_status": "open_global_coverage",
        "artifacts": [
            "robot_final/P3_INTERVAL_BOUNDS.md", "robot_final/routeB_interval_bounds.csv",
            "routeB_dense_Mq/P3_INTERVAL_BOUNDS.md", "routeB_dense_Mq/routeB_interval_bounds.csv",
        ],
        "command": ["python", "robot_final/verify_interval_artifacts.py"],
    },
    {
        "name": "P4.residual_schur_pmi",
        "statement": "The actual true-DH residual is absorbed by a strict partitioned matrix Schur/PMI certificate.",
        "proof_sketch": "Inject the residual, preserve its direction, and prove strict PSD on every covered cell.",
        "dependencies": ["P3.strict_true_dh_bounds"],
        "evidence_level": "numerical_candidate",
        "claim_status": "remainder_absorption_open",
        "artifacts": [
            "robot_final/P4_SCHUR_INTERVAL_PROBE.md", "robot_final/P4_RESIDUAL_MATRIX_CERTIFICATE.md",
            "routeB_dense_Mq/P4_SCHUR_INTERVAL_PROBE.md", "routeB_dense_Mq/P4_RESIDUAL_MATRIX_CERTIFICATE.md",
        ],
        "command": ["python", "robot_final/verify_residual_sos_bridge.py"],
    },
    {
        "name": "P5.sparse_disjunctive_sos",
        "statement": "A sparse/disjunctive SOS or exact descriptor certificate closes the finite-horizon residual inequality.",
        "proof_sketch": "Use the fixed Newton-Euler syzygy first, then a direct residual PMI; reject surrogate-only SOS claims.",
        "dependencies": ["P4.residual_schur_pmi"],
        "evidence_level": "exact_algebraic_structure_plus_candidate",
        "claim_status": "candidate_structure_only",
        "artifacts": [
            "routeB_dense_Mq/routeB_compact_corrected_newton_euler_dh_supply_audit.jl",
            "routeB_dense_Mq/routeB_compact_corrected_newton_euler_dh_supply_audit.csv",
            "routeB_dense_Mq/P5_COMPACT_CORRECTED_NEWTON_EULER_DH_SUPPLY_AUDIT.md",
        ],
        "command": ["julia", "routeB_dense_Mq/routeB_compact_corrected_newton_euler_dh_supply_audit.jl"],
    },
    {
        "name": "P6.exact_gram_interval_check",
        "statement": "Printed Gram matrices, polynomial identities, and interval refinements pass exact/high-precision checks.",
        "proof_sketch": "Require exact rational identity and strict PSD/interval margins after rounding; never trust solver OPTIMAL alone.",
        "dependencies": ["P5.sparse_disjunctive_sos"],
        "evidence_level": "algebraic_certificate_candidate",
        "claim_status": "rounded_identity_open",
        "artifacts": ["robot_final/verify_gram_rational.py", "robot_final/routeB_pmi_gram_manifest.csv",
                      "routeB_dense_Mq/routeB_pmi_gram_manifest.csv"],
        "command": ["python", "robot_final/verify_gram_rational.py"],
    },
    {
        "name": "P7.strict_tail_fallback",
        "statement": "If the finite-dimensional route fails, a Carleman/Fourier/Krylov tail bound closes with strict remainder control.",
        "proof_sketch": "Conditional fallback only; require a theorem-backed tail and do not let it silently replace P5.",
        "dependencies": ["P4.residual_schur_pmi"],
        "evidence_level": "not_started",
        "claim_status": "conditional_fallback",
        "artifacts": ["robot_final/P5_COMPACT_FOURIER_GRAM_FORMAL_CORE.md"],
        "command": ["python", "robot_final/verify_physical_rational_tail_global_bound.py"],
        "conditional": True,
    },
    {
        "name": "P8.independent_reachability",
        "statement": "An independent true-DH reachability flowpipe covers the same finite horizon and initial domain.",
        "proof_sketch": "Use the complete six-DOF RHS adapter only as an independent enclosure; bind it to the residual and terminal claims.",
        "dependencies": ["P6.exact_gram_interval_check"],
        "evidence_level": "rigorous_numerical_local_candidate",
        "claim_status": "full_dh_binding_open",
        "artifacts": ["robot_final/verify_full_dh_probe.py",
                      "robot_final/cross_validation/P8_FULL_DH_PROBE.md",
                      "robot_final/cross_validation/routeB_reachability_full_dh_probe.jl",
                      "robot_final/cross_validation/routeB_reachability_full_dh_probe.csv",
                      "robot_final/cross_validation/P8_FULL_DH_PROBE_local_narrow_t1e3_order2.md",
                      "robot_final/cross_validation/routeB_reachability_full_dh_probe_local_narrow_t1e3_order2.csv",
                      "robot_final/cross_validation/P8_FULL_DH_PROBE_local_narrow_t1e3_order2_max100.md",
                      "robot_final/cross_validation/routeB_reachability_full_dh_probe_local_narrow_t1e3_order2_max100.csv"],
        "command": ["python", "robot_final/verify_full_dh_probe.py"],
    },
    {
        "name": "M4.block45_full_certificate",
        "statement": "The block-(4,5) finite-horizon true-DH certificate closes residual, domain, flowpipe, and terminal transfer obligations.",
        "proof_sketch": "Assemble P5/P6/P8 under the exact dynamics semantics; every unresolved gate must be closed before promotion.",
        "dependencies": ["P5.sparse_disjunctive_sos", "P6.exact_gram_interval_check", "P8.independent_reachability"],
        "evidence_level": "theorem_backed_target",
        "claim_status": "open",
        "gate_requirements": {"formal_certificate_allowed": True,
                              "coverage_complete": True, "remainder_absorbed": True},
        "artifacts": ["robot_formal_v1/manifest.json", "PROJECT_REFORM_AUDIT.md"],
        # Read-only checker; the manifest builder is intentionally not used as
        # a gate because it rewrites the manifest and would mask source drift.
        "command": ["python", "robot_final/verify_solver_metadata.py"],
    },
    {
        "name": "P9.full_6dof_extension",
        "statement": "The closed block-(4,5) certificate extends to the full six-DOF Route-B theorem.",
        "proof_sketch": "Only start after M4 is closed; independently recheck all six-DOF source, flowpipe, and comparator obligations.",
        "dependencies": ["M4.block45_full_certificate"],
        "evidence_level": "theorem_backed_target",
        "claim_status": "gated_on_M4",
        "gate_requirements": {"formal_certificate_allowed": True},
        "artifacts": ["robot_formal_v1/manifest.json", "PROJECT_REFORM_AUDIT.md"],
        "command": ["python", "robot_final/verify_all.py"],
    },
)


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _safe_rel(value: str) -> str:
    rel = PurePosixPath(value)
    if (rel.is_absolute() or ".." in rel.parts or "\\" in value or
            any(char in value for char in (":", "\x00", "*", "?"))):
        raise ValueError(f"unsafe external artifact path: {value}")
    return rel.as_posix()


def _snapshot(root: Path, paths: Iterable[str]) -> tuple[dict[str, str], list[str]]:
    hashes: dict[str, str] = {}
    missing: list[str] = []
    for raw in paths:
        rel = _safe_rel(raw)
        path = root / rel
        if path.is_file():
            hashes[rel] = sha256_file(path)
        else:
            missing.append(rel)
    return hashes, missing


def _load_target_manifest(project_root: Path) -> dict[str, Any]:
    path = project_root / "robot_formal_v1" / "manifest.json"
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        raise ValueError(f"cannot read target formal manifest: {path}") from exc
    if not isinstance(payload, dict):
        raise ValueError("target formal manifest must be an object")
    return payload


def _load_target_gate(project_root: Path) -> dict[str, Any]:
    payload = _load_target_manifest(project_root)
    gate = payload.get("current_gate", {})
    if not isinstance(gate, dict):
        raise ValueError("target formal manifest current_gate must be an object")
    return dict(gate)


def _baseline_input_inventory(project_root: Path) -> set[str]:
    """Conservative P0 inputs, not a sandbox or a transitive import analysis.

    Enumerate only the delivery root and cross_validation's immediate files,
    plus exact manifest path entries.  Never traverse caches/backups/archives.
    Re-enumeration at both snapshot boundaries detects newly created inputs.
    """
    extensions = {".py", ".jl", ".csv", ".md", ".toml", ".json", ".ps1", ".bat"}
    root = project_root.resolve()
    paths: set[str] = set()

    def include(value: Any) -> None:
        if not isinstance(value, str) or not value:
            return
        try:
            rel = _safe_rel(value)
            parts = PurePosixPath(rel).parts
            if any(part.lower() == ".lake" or any(token in part.lower()
                   for token in ("depot", "backup", "archive")) for part in parts):
                return
            candidate = root / rel
            if not candidate.resolve().is_relative_to(root) or candidate.is_dir():
                return
            # Keep safe missing manifest inputs so they fail closed.
            paths.add(rel)
        except (ValueError, OSError):
            return

    for directory in (root / "robot_final", root / "robot_final/cross_validation"):
        if directory.is_dir() and directory.resolve().is_relative_to(root):
            for path in directory.iterdir():
                if path.suffix.lower() in extensions and path.is_file():
                    include(path.relative_to(root).as_posix())

    def manifest_paths(value: Any, key: str = "") -> None:
        if isinstance(value, dict):
            for name, child in value.items():
                manifest_paths(child, name)
        elif isinstance(value, list):
            for child in value:
                manifest_paths(child, key)
        elif key in {"path", "paths", "source_path", "input", "inputs", "input_path", "input_paths"}:
            include(value)

    manifest_paths(_load_target_manifest(root))
    return paths


def _metadata(project_root: Path, stage: dict[str, Any], gate: dict[str, Any]) -> dict[str, Any]:
    shared = [
        "PROJECT_REFORM_TARGET.md", "PROJECT_REFORM_AUDIT.md",
        "robot_formal_v1/manifest.json", "robot_formal_v1/README.md",
    ]
    command = list(stage.get("command", []))
    checker = command[1:2] if len(command) > 1 and not command[1].startswith("-") else []
    paths = sorted(set([*shared, *stage.get("artifacts", []), *checker]))
    if stage["name"] == "P0.reproducibility_baseline":
        paths = sorted(set(paths) | _baseline_input_inventory(project_root))
    hashes, missing = _snapshot(project_root, paths)
    # The first stage runs from the project root.  Later commands are
    # advisory until a coordinator supplies a concrete checker invocation.
    return {
        "verification_domain": EXTERNAL_DOMAIN,
        "registry_eligible": False,
        "statement_status": "external-research",
        "evidence_level": stage["evidence_level"],
        "claim_status": stage["claim_status"],
        "closure_scope": stage.get("closure_scope", "mathematical"),
        "conditional": bool(stage.get("conditional", False)),
        "target_root": str(project_root),
        "artifact_paths": paths,
        "missing_artifacts": missing,
        "source_hashes": hashes,
        "recommended_command": command,
        "target_gate_snapshot": gate,
        "gate_requirements": dict(stage.get("gate_requirements", {})),
    }


def initialize_routeb_intake(project_root: str | Path, store: StateStore,
                             *, descriptor_path: str | Path | None = None) -> WorkflowState:
    """Create an idempotence-safe Route-B research DAG from the target tree.

    Existing state is never replaced.  The generated descriptor is a portable
    identity record for the target snapshot; it contains no proof claim.
    """
    project_root = Path(project_root).resolve()
    if not project_root.is_dir():
        raise ValueError(f"external project root is not a directory: {project_root}")
    for required in ("PROJECT_REFORM_TARGET.md", "PROJECT_REFORM_AUDIT.md",
                     "robot_formal_v1/manifest.json"):
        if not (project_root / required).is_file():
            raise ValueError(f"external project is missing required intake file: {required}")
    if store.path.exists():
        raise FileExistsError(f"research state already exists: {store.path}")

    gate = _load_target_gate(project_root)
    state = WorkflowState(project="routeb-6dof-external")
    ids: dict[str, str] = {}
    for stage in ROUTEB_STAGES:
        metadata = _metadata(project_root, stage, gate)
        ids[stage["name"]] = state.add_node(
            stage["name"], stage["statement"], proof_sketch=stage["proof_sketch"],
            metadata=metadata)
    for stage in ROUTEB_STAGES:
        node = state.nodes[ids[stage["name"]]]
        node.dependencies = [ids[name] for name in stage["dependencies"]]
    state.root_id = ids["P9.full_6dof_extension"]

    descriptor = Path(descriptor_path).resolve() if descriptor_path else store.path.with_name("intake-manifest.json")
    descriptor.parent.mkdir(parents=True, exist_ok=True)
    descriptor_payload = {
        "schema_version": INTAKE_SCHEMA,
        "project": state.project,
        "target_root": str(project_root),
        "target_manifest": "robot_formal_v1/manifest.json",
        "target_manifest_sha256": sha256_file(project_root / "robot_formal_v1/manifest.json"),
        "nodes": [{"name": s["name"], "dependencies": s["dependencies"],
                   "conditional": bool(s.get("conditional", False))} for s in ROUTEB_STAGES],
    }
    descriptor.write_text(json.dumps(descriptor_payload, ensure_ascii=False, indent=2) + "\n",
                          encoding="utf-8")
    state.manifest = {
        "path": os.path.relpath(descriptor, store.path.parent).replace("\\", "/"),
        "sha256": sha256_file(descriptor),
        "target": str(project_root),
    }
    state.event("external_project_intake", schema=INTAKE_SCHEMA,
                target_root=str(project_root), descriptor=state.manifest,
                root=state.root_id, nodes=len(state.nodes),
                registry_eligible=False)
    state.validate()
    store.save(state)
    return state


def _node_by_name(state: WorkflowState, name: str):
    matches = [node for node in state.nodes.values() if node.name == name]
    if len(matches) != 1:
        raise ValueError(f"external node name is not unique: {name}")
    return matches[0]


def refresh_routeb_tracking(store: StateStore) -> dict[str, Any]:
    """Migrate tracking atomically, retaining attempts and superseded receipts."""
    state = store.load()
    # Refuse before changing anything, including when a running descendant
    # would be invalidated by migration of its ancestor.
    if any(n.status == NodeStatus.IN_PROGRESS for n in state.nodes.values()):
        raise ValueError("cannot refresh external tracking while a node is in progress")
    by_name = {stage["name"]: stage for stage in ROUTEB_STAGES}
    refreshed: list[str] = []
    invalid: set[str] = set()
    diagnostic_invalid: set[str] = set()
    for node in state.nodes.values():
        if node.metadata.get("verification_domain") != EXTERNAL_DOMAIN:
            continue
        stage = by_name.get(node.name)
        if node.status in {NodeStatus.EVIDENCE_COMPLETE, NodeStatus.VERIFIED} and (
                node.status == NodeStatus.VERIFIED or external_evidence_staleness(node)):
            invalid.add(node.id)
        if stage is not None:
            root = Path(node.metadata["target_root"]).resolve()
            new_meta = _metadata(root, stage, _load_target_gate(root))
            keys = ("artifact_paths", "missing_artifacts", "source_hashes", "recommended_command",
                    "evidence_level", "conditional", "gate_requirements", "target_gate_snapshot")
            changed = any(node.metadata.get(key) != new_meta[key] for key in keys)
            scope_changed = node.metadata.get("closure_scope", "mathematical") != new_meta["closure_scope"]
            if changed or scope_changed:
                invalid.add(node.id)
                diagnostic_invalid.add(node.id)
            node.metadata.update(new_meta)
        refreshed.append(node.name)
    # A reopened premise also invalidates every transitive consumer, including
    # any mixed-domain registry entry.  Keep the historical evidence intact.
    affected = set(invalid)
    while True:
        descendants = {n.id for n in state.nodes.values() if affected.intersection(n.dependencies)}
        if descendants <= affected:
            break
        affected.update(descendants)
    reopened = []
    for node in state.nodes.values():
        if node.id not in affected:
            continue
        if node.status != NodeStatus.OPEN:
            reopened.append(node.name)
        receipt = node.metadata.pop("evidence_receipt", None)
        if receipt is not None:
            node.metadata.setdefault("previous_external_receipts", []).append(receipt)
            node.metadata.setdefault("last_external_receipt", receipt)
        previous = state.registry.pop(node.id, None)
        if previous is not None:
            node.metadata.setdefault("previous_verifications", []).append(previous)
        node.verified_artifact = None
        node.status = NodeStatus.OPEN
        if node.id in diagnostic_invalid or affected.intersection(node.dependencies):
            node.metadata["execution_status"] = "tracking_invalidated"
        elif node.metadata.get("last_external_receipt", {}).get("exit_code") == 0:
            node.metadata["execution_status"] = "checker_passed"
    state.event("external_tracking_refreshed", refreshed=refreshed, reopened=reopened)
    state.validate()
    store.save(state)
    return {"refreshed": refreshed, "reopened": reopened}


def _policy(node) -> dict[str, Any]:
    # Known mathematical stages cannot become engineering gates via flags in
    # stored metadata or in the target manifest.
    return next((s for s in ROUTEB_STAGES if s["name"] == node.name), {
        "closure_scope": node.metadata.get("closure_scope", "mathematical"),
        "command": node.metadata.get("recommended_command", []),
        "gate_requirements": node.metadata.get("gate_requirements", {}),
    })


def _approved_command(node, command: list[str], cwd: Path) -> bool:
    approved = list(_policy(node).get("command", []))
    if not command or not approved or command[1:] != approved[1:]:
        return False
    if cwd.resolve() != Path(node.metadata["target_root"]).resolve():
        return False
    def executable(value: str) -> Path:
        return Path(shutil.which(value) or value).resolve()
    allowed = {executable(approved[0])}
    if approved[0] in {"python", "python3", "python.exe"}:
        allowed.add(Path(sys.executable).resolve())
    return executable(command[0]) in allowed


def _tracked_paths(node) -> list[str]:
    paths = set(node.metadata.get("artifact_paths", []))
    paths.update(node.metadata.get("missing_artifacts", []))
    stage = next((s for s in ROUTEB_STAGES if s["name"] == node.name), None)
    if stage is not None:
        paths = set(stage.get("artifacts", []))
        command = stage.get("command", [])
        if len(command) > 1 and not command[1].startswith("-"):
            paths.add(command[1])
        paths.update(["PROJECT_REFORM_TARGET.md", "PROJECT_REFORM_AUDIT.md",
                      "robot_formal_v1/manifest.json", "robot_formal_v1/README.md"])
        if stage["name"] == "P0.reproducibility_baseline":
            paths.update(_baseline_input_inventory(Path(node.metadata["target_root"])))
    return sorted(paths)


def _receipt_changes(node, receipt) -> list[str]:
    if not isinstance(receipt, dict) or not receipt.get("source_hashes"):
        return ["missing_source_receipt"]
    try:
        root = Path(node.metadata["target_root"]).resolve()
        hashes, missing = _snapshot(root, _tracked_paths(node))
        expected = receipt["source_hashes"]
        changes = [f"missing:{rel}" for rel in missing]
        changes += [f"changed:{rel}" for rel in set(hashes) | set(expected)
                    if hashes.get(rel) != expected.get(rel)]
        if expected != node.metadata.get("source_hashes"):
            changes.append("intake_snapshot_changed")
        if not _approved_command(node, receipt.get("command", []), Path(receipt.get("cwd", ""))):
            changes.append("command_not_approved")
        if receipt.get("exit_code") != 0 or receipt.get("source_unchanged") is not True:
            changes.append("unsuccessful_receipt")
        if receipt.get("status") not in {None, "passed", "target_gate_not_satisfied"}:
            changes.append("rejected_receipt")
        return changes
    except (OSError, ValueError, KeyError, TypeError) as exc:
        return [f"unreadable_source:{exc}"]


def external_evidence_staleness(node) -> list[str]:
    """Check closure authority, receipt scope, and live sources (also for legacy state)."""
    receipt = node.metadata.get("evidence_receipt")
    changes = _receipt_changes(node, receipt)
    scope = _policy(node).get("closure_scope", "mathematical")
    if scope not in {"engineering", "audit"}:
        changes.append("mathematical_obligation_not_discharged")
    if not isinstance(receipt, dict) or (
            receipt.get("dependency_closing") is not True or
            receipt.get("approved_command") is not True or receipt.get("status") != "passed" or
            receipt.get("closure_scope") != scope or
            receipt.get("gate_requirements") != _policy(node).get("gate_requirements", {}) or
            receipt.get("gate_satisfied") is not True):
        changes.append("invalid_closure_receipt")
    return changes


def external_diagnostic_is_current(node) -> bool:
    return (node.metadata.get("execution_status") == "checker_passed" and
            not _receipt_changes(node, node.metadata.get("last_external_receipt")))


def _check_ancestors(state: WorkflowState, node) -> None:
    work = list(node.dependencies)
    seen = set()
    while work:
        dependency = work.pop()
        if dependency in seen:
            continue
        seen.add(dependency)
        ancestor = state.nodes[dependency]
        if not node_is_closed(ancestor):
            raise ValueError(f"external dependency is open or stale: {ancestor.name}")
        work.extend(ancestor.dependencies)


def _text(value: str | bytes | None) -> str:
    return value.decode("utf-8", errors="replace") if isinstance(value, bytes) else value or ""


def run_external_gate(store: StateStore, node_name: str, *, command: list[str] | None = None,
                      cwd: str | Path | None = None, agent_id: str = "external-coordinator",
                      timeout_seconds: int | None = None) -> dict[str, Any]:
    """Persist diagnostics; close only an approved engineering/audit checker.

    The source snapshot is taken before and after execution.  A successful
    process with source drift is recorded as rejected, never as completed.
    stdout/stderr and the exact command are retained in the attempt and receipt.
    """
    state = store.load()
    state.validate()
    node = _node_by_name(state, node_name)
    if node.metadata.get("verification_domain") != EXTERNAL_DOMAIN:
        raise ValueError("run_external_gate only accepts external research nodes")
    if node.status != NodeStatus.OPEN:
        raise ValueError("external node is not open")
    _check_ancestors(state, node)
    root = Path(cwd).resolve() if cwd else Path(node.metadata["target_root"]).resolve()
    selected = list(command) if command is not None else list(node.metadata.get("recommended_command", []))
    if not selected:
        raise ValueError("external gate has no command")
    intake = dict(node.metadata.get("source_hashes", {}))
    target_root = Path(node.metadata["target_root"]).resolve()
    paths = list(node.metadata.get("artifact_paths", []))
    before, after, initial_missing, missing = {}, {}, [], []
    target_gate: dict[str, Any] = {}
    requirements = dict(_policy(node).get("gate_requirements", {}))
    scope = _policy(node).get("closure_scope", "mathematical")
    approved = _approved_command(node, selected, root)
    stdout, stderr, exit_code = "", "", 125
    status = "source_read_error"
    gate_satisfied = False
    attempt_id = state.begin_attempt(node.id, agent_id)
    store.save(state)
    try:
        paths = _tracked_paths(node)
        before, initial_missing = _snapshot(target_root, paths)
        if before != intake or initial_missing or node.metadata.get("missing_artifacts"):
            status = "intake_drift_rejected"
        else:
            result = subprocess.run(selected, cwd=root, text=True, encoding="utf-8",
                                    errors="replace", capture_output=True,
                                    env={**os.environ, "PYTHONIOENCODING": "utf-8"},
                                    timeout=timeout_seconds, check=False)
            stdout, stderr, exit_code = _text(result.stdout), _text(result.stderr), result.returncode
            status = "passed" if exit_code == 0 else "external_gate_error"
    except subprocess.TimeoutExpired as exc:
        stdout = _text(exc.stdout)
        stderr = _text(exc.stderr) + "\nexternal gate timed out"
        exit_code = 124
        status = "external_timeout"
    except (OSError, ValueError) as exc:
        stdout, stderr, exit_code = "", repr(exc), 127
        status = "external_gate_error"
    try:
        paths = _tracked_paths(node)
        after, missing = _snapshot(target_root, paths)
    except (OSError, ValueError) as exc:
        status = "source_read_error"
        stderr += f"\n{exc}"
    try:
        target_gate = _load_target_gate(target_root)
        gate_satisfied = all(type(target_gate.get(key)) is type(value) and target_gate.get(key) == value
                             for key, value in requirements.items())
    except ValueError as exc:
        status = "target_manifest_error"
        stderr += f"\n{exc}"
    unchanged = before == after == intake and bool(before) and not missing and not initial_missing
    if status == "passed" and not unchanged:
        status = "source_drift_rejected"
    if status == "passed" and not approved:
        status = "command_not_approved"
    if status == "passed" and not gate_satisfied:
        status = "target_gate_not_satisfied"
    state = store.load()
    try:
        _check_ancestors(state, node)
    except ValueError as exc:
        status = "stale_dependency_rejected"
        stderr += f"\n{exc}"
    state.finish_attempt(attempt_id, status=status, command=selected,
                         stdout=stdout, stderr=stderr, exit_code=exit_code)
    close = status == "passed" and scope in {"engineering", "audit"}
    receipt = {
        "schema_version": "external-evidence-receipt-v1",
        "attempt_id": attempt_id,
        "command": selected,
        "cwd": str(root),
        "exit_code": exit_code,
        "source_hashes": after,
        "source_hashes_before": before,
        "source_hashes_at_intake": intake,
        "source_unchanged": unchanged,
        "missing_artifacts": sorted(set(initial_missing + missing)),
        "evidence_level": node.metadata.get("evidence_level"),
        "registry_eligible": False,
        "target_gate": target_gate,
        "gate_requirements": requirements,
        "gate_satisfied": gate_satisfied,
        "closure_scope": scope,
        "approved_command": approved,
        "dependency_closing": close,
        "status": status,
    }
    node = state.nodes[node.id]
    previous = node.metadata.get("last_external_receipt")
    if previous is not None:
        node.metadata.setdefault("previous_external_receipts", []).append(previous)
    node.metadata["last_external_receipt"] = receipt
    node.metadata["execution_status"] = (
        "checker_passed" if status in {"passed", "target_gate_not_satisfied"} else status)
    if close:
        node.metadata["evidence_receipt"] = receipt
        node.metadata["execution_status"] = "checker_passed"
        node.status = NodeStatus.EVIDENCE_COMPLETE
        state.event("external_evidence_closed", node_id=node.id,
                    attempt_id=attempt_id, evidence_level=receipt["evidence_level"],
                    registry_eligible=False)
    else:
        state.event("external_diagnostic_recorded", node_id=node.id,
                    attempt_id=attempt_id, status=status, dependency_closing=False)
    state.validate()
    store.save(state)
    return {"node": node.name, "status": node.status.value, "attempt_id": attempt_id,
            "exit_code": exit_code, "source_unchanged": unchanged,
            "stdout": stdout, "stderr": stderr}
