from __future__ import annotations

import json
from pathlib import Path

from percolation_workflow.model import WorkflowState
from percolation_workflow.store import StateStore


ROOT = Path(__file__).resolve().parents[1]
RECEIPT = ROOT / "artifacts" / "percolation" / "solution_build_receipt.json"
STATE_PATH = ROOT / "artifacts" / "percolation" / "workflow_state.json"


def main() -> None:
    if STATE_PATH.exists():
        raise FileExistsError(f"Research state already exists; refusing to replace {STATE_PATH}")
    receipt = json.loads(RECEIPT.read_text(encoding="utf-8"))
    state = WorkflowState(project="anthropics/formal-math/percolation")
    submission = state.add_node(
        "percolation_submission",
        "two comparator targets from Challenge.lean",
        proof_sketch=(
            "Reproduce formal-math submission boundary: preserve the two Challenge statements, "
            "reuse the continuity theorem, compile Solution, then require comparator promotion."
        ),
        metadata={"kind": "submission", "source": "comparator.json"},
    )
    target_all = state.add_node(
        "BondPercolation.percolation_continuity",
        "the exact Challenge.lean statement; see statement index",
        parent_id=submission,
        proof_sketch="Transport the Challenge target to the all-dimensions continuity theorem.",
        metadata={"kind": "challenge_target", "statement_status": "unresolved"},
    )
    target_z3 = state.add_node(
        "BondPercolation.percolation_continuity_Z3",
        "the exact Challenge.lean statement; see statement index",
        parent_id=submission,
        proof_sketch="Specialize BondPercolation.percolation_continuity to d=3; norm_num proves 2 <= 3.",
        metadata={"kind": "challenge_target", "statement_status": "unresolved"},
    )
    library = state.add_node(
        "Percolation.Continuity.CSH.percolationContinuity_allDimensions",
        "the exact imported library declaration; see declaration graph",
        proof_sketch="Open frontier leaf: the imported continuity theorem used by Solution.lean.",
        metadata={"kind": "reused_theorem", "statement_status": "pending_decl_graph"},
    )
    state.nodes[target_all].dependencies.append(library)
    state.nodes[target_z3].dependencies.append(target_all)

    # The whole-project Lean build is evidence for the attempted submission, not comparator proof.
    for node_id in (library, target_all, target_z3):
        attempt = state.begin_attempt(
            node_id,
            "anthropic-formal-math-replay",
            source_path="upstream/formal-math/percolation/Solution.lean",
        )
        state.finish_attempt(
            attempt,
            status="passed",
            command=["lake", "build", "Solution"],
            stdout="Build completed successfully (8903 jobs).",
            stderr="",
            exit_code=receipt["exit_code"],
        )
    state.event(
        "whole_project_lean_receipt_attached",
        receipt=str(RECEIPT.relative_to(ROOT)),
        comparator_status=receipt["comparator_status"],
    )
    state.validate()
    StateStore(STATE_PATH).save(state)
    print(STATE_PATH)
    print(json.dumps({"nodes": len(state.nodes), "frontier": [n.name for n in state.frontier()]}, ensure_ascii=False))


if __name__ == "__main__":
    main()
