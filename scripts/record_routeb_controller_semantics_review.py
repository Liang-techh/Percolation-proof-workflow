"""Record and resolve conflicts between an agent review and live source audit."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
ROUTE_B = ROOT.parent / "6dof_sos_optimized" / "6dof_sos_optimized"
DEPLOYED = ROUTE_B / "robot_final" / "dhport_lib.jl"
LIFTED = ROUTE_B / "routeB_dense_Mq" / "routeB_fourier_lifted_descriptor_model.jl"
TASK = ROOT / "artifacts/task_controller_damping_semantics_20260907"
sys.path.insert(0, str(ROOT / "src"))

from percolation_workflow.routeb_controller_semantics import (  # noqa: E402
    audit_controller_damping_semantics,
)
from percolation_workflow.store import StateStore  # noqa: E402


def ref(path: Path) -> dict[str, str]:
    return {"path": str(path.resolve()),
            "sha256": hashlib.sha256(path.read_bytes()).hexdigest().upper()}


def find(state, name: str):
    for node in state.nodes.values():
        if node.name == name:
            return node
    raise ValueError(f"missing node: {name}")


def main() -> int:
    report = TASK / "REPORT.md"
    receipt = TASK / "RECEIPT.json"
    for path in (report, receipt, DEPLOYED, LIFTED):
        if not path.is_file():
            raise FileNotFoundError(path)
    report_text = report.read_text(encoding="utf-8", errors="replace")
    receipt_data = json.loads(receipt.read_text(encoding="utf-8"))
    live = audit_controller_damping_semantics(
        DEPLOYED.read_text(encoding="utf-8", errors="replace"),
        LIFTED.read_text(encoding="utf-8", errors="replace"),
    )
    report_claims_no_mismatch = "没有系数不一致" in report_text
    conflict = report_claims_no_mismatch != (not live.mismatched_indices)
    review = {
        "schema_version": 1,
        "review_status": receipt_data.get("status", "unknown"),
        "live_audit_status": live.status,
        "live_mismatched_joint_indices": list(live.mismatched_indices),
        "report_claims_no_mismatch": report_claims_no_mismatch,
        "conflict": conflict,
        "verdict": "CONFLICTING_REVIEW_FAIL_CLOSED" if conflict else "REVIEW_CONSISTENT_PENDING_ADMISSION",
        "source_artifacts": [ref(DEPLOYED), ref(LIFTED)],
        "review_artifacts": [ref(report), ref(receipt)],
        "coordinator_resolution": (
            "retain the live source audit and keep the node open; resolve by declaring "
            "the canonical lifted/DH branch and regenerating the stale branch, not by "
            "editing labels in historical evidence"
        ) if conflict else "retain the review as independent corroboration; source binding remains open",
        "registry_promoted": False,
        "formal_certificate_allowed": False,
    }

    store = StateStore(ROOT / "artifacts/routeb_6dof/state.json")
    state = store.load()
    node = find(state, "P4.true_dh_force_descriptor_semantics")
    reviews = list(node.metadata.get("independent_controller_reviews", []))
    if review not in reviews:
        reviews.append(review)
    changed = reviews != node.metadata.get("independent_controller_reviews")
    node.metadata["independent_controller_reviews"] = reviews
    unresolved = list(node.metadata.get("unresolved", []))
    if conflict and "controller_semantics_review_conflict_resolution" not in unresolved:
        unresolved.append("controller_semantics_review_conflict_resolution")
        changed = True
    if unresolved != node.metadata.get("unresolved"):
        node.metadata["unresolved"] = unresolved
        changed = True
    if changed:
        state.event(
            "routeb_controller_semantics_review_recorded",
            node_id=node.id,
            verdict=review["verdict"],
            conflict=conflict,
            live_mismatched_joint_indices=list(live.mismatched_indices),
            registry_promoted=False,
            formal_certificate_allowed=False,
        )
        state.validate()
        store.save(state)
    print({"status": "recorded" if changed else "already_recorded",
           "verdict": review["verdict"], "live_audit_status": live.status,
           "mismatched_joint_indices": list(live.mismatched_indices),
           "state_revision": state.revision})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
