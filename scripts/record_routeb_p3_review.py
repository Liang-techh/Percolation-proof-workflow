"""Attach an inbox review of the P3 trig-chain boundary to O2.

The inbox document is a coordinator-visible review receipt, not a Lean proof.
The operation is fail-closed and records the live external artifact hashes.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
ROUTE_B = ROOT.parent / "6dof_sos_optimized" / "6dof_sos_optimized"
REVIEW = ROOT / "agent_review_inbox/review-T-P4-036-01a07bb4-920-20260907.md"
REPORT = ROUTE_B / "routeB_dense_Mq/P3_DH_TRIG_CHAIN_CONTRACT.md"
CSV = ROUTE_B / "routeB_dense_Mq/routeB_p3_dh_trig_chain_contract.csv"
STATE = ROOT / "artifacts/routeb_6dof/state.json"
sys.path.insert(0, str(ROOT / "src"))

from percolation_workflow.store import StateStore  # noqa: E402


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def ref(path: Path) -> dict[str, str]:
    return {"path": str(path.resolve()), "sha256": sha(path)}


def find(state, name: str):
    for node in state.nodes.values():
        if node.name == name:
            return node
    raise ValueError(f"missing node: {name}")


def main() -> int:
    for path in (REVIEW, REPORT, CSV):
        if not path.is_file():
            raise FileNotFoundError(path)
    text = REVIEW.read_text(encoding="utf-8", errors="replace")
    required = (
        "条件式 exact-real DH 三角原子",
        "alpha 行是固定输入 `q=0`",
        "不能进入 verified registry",
        "formal_certificate_allowed=false",
    )
    if not all(phrase in text for phrase in required):
        raise ValueError("P3 inbox review is missing its fail-closed boundary")

    review = {
        "schema_version": 1,
        "source_agent": "01a07bb4-9206-7263-873e-f182a09a90c6",
        "task_id": "T-P4-036",
        "review_status": "EXACT_REAL_TRIG_LEAF_PRESENT__O2_FLOAT64_BINDING_OPEN",
        "review_artifact": ref(REVIEW),
        "source_artifacts": [ref(REPORT), ref(CSV)],
        "evidence_level": "independent_static_review",
        "claims": {
            "conditional_exact_real_leaf": True,
            "theta_box": "[-3/20,3/20]",
            "alpha_input": "singleton q=0",
            "float64_binding": False,
            "libm_enclosure": False,
            "registry_promoted": False,
            "formal_certificate_allowed": False,
        },
        "unresolved": [
            "Float64_pi_offset_and_angle_formation",
            "per_atom_libm_sin_cos_enclosure",
            "finite_dh_evaluator_DAG_propagation",
            "central_fd_and_linear_solve_enclosure",
            "box_coverage_and_composition",
        ],
        "admission_status": "pending_coordinator_admission",
        "registry_promoted": False,
        "formal_certificate_allowed": False,
    }

    store = StateStore(STATE)
    state = store.load()
    node = find(state, "P4.true_dh_float64_evaluator_enclosure")
    reviews = list(node.metadata.get("independent_static_reviews", []))
    changed = review not in reviews
    if changed:
        reviews.append(review)
        node.metadata["independent_static_reviews"] = reviews
    unresolved = list(node.metadata.get("unresolved", []))
    marker = "p3_alpha_singleton_q_zero_review_confirmed"
    if marker not in unresolved:
        unresolved.append(marker)
        node.metadata["unresolved"] = unresolved
        changed = True
    if changed:
        state.event(
            "routeb_p3_independent_review_recorded",
            node_id=node.id,
            source_agent=review["source_agent"],
            review_status=review["review_status"],
            admission_status="pending_coordinator_admission",
            registry_promoted=False,
            formal_certificate_allowed=False,
        )
        state.validate()
        store.save(state)
    print({
        "status": "recorded" if changed else "already_recorded",
        "review_status": review["review_status"],
        "state_revision": store.load().revision,
        "registry_promoted": False,
        "formal_certificate_allowed": False,
    })
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
