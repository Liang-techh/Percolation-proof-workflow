"""Record the weighted Frobenius-to-port-energy theorem target."""
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
    generic = find(state, "P4.frobenius_operator_norm_bridge")
    name = "P4.weighted_frobenius_port_energy_bridge"
    metadata = {
        "verification_domain": "lean",
        "research_stage": "P4",
        "statement_status": "formalization_target",
        "claim_status": "weighted_port_energy_bridge_open",
        "evidence_level": "generic-linear-algebra-theorem-target",
        "registry_eligible": False,
        "comparator_accepted": False,
        "formal_certificate_allowed": False,
        "required_node_ids": [generic.id],
        "source_provenance": {
            "origin": "new typed adapter target; no upstream code copied",
            "upstream_inspiration": "Route-B combined-Schur port-energy interface",
            "attribution_required": True,
        },
        "mathematical_contract": {
            "indices": "finite real matrix spaces",
            "premises": [
                "B = S^T S",
                "S is invertible",
                "T = R S^(-1)",
                "||T||_F^2 <= rho",
                "0 <= rho",
            ],
            "conclusion": "for every a, ||R a||_2^2 <= rho * (a^T B a)",
            "proof_route": "generic Frobenius operator bridge on z=S*a, then factor identity",
            "routeb_binding": "B is B_up and R is the declared port map",
            "not_an_E_k_bridge": True,
        },
        "unresolved": [
            "pinned_matrix_factor_api",
            "finite-dimensional_norm_and_transpose_statement_identity",
            "source_binding_of_R_and_B_up",
            "combined_schur_base_residual_premise",
        ],
    }
    existing = next((node for node in state.nodes.values() if node.name == name), None)
    if existing is None:
        node_id = state.add_node(
            name,
            "If B=SᵀS with S invertible, T=R S⁻¹, and "
            "||T||_F²≤rho, then ||R a||₂²≤rho*(aᵀB a) for every a.",
            parent_id=parent.id,
            proof_sketch=(
                "Set z=S*a, use the Frobenius operator bound for T z, and "
                "rewrite ||S*a||₂² as aᵀSᵀS*a. Keep the source binding "
                "of R and B_up outside this generic theorem."),
            metadata=metadata,
        )
        state.event("routeb_weighted_frobenius_bridge_target_added",
                    node_id=node_id, parent_id=parent.id,
                    required_node_ids=[generic.id], registry_promoted=False,
                    formal_certificate_allowed=False)
        store.save(state)
        print({"status": "recorded", "node_id": node_id,
               "state_revision": state.revision})
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
        state.event("routeb_weighted_frobenius_bridge_target_refresh",
                    node_id=existing.id, parent_id=parent.id,
                    required_node_ids=[generic.id], registry_promoted=False,
                    formal_certificate_allowed=False)
        store.save(state)
        print({"status": "refreshed", "node_id": existing.id,
               "state_revision": state.revision})
    else:
        print({"status": "already_recorded", "node_id": existing.id,
               "state_revision": state.revision})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
