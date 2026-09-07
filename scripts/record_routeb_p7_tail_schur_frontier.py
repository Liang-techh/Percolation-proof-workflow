"""Attach the source-independent P7 Schur-completion child to the DAG."""
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
    parent = find(state, "P7.strict_tail_fallback")
    name = "P7.tail_schur_completion_2x2"
    source_artifacts = [ref(path) for path in (
        ROOT / "examples/routeb_p7_tail_schur_completion_lean/TailSchurCompletion.lean",
        ROOT / "examples/routeb_p7_tail_schur_completion_lean/README.md",
        ROOT / "examples/routeb_p7_tail_schur_completion_lean/lean-toolchain",
        ROOT / "examples/routeb_p7_tail_schur_completion_lean/verify.sh",
    )]
    unresolved = [
        "pinned_lean_compile_receipt",
        "zero_sorry_and_allowed_axioms_receipt",
        "P7_seven_term_polynomial_source_binding",
        "P7_inverse_block_and_normalization_binding",
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
            state.event(
                "routeb_p7_tail_schur_provenance_refresh",
                node_id=existing.id, parent_id=parent.id,
                source_artifacts=source_artifacts,
                status="pending_pinned_lean_compile",
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
        "A typed 2x2 Schur completion and robust inverse-quadratic bound "
        "consume the P7 tail eta inequality.",
        parent_id=parent.id,
        dependencies=[],
        proof_sketch=(
            "Prove the exact completion identity by field_simp/ring; bound "
            "the inverse quadratic form using absolute-value envelopes; "
            "then absorb tau-eta times s^2. Keep seven-term source binding "
            "and normalization as separate premises."),
        metadata={
            "verification_domain": "lean-source-independent-real-analysis",
            "statement_status": "pending_pinned_lean_compile",
            "evidence_level": "generic_schur_completion_child",
            "claim_status": "p7_tail_schur_open",
            "registry_eligible": False,
            "comparator_accepted": False,
            "formal_certificate_allowed": False,
            "preferred_route": True,
            "unresolved": unresolved,
            "source_artifacts": source_artifacts,
        },
    )
    state.event(
        "routeb_p7_tail_schur_frontier_created",
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
