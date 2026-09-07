"""Split the Route-B coefficient seam into O0/O1/O2 proof obligations."""
from __future__ import annotations

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from percolation_workflow.store import StateStore  # noqa: E402


def find(state, name: str):
    for node in state.nodes.values():
        if node.name == name:
            return node
    raise ValueError(f"missing node: {name}")


CHILDREN = (
    (
        "P4.true_dh_regularizer_semantics_bridge",
        "Bind the deployed Float64 mass regularizer 1e-6 to the exact-real mu=1/1000000 model by an explicit rounding inclusion or an authoritative exact-real evaluation contract.",
        "Treat the IEEE-754 literal as a contained interval, not as exact equality; carry the same mu through M_mu, M_DD, and the port map.",
        "evaluator_enclosure",
        "source_semantics",
    ),
    (
        "P4.true_dh_exact_real_coefficient_identity",
        "Under the common exact-real descriptor equations and det(M_DD) != 0, prove R_port*a_B=r_B for R_port=-M_BD*M_DD^(-1)*(M_DB-M0_DB).",
        "Use M_DD*v+DeltaM_DB*a_B=0 and r_B-M_BD*v=0; preserve the minus sign and retain the explicit remote block term. This is conditional exact-real algebra, not Float64 source equivalence.",
        "source_binding",
        "lean_adapter",
    ),
    (
        "P4.true_dh_float64_evaluator_enclosure",
        "On every certified input box, contain the deployed dhport_lib.jl Float64 evaluation of M, central-FD C/G, tau, and the backslash solve inside the exact-real outward interval evaluator.",
        "Decompose later into elementary-function/libm rounding, finite-DAG operation rounding, FD-shift semantics, regularizer conversion, and linear-solve conditioning; pointwise BigFloat agreement is insufficient.",
        "evaluator_enclosure",
        "source_semantics",
    ),
)


def contract(parent, child_ids):
    return {
        "schema_version": 1,
        "required_child_ids": child_ids,
        "required_parent_receipt": "typed_R_port_coefficient_binding",
        "required_obligations": [
            "regularizer_semantics_bridge",
            "exact_real_R_port_aB_equals_rB",
            "float64_evaluator_box_enclosure",
        ],
        "repair_route": {
            "owner": "P4.true_dh_exact_real_coefficient_identity",
            "action": "compile_conditional_exact_real_R_port_aB_equals_rB_adapter",
        },
        "promotion_boundary": (
            "O0, O1, and O2 must each have pinned evidence and registry entries; "
            "O1 alone never implies deployed Float64 source equivalence"
        ),
    }


def main() -> int:
    store = StateStore(ROOT / "artifacts/routeb_6dof/state.json")
    state = store.load()
    parent = find(state, "P4.true_dh_residual_map_coefficient_binding")
    by_name = {node.name: node for node in state.nodes.values()}
    child_ids: list[str] = []
    changed = False
    for name, statement, sketch, bottleneck, lane in CHILDREN:
        child = by_name.get(name)
        if child is None:
            child_id = state.add_node(
                name, statement, parent_id=parent.id, proof_sketch=sketch,
                metadata={
                    "verification_domain": "lean",
                    "research_stage": "P4",
                    "math_lane": lane,
                    "math_bottleneck": bottleneck,
                    "statement_status": "formalization_target",
                    "claim_status": "true_dh_evaluator_child_open",
                    "evidence_level": "typed-source-binding-target",
                    "registry_eligible": False,
                    "comparator_accepted": False,
                    "formal_certificate_allowed": False,
                    "decomposition_role": name.rsplit("_", 1)[-1],
                    "source_provenance": {
                        "origin": "coordinator-created O0/O1/O2 decomposition",
                        "upstream_inspiration": "Route-B exact-real/source evaluator audit",
                        "attribution_required": True,
                    },
                    "frontier_repair_contract": {
                        "schema_version": 1,
                        "parent": parent.name,
                        "next_agent_action": sketch,
                        "preserve_semantic_boundary": (
                            "conditional exact-real algebra, Float64 enclosure, and "
                            "global coverage must remain separate"
                        ),
                        "success_callback": (
                            "return pinned Lean/source comparator evidence; child remains "
                            "open until coordinator admission"
                        ),
                        "formal_boundary": "no global residual absorption or flowpipe closure",
                    },
                    "unresolved": [
                        "pinned_lean_compile_receipt",
                        "zero_sorry_and_allowed_axioms_receipt",
                        "statement_comparator_receipt",
                    ],
                },
            )
            child = state.nodes[child_id]
            by_name[name] = child
            changed = True
        elif child.parent_id != parent.id:
            raise ValueError(f"existing child contract mismatch: {name}")
        if child.id not in parent.dependencies:
            parent.dependencies.append(child.id)
            changed = True
        child_ids.append(child.id)

    decomposition = {
        "schema_version": 1,
        "status": "open_O0_O1_O2_pending_pinned_receipts",
        "children": child_ids,
        "child_order": child_ids,
        "closure_rule": "coefficient seam closes only after O0/O1/O2 are registry-verified and a typed parent receipt exists",
        "closure_gate": contract(parent, child_ids),
        "parallelism": "O0, O1, and O2 may be investigated independently; O1 is the smallest next algebraic target",
        "promotion_boundary": "O1 is conditional exact-real only until O2 binds the deployed Float64 evaluator",
    }
    if parent.metadata.get("decomposition_contract") != decomposition:
        parent.metadata["decomposition_contract"] = decomposition
        changed = True
    parent.metadata["math_bottleneck"] = "evaluator_enclosure"
    unresolved = list(dict.fromkeys(
        list(parent.metadata.get("unresolved", [])) + [
            "regularizer_semantics_bridge",
            "exact_real_R_port_aB_equals_rB",
            "float64_evaluator_box_enclosure",
        ]))
    if unresolved != parent.metadata.get("unresolved"):
        parent.metadata["unresolved"] = unresolved
        changed = True
    if changed:
        state.event(
            "routeb_evaluator_enclosure_decomposition_recorded",
            parent_id=parent.id,
            children=child_ids,
            next_algebraic_target="P4.true_dh_exact_real_coefficient_identity",
            registry_promoted=False,
            formal_certificate_allowed=False,
        )
        state.validate()
        store.save(state)
    print({"status": "recorded" if changed else "already_recorded",
           "parent_id": parent.id, "children": child_ids,
           "state_revision": state.revision,
           "next_algebraic_target": "P4.true_dh_exact_real_coefficient_identity"})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
