"""Record the physical nominal-distal tail PMI as an independent P4 leaf."""
from __future__ import annotations

import hashlib
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
EXTERNAL = ROOT.parent / "6dof_sos_optimized" / "6dof_sos_optimized"
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
    name = "P4.nominal_distal_tail_pmi"
    parent = find(state, "P4.residual_schur_pmi")
    source_artifacts = [ref(path) for path in (
        TARGET / "routeB_physical_rational_descriptor_bridge.csv",
        TARGET / "routeB_physical_rational_tail_cs_polynomial.csv",
        TARGET / "routeB_physical_rational_tail_pmi_scalar.csv",
        TARGET / "routeB_physical_rational_tail_pmi_scalar_meta.csv",
        TARGET / "routeB_tail_pmi_scalar_gram_rational_audit.csv",
        TARGET / "P4_PHYSICAL_RATIONAL_TAIL_PMI_SCALAR.md",
        ROOT / "src/percolation_workflow/routeb_nominal_distal_contract.py",
    )]

    existing = next((n for n in state.nodes.values() if n.name == name), None)
    if existing is not None:
        changed = existing.metadata.get("source_artifacts") != source_artifacts
        if changed:
            existing.metadata["source_artifacts"] = source_artifacts
            state.event(
                "routeb_nominal_tail_pmi_provenance_refresh",
                node_id=existing.id, parent_id=parent.id,
                source_artifacts=source_artifacts,
                status=existing.metadata.get("statement_status"),
                formal_certificate_allowed=False, registry_promoted=False,
            )
        if existing.id not in parent.dependencies:
            parent.dependencies.append(existing.id)
            changed = True
        if changed:
            store.save(state)
            print({"status": "provenance_refreshed", "node_id": existing.id,
                   "state_revision": state.revision})
        else:
            print({"status": "already_recorded", "node_id": existing.id,
                   "state_revision": state.revision})
        return 0

    node_id = state.add_node(
        name,
        "The full 3x3 square-root-free tail PMI for "
        "[delta^2*rho, (M_BD*r_hat)'; M_BD*r_hat, M0_BB] is "
        "nonnegative on the lifted trigonometric domain.",
        dependencies=[],
        proof_sketch=(
            "Use the exact rational scalar Schur polynomial "
            "delta^2*rho*det(M0_BB)-M22*g1^2+2*M12*g1*g2-M11*g2^2. "
            "Retain the off-diagonal M0_BB term and prove nonnegativity "
            "with exact SOS/ideal or a pinned Lean certificate; do not "
            "replace it by two independent component gains."
        ),
        metadata={
            "verification_domain": "lean-source-independent",
            "statement_status": "pending_exact_tail_positivity_and_pinned_compile",
            "evidence_level": "exact_rational_sos_input_candidate",
            "claim_status": "tail_pmi_global_positivity_open",
            "registry_eligible": False,
            "comparator_accepted": False,
            "formal_certificate_allowed": False,
            "preferred_route": True,
            "unresolved": [
                "exact_nonnegativity_on_circle_identities_and_q_domain",
                "certified_gram_or_Lean_proof_of_27_term_scalar_polynomial",
                "finite_difference_and_partition_remainder_absorption",
                "pinned_lean_compile_and_comparator_receipt",
            ],
            "source_artifacts": source_artifacts,
        },
    )
    parent.dependencies.append(node_id)
    state.event(
        "routeb_nominal_tail_pmi_checkpoint",
        node_id=node_id, parent_id=parent.id,
        source_artifacts=source_artifacts,
        scalar_terms=27, scalar_max_total_cs_degree=6,
        status="pending_exact_tail_positivity_and_pinned_compile",
        formal_certificate_allowed=False, registry_promoted=False,
    )
    store.save(state)
    print({"status": "recorded", "node_id": node_id,
           "state_revision": state.revision})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
