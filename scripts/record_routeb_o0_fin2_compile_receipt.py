"""Ingest the pinned Fin 2 norm-conversion receipt as a conditional child."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
RECEIPT = ROOT / "agent_review_inbox/receipt-Fin2NormConversionCandidate-pinned-20260907.json"
STATE = ROOT / "artifacts/routeb_6dof/state.json"
SOURCE = ROOT / "examples/local_fkg/Fin2NormConversionCandidate.lean"
PRINT = ROOT / "examples/local_fkg/Fin2NormConversionPrint.lean"
OLEAN = ROOT / "examples/local_fkg/Fin2NormConversionCandidate.olean"
sys.path.insert(0, str(ROOT / "src"))
from percolation_workflow.store import StateStore  # noqa: E402


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def find(state, name: str):
    for node in state.nodes.values():
        if node.name == name:
            return node
    raise ValueError(f"missing node: {name}")


def main() -> int:
    for path in (RECEIPT, STATE, SOURCE, PRINT, OLEAN):
        if not path.is_file():
            raise FileNotFoundError(path)
    receipt = json.loads(RECEIPT.read_text(encoding="utf-8"))
    required = {
        "schema": "routeb-o0-fin2-norm-conversion-compiled-receipt-v1",
        "status": "PASS_CONDITIONAL_LEAN_COMPILE",
        "main_state_modified": False,
        "registry_registered": False,
    }
    for key, expected in required.items():
        if receipt.get(key) != expected:
            raise ValueError(f"Fin2 receipt {key} is not fail-closed as expected")
    build = receipt.get("build") or {}
    if any(build.get(key) != 0 for key in ("source_exit_code", "olean_exit_code", "print_exit_code")):
        raise ValueError("Fin2 receipt has a nonzero build exit")
    artifacts = receipt.get("artifacts") or {}
    expected_hashes = {
        "source": sha(SOURCE),
        "print_harness": sha(PRINT),
        "olean": sha(OLEAN),
    }
    actual_hashes = {
        "source": (artifacts.get("source") or {}).get("sha256", "").upper(),
        "print_harness": (artifacts.get("print_harness") or {}).get("sha256", "").upper(),
        "olean": ((artifacts.get("olean") or {}).get("cwd_copy") or {}).get("sha256", "").upper(),
    }
    if actual_hashes != expected_hashes:
        raise ValueError(f"Fin2 source/print/olean hash mismatch: {actual_hashes} != {expected_hashes}")
    comparator = receipt.get("statement_comparator") or {}
    if comparator.get("overall_match") is not True:
        raise ValueError("Fin2 statement comparator did not pass")
    audit = receipt.get("axiom_audit") or {}
    if audit.get("sorryAx_present") is not False or audit.get("admitAx_present") is not False:
        raise ValueError("Fin2 axiom audit has sorry/admit")
    allowed = {"propext", "Classical.choice", "Quot.sound"}
    for theorem in ("norm2_le_two_normInf", "fin2_euclidean_weighted_adapter"):
        if set(audit.get(theorem, ())) - allowed:
            raise ValueError(f"Fin2 theorem {theorem} uses an unpermitted axiom")

    entry = {
        "schema_version": 1,
        "task_id": "T-P4-033-O0-R2",
        "source_agent": "codex-inbox",
        "review_status": "COMPILED_CONDITIONAL_FIN2_OUTPUT_NORM_CONVERSION",
        "receipt": {"path": str(RECEIPT.resolve()), "sha256": sha(RECEIPT)},
        "toolchain": receipt["toolchain"],
        "build": build,
        "artifact_hashes": expected_hashes,
        "statement_comparator": "PASS",
        "axiom_audit": {
            "allowed": sorted(allowed),
            "sorryAx_present": False,
            "admitAx_present": False,
        },
        "scope": "Fin2 output norm only; exact factor 2; no Schur/source/global closure",
        "formal_certificate_allowed": False,
        "registry_promoted": False,
    }
    store = StateStore(STATE)
    state = store.load()
    node = find(state, "P4.true_dh_regularizer_semantics_bridge")
    prior = list(node.metadata.get("o0_fin2_norm_compile_receipts", []))
    changed = entry not in prior
    if changed:
        prior.append(entry)
        node.metadata["o0_fin2_norm_compile_receipts"] = prior
    desired = {
        "status": entry["review_status"],
        "receipt_sha256": entry["receipt"]["sha256"],
        "source_sha256": expected_hashes["source"],
        "print_harness_sha256": expected_hashes["print_harness"],
        "olean_sha256": expected_hashes["olean"],
        "lean_pin": receipt["toolchain"]["lean_pin"],
        "statement_comparator": "PASS",
        "axiom_audit": entry["axiom_audit"],
        "scope": entry["scope"],
        "formal_certificate_allowed": False,
        "registry_promoted": False,
    }
    if node.metadata.get("o0_fin2_norm_conversion") != desired:
        node.metadata["o0_fin2_norm_conversion"] = desired
        changed = True
    if changed:
        state.event(
            "routeb_o0_fin2_norm_compile_receipt_recorded",
            node_id=node.id,
            review_status=entry["review_status"],
            statement_comparator="PASS",
            source_bound=False,
            schur_consumed=False,
            registry_promoted=False,
            formal_certificate_allowed=False,
        )
        state.validate()
        store.save(state)
    print({
        "status": "recorded" if changed else "already_recorded",
        "review_status": entry["review_status"],
        "state_revision": store.load().revision,
        "source_sha256": expected_hashes["source"],
        "olean_sha256": expected_hashes["olean"],
        "registry_promoted": False,
        "formal_certificate_allowed": False,
    })
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
