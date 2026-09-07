"""Decompose the generic Young cross-term target into reusable math leaves."""
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
        "P4.inner_product_cauchy_schwarz",
        "For finite real vectors l,r, prove <l,r> <= ||l||₂*||r||₂ and hence 2<l,r> <= 2||l||₂||r||₂.",
        "Apply the pinned real inner-product Cauchy–Schwarz theorem and multiply by the nonnegative scalar 2.",
        "first derive the vector cross-term bound",
    ),
    (
        "P4.scalar_young_square",
        "For theta>0 and nonnegative real x,y, prove 2*x*y <= theta*x^2 + theta^(-1)*y^2.",
        "Use the nonnegativity of (sqrt(theta)*x - y/sqrt(theta))^2 or an equivalent division-free square identity; keep theta positivity explicit.",
        "then convert the product of norms to the theta-budget",
    ),
    (
        "P4.norm_nonneg_for_young",
        "For finite real vectors l,r, prove 0<=||l||₂ and 0<=||r||₂ for the scalar Young instantiation.",
        "Use norm nonnegativity only as a typed premise bridge; this child carries no Route-B source or numerical semantics.",
        "supply nonnegative scalar premises",
    ),
)


def main() -> int:
    store = StateStore(ROOT / "artifacts/routeb_6dof/state.json")
    state = store.load()
    parent = find(state, "P4.young_cross_term_bound")
    by_name = {node.name: node for node in state.nodes.values()}
    child_ids = []
    changed = False
    for name, statement, sketch, action in CHILDREN:
        child = by_name.get(name)
        if child is None:
            child_id = state.add_node(
                name, statement, parent_id=parent.id, proof_sketch=sketch,
                metadata={
                    "verification_domain": "lean",
                    "statement_status": "formalization_target",
                    "claim_status": "young_decomposition_child_open",
                    "evidence_level": "generic-real-inequality-target",
                    "registry_eligible": False,
                    "comparator_accepted": False,
                    "formal_certificate_allowed": False,
                    "source_provenance": {
                        "origin": "coordinator-created decomposition of generic Route-B Young lemma",
                        "upstream_inspiration": "Route-B combined-Schur/Young interface",
                        "attribution_required": True,
                    },
                    "decomposition_role": "young_cross_term",
                    "frontier_repair_contract": {
                        "schema_version": 1,
                        "parent": parent.name,
                        "next_agent_action": action,
                        "formal_boundary": "generic real finite-dimensional inequality only",
                        "promotion_blocked_until": [
                            "pinned_lean_compile_receipt",
                            "zero_sorry_and_allowed_axioms_receipt",
                            "statement_comparator_receipt",
                        ],
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
        elif child.statement != statement or child.parent_id != parent.id:
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
        "closure_rule": "Young cross-term closes only after all three generic children are VERIFIED",
        "routeb_boundary": "combined-Schur/source/port/coverage remain independent consumers",
    }
    if parent.metadata.get("decomposition_contract") != decomposition:
        parent.metadata["decomposition_contract"] = decomposition
        changed = True
    parent.proof_sketch = (
        "Bound the vector cross term by Cauchy–Schwarz, instantiate scalar Young "
        "at nonnegative norms with explicit theta>0, and preserve the generic "
        "lemma as independent from Route-B source and coverage semantics."
    )
    if changed:
        state.event(
            "routeb_young_cross_term_decomposition_recorded",
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
