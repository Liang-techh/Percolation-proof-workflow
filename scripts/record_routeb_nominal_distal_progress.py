"""Record the nominal distal descriptor bridge as the preferred Route-B P4 child."""
from __future__ import annotations

import hashlib
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
EXTERNAL = (ROOT.parent / "6dof_sos_optimized" / "6dof_sos_optimized")
TARGET = EXTERNAL / "routeB_dense_Mq"
sys.path.insert(0, str(ROOT / "src"))

from percolation_workflow.store import StateStore


def ref(path: Path) -> dict[str, str]:
    return {"path": str(path.resolve()),
            "sha256": hashlib.sha256(path.read_bytes()).hexdigest()}


def find(state, name: str):
    for node in state.nodes.values():
        if node.name == name:
            return node
    raise ValueError(f"missing node: {name}")


def main() -> int:
    state_path = ROOT / "artifacts/routeb_6dof/state.json"
    store = StateStore(state_path)
    state = store.load()
    if state.project != "routeb-6dof-external":
        raise ValueError(f"unexpected project: {state.project!r}")

    name = "P4.nominal_distal_descriptor_bridge"
    audit = TARGET / "routeB_compact_dh_nominal_distal_bridge_audit.csv"
    interface = TARGET / "routeB_compact_nominal_descriptor_interface.csv"
    source = TARGET / "dhport_lib.jl"
    design = TARGET / "P4_PHYSICAL_RATIONAL_DESCRIPTOR_BRIDGE.md"
    dh_audit = TARGET / "P5_COMPACT_DH_NOMINAL_DISTAL_BRIDGE_AUDIT.md"
    nominal_doc = TARGET / "P5_COMPACT_NOMINAL_DESCRIPTOR_INTERFACE.md"
    bridge_meta = TARGET / "routeB_physical_rational_descriptor_bridge.csv"
    tail_meta = TARGET / "routeB_physical_rational_tail_pmi_scalar_meta.csv"
    tail_scalar = TARGET / "routeB_physical_rational_tail_pmi_scalar.csv"
    tail_polynomial = TARGET / "routeB_physical_rational_tail_cs_polynomial.csv"
    m0 = TARGET / "routeB_Mq_M0.csv"
    reform = EXTERNAL / "PROJECT_REFORM_TARGET.md"
    contract = ROOT / "src/percolation_workflow/routeb_nominal_distal_contract.py"
    source_artifacts = [ref(path) for path in
                        (audit, interface, source, design, dh_audit, nominal_doc,
                         bridge_meta, tail_meta,
                         tail_scalar, tail_polynomial, m0, reform, contract)]

    existing = next((n for n in state.nodes.values() if n.name == name), None)
    p4 = find(state, "P4.residual_schur_pmi")
    mathematical_contract = {
        "descriptor_equations": [
            "M_mu,DD(q)*v + (M_DB(q)-M0_DB)*a_B = 0",
            "r_B - M_BD(q)*v = 0",
        ],
        "nominal_subtraction": "M_mu,DD*a_D^nom + M0_DB*a_B - b_D = 0",
        "regularization": "M_mu(q)=M(q)+(1/1000000)I; no unregularized mass may be mixed into this branch",
        "polynomial_boundary": "the descriptor identities are exact inverse-free algebraic equalities; they do not prove interval remainder, SOS positivity, flowpipe, or terminal transfer",
        "port_semantics": "the compact PMI consumes raw Euclidean r_B^T*r_B with gamma_k >= rho_k^2; an energy-normalized two-sided metric needs a separate typed conversion",
        "metric_orientation": "for W^(1/2) R B_up^(-1/2), W scales output rows on the left; old right-scaled weighted ledgers are not interchangeable",
        "angle_bridge": "q-box interval bounds cannot be inserted into c/s SOS coefficients without a certified cos/sin graph or an explicit external robust-budget adapter",
        "preferred_consumption": "combined Schur/Young on L_B=l_base+r_B; do not relabel the raw port bound as robust-PMI E_k",
    }
    extra_unresolved = [
        "certified q-to-cs angle graph or external interval-to-polynomial adapter",
        "raw Euclidean port gamma_k versus energy-normalized cross-term metric binding",
    ]
    if existing is not None:
        changed = False
        if existing.metadata.get("source_artifacts") != source_artifacts:
            existing.metadata["source_artifacts"] = source_artifacts
            changed = True
        if existing.metadata.get("mathematical_contract") != mathematical_contract:
            existing.metadata["mathematical_contract"] = mathematical_contract
            changed = True
        unresolved = list(existing.metadata.get("unresolved", []))
        for item in extra_unresolved:
            if item not in unresolved:
                unresolved.append(item)
        if unresolved != existing.metadata.get("unresolved"):
            existing.metadata["unresolved"] = unresolved
            changed = True
        if existing.id not in p4.dependencies:
            p4.dependencies.append(existing.id)
            changed = True
        if not changed:
            print({"status": "already_recorded", "node_id": existing.id,
                   "state_revision": state.revision})
            return 0
        state.event(
            "routeb_nominal_distal_bridge_provenance_refresh",
            node_id=existing.id, parent_id=p4.id,
            source_artifacts=source_artifacts,
            status=existing.metadata.get("statement_status"),
            formal_certificate_allowed=False, registry_promoted=False,
        )
        store.save(state)
        print({"status": "provenance_refreshed", "node_id": existing.id,
               "state_revision": state.revision})
        return 0

    node_id = state.add_node(
        name,
        "The block-(4,5) Route-B residual closes through a nominal distal "
        "remote descriptor a_D^nom, reduced variable v, and retained port "
        "r_B-M_BD*v, with exact rational bridge identities.",
        dependencies=[],
        proof_sketch=(
            "Use M_mu,DD*a_D^nom=b_D-M0_DB*a_B; derive "
            "M_mu,DD*v+DeltaM_DB*a_B=0 and r_B-M_BD*v=0. "
            "Keep the retained M_BD*S*y contribution in the descriptor "
            "linking equations and certify the tail PMI without a coarse "
            "norm re-charge."
        ),
        metadata={
            "verification_domain": "lean-source-independent",
            "statement_status": "pending_source_binding_and_pinned_compile",
            "evidence_level": "exact_descriptor_design",
            "claim_status": "algebraic_bridge_open",
            "registry_eligible": False,
            "comparator_accepted": False,
            "formal_certificate_allowed": False,
            "preferred_route": True,
            "fallback_route": False,
            "competes_with": [
                "P4.remote_acceleration_budget",
                "P4.vector_remote_budget_pmi_composition",
            ],
            "source_artifacts": source_artifacts,
            "mathematical_contract": mathematical_contract,
            "unresolved": [
                "source_binding_of_nominal_and_reduced_DH_descriptors",
                "rational_tail_PMI_or_co-state_aware_Schur_certificate",
                "covered_domain_and_global_residual_absorption",
                "pinned_lean_compile_and_comparator_receipt",
                *extra_unresolved,
            ],
        },
    )
    p4.dependencies.append(node_id)
    state.event(
        "routeb_nominal_distal_bridge_checkpoint",
        node_id=node_id, parent_id=p4.id,
        source_artifacts=source_artifacts,
        preferred_route=True, fallback_route=False,
        status="pending_source_binding_and_pinned_compile",
        formal_certificate_allowed=False, registry_promoted=False,
    )
    store.save(state)
    print({"status": "recorded", "node_id": node_id,
           "state_revision": state.revision})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
