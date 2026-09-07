"""Refine the combined-Schur adapter into independently provable lemmas."""
from __future__ import annotations

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from percolation_workflow.store import StateStore


def find(state, name: str):
    for node in state.nodes.values():
        if node.name == name:
            return node
    raise ValueError(f"missing node: {name}")


def add_or_refresh(state, parent, name, statement, proof_sketch, metadata, event):
    existing = next((node for node in state.nodes.values() if node.name == name), None)
    if existing is None:
        node_id = state.add_node(
            name,
            statement,
            parent_id=parent.id,
            proof_sketch=proof_sketch,
            metadata=metadata,
        )
        state.event(event + "_added", node_id=node_id, parent_id=parent.id,
                    registry_promoted=False, formal_certificate_allowed=False)
        return True, node_id
    changed = False
    if existing.parent_id != parent.id:
        existing.parent_id = parent.id
        changed = True
    for key, value in metadata.items():
        if existing.metadata.get(key) != value:
            existing.metadata[key] = value
            changed = True
    if changed:
        state.event(event + "_refresh", node_id=existing.id, parent_id=parent.id,
                    registry_promoted=False, formal_certificate_allowed=False)
    return changed, existing.id


def main() -> int:
    store = StateStore(ROOT / "artifacts/routeb_6dof/state.json")
    state = store.load()
    parent = find(state, "P4.combined_schur_port_energy_adapter")
    common = {
        "verification_domain": "lean",
        "research_stage": "P4",
        "statement_status": "formalization_target",
        "evidence_level": "generic-real-inner-product-lemma-target",
        "registry_eligible": False,
        "comparator_accepted": False,
        "formal_certificate_allowed": False,
        "source_provenance": {
            "origin": "new decomposition lemma; no upstream code copied",
            "upstream_inspiration": "Route-B combined-Schur/Young interface",
            "attribution_required": True,
        },
    }
    expansion_meta = {
        **common,
        "claim_status": "norm_square_expansion_open",
        "mathematical_contract": {
            "premises": ["l and r are vectors in a real inner-product space"],
            "conclusion": "||l+r||₂² = ||l||₂² + 2*<l,r> + ||r||₂²",
            "consumption": "exact first step of the combined-Schur adapter",
        },
        "unresolved": ["pinned_real_inner_product_norm_sq API", "finite-dimensional coercion identity"],
    }
    young_meta = {
        **common,
        "claim_status": "young_cross_term_bound_open",
        "mathematical_contract": {
            "premises": ["theta > 0", "l and r are vectors in a real inner-product space"],
            "conclusion": "2*<l,r> ≤ theta*||l||₂² + theta⁻¹*||r||₂²",
            "consumption": "cross-term absorption in the combined-Schur adapter",
        },
        "unresolved": ["pinned Cauchy-Schwarz/Young lemma names", "strict positive theta division API"],
    }
    changed = False
    for args in [
        (
            "P4.real_norm_square_expansion",
            "For real finite-dimensional vectors l,r, ||l+r||₂² = ||l||₂² + 2*<l,r> + ||r||₂².",
            "Expand the inner product bilinearly and use the norm-square definition; keep this identity independent of Route-B source semantics.",
            expansion_meta,
            "routeb_norm_square_expansion_target",
        ),
        (
            "P4.young_cross_term_bound",
            "For theta>0 and real finite-dimensional vectors l,r, 2*<l,r> ≤ theta*||l||₂² + theta⁻¹*||r||₂².",
            "Apply Cauchy-Schwarz followed by the scalar Young inequality, with strict positivity of theta explicit.",
            young_meta,
            "routeb_young_cross_term_target",
        ),
    ]:
        did_change, _ = add_or_refresh(state, parent, *args)
        changed = changed or did_change
    if changed:
        store.save(state)
    print({"status": "recorded" if changed else "already_recorded",
           "state_revision": state.revision,
           "children": [
               find(state, "P4.real_norm_square_expansion").id,
               find(state, "P4.young_cross_term_bound").id,
           ]})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
