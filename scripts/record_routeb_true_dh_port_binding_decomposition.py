"""Decompose the true-DH port source-binding target into semantic leaves."""
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
        "P4.true_dh_force_descriptor_semantics",
        "On the canonical source, bind the same regularized force equation and central-FD C/G semantics used by the deployed DH acceleration.",
        "Read the source force formula and descriptor solve as one typed real interface, explicitly retaining mu=1/1000000 and h=1/100000; do not infer exact-real equality from Float64 execution.",
        "source_semantics",
    ),
    (
        "P4.true_dh_block_projection_B",
        "Project the common descriptor equation to block B and expose r_B=M_BB(q)a_B+M_BD(q)a_D, with the remote term retained explicitly.",
        "Use a typed finite-dimensional block projection with the declared B=(4,5), D=(1,2,3,6) coordinates; reject replacement of M_BD*a_D by a nominal or difference surrogate.",
        "block_projection",
    ),
    (
        "P4.true_dh_residual_map_coefficient_binding",
        "Prove that the residual map R_port consumed by the Frobenius port bound has exactly the deployed source coefficients, so R_port*a_B=r_B on the common declared domain.",
        "Compare source-defined force/residual coefficients in force coordinates against the typed port map, including the kc scale and regularizer; expose any unmatched coefficient as an obstruction rather than weakening the statement.",
        "coefficient_binding",
    ),
)


def main() -> int:
    store = StateStore(ROOT / "artifacts/routeb_6dof/state.json")
    state = store.load()
    parent = find(state, "P4.true_dh_port_source_binding")
    by_name = {node.name: node for node in state.nodes.values()}
    child_ids: list[str] = []
    changed = False
    for name, statement, sketch, role in CHILDREN:
        child = by_name.get(name)
        if child is None:
            child_id = state.add_node(
                name, statement, parent_id=parent.id, proof_sketch=sketch,
                metadata={
                    "verification_domain": "lean",
                    "research_stage": "P4",
                    "math_lane": "source_semantics",
                    "math_bottleneck": "source_binding",
                    "statement_status": "formalization_target",
                    "claim_status": "true_dh_port_binding_child_open",
                    "evidence_level": "typed-source-binding-target",
                    "registry_eligible": False,
                    "comparator_accepted": False,
                    "formal_certificate_allowed": False,
                    "decomposition_role": role,
                    "source_provenance": {
                        "origin": "coordinator-created decomposition of the true-DH port binding target",
                        "upstream_inspiration": "Route-B DH source contract and block-(4,5) descriptor bridge",
                        "attribution_required": True,
                    },
                    "frontier_repair_contract": {
                        "schema_version": 1,
                        "parent": parent.name,
                        "role": role,
                        "next_agent_action": sketch,
                        "preserve_semantic_boundary": "force scale, regularizer, FD semantics, and M_BD*a_D must remain explicit",
                        "success_callback": "return pinned Lean/source comparator evidence to coordinator; child remains open until accepted",
                        "formal_boundary": "source-binding target only; no interval coverage, residual absorption, or global gate",
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
        elif child.statement != statement:
            # One intentional semantic migration: the original target used
            # the unsigned gain matrix R, while the descriptor equations
            # require the actual port map R_port=-R_gain. Preserve the node
            # identity but update this statement so stale agents cannot
            # continue proving the wrong sign.
            if (name == "P4.true_dh_residual_map_coefficient_binding"
                    and "residual map R consumed" in child.statement
                    and "R*a_B=r_B" in child.statement):
                child.statement = statement
                changed = True
            else:
                raise ValueError(f"existing child contract mismatch: {name}")
        if child.id not in parent.dependencies:
            parent.dependencies.append(child.id)
            changed = True
        child_ids.append(child.id)

    decomposition = {
        "schema_version": 1,
        "status": "open_children_pending_pinned_receipts",
        "children": child_ids,
        "child_order": child_ids,
        "closure_rule": "true-DH port source binding closes only after all three semantic children are VERIFIED",
        "closure_gate": {
            "schema_version": 1,
            "required_child_ids": child_ids,
            "required_parent_receipt": "typed_true_dh_port_source_binding",
            "required_obligations": [
                "coefficient_level_R_port_aB_equals_rB_identity",
                "typed_R_port_aB_equals_rB_adapter",
                "same_regularizer_and_fd_semantics",
            ],
            "repair_route": {
                "owner": "P4.true_dh_residual_map_coefficient_binding",
                "action": "build_typed_R_port_aB_equals_rB_adapter",
            },
            "promotion_boundary": "children and parent receipt must be registry-eligible before parent assembly",
        },
        "parallelism": "source semantics, block projection, and coefficient comparison may be investigated independently; no child is treated as proof of another",
        "promotion_boundary": "all children remain below registry until source, comparator, and global domain gates close",
    }
    parent.metadata.setdefault("parent_receipts", {})
    if parent.metadata.get("decomposition_contract") != decomposition:
        parent.metadata["decomposition_contract"] = decomposition
        changed = True
    parent.proof_sketch = (
        "Split the source binding into canonical force/descriptor semantics, an "
        "exact B-block projection retaining M_BD*a_D, and a coefficient-level "
        "identity for the residual map R_port. Keep all three source/Lean obligations "
        "separate from numerical port budgets and global coverage."
    )
    if changed:
        state.event(
            "routeb_true_dh_port_binding_decomposition_recorded",
            parent_id=parent.id,
            children=child_ids,
            registry_promoted=False,
            formal_certificate_allowed=False,
        )
        state.validate()
        store.save(state)
        print({"status": "recorded", "parent_id": parent.id,
               "children": child_ids, "state_revision": state.revision})
    else:
        print({"status": "already_recorded", "parent_id": parent.id,
               "children": child_ids, "state_revision": state.revision})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
