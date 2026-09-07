"""Attach the O2.4 finite-DAG source-order review to the T-P4-036 frontier."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
ROUTE_B = ROOT.parent / "6dof_sos_optimized" / "6dof_sos_optimized"
REVIEW = ROOT / "agent_review_inbox/review-T-P4-036.4-dag-01a07bb4-be84-20260907.md"
SOURCE = ROUTE_B / "routeB_dense_Mq/dhport_lib.jl"
STATE = ROOT / "artifacts/routeb_6dof/state.json"
EXPECTED_SOURCE_SHA256 = "AEBE6DB09B2D943448C5D701631109DBA8F5EEB070CC66593E5DBACA26485936"
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
    for path in (REVIEW, SOURCE):
        if not path.is_file():
            raise FileNotFoundError(path)
    text = REVIEW.read_text(encoding="utf-8", errors="replace")
    for phrase in (
        "D1 `DHLinkFiniteDAGEnclosure",
        "D2 `DHChainFiniteGeometryEnclosure",
        "D3 `DHChainFloat64EvaluatorEnclosure",
        "mass_matrix` 与 `potential`",
        "formal_certificate_allowed=false",
        EXPECTED_SOURCE_SHA256,
    ):
        if phrase not in text:
            raise ValueError(f"O2.4 review boundary missing: {phrase}")
    if sha(SOURCE) != EXPECTED_SOURCE_SHA256:
        raise ValueError("O2.4 source hash drifted; reject stale review")
    review = {
        "schema_version": 1,
        "task_id": "T-P4-036.4",
        "source_agent": "01a07bbd-be84-7471-b20d-5b0b39fc5d40",
        "review_status": "DAG_PROPAGATION_INTERFACE_DRAFT__UNCOMPILED_OPEN",
        "review_artifact": ref(REVIEW),
        "source_artifact": ref(SOURCE),
        "line_contract": {
            "fk_frames": "31-44",
            "mass_matrix": "46-61",
            "potential": "63-70",
            "arm_MCG": "73-100",
            "exact_ddq": "102-110",
        },
        "interfaces": [
            "RouteB.P3.DHLinkFiniteDAGEnclosure",
            "RouteB.P3.DHChainFiniteGeometryEnclosure",
            "RouteB.P3.DHChainFloat64EvaluatorEnclosure",
        ],
        "runtime_requirements": [
            "operation_schedule_hash",
            "Julia/runtime/libm/BLAS/rounding/FMA/threading",
            "per_box_input_output_and_coverage",
            "finite_non_nan_no_overflow",
        ],
        "formal_certificate_allowed": False,
        "registry_promoted": False,
        "admission_status": "pending_pinned_runtime_and_lean_receipt",
    }
    store = StateStore(STATE)
    state = store.load()
    node = find(state, "P4.true_dh_float64_evaluator_enclosure")
    prior = list(node.metadata.get("independent_static_reviews", []))
    changed = review not in prior
    if changed:
        prior.append(review)
        node.metadata["independent_static_reviews"] = prior
    dag = dict(node.metadata.get("o2_dag_propagation") or {})
    desired = {
        "task_id": "T-P4-036.4",
        "status": "OPEN_INTERFACE_DRAFT__UNCOMPILED",
        "source_artifact": ref(SOURCE),
        "interfaces": review["interfaces"],
        "line_contract": review["line_contract"],
        "mass_and_potential_reinvoke_fk_frames": True,
        "central_fd_consumes_two_shifted_dag_copies": True,
        "operation_schedule": [
            "T_prev * A_i",
            "extract z_i from T_prev before A_i",
            "translation/rotation slices",
            "cross-product subtraction order",
            "Jv_transpose * Jv",
            "Ri * Ii * Ri_transpose",
            "Jw_transpose * rotated_inertia * Jw",
            "M accumulator then mu*I",
            "pcom_z * mass * gravity then P accumulator",
        ],
        "runtime_receipt_requirements": [
            "operation_schedule_hash",
            "Julia/runtime/libm/BLAS/rounding/FMA/threading",
            "mu_and_h_binary64_bits",
            "per_box_input_output_and_coverage",
            "finite_non_nan_no_overflow",
        ],
        "formal_certificate_allowed": False,
        "registry_promoted": False,
    }
    if dag != desired:
        node.metadata["o2_dag_propagation"] = desired
        changed = True
    if changed:
        state.event(
            "routeb_o2_dag_propagation_review_recorded",
            node_id=node.id,
            review_status=review["review_status"],
            admission_status=review["admission_status"],
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
