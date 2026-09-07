"""Materialize the O1 source-comparator frontier as theorem-DAG leaves."""
from __future__ import annotations

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from percolation_workflow.store import StateStore  # noqa: E402


STATE = ROOT / "artifacts/routeb_6dof/state.json"
PARENT_NAME = "P4.true_dh_exact_real_coefficient_identity"
PREFIX = "P4.O1.source_comparator"


def find(state, name: str):
    for node in state.nodes.values():
        if node.name == name:
            return node
    return None


def add_if_missing(state, *, name: str, statement: str, parent_id: str,
                   sketch: str, frontier_kind: str) -> str:
    existing = find(state, name)
    if existing is not None:
        if existing.parent_id != parent_id or existing.statement != statement:
            raise ValueError(f"existing O1 leaf contract drifted: {name}")
        return existing.id
    return state.add_node(
        name,
        statement,
        parent_id=parent_id,
        proof_sketch=sketch,
        metadata={
            "verification_domain": "lean",
            "research_stage": "P4",
            "statement_status": "open_source_comparator_frontier",
            "frontier_kind": frontier_kind,
            "source_key": "routeb-exact-fourier-mass:a986a208b62f585c6ca1b9c81b958710d2043e5bf786ddc930a6fa29f7a232b8|mu=1/1000000|contract=exp(i*nu*q)",
            "state_key": "routeb-qcell:center=(0,0,0,0,0,0)|radius=1/1000|B=(4,5)|D=(1,2,3,6)|orientation=M_BD[B,D],DeltaM_DB[D,B]|norm=induced_infinity",
            "registry_eligible": False,
            "comparator_accepted": False,
            "source_binding_proven": False,
            "formal_certificate_allowed": False,
        },
    )


def main() -> None:
    store = StateStore(STATE)
    state = store.load()
    parent = find(state, PARENT_NAME)
    if parent is None:
        raise ValueError(f"missing parent: {PARENT_NAME}")
    leaves: list[str] = []
    leaves.append(add_if_missing(
        state,
        name=f"{PREFIX}.h_aggregate_function_lift",
        statement=(
            "For the exact 610-row payload, lift finite-key aggregate equality "
            "to the real q-domain: csvAggregate massPayload q i j = "
            "∑ body : Fin 6, fourierBody body q i j."
        ),
        parent_id=parent.id,
        sketch=(
            "Prove the finite-key equality and the real cos/sin evaluator lift "
            "under the exact q-cell; retain the payload and source hashes."
        ),
        frontier_kind="h_aggregate_function_lift",
    ))
    for body in range(1, 7):
        leaves.append(add_if_missing(
            state,
            name=f"{PREFIX}.h_body_{body}",
            statement=(
                f"For body {body}, prove sourceBody {body} q i j = "
                "fourierBody body q i j for the exact DH source under the "
                "same source/state/mu/q contract."
            ),
            parent_id=parent.id,
            sketch=(
                f"Expand the exact DH bodyMass/sourceBody definition for body {body}, "
                "transport the coefficient identity to the real evaluator, and "
                "retain a pinned source-comparator receipt."
            ),
            frontier_kind="h_body_exact_dh",
        ))
    if not parent.metadata.get("o1_source_comparator_leaf_ids"):
        parent.metadata["o1_source_comparator_leaf_ids"] = leaves
        parent.metadata["o1_source_comparator_decomposition"] = {
            "status": "OPEN_FRONTIER_MATERIALIZED",
            "required_leaf_count": 7,
            "h_aggregate_function_lift": leaves[0],
            "h_body_leaves": leaves[1:],
            "parent_closure_requires_all": True,
            "registry_promoted": False,
            "formal_certificate_allowed": False,
        }
        state.event(
            "routeb_o1_source_comparator_decomposed",
            parent_id=parent.id,
            leaf_ids=leaves,
            leaf_count=len(leaves),
            parent_closure_requires_all=True,
            registry_promoted=False,
            formal_certificate_allowed=False,
        )
        state.validate()
        store.save(state)
        status = "decomposed"
    else:
        status = "already_decomposed"
    print({"status": status, "leaf_count": len(leaves), "revision": store.load().revision})


if __name__ == "__main__":
    main()
