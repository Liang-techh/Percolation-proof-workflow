"""Record the remote-budget-to-PMI Lean seam as a pending DAG child."""
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


def node_by_name(state, name: str):
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

    name = "P4.remote_budget_pmi_composition"
    existing = next((n for n in state.nodes.values() if n.name == name), None)
    if existing is not None:
        print({"status": "already_recorded", "node_id": existing.id,
               "state_revision": state.revision})
        return 0

    p4 = node_by_name(state, "P4.residual_schur_pmi")
    budget = node_by_name(state, "P4.remote_acceleration_budget")
    source = ROOT / "examples/routeb_remote_pmi_composition/RemotePMIComposition.lean"
    readme = source.parent / "README.md"
    node_id = state.add_node(
        name,
        "A remote residual bound residual^2 <= kappa^2*mass and a scale bridge "
        "mass <= beta^2*y^2 imply the scalar P4 Schur envelope with coefficient "
        "(kappa*beta)^2.",
        dependencies=[budget.id],
        proof_sketch=(
            "Multiply the mass bridge by kappa^2, normalize the exact square, "
            "then apply the existing scalar Schur completion."
        ),
        metadata={
            "verification_domain": "lean-source-independent",
            "statement_status": "pending_pinned_compile",
            "evidence_level": "isolated_lean_candidate",
            "claim_status": "physical_binding_open",
            "registry_eligible": False,
            "comparator_accepted": False,
            "formal_certificate_allowed": False,
            "upstream_node": budget.id,
            "p4_parent": p4.id,
            "source_artifacts": [ref(source), ref(readme)],
            "unresolved": [
                "pinned_lean_compile_and_axioms",
                "MBD_operator_source_bound",
                "mass_to_PMI_scale_source_bridge",
            ],
        },
    )
    p4.dependencies.append(node_id)
    state.event(
        "routeb_remote_pmi_composition_checkpoint",
        node_id=node_id,
        parent_id=p4.id,
        upstream_node=budget.id,
        source_artifacts=[ref(source), ref(readme)],
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
