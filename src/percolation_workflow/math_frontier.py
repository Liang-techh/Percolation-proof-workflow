"""Opt-in mathematical bottleneck lanes for frontier scheduling.

This module deliberately does not alter the ordinary scheduler contract.  It
adds a read-only view for theorem-DAG audits where an open leaf can represent
three very different kinds of work:

* a Lean adapter that can be compiled immediately;
* a conditional bridge whose missing premise is source semantics; or
* a numerical/coverage obstruction that should not consume a Lean slot.

Callers may provide ``metadata["math_lane"]`` (or the same top-level field on
an imported DAG row) to make the classification authoritative.  The small
row adapter below exists for proposed proof-DAG snapshots such as block45
v125, which predate the WorkflowState metadata contract.
"""

from __future__ import annotations

from collections.abc import Mapping
from enum import StrEnum
import hashlib
import json
from typing import Any

from .model import WorkflowState
from .scheduler import obstruction_rank


class MathLane(StrEnum):
    LEAN_ADAPTER = "lean_adapter"
    SOURCE_SEMANTICS = "source_semantics"
    NUMERICAL_BLOCKER = "numerical_blocker"
    OTHER = "other"


_ALIASES = {
    "lean": MathLane.LEAN_ADAPTER,
    "adapter": MathLane.LEAN_ADAPTER,
    "lean_adapter": MathLane.LEAN_ADAPTER,
    "source": MathLane.SOURCE_SEMANTICS,
    "source_bridge": MathLane.SOURCE_SEMANTICS,
    "source_semantics": MathLane.SOURCE_SEMANTICS,
    "conditional_bridge": MathLane.SOURCE_SEMANTICS,
    "numeric": MathLane.NUMERICAL_BLOCKER,
    "numerical": MathLane.NUMERICAL_BLOCKER,
    "numerical_blocker": MathLane.NUMERICAL_BLOCKER,
    "coverage": MathLane.NUMERICAL_BLOCKER,
    "other": MathLane.OTHER,
}

_NUMERIC_TOKENS = (
    "coverage", "flowpipe", "interval", "residual", "error_budget",
    "finite_difference", "finite_diff", "pmi", "numerical", "scaling",
    "domain_feasibility", "joint_domain", "continuation",
)


def _token(value: Any) -> str:
    return str(value).strip().lower().replace("-", "_").replace(" ", "_")


def _explicit_lane(item: Any) -> MathLane | None:
    metadata = item.get("metadata", {}) if isinstance(item, Mapping) else getattr(item, "metadata", {})
    value = metadata.get("math_lane") if isinstance(metadata, Mapping) else None
    if value is None and isinstance(item, Mapping):
        value = item.get("math_lane")
    return _ALIASES.get(_token(value))


def math_lane(item: Any) -> MathLane:
    """Classify a node/JSON row without changing theorem or evidence state."""
    explicit = _explicit_lane(item)
    if explicit is not None:
        return explicit

    if isinstance(item, Mapping):
        name = _token(item.get("id", item.get("name", "")))
        status = _token(item.get("status", ""))
        deps = [_token(dep) for dep in item.get("dependencies", [])]
        statement = _token(item.get("statement", ""))
        source = _token(item.get("source", ""))
        verification_domain = _token(item.get("verification_domain", ""))
        if isinstance(item.get("metadata"), Mapping):
            verification_domain = verification_domain or _token(
                item["metadata"].get("verification_domain", ""))
    else:
        name = _token(getattr(item, "name", ""))
        status = _token(getattr(item, "status", ""))
        deps = [_token(dep) for dep in getattr(item, "dependencies", [])]
        statement = _token(getattr(item, "statement", ""))
        source = _token(getattr(item, "verified_artifact", ""))
        verification_domain = _token(getattr(item, "verification_domain", ""))
        metadata = getattr(item, "metadata", {})
        if isinstance(metadata, Mapping):
            verification_domain = verification_domain or _token(
                metadata.get("verification_domain", ""))

    # Imported DAG rows often carry the domain at top level, while live
    # ProofNode instances keep it in metadata.  Treating an explicit Lean
    # domain as an adapter lane prevents formal leaves from falling into
    # ``other`` merely because they lack the newer ``math_lane`` field.
    if verification_domain in {"lean", "lean4", "kernel", "formal"}:
        return MathLane.LEAN_ADAPTER
    if verification_domain in {"external_research", "source_semantics"}:
        return MathLane.SOURCE_SEMANTICS

    # Proposed block45 rows use this status for already-produced Lean-shaped
    # candidates.  They are adapter-lane evidence, not a claim of theorem
    # closure; the ordinary scheduler still decides whether they are runnable.
    if status.startswith("compiled_candidate") or source.endswith(".lean"):
        return MathLane.LEAN_ADAPTER
    if "source_semantics" in name or "source_semantics" in deps or "source_audit" in status:
        return MathLane.SOURCE_SEMANTICS
    haystack = " ".join((name, statement, status, " ".join(deps)))
    if any(token in haystack for token in _NUMERIC_TOKENS):
        return MathLane.NUMERICAL_BLOCKER
    return MathLane.OTHER


_LANE_ORDER = {
    MathLane.LEAN_ADAPTER: 0,
    MathLane.SOURCE_SEMANTICS: 1,
    MathLane.NUMERICAL_BLOCKER: 2,
    MathLane.OTHER: 3,
}

# This order is intentionally an audit/obstruction order, not a dispatch
# permission.  It mirrors the current Route-B mathematical critical path:
# coverage and physical matrix binding dominate local sign/FD diagnostics.
_BOTTLENECK_ORDER = {
    "coverage": 0,
    "physical_schur_binding": 1,
    "schur_binding": 1,
    "interval_sign": 2,
    "central_fd": 3,
    "source_semantics": 1,
    "other": 4,
}


def math_bottleneck(item: Any) -> str:
    """Return a stable audit label for a mathematical obstruction.

    Explicit ``metadata["math_bottleneck"]`` wins.  The fallback is only a
    naming aid for imported DAG rows and never changes proof eligibility.
    """
    metadata = item.get("metadata", {}) if isinstance(item, Mapping) else getattr(item, "metadata", {})
    value = metadata.get("math_bottleneck") if isinstance(metadata, Mapping) else None
    if value is None and isinstance(item, Mapping):
        value = item.get("math_bottleneck")
    token = _token(value)
    if token in _BOTTLENECK_ORDER:
        return token
    if isinstance(item, Mapping):
        fields = [item.get("id", ""), item.get("name", ""), item.get("statement", ""), item.get("status", "")]
    else:
        fields = [getattr(item, "id", ""), getattr(item, "name", ""), getattr(item, "statement", ""), getattr(item, "status", "")]
    haystack = " ".join(_token(field) for field in fields)
    if "coverage" in haystack or "flowpipe" in haystack or "partition" in haystack:
        return "coverage"
    if "schur" in haystack or "krawczyk" in haystack or "operator_binding" in haystack:
        return "physical_schur_binding"
    if "interval_sign" in haystack or "h_src" in haystack or "sign_normal" in haystack:
        return "interval_sign"
    if "central_fd" in haystack or "finite_difference" in haystack:
        return "central_fd"
    if "source_semantics" in haystack or "true_dh" in haystack:
        return "source_semantics"
    return "other"


def rank_math_obstruction_frontier(state: WorkflowState,
                                   jobs: Mapping[str, Any] | None = None) -> list[str]:
    """Order every frontier leaf by mathematical bottleneck, read-only.

    Unlike ``rank_math_frontier``, this includes obstructed leaves so a
    coordinator can expose the next proof bottleneck to a numerical/source
    agent.  It never creates a dispatch request and never relaxes the
    scheduler obstruction gate.
    """
    job_ids = set(jobs) if jobs is not None else None
    candidates = [node for node in state.frontier()
                  if job_ids is None or node.id in job_ids]
    candidates.sort(key=lambda node: (
        _BOTTLENECK_ORDER[math_bottleneck(node)],
        obstruction_rank(node),
        _LANE_ORDER[math_lane(node)],
        -state.frontier_closability(node.id),
        node.id,
    ))
    return [node.id for node in candidates]


def rank_math_frontier(state: WorkflowState, jobs: Mapping[str, Any] | None = None) -> list[str]:
    """Return runnable frontier ids in math-lane order.

    Existing DAG eligibility and obstruction policy remain authoritative.  This
    function only changes tie-breaking for callers that explicitly opt in.
    """
    job_ids = set(jobs) if jobs is not None else None
    candidates = [node for node in state.frontier()
                  if obstruction_rank(node) == 0
                  and (job_ids is None or node.id in job_ids)]
    candidates.sort(key=lambda node: (
        _LANE_ORDER[math_lane(node)],
        -state.frontier_closability(node.id),
        node.id,
    ))
    return [node.id for node in candidates]


def rank_formalizable_frontier(state: WorkflowState,
                               jobs: Mapping[str, Any] | None = None) -> list[str]:
    """Return an opt-in dispatch order that excludes known numerical dead ends.

    ``rank_math_frontier`` remains an audit ordering and keeps numerical
    blockers visible.  This adapter is for callers with a formal/bridge lane:
    it preserves the obstruction gate and deterministic ordering while
    returning no numerical blocker when that is the only available work.
    Ordinary scheduler callers are unchanged.
    """
    ranked = rank_math_frontier(state, jobs)
    return [node_id for node_id in ranked
            if math_lane(state.nodes[node_id]) != MathLane.NUMERICAL_BLOCKER]


def explain_math_frontier(state: WorkflowState, jobs: Mapping[str, Any] | None = None) -> list[dict[str, Any]]:
    """Produce a read-only lane explanation for every current frontier leaf."""
    state.validate()
    job_ids = set(jobs) if jobs is not None else None
    rows = []
    for node in state.frontier():
        lane = math_lane(node)
        rows.append({
            "node_id": node.id,
            "name": node.name,
            "math_lane": lane.value,
            "lane_priority": _LANE_ORDER[lane],
            "math_bottleneck": math_bottleneck(node),
            "bottleneck_priority": _BOTTLENECK_ORDER[math_bottleneck(node)],
            "obstruction_rank": obstruction_rank(node),
            "eligible": obstruction_rank(node) == 0 and (job_ids is None or node.id in job_ids),
        })
    return rows


def _evidence_hash(node: Any) -> str:
    """Hash the node's advisory frontier evidence, never formal admission state."""
    metadata = node.metadata if isinstance(getattr(node, "metadata", None), Mapping) else {}
    payload = {"node_id": node.id, "metadata": dict(metadata)}
    encoded = json.dumps(payload, sort_keys=True, ensure_ascii=False, default=str).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def project_frontier_receipt(state: WorkflowState, jobs: Mapping[str, Any] | None = None) -> dict[str, Any]:
    """Return a read-only frontier projection suitable for an audit receipt.

    This is advisory metadata only: it derives rows from the current DAG and
    does not create attempts, alter evidence stages, or participate in formal
    admission.  ``evidence_hash`` fingerprints the advisory node metadata so
    a later consumer can detect projection drift.
    """
    state.validate()
    job_ids = set(jobs) if jobs is not None else None
    rows = []
    for node in state.frontier():
        lane = math_lane(node)
        rank = obstruction_rank(node)
        if rank == 2:
            blocker = "compile_obstruction"
        elif rank == 1:
            blocker = "comparator_or_candidate_obstruction"
        elif job_ids is not None and node.id not in job_ids:
            blocker = "no_registered_job"
        else:
            blocker = None
        rows.append({
            "node_id": node.id,
            "lane": lane.value,
            "blocker": blocker,
            "evidence_hash": _evidence_hash(node),
            "priority": _LANE_ORDER[lane],
        })
    return {"schema_version": 1, "formal_admission": "unchanged", "frontier": rows}


def build_frontier_cut(state: WorkflowState, jobs: Mapping[str, Any] | None = None) -> dict[str, Any]:
    """Build a deterministic, read-only Prove2Me-style frontier cut.

    The cut groups every current frontier leaf by its mathematical lane while
    preserving the obstruction gate.  It is an audit/scheduling projection:
    it never closes a node, creates an attempt, or turns a compiled candidate
    into a verified theorem.  ``cut_sha256`` lets a later agent request prove
    exactly the same frontier even if completion order changes.
    """
    state.validate()
    job_ids = set(jobs) if jobs is not None else None
    rows = explain_math_frontier(state, jobs)
    rows.sort(key=lambda row: (
        not row["eligible"], row["lane_priority"], -row["obstruction_rank"],
        row["bottleneck_priority"], row["node_id"],
    ))
    lanes: dict[str, list[str]] = {lane.value: [] for lane in MathLane}
    for row in rows:
        lanes[row["math_lane"]].append(row["node_id"])
    payload = {
        "schema_version": 1,
        "formal_admission": "unchanged",
        "job_filter": sorted(job_ids) if job_ids is not None else None,
        "frontier": rows,
        "lanes": lanes,
    }
    encoded = json.dumps(payload, ensure_ascii=False, sort_keys=True,
                         separators=(",", ":"), default=str).encode("utf-8")
    payload["cut_sha256"] = hashlib.sha256(encoded).hexdigest()
    return payload
