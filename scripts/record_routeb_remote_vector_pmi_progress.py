"""Record the vector remote PMI seam as a pending Route-B DAG child."""
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
    state_path = ROOT / "artifacts/routeb_6dof/state.json"
    store = StateStore(state_path)
    state = store.load()
    if state.project != "routeb-6dof-external":
        raise ValueError(f"unexpected project: {state.project!r}")
    name = "P4.vector_remote_budget_pmi_composition"
    source = ROOT / "examples/routeb_remote_vector_pmi/RemoteVectorPMI.lean"
    readme = source.parent / "README.md"
    source_artifacts = [ref(source), ref(readme)]
    existing = next((n for n in state.nodes.values() if n.name == name), None)
    if existing is not None:
        if existing.metadata.get("source_artifacts") != source_artifacts:
            existing.metadata["source_artifacts"] = source_artifacts
            state.event(
                "routeb_vector_remote_pmi_provenance_refresh",
                node_id=existing.id,
                source_artifacts=source_artifacts,
                status=existing.metadata.get("statement_status"),
                formal_certificate_allowed=False,
                registry_promoted=False,
            )
            store.save(state)
            print({"status": "provenance_refreshed", "node_id": existing.id,
                   "state_revision": state.revision})
            return 0
        print({"status": "already_recorded", "node_id": existing.id,
               "state_revision": state.revision})
        return 0

    p4 = find(state, "P4.residual_schur_pmi")
    scalar = find(state, "P4.remote_budget_pmi_composition")
    node_id = state.add_node(
        name,
        "A single squared-norm bound for the two-dimensional remote action, "
        "combined with a mass-to-scale bridge and K*beta^2 <= p*d, closes the "
        "vector P4 PMI quadratic without per-component recharging.",
        dependencies=[scalar.id],
        proof_sketch=(
            "Use the sum of two completed squares and one exact residual budget; "
            "keep K nonnegative as an explicit adapter premise."
        ),
        metadata={
            "verification_domain": "lean-source-independent",
            "statement_status": "pending_pinned_compile",
            "evidence_level": "isolated_lean_candidate",
            "claim_status": "vector_physical_binding_open",
            "registry_eligible": False,
            "comparator_accepted": False,
            "formal_certificate_allowed": False,
            "upstream_node": scalar.id,
            "p4_parent": p4.id,
            "source_artifacts": source_artifacts,
            "unresolved": [
                "pinned_lean_compile_and_axioms",
                "K_is_a_covered_domain_MBD_squared_operator_bound",
                "mass_to_PMI_scale_source_bridge",
            ],
        },
    )
    p4.dependencies.append(node_id)
    state.event(
        "routeb_vector_remote_pmi_checkpoint",
        node_id=node_id,
        parent_id=p4.id,
        upstream_node=scalar.id,
        source_artifacts=source_artifacts,
        status="pending_pinned_compile",
        formal_certificate_allowed=False,
        registry_promoted=False,
    )
    store.save(state)
    print({"status": "recorded", "node_id": node_id,
           "state_revision": state.revision})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
