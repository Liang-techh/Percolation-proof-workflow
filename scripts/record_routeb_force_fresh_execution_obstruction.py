"""Record a fresh force-export execution obstruction without weakening the gate."""
from __future__ import annotations

import hashlib
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
REVIEW = ROOT / "agent_review_inbox/review-T-P4-fresh-general-state-force-receipt-immutable-codex-20260907.md"
EXPORTER = ROOT / "examples/routeb_b45_5_descriptor_terms_adapter_lean/general_state_force_binding_export.jl"
SOURCE = ROOT.parent / "6dof_sos_optimized" / "6dof_sos_optimized" / "robot_final" / "dhport_lib.jl"
STATE = ROOT / "artifacts/routeb_6dof/state.json"
EXPECTED_EXPORTER = "5351110E81327EBC059074A2E445A33E00859320BCE37B5B0220BB189F4E46A4"
EXPECTED_SOURCE = "AEBE6DB09B2D943448C5D701631109DBA8F5EEB070CC66593E5DBACA26485936"
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
    for path in (REVIEW, EXPORTER, SOURCE, STATE):
        if not path.is_file():
            raise FileNotFoundError(path)
    text = REVIEW.read_text(encoding="utf-8", errors="replace")
    for phrase in (
        "JULIA_COMMAND_FOUND=False",
        "WHERE_JULIA_EXIT_CODE=1",
        "PENDING_JULIA_EXECUTION",
        "FRESH_CSV_EXISTS=False",
        "registry_promotion = false",
        "main_state_mutation = false",
    ):
        if phrase not in text:
            raise ValueError(f"fresh force obstruction missing: {phrase}")
    exporter_sha = sha(EXPORTER)
    source_sha = sha(SOURCE)
    if exporter_sha != EXPECTED_EXPORTER or source_sha != EXPECTED_SOURCE:
        raise ValueError("frozen force execution input hash drift")
    entry = {
        "schema_version": 1,
        "task_id": "T-P4-KC-COORDINATE-ADAPTER",
        "source_agent": "codex-inbox",
        "review_status": "PENDING_JULIA_EXECUTION",
        "review_artifact": {"path": str(REVIEW.resolve()), "sha256": sha(REVIEW)},
        "exporter_sha256": exporter_sha,
        "deployed_source_sha256": source_sha,
        "julia_command_found": False,
        "fresh_csv_present": False,
        "fresh_receipt_present": False,
        "runtime_status": "NOT_OBTAINED",
        "deployed_tau_equivalence": "NOT_CLAIMED",
        "formal_certificate_allowed": False,
        "registry_promoted": False,
    }
    store = StateStore(STATE)
    state = store.load()
    node = find(state, "P4.true_dh_force_descriptor_semantics")
    prior = list(node.metadata.get("force_fresh_execution_obstructions", []))
    changed = entry not in prior
    if changed:
        prior.append(entry)
        node.metadata["force_fresh_execution_obstructions"] = prior
    desired = {
        "status": entry["review_status"],
        "review_sha256": entry["review_artifact"]["sha256"],
        "exporter_sha256": exporter_sha,
        "deployed_source_sha256": source_sha,
        "julia_command_found": False,
        "fresh_csv_present": False,
        "fresh_receipt_present": False,
        "runtime_status": "NOT_OBTAINED",
        "formal_certificate_allowed": False,
        "registry_promoted": False,
    }
    if node.metadata.get("force_fresh_execution_obstruction") != desired:
        node.metadata["force_fresh_execution_obstruction"] = desired
        changed = True
    if changed:
        state.event(
            "routeb_force_fresh_execution_obstruction_recorded",
            node_id=node.id,
            review_status=entry["review_status"],
            julia_command_found=False,
            fresh_receipt_present=False,
            registry_promoted=False,
            formal_certificate_allowed=False,
        )
        state.validate()
        store.save(state)
    print({
        "status": "recorded" if changed else "already_recorded",
        "review_status": entry["review_status"],
        "state_revision": store.load().revision,
        "julia_command_found": False,
        "fresh_receipt_present": False,
        "registry_promoted": False,
        "formal_certificate_allowed": False,
    })
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
