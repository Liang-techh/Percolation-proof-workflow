"""Record exact target-minus-opt Gram reconstruction as a separate P4 leaf."""
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
    store = StateStore(ROOT / "artifacts/routeb_6dof/state.json")
    state = store.load()
    if state.project != "routeb-6dof-external":
        raise ValueError(f"unexpected project: {state.project!r}")
    parent = find(state, "P4.residual_schur_pmi")
    name = "P4.nominal_distal_gram_reconstruction"
    source_artifacts = [ref(path) for path in (
        TARGET / "routeB_physical_rational_tail_pmi_scalar.csv",
        TARGET / "routeB_tail_pmi_scalar_gram_rational_audit.csv",
        TARGET / "routeB_tail_pmi_scalar_gram_rational.csv",
        TARGET / "routeB_tail_pmi_scalar_gram_basis.csv",
        TARGET / "routeB_tail_pmi_scalar_gram_probe.jl",
        TARGET / "routeB_physical_rational_tail_pmi_scalar_meta.csv",
        ROOT / "scripts/check_routeb_rational_gram_payload.py",
        ROOT / "src/percolation_workflow/routeb_nominal_distal_contract.py",
    )]
    unresolved = [
        "exact_opt_lower_bound_receipt",
        "target_minus_opt_exact_monomial_expansion",
        "rationalized_gram_residual_l1_bound",
        "pinned_lean_kernel_and_comparator_receipt",
    ]
    existing = next((n for n in state.nodes.values() if n.name == name), None)
    if existing is not None:
        changed = existing.metadata.get("source_artifacts") != source_artifacts
        if existing.metadata.get("unresolved") != unresolved:
            existing.metadata["unresolved"] = unresolved
            changed = True
        if existing.id not in parent.dependencies:
            parent.dependencies.append(existing.id)
            changed = True
        if changed:
            existing.metadata["source_artifacts"] = source_artifacts
            state.event(
                "routeb_tail_gram_reconstruction_provenance_refresh",
                node_id=existing.id, parent_id=parent.id,
                source_artifacts=source_artifacts,
                status=existing.metadata.get("statement_status"),
                formal_certificate_allowed=False, registry_promoted=False,
            )
            store.save(state)
            print({"status": "provenance_refreshed", "node_id": existing.id,
                   "state_revision": state.revision})
        else:
            print({"status": "already_recorded", "node_id": existing.id,
                   "state_revision": state.revision})
        return 0

    node_id = state.add_node(
        name,
        "The rational Gram payload reconstructs the scaled tail PMI "
        "minus its certified lower-bound candidate, modulo the box and "
        "circle generators, with an exact residual bound.",
        dependencies=[],
        proof_sketch=(
            "Parse the local monomial bases and every rational Gram block; "
            "expand the 14 blocks and three circle multipliers exactly. "
            "Bind the exact objective lower bound, compute the target-minus-"
            "expansion residual, and close it with a rational coefficient "
            "l1 bound. Keep this candidate separate from kernel admission."
        ),
        metadata={
            "verification_domain": "lean-source-independent",
            "statement_status": "pending_exact_target_minus_opt_reconstruction",
            "evidence_level": "rationalized_gram_candidate",
            "claim_status": "tail_gram_identity_open",
            "registry_eligible": False,
            "comparator_accepted": False,
            "formal_certificate_allowed": False,
            "preferred_route": True,
            "unresolved": unresolved,
            "source_artifacts": source_artifacts,
        },
    )
    parent.dependencies.append(node_id)
    state.event(
        "routeb_tail_gram_reconstruction_checkpoint",
        node_id=node_id, parent_id=parent.id,
        source_artifacts=source_artifacts,
        status="pending_exact_target_minus_opt_reconstruction",
        formal_certificate_allowed=False, registry_promoted=False,
    )
    store.save(state)
    print({"status": "recorded", "node_id": node_id,
           "state_revision": state.revision})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
