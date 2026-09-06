from __future__ import annotations

from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed, wait
from dataclasses import dataclass
from collections.abc import Callable
from typing import Any
import os
from .lean import run_lean
from .model import EvidenceStage, WorkflowState
from .store import StateStore


@dataclass
class FrontierResult:
    status: str
    command: list[str]
    stdout: str = ""
    stderr: str = ""
    exit_code: int = 0


FrontierJob = Callable[[str], FrontierResult]


def _numeric_metadata(node, key: str, default: float) -> float:
    """Read optional scheduling metadata without making it part of theorem semantics."""
    value = node.metadata.get(key, default)
    try:
        value = float(value)
    except (TypeError, ValueError):
        return default
    return value if value > 0 else default


_COMPILE_OBSTRUCTION_VALUES = {
    "compile_blocked", "open_compile_blocked", "blocked_compile",
    "compile_obstruction", "compile_environment_blocked",
}
_COMPARATOR_OBSTRUCTION_VALUES = {
    "comparator_open", "comparator_pending", "source_comparator",
    "source_comparator_open", "source_comparator_pending",
    "source_comparator_blocked", "source_comparator_obstruction",
    "compiled_candidate", "compiled_candidate_comparator_pending",
    "compiled_candidates_comparator_pending", "lean_compiled_candidate",
}
_OBSTRUCTION_FIELDS = (
    "obstruction", "obstruction_kind", "obstruction_status", "status",
    "execution_status", "compile_status", "source_comparator",
    "source_comparator_status", "evidence_level",
)
_CANDIDATE_ID_FIELDS = (
    "candidate_key", "candidate_id", "candidate_source",
    "candidate_digest",
    "candidate_sha256", "candidate_source_digest", "source_digest",
    "source_sha256",
)


def _normalized_token(value: Any) -> str:
    if not isinstance(value, str):
        return ""
    return value.strip().lower().replace("-", "_").replace(" ", "_")


def _metadata_values(metadata: dict[str, Any], key: str) -> list[Any]:
    """Read a scalar or structured obstruction field without guessing prose."""
    value = metadata.get(key)
    if isinstance(value, dict):
        return [*value.values(), *[value.get(name) for name in
                                   ("kind", "status", "reason", "value", "name")]]
    if isinstance(value, (list, tuple, set)):
        return list(value)
    return [value]


def obstruction_rank(node) -> int:
    """Return the explicit scheduler obstruction rank for ``node``.

    Rank ``0`` is dispatchable.  Rank ``1`` means a compiled candidate is
    waiting for source-comparator work; rank ``2`` means compilation is
    blocked by the environment.  Metadata is intentionally advisory and this
    function never changes ``NodeStatus`` or evidence stages.
    """
    metadata = node.metadata if isinstance(node.metadata, dict) else {}
    rank = metadata.get("obstruction_rank", metadata.get("scheduler_obstruction_rank", 0))
    try:
        rank = int(rank)
    except (TypeError, ValueError):
        rank = 0
    rank = max(0, min(rank, 2))

    if metadata.get("open_compile_blocked") is True:
        rank = max(rank, 2)
    if metadata.get("source_comparator_open") is True:
        rank = max(rank, 1)
    for field in _OBSTRUCTION_FIELDS:
        for value in _metadata_values(metadata, field):
            token = _normalized_token(value)
            if token in _COMPILE_OBSTRUCTION_VALUES:
                rank = max(rank, 2)
            elif token in _COMPARATOR_OBSTRUCTION_VALUES:
                rank = max(rank, 1)
            elif field in {"source_comparator", "source_comparator_status"} and token in {
                    "open", "pending", "blocked", "incomplete", "unresolved"}:
                rank = max(rank, 1)

    # These stages are the durable evidence boundary used by the workflow.
    # A compiled candidate is not another proof-agent job; it is waiting for
    # comparator/verification handling.
    stage = metadata.get("evidence_stage", EvidenceStage.OPEN)
    try:
        stage = EvidenceStage(stage)
    except ValueError:
        stage = EvidenceStage.OPEN
    if stage == EvidenceStage.COMPILED_CANDIDATE:
        rank = max(rank, 1)
    elif stage == EvidenceStage.SOURCE_COMPARATOR_PENDING:
        rank = max(rank, 1)
    return rank


def _candidate_value(metadata: dict[str, Any]) -> str | None:
    values: list[Any] = []
    for key in _CANDIDATE_ID_FIELDS:
        values.append(metadata.get(key))
    for key in ("candidate", "candidate_evidence", "compiled_candidate"):
        nested = metadata.get(key)
        if isinstance(nested, dict):
            values.extend(nested.get(name) for name in _CANDIDATE_ID_FIELDS)
            values.extend(nested.get(name) for name in
                          ("key", "id", "digest", "sha256", "source", "path", "artifact"))
    for value in values:
        if isinstance(value, str) and value.strip():
            # Candidate digests are normally hashes; normalizing paths as well
            # makes an explicitly supplied source identity stable on Windows.
            return os.path.normcase(os.path.normpath(value.strip()))
    return None


def candidate_identity(node) -> str | None:
    """Return an explicit candidate identity, or ``None`` for legacy nodes."""
    metadata = node.metadata if isinstance(node.metadata, dict) else {}
    return _candidate_value(metadata)


def _math_bottleneck_decision(node):
    """Load the optional math policy lazily to avoid a module import cycle."""
    from .math_frontier import explain_math_bottleneck
    return explain_math_bottleneck(node)


def _math_bottleneck_sort_key(node) -> tuple[int, str]:
    decision = _math_bottleneck_decision(node)
    return decision.priority, decision.label


def rank_frontier(state: WorkflowState, jobs: dict[str, FrontierJob]) -> list[str]:
    """Return eligible jobs in a deterministic, dependency-aware order.

    The obstruction gate is applied before ordering.  Canonical mathematical
    bottlenecks then provide the primary dispatch key; ``frontier_closability``
    is recomputed from the DAG, and optional engineering cost metadata only
    breaks later ties.  None of these advisory fields can make an ineligible
    theorem runnable or close a theorem edge.
    """
    frontier = {node.id: node for node in state.frontier()}
    selected = [node for node_id, node in frontier.items()
                if node_id in jobs and obstruction_rank(node) == 0]
    selected.sort(key=lambda node: (
        *_math_bottleneck_sort_key(node),
        -state.frontier_closability(node.id),
        -_numeric_metadata(node, "scheduler_priority", 1.0),
        _numeric_metadata(node, "resource_cost", 1.0),
        _numeric_metadata(node, "estimated_seconds", 1.0),
        node.id,
    ))
    # Keep the best-ranked representative of an explicitly identified
    # candidate.  Nodes without identity metadata remain fully backward
    # compatible and are never deduplicated by statement/name heuristics.
    seen_candidates: set[str] = set()
    unique: list[str] = []
    for node in selected:
        identity = candidate_identity(node)
        if identity is not None and identity in seen_candidates:
            continue
        if identity is not None:
            seen_candidates.add(identity)
        unique.append(node.id)
    return unique


def explain_frontier(state: WorkflowState, jobs: dict[str, FrontierJob] | None = None) -> list[dict[str, Any]]:
    """Return a durable, read-only explanation of the current open frontier.

    The scheduler previously exposed only selected ids.  That was enough for
    dispatch, but it lost the Prove2Me-style obstruction trail: a node can be
    an open leaf while waiting for a comparator, a compiler environment, or a
    repair round.  This view is intentionally derived from the current DAG and
    never changes node status or creates an attempt, so callers can persist it
    alongside an agent request without turning advisory metadata into proof
    evidence.
    """
    state.validate()
    job_ids = set(jobs) if jobs is not None else None
    rows: list[dict[str, Any]] = []
    for node in state.frontier():
        rank = obstruction_rank(node)
        bottleneck = _math_bottleneck_decision(node)
        eligible = rank == 0 and (job_ids is None or node.id in job_ids)
        if rank == 2:
            reason = "compile_obstruction"
        elif rank == 1:
            reason = "comparator_or_candidate_obstruction"
        elif job_ids is not None and node.id not in job_ids:
            reason = "no_registered_job"
        else:
            reason = "dispatchable"
        rows.append({
            "node_id": node.id,
            "name": node.name,
            "status": node.status.value,
            "closability": state.frontier_closability(node.id),
            "obstruction_rank": rank,
            "obstruction_reason": reason,
            "math_bottleneck": bottleneck.label,
            "math_bottleneck_priority": bottleneck.priority,
            "math_bottleneck_source": bottleneck.source,
            "math_bottleneck_reason": bottleneck.reason,
            "candidate_identity": candidate_identity(node),
            "dependencies": list(node.dependencies),
            "resource_cost": _numeric_metadata(node, "resource_cost", 1.0),
            "scheduler_priority": _numeric_metadata(node, "scheduler_priority", 1.0),
            "eligible": eligible,
        })
    return rows


def select_frontier_jobs(state: WorkflowState, jobs: dict[str, FrontierJob], *,
                         max_workers: int, max_cost: float | None = None) -> dict[str, FrontierJob]:
    """Pack a frontier batch by closability and an optional resource budget.

    A too-expensive node is deferred, not marked blocked.  If every node is
    above the budget, the cheapest one is admitted so a miscalibrated budget
    cannot deadlock the frontier permanently.
    """
    if max_workers < 1:
        raise ValueError("max_workers must be positive")
    ordered = rank_frontier(state, jobs)
    chosen: list[str] = []
    spent = 0.0
    for node_id in ordered:
        node = state.nodes[node_id]
        cost = _numeric_metadata(node, "resource_cost", 1.0)
        if len(chosen) >= max_workers:
            break
        if max_cost is not None and spent + cost > max_cost and chosen:
            continue
        if max_cost is not None and spent + cost > max_cost:
            continue
        chosen.append(node_id)
        spent += cost
    if not chosen and ordered:
        cheapest = min(ordered, key=lambda node_id: (
            _numeric_metadata(state.nodes[node_id], "resource_cost", 1.0), node_id))
        chosen = [cheapest]
    return {node_id: jobs[node_id] for node_id in chosen}


def run_frontier_parallel(state: WorkflowState, jobs: dict[str, FrontierJob], *, max_workers: int = 4,
                          max_cost: float | None = None, timeout_s: float | None = None,
                          store: StateStore | None = None) -> dict[str, str]:
    """Run independent frontier jobs concurrently while serializing state transitions.

    Each job should use its own worktree/project directory. Jobs return data rather than mutating `state`,
    so concurrent agents cannot corrupt the JSON-backed research state; results are committed in the caller.
    """
    state.validate()
    selected = select_frontier_jobs(state, jobs, max_workers=max_workers, max_cost=max_cost)
    attempt_ids = {node_id: state.begin_attempt(node_id, f"parallel-agent:{node_id}") for node_id in selected}
    if store:
        store.save(state)
    outcomes: dict[str, str] = {}
    pool = ThreadPoolExecutor(max_workers=min(max_workers, len(selected) or 1))
    futures = {pool.submit(job, node_id): node_id for node_id, job in selected.items()}
    try:
        done, pending = wait(futures, timeout=timeout_s)
        for future in as_completed(done):
            node_id = futures[future]
            try:
                result = future.result()
            except Exception as exc:  # keep an agent crash as repairable history
                result = FrontierResult("agent_error", [], stderr=repr(exc), exit_code=1)
            state.finish_attempt(attempt_ids[node_id], status=result.status, command=result.command,
                                 stdout=result.stdout, stderr=result.stderr, exit_code=result.exit_code)
            if result.status == "passed":
                state.set_evidence_stage(node_id, EvidenceStage.COMPILED_CANDIDATE)
            outcomes[node_id] = result.status
            if store:
                store.save(state)
        for future in pending:
            node_id = futures[future]
            future.cancel()
            result = FrontierResult("timeout", [], stderr="frontier job timed out", exit_code=124)
            state.finish_attempt(attempt_ids[node_id], status=result.status, command=result.command,
                                 stdout=result.stdout, stderr=result.stderr, exit_code=result.exit_code)
            state.event("frontier_job_timed_out", node_id=node_id, timeout_s=timeout_s)
            outcomes[node_id] = result.status
            if store:
                store.save(state)
    finally:
        # Do not let a slow worker hold the coordinator hostage.  Jobs must be
        # isolated and must not mutate WorkflowState after submission.
        pool.shutdown(wait=False, cancel_futures=True)
    state.event("frontier_batch_finished", jobs=len(selected), outcomes=outcomes)
    if store:
        store.save(state)
    return outcomes


def verify_attempt(state: WorkflowState, node_id: str, agent_id: str, project_dir: str | Path,
                   source_path: str | None = None, command: list[str] | None = None) -> str:
    """Run one agent artifact and persist compiler feedback in the state object."""
    attempt_id = state.begin_attempt(node_id, agent_id, source_path)
    result = run_lean(project_dir, command)
    state.finish_attempt(attempt_id, status="passed" if result.ok else "compile_error",
                         command=result.command, stdout=result.stdout, stderr=result.stderr,
                         exit_code=result.exit_code)
    return attempt_id
