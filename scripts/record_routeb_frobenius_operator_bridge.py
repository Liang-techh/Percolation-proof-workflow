"""Add the generic finite-dimensional Frobenius operator bridge target."""
from __future__ import annotations

import hashlib
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from percolation_workflow.store import StateStore


def ref(path: Path) -> dict[str, str]:
    return {"path": str(path.resolve()),
            "sha256": hashlib.sha256(path.read_bytes()).hexdigest().upper()}


def find(state, name: str):
    for node in state.nodes.values():
        if node.name == name:
            return node
    raise ValueError(f"missing node: {name}")


def main() -> int:
    store = StateStore(ROOT / "artifacts/routeb_6dof/state.json")
    state = store.load()
    parent = find(state, "P4.residual_port_frobenius_bound")
    name = "P4.frobenius_operator_norm_bridge"
    metadata = {
        "verification_domain": "lean",
        "research_stage": "P4",
        "statement_status": "formalization_target",
        "claim_status": "operator_norm_bridge_open",
        "evidence_level": "generic-linear-algebra-theorem-target",
        "registry_eligible": False,
        "comparator_accepted": False,
        "formal_certificate_allowed": False,
        "source_provenance": {
            "origin": "new generic theorem target; no upstream code copied",
            "upstream_inspiration": "Anthropic FLT derivation/calculus and linear-algebra transport patterns",
            "attribution_required": True,
        },
        "mathematical_contract": {
            "indices": "finite I and finite J",
            "matrix": "T : I -> J -> R",
            "vector": "z : J -> R",
            "entrywise_factor": "U : I -> J -> R",
            "premises": [
                "0 <= U i j",
                "|T i j| <= U i j",
            ],
            "conclusion": "||T z||_2^2 <= (sum i j, U i j ^ 2) * ||z||_2^2",
            "consumption": "a fixed interval entry upper matrix yields a valid E_k Frobenius factor",
            "no_pointwise_norm_order": True,
        },
        "unresolved": [
            "pinned_mathlib_matrix_or_finsupp_api",
            "finite_sum_reindexing_and_cauchy_schwarz_lemma_names",
            "interval_entry_upper_bound_source_binding",
            "residual_PMI_and_flowpipe_consumption",
        ],
    }
    existing = next((node for node in state.nodes.values() if node.name == name), None)
    if existing is None:
        node_id = state.add_node(
            name,
            "For finite real matrices T and entrywise upper bounds U >= 0, "
            "the squared Euclidean operator action satisfies "
            "||T z||_2^2 <= (sum_{i,j} U_{i,j}^2) ||z||_2^2.",
            parent_id=parent.id,
            proof_sketch=(
                "Expand each output coordinate, apply Cauchy-Schwarz to the "
                "row dot product, sum rows, and use |T_ij| <= U_ij. Keep "
                "this generic bridge separate from interval rounding and "
                "from the choice between Frobenius and induced estimates."),
            metadata=metadata,
        )
        state.event("routeb_frobenius_operator_bridge_target_added",
                    node_id=node_id, parent_id=parent.id,
                    registry_promoted=False, formal_certificate_allowed=False)
        store.save(state)
        print({"status": "recorded", "node_id": node_id,
               "state_revision": state.revision})
        return 0
    changed = False
    for key, value in metadata.items():
        if existing.metadata.get(key) != value:
            existing.metadata[key] = value
            changed = True
    if changed:
        state.event("routeb_frobenius_operator_bridge_target_refresh",
                    node_id=existing.id, parent_id=parent.id,
                    registry_promoted=False, formal_certificate_allowed=False)
        store.save(state)
        print({"status": "refreshed", "node_id": existing.id,
               "state_revision": state.revision})
    else:
        print({"status": "already_recorded", "node_id": existing.id,
               "state_revision": state.revision})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
