"""Record the combined-Schur/Young port-energy adapter target."""
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


def main() -> int:
    store = StateStore(ROOT / "artifacts/routeb_6dof/state.json")
    state = store.load()
    parent = find(state, "P4.residual_port_frobenius_bound")
    weighted = find(state, "P4.weighted_frobenius_port_energy_bridge")
    name = "P4.combined_schur_port_energy_adapter"
    metadata = {
        "verification_domain": "lean",
        "research_stage": "P4",
        "statement_status": "formalization_target",
        "claim_status": "combined_schur_port_adapter_open",
        "evidence_level": "typed-inequality-adapter-target",
        "registry_eligible": False,
        "comparator_accepted": False,
        "formal_certificate_allowed": False,
        "required_node_ids": [weighted.id],
        "source_provenance": {
            "origin": "new typed adapter target; no upstream code copied",
            "upstream_inspiration": "Route-B P5_COMPACT_COMBINED_SCHUR_INTERFACE.md",
            "attribution_required": True,
        },
        "mathematical_contract": {
            "variables": "real finite-dimensional vectors l and r",
            "rho_semantics": "rho is rho_F^2, the squared Frobenius budget; it is not rho_F",
            "energy_symbol": "A is A_up = a_B^T B_up a_B",
            "premises": [
                "theta > 0",
                "||r||_2^2 <= rho * A",
                "b >= (1+theta)||l||_2^2 + (1+1/theta)rho*A",
            ],
            "conclusion": "||l+r||_2^2 <= b",
            "proof_route": "expand the square, apply Young 2<l,r> <= theta||l||^2 + theta^(-1)||r||^2, then consume the weighted port-energy bound",
            "routeb_binding": "l is the declared base residual, A=A_up=a_B^T B_up a_B, and rho=rho_F^2; source binding remains an adapter obligation",
            "not_an_E_k_bridge": True,
            "not_a_pmi_closure": True,
        },
        "unresolved": [
            "pinned_inner_product_norm_sq_expansion_api",
            "strict_positive_theta_division_api",
            "typed_binding_of_l_base_and_A_up",
            "residual_PMI_and_flowpipe_consumption",
        ],
    }
    existing = next((node for node in state.nodes.values() if node.name == name), None)
    if existing is None:
        node_id = state.add_node(
            name,
            "If theta>0, ||r||₂²≤rho*A, and "
            "b≥(1+theta)||l||₂²+(1+1/theta)rho*A, then "
            "||l+r||₂²≤b.",
            parent_id=parent.id,
            proof_sketch=(
                "Use the exact norm-square expansion and Young's inequality "
                "for the cross term. Keep rho*A as the typed port-energy "
                "input supplied by the weighted Frobenius adapter; do not "
                "reinterpret it as robust-PMI E_k or claim global closure."),
            metadata=metadata,
        )
        state.event(
            "routeb_combined_schur_adapter_target_added",
            node_id=node_id,
            parent_id=parent.id,
            required_node_ids=[weighted.id],
            registry_promoted=False,
            formal_certificate_allowed=False,
        )
        store.save(state)
        print({"status": "recorded", "node_id": node_id, "state_revision": state.revision})
        return 0
    changed = False
    for key, value in metadata.items():
        if existing.metadata.get(key) != value:
            existing.metadata[key] = value
            changed = True
    if existing.parent_id != parent.id:
        existing.parent_id = parent.id
        changed = True
    if changed:
        state.event(
            "routeb_combined_schur_adapter_target_refresh",
            node_id=existing.id,
            parent_id=parent.id,
            required_node_ids=[weighted.id],
            registry_promoted=False,
            formal_certificate_allowed=False,
        )
        store.save(state)
        print({"status": "refreshed", "node_id": existing.id, "state_revision": state.revision})
    else:
        print({"status": "already_recorded", "node_id": existing.id, "state_revision": state.revision})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
