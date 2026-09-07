from __future__ import annotations

from collections.abc import Callable
from pathlib import Path
from .lean import run_lean
from .disjoint import audit_do, build_repair_do
from .model import EvidenceStage, NodeStatus, WorkflowState
from .store import StateStore


Repair = Callable[[str, str, str, int], str | Path | None]


def _portable_repair_path(project_dir: str | Path, source_path: str | Path) -> str:
    """Return a stable project-relative receipt path when possible.

    Repair callbacks may operate on absolute temporary paths.  The disjoint DO
    receipt surface intentionally accepts only portable relative POSIX paths, so
    normalize a source inside ``project_dir`` before building the receipt.
    """
    project = Path(project_dir).resolve()
    source = Path(source_path).resolve()
    try:
        return source.relative_to(project).as_posix()
    except ValueError:
        # Keep fail-closed behavior for sources outside the assigned project.
        return str(source_path)


def repair_until_verified(state: WorkflowState, node_id: str, agent_id: str, project_dir: str | Path,
                          source_path: str, repair: Repair, *, max_rounds: int = 3,
                          command: list[str] | None = None, store: StateStore | None = None) -> bool:
    """Compile, feed the exact diagnostic to a repair agent, and retain every round.

    `repair` is deliberately an injected adapter: Codex/multi-agent orchestration can supply it without
    coupling this mathematical layer to a model provider. No round is promoted unless Lean exits zero.
    """
    if isinstance(max_rounds, bool) or not isinstance(max_rounds, int) or max_rounds < 1:
        raise ValueError("max_rounds must be a positive integer")
    for round_no in range(1, max_rounds + 1):
        attempt_id = state.begin_attempt(node_id, agent_id, source_path)
        if store:
            store.save(state)
        result = run_lean(project_dir, command)
        state.finish_attempt(attempt_id, status="passed" if result.ok else "compile_error",
                             command=result.command, stdout=result.stdout, stderr=result.stderr,
                             exit_code=result.exit_code)
        if store:
            store.save(state)
        if result.ok:
            state.set_evidence_stage(node_id, EvidenceStage.COMPILED_CANDIDATE)
            state.event("repair_loop_passed", node_id=node_id, round=round_no)
            if store:
                store.save(state)
            return True
        try:
            next_path = repair(source_path, result.stdout, result.stderr, round_no)
        except Exception as exc:
            state.event("repair_agent_error", node_id=node_id, round=round_no, error=repr(exc))
            if store:
                store.save(state)
            return False
        receipt_path = _portable_repair_path(project_dir, source_path)
        state.event("repair_requested", node_id=node_id, round=round_no,
                    diagnostic=result.stderr or result.stdout, next_path=str(next_path) if next_path else None,
                    # DO paths are portable receipt paths; the live source path
                    # remains in ``next_path`` and is intentionally untouched.
                    disjoint_do=audit_do(build_repair_do(receipt_path)))
        if store:
            store.save(state)
        if next_path is None:
            break
        source_path = str(next_path)
    state.nodes[node_id].status = NodeStatus.OPEN
    state.event("repair_loop_exhausted", node_id=node_id, max_rounds=max_rounds)
    if store:
        store.save(state)
    return False
