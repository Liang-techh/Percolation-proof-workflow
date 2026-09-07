"""Attach the source-independent P5 componentwise decay child to the DAG."""
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
    parent = find(state, "P5.sparse_disjunctive_sos")
    name = "P5.componentwise_relative_decay"
    source_artifacts = [ref(path) for path in (
        ROOT / "examples/routeb_p5_componentwise_relative_decay_lean/ComponentwiseRelativeDecay.lean",
        ROOT / "examples/routeb_p5_componentwise_relative_decay_lean/README.md",
        ROOT / "examples/routeb_p5_componentwise_relative_decay_lean/lean-toolchain",
        ROOT / "examples/routeb_p5_componentwise_relative_decay_lean/verify.sh",
    )]
    unresolved = [
        "pinned_lean_compile_receipt",
        "zero_sorry_and_allowed_axioms_receipt",
        "same_domain_force_error_relative_bound",
        "true_DH_FD_solve_source_binding",
    ]
    existing = next((n for n in state.nodes.values() if n.name == name), None)
    if existing is not None:
        changed = False
        if existing.parent_id != parent.id:
            existing.parent_id = parent.id
            changed = True
        if existing.id not in parent.dependencies:
            parent.dependencies.append(existing.id)
            changed = True
        if existing.metadata.get("source_artifacts") != source_artifacts:
            existing.metadata["source_artifacts"] = source_artifacts
            changed = True
        if existing.metadata.get("unresolved") != unresolved:
            existing.metadata["unresolved"] = unresolved
            changed = True
        if changed:
            state.event("routeb_p5_componentwise_decay_provenance_refresh",
                        node_id=existing.id, parent_id=parent.id,
                        source_artifacts=source_artifacts,
                        status="pending_pinned_lean_compile",
                        formal_certificate_allowed=False, registry_promoted=False)
            store.save(state)
            print({"status": "provenance_refreshed", "node_id": existing.id,
                   "state_revision": state.revision})
        else:
            print({"status": "already_recorded", "node_id": existing.id,
                   "state_revision": state.revision})
        return 0

    node_id = state.add_node(
        name,
        "Coordinatewise relative force residual bounds strictly below "
        "coordinate damping imply retained dissipation.",
        parent_id=parent.id,
        dependencies=[],
        proof_sketch=(
            "Bound each r_i*v_i by rho_i*v_i^2 using absolute values, sum "
            "the inequalities, and optionally lower-bound d_i-rho_i by a "
            "uniform lambda. Keep relative-bound source semantics separate."),
        metadata={
            "verification_domain": "lean-source-independent-real-analysis",
            "statement_status": "pending_pinned_lean_compile",
            "evidence_level": "generic_componentwise_decay_child",
            "claim_status": "componentwise_relative_decay_open",
            "registry_eligible": False,
            "comparator_accepted": False,
            "formal_certificate_allowed": False,
            "preferred_route": True,
            "unresolved": unresolved,
            "source_artifacts": source_artifacts,
        },
    )
    state.event("routeb_p5_componentwise_decay_frontier_created",
                node_id=node_id, parent_id=parent.id,
                source_artifacts=source_artifacts,
                status="pending_pinned_lean_compile",
                formal_certificate_allowed=False, registry_promoted=False)
    store.save(state)
    print({"status": "recorded", "node_id": node_id,
           "state_revision": state.revision})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
