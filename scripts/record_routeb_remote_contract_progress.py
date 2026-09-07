"""Record the remote-action contract and acceleration budget in the Route-B DAG.

This is an idempotent state migration for a mathematical child.  It records a
pending conditional interface only; it never promotes a theorem or changes the
formal admission gate.
"""
from __future__ import annotations

import hashlib
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from percolation_workflow.store import StateStore


def file_ref(path: Path) -> dict[str, str]:
    return {
        "path": str(path.resolve()),
        "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
    }


def find_node(state, name: str):
    for node in state.nodes.values():
        if node.name == name:
            return node
    raise ValueError(f"missing Route-B node: {name}")


def main() -> int:
    state_path = ROOT / "artifacts/routeb_6dof/state.json"
    store = StateStore(state_path)
    state = store.load()
    if state.project != "routeb-6dof-external":
        raise ValueError(f"unexpected project: {state.project!r}")

    name = "P4.remote_acceleration_budget"
    existing = next((node for node in state.nodes.values() if node.name == name), None)
    if existing is not None:
        print({"status": "already_recorded", "node_id": existing.id,
               "state_revision": state.revision})
        return 0

    p4 = find_node(state, "P4.residual_schur_pmi")
    dual = find_node(state, "RouteBRotationalDual.dh_axes_mass_dual")
    contract = ROOT / "src/percolation_workflow/routeb_remote_contract.py"
    budget = ROOT / "src/percolation_workflow/routeb_remote_accel_budget.py"
    node_id = state.add_node(
        name,
        "Under a same-key full-state dual premise, the remote acceleration block "
        "D=(1,2,3,6) satisfies ||a_D||^2 <= 90*mass and can feed an admissible "
        "M_BD a_D binding.",
        dependencies=[dual.id],
        proof_sketch=(
            "Restrict the compiled full-state scalar coercivity lemma to D; "
            "then bind the resulting mass budget and M_BD operator through "
            "the routeb.remote_binding.v1 contract."
        ),
        metadata={
            "verification_domain": "conditional-lean-plus-source-adapter",
            "statement_status": "conditional_candidate",
            "evidence_level": "compiled_candidate_arithmetic_seam",
            "claim_status": "full_state_source_binding_open",
            "registry_eligible": False,
            "comparator_accepted": False,
            "formal_certificate_allowed": False,
            "binding_mode_candidates": ["full_state", "d_row_schur"],
            "remote_coordinates": [1, 2, 3, 6],
            "euclidean_squared_coefficient": "90",
            "conditional_budget_artifact": file_ref(budget),
            "typed_contract_artifact": file_ref(contract),
            "upstream_dual_node": dual.id,
            "unresolved": [
                "mass_is_same_deployed_full_state_kinetic_budget",
                "MBD_operator_bound_on_covered_domain",
                "descriptor_identity_or_exact_schur_elimination",
                "true_DH_and_flowpipe_coverage",
            ],
        },
    )
    # Dependencies are prerequisite edges in the authoritative WorkflowState.
    # Keep the P4 parent open until this new child and all existing prerequisites
    # are closed through the normal verification path.
    p4.dependencies.append(node_id)
    state.event(
        "routeb_remote_contract_math_checkpoint",
        node_id=node_id,
        parent_id=p4.id,
        upstream_node=dual.id,
        budget_artifact=file_ref(budget),
        contract_artifact=file_ref(contract),
        coefficient="90",
        status="conditional_candidate",
        formal_certificate_allowed=False,
        registry_promoted=False,
    )
    store.save(state)
    print({"status": "recorded", "node_id": node_id,
           "state_revision": state.revision, "formal_certificate_allowed": False})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
