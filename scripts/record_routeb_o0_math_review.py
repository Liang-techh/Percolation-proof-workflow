"""Integrate the T-P4-033 O0 mathematical review fail-closed.

The inbox report is a mathematical decomposition and obstruction analysis, not
a Lean receipt.  This intake records its provenance and the executable child
boundaries on the O0 node without changing node closure, registry, or the
formal-certificate gate.
"""
from __future__ import annotations

import hashlib
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
ROUTE_B = ROOT.parent / "6dof_sos_optimized" / "6dof_sos_optimized"
REVIEW = ROOT / "agent_review_inbox/review-T-P4-033-codex-20260907.md"
HELPER = ROOT / "src/percolation_workflow/routeb_regularizer_semantics.py"
DOC = ROOT / "docs/routeb-p4-o0-regularizer-semantics-bridge.md"
STATE = ROOT / "artifacts/routeb_6dof/state.json"
DEPLOYED = ROUTE_B / "robot_final/dhport_lib.jl"
LIFTED = ROUTE_B / "routeB_dense_Mq/routeB_fourier_lifted_descriptor_model.jl"
sys.path.insert(0, str(ROOT / "src"))

from percolation_workflow.store import StateStore  # noqa: E402


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def ref(path: Path) -> dict[str, str]:
    return {"path": str(path.resolve()), "sha256": sha256(path)}


def find_node(state, name: str):
    for node in state.nodes.values():
        if node.name == name:
            return node
    raise ValueError(f"missing node: {name}")


def main() -> int:
    for path in (REVIEW, HELPER, DOC, STATE, DEPLOYED, LIFTED):
        if not path.is_file():
            raise FileNotFoundError(path)
    text = REVIEW.read_text(encoding="utf-8", errors="replace")
    required = (
        "review_status: OPEN_MATH_CLOSURE_PREMISES",
        "O0-R1:", "O0-R2:", "O0-R3:",
        "not a compiled or admitted certificate",
    )
    if not all(phrase in text for phrase in required):
        raise ValueError("T-P4-033 review is missing its mathematical fail-closed boundary")

    review = {
        "schema_version": 1,
        "source_agent": "Codex",
        "task_id": "T-P4-033",
        "review_status": "OPEN_MATH_CLOSURE_PREMISES",
        "review_artifact": ref(REVIEW),
        "supporting_artifacts": [ref(HELPER), ref(DOC), ref(DEPLOYED), ref(LIFTED)],
        "review_observed_state_sha256": (
            "86E17CAD6FA5DD42C2201D2DE9422AA51BDCC4E2DFCC9D4F288719586149A933"
        ),
        "evidence_level": "read_only_mathematical_decomposition",
        "claims": {
            "scalar_regularizer_order_closed": True,
            "common_base_binding": False,
            "quantitative_base_error_bound": False,
            "exact_d_block_resolvent": False,
            "weighted_port_metric_conversion": False,
            "baseline_schur_margin_consumed": False,
            "lean_verified": False,
            "registry_promoted": False,
            "formal_certificate_allowed": False,
        },
        "minimal_decomposition": [
            {
                "id": "O0-R1",
                "name": "common_base_and_d_block_resolvent",
                "status": "OPEN",
                "requires": [
                    "common M0 binding or epsilon_A",
                    "exact inverse/coercivity bound K",
                    "delta*K < 1",
                ],
            },
            {
                "id": "O0-R2",
                "name": "weighted_port_metric_conversion",
                "status": "OPEN",
                "requires": [
                    "same-key M_BD and DeltaM_DB bounds",
                    "B_up weighted operator bound or metric lower bound",
                ],
            },
            {
                "id": "O0-R3",
                "name": "schur_budget_consumer",
                "status": "OPEN",
                "requires": [
                    "baseline rho_r",
                    "epsilon_R",
                    "strict Young/Schur remaining-margin inequality",
                ],
            },
        ],
        "unresolved": [
            "common_base_or_quantitative_mass_error",
            "exact_d_block_inverse_norm_bound",
            "weighted_port_perturbation_bound",
            "baseline_weighted_port_gain_and_schur_margin",
        ],
        "admission_status": "pending_coordinator_admission",
        "registry_promoted": False,
        "formal_certificate_allowed": False,
    }

    store = StateStore(STATE)
    state = store.load()
    node = find_node(state, "P4.true_dh_regularizer_semantics_bridge")
    prior = list(node.metadata.get("independent_math_reviews", []))
    changed = review not in prior
    if changed:
        prior.append(review)
        node.metadata["independent_math_reviews"] = prior

    closure = {
        "schema_version": 1,
        "task_id": "T-P4-033",
        "status": "OPEN_MATH_CLOSURE_PREMISES",
        "review_artifact": review["review_artifact"],
        "scalar_fact": "CLOSED_AS_EXACT_RATIONAL_FACT_ONLY",
        "decomposition": review["minimal_decomposition"],
        "counterexample_boundary": (
            "regularizer positivity alone does not imply D-block invertibility, "
            "unweighted inverse difference does not imply weighted port gain"
        ),
        "formal_certificate_allowed": False,
        "registry_promoted": False,
    }
    if node.metadata.get("o0_math_closure") != closure:
        node.metadata["o0_math_closure"] = closure
        changed = True

    unresolved = list(node.metadata.get("unresolved", []))
    for marker in (
        "o0_math_closure_premises_open",
        "o0_weighted_port_metric_open",
        "o0_schur_margin_consumer_open",
    ):
        if marker not in unresolved:
            unresolved.append(marker)
            changed = True
    if node.metadata.get("unresolved") != unresolved:
        node.metadata["unresolved"] = unresolved
        changed = True

    if changed:
        state.event(
            "routeb_o0_math_review_recorded",
            node_id=node.id,
            task_id="T-P4-033",
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
