"""Attach the reusable residual-l1 Lean seam to the Route-B P4 DAG."""
from __future__ import annotations

import hashlib
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
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
    parent = find(state, "P4.nominal_distal_gram_reconstruction")
    name = "P4.nominal_distal_residual_l1_lean_seam"
    source_artifacts = [ref(path) for path in (
        ROOT / "examples/routeb_gram_residual_lean/GramResidual.lean",
        ROOT / "examples/routeb_gram_residual_lean/README.md",
    )]
    unresolved = [
        "pinned_lean_compile_receipt",
        "zero_sorry_and_allowed_axioms_receipt",
        "concrete_t_p4_017_coefficient_list_binding",
    ]
    existing = next((n for n in state.nodes.values() if n.name == name), None)
    if existing is not None:
        changed = existing.metadata.get("source_artifacts") != source_artifacts
        if existing.metadata.get("unresolved") != unresolved:
            existing.metadata["unresolved"] = unresolved
            changed = True
        if existing.parent_id != parent.id:
            existing.parent_id = parent.id
            changed = True
        if parent.id in existing.dependencies:
            existing.dependencies = [
                dependency for dependency in existing.dependencies
                if dependency != parent.id
            ]
            changed = True
        if existing.id not in parent.dependencies:
            parent.dependencies.append(existing.id)
            changed = True
        if changed:
            existing.metadata["source_artifacts"] = source_artifacts
            state.event(
                "routeb_residual_l1_seam_provenance_refresh",
                node_id=existing.id, parent_id=parent.id,
                source_artifacts=source_artifacts,
                dag_orientation="parent_id_to_parent_dependency",
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
        "A generic Lean theorem bounds a finite weighted residual by its "
        "coefficient l1 norm and absorbs it into a positive decomposition.",
        parent_id=parent.id,
        dependencies=[],
        proof_sketch=(
            "Use Finset.abs_sum_le_sum_abs and nonnegative multiplication to "
            "prove the weighted residual l1 bound; use abs_le and linarith "
            "for the positive-decomposition absorption. Keep the concrete "
            "Gram CSV identity as a separate source-bound receipt."),
        metadata={
            "verification_domain": "lean-generic-real-finite-sum",
            "statement_status": "pending_pinned_lean_compile",
            "evidence_level": "generic_kernel_seam_uncompiled",
            "claim_status": "residual_l1_lean_seam_open",
            "registry_eligible": False,
            "comparator_accepted": False,
            "formal_certificate_allowed": False,
            "preferred_route": True,
            "unresolved": unresolved,
            "source_artifacts": source_artifacts,
        },
    )
    state.event(
        "routeb_residual_l1_seam_frontier_created",
        node_id=node_id, parent_id=parent.id,
        source_artifacts=source_artifacts,
        status="pending_pinned_lean_compile",
        formal_certificate_allowed=False, registry_promoted=False,
    )
    store.save(state)
    print({"status": "recorded", "node_id": node_id,
           "state_revision": state.revision})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
