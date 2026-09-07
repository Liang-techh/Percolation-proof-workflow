"""Opt-in mathematical bottleneck lanes for frontier scheduling.

This module deliberately does not alter the ordinary scheduler contract.  It
adds a read-only view for theorem-DAG audits where an open leaf can represent
three very different kinds of work:

* a Lean adapter that can be compiled immediately;
* a conditional bridge whose missing premise is source semantics; or
* a numerical/coverage obstruction or exact structural countermodel that
  should not consume a Lean slot.

Callers may provide ``metadata["math_lane"]`` (or the same top-level field on
an imported DAG row) to make the classification authoritative.  The small
row adapter below exists for proposed proof-DAG snapshots such as block45
v125, which predate the WorkflowState metadata contract.
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
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
    STRUCTURAL_OBSTRUCTION = "structural_obstruction"
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
    "obstruction": MathLane.STRUCTURAL_OBSTRUCTION,
    "countermodel": MathLane.STRUCTURAL_OBSTRUCTION,
    "projection_obstruction": MathLane.STRUCTURAL_OBSTRUCTION,
    "structural_obstruction": MathLane.STRUCTURAL_OBSTRUCTION,
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

    if any(token in " ".join((name, status, statement))
           for token in ("projection_obstruction", "countermodel",
                         "structural_obstruction")):
        return MathLane.STRUCTURAL_OBSTRUCTION

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
    MathLane.STRUCTURAL_OBSTRUCTION: 3,
    MathLane.OTHER: 4,
}

# This order is intentionally an audit/obstruction order, not proof admission.
# Every canonical bottleneck has a distinct value so the scheduler cannot let
# an unrelated lane/closability tie silently decide between different kinds of
# mathematical work.  Coverage remains first, source semantics precedes its
# physical Schur consumer, and local sign/FD diagnostics remain downstream.
_BOTTLENECK_ORDER = {
    "coverage": 0,
    # Exact-real algebra can close a useful conditional interface before the
    # larger evaluator enclosure is available.  It shares the high priority
    # band with the enclosure, but its Lean-adapter lane breaks the tie.
    "coefficient_identity": 1,
    "evaluator_enclosure": 1,
    "source_semantics": 2,
    "physical_schur_binding": 3,
    "interval_sign": 4,
    "central_fd": 5,
    "other": 6,
}

_BOTTLENECK_ALIASES = {
    "coverage": "coverage",
    "flowpipe_coverage": "coverage",
    "source": "source_semantics",
    "source_semantics": "source_semantics",
    "source_semantic": "source_semantics",
    "source_binding": "source_semantics",
    "evaluator_enclosure": "evaluator_enclosure",
    "source_evaluator": "evaluator_enclosure",
    "float64_enclosure": "evaluator_enclosure",
    "roundoff_enclosure": "evaluator_enclosure",
    "coefficient_identity": "coefficient_identity",
    "exact_real_coefficient_identity": "coefficient_identity",
    "port_coefficient_identity": "coefficient_identity",
    "physical_schur": "physical_schur_binding",
    "physical_schur_binding": "physical_schur_binding",
    "schur_binding": "physical_schur_binding",
    "interval_sign": "interval_sign",
    "sign": "interval_sign",
    "central_fd": "central_fd",
    "finite_difference": "central_fd",
    "finite_diff": "central_fd",
    "other": "other",
}

# Ambiguous compound names must use explicit metadata.  This deterministic
# fallback order chooses the broader domain obstruction before a local
# diagnostic and records the exact field/token used in the audit explanation.
_BOTTLENECK_MARKERS = (
    ("coverage", ("coverage", "flowpipe", "first_exit", "partition", "continuation")),
    ("physical_schur_binding", (
        "physical_schur_binding", "physical_schur", "schur_binding",
        "schur", "krawczyk", "operator_binding",
    )),
    ("evaluator_enclosure", (
        "evaluator_enclosure", "source_evaluator", "float64_enclosure",
        "roundoff_enclosure", "evaluator", "roundoff",
    )),
    ("interval_sign", ("interval_sign", "h_src", "sign_normal", "sign_theorem")),
    ("central_fd", ("central_fd", "central_difference", "finite_difference", "finite_diff")),
    ("source_semantics", (
        "source_semantics", "source_semantic", "source_comparator",
        "source_soundness", "true_dh", "exact_dh", "deployed_source",
    )),
)


@dataclass(frozen=True)
class MathBottleneckDecision:
    """Canonical, read-only classification used by audit and dispatch views."""

    label: str
    priority: int
    source: str
    reason: str


def _metadata(item: Any) -> Mapping[str, Any]:
    metadata = item.get("metadata", {}) if isinstance(item, Mapping) else getattr(item, "metadata", {})
    return metadata if isinstance(metadata, Mapping) else {}


def _bottleneck_fields(item: Any) -> list[tuple[str, str]]:
    metadata = _metadata(item)
    if isinstance(item, Mapping):
        raw_dependencies = item.get("dependencies", [])
        fields = [
            ("id", item.get("id", "")),
            ("name", item.get("name", "")),
            ("statement", item.get("statement", "")),
            ("status", item.get("status", "")),
            ("dependencies", " ".join(map(str, raw_dependencies))
             if isinstance(raw_dependencies, (list, tuple, set)) else raw_dependencies),
            ("verification_domain", item.get("verification_domain", "")),
        ]
    else:
        raw_dependencies = getattr(item, "dependencies", [])
        fields = [
            ("name", getattr(item, "name", "")),
            ("statement", getattr(item, "statement", "")),
            ("status", getattr(item, "status", "")),
            ("dependencies", " ".join(map(str, raw_dependencies))
             if isinstance(raw_dependencies, (list, tuple, set)) else raw_dependencies),
            ("verified_artifact", getattr(item, "verified_artifact", "")),
        ]
    fields.extend((f"metadata.{key}", metadata.get(key, "")) for key in (
        "verification_domain", "source_comparator", "source_comparator_status",
    ))
    return [(name, _token(value)) for name, value in fields if value is not None]


def explain_math_bottleneck(item: Any) -> MathBottleneckDecision:
    """Classify one item and retain a deterministic, auditable reason.

    A present but unsupported explicit value is fail-closed to ``other``; it
    is never silently replaced by a name heuristic.  This keeps typos visible
    to receipt consumers instead of changing dispatch priority unexpectedly.
    """
    metadata = _metadata(item)
    explicit_source = None
    explicit_value: Any = None
    if "math_bottleneck" in metadata:
        explicit_source = "metadata.math_bottleneck"
        explicit_value = metadata["math_bottleneck"]
    elif isinstance(item, Mapping) and "math_bottleneck" in item:
        explicit_source = "math_bottleneck"
        explicit_value = item["math_bottleneck"]

    if explicit_source is not None:
        explicit_token = _token(explicit_value)
        label = _BOTTLENECK_ALIASES.get(explicit_token)
        if label is None:
            return MathBottleneckDecision(
                "other", _BOTTLENECK_ORDER["other"], explicit_source,
                f"unsupported explicit bottleneck {explicit_token!r}; classified fail-closed as other",
            )
        return MathBottleneckDecision(
            label, _BOTTLENECK_ORDER[label], explicit_source,
            f"explicit {explicit_source}={explicit_token!r} canonicalizes to {label}",
        )

    fields = _bottleneck_fields(item)
    for label, markers in _BOTTLENECK_MARKERS:
        for field, value in fields:
            for marker in markers:
                if marker in value:
                    return MathBottleneckDecision(
                        label, _BOTTLENECK_ORDER[label], field,
                        f"inferred {label} from token {marker!r} in {field}",
                    )

    lane = _explicit_lane(item)
    if lane == MathLane.SOURCE_SEMANTICS:
        return MathBottleneckDecision(
            "source_semantics", _BOTTLENECK_ORDER["source_semantics"],
            "math_lane", "explicit source_semantics lane with no more specific bottleneck token",
        )
    return MathBottleneckDecision(
        "other", _BOTTLENECK_ORDER["other"], "fallback",
        "no canonical mathematical bottleneck token or explicit classification",
    )


def math_bottleneck(item: Any) -> str:
    """Return a stable audit label for a mathematical obstruction.

    Explicit ``metadata["math_bottleneck"]`` wins.  The fallback is only a
    naming aid for imported DAG rows and never changes proof eligibility.
    """
    return explain_math_bottleneck(item).label


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
        explain_math_bottleneck(node).priority,
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
    """Return an opt-in dispatch order that excludes known dead ends.

    ``rank_math_frontier`` remains an audit ordering and keeps numerical
    blockers visible.  This adapter is for callers with a formal/bridge lane:
    it preserves the obstruction gate and deterministic ordering while
    returning no numerical or structural obstruction when those are the only
    available work items.
    Ordinary scheduler callers are unchanged.
    """
    ranked = rank_math_frontier(state, jobs)
    return [node_id for node_id in ranked
            if math_lane(state.nodes[node_id]) not in {
                MathLane.NUMERICAL_BLOCKER,
                MathLane.STRUCTURAL_OBSTRUCTION,
            }]


def explain_math_frontier(state: WorkflowState, jobs: Mapping[str, Any] | None = None) -> list[dict[str, Any]]:
    """Produce a read-only lane explanation for every current frontier leaf."""
    state.validate()
    job_ids = set(jobs) if jobs is not None else None
    rows = []
    for node in state.frontier():
        lane = math_lane(node)
        bottleneck = explain_math_bottleneck(node)
        rank = obstruction_rank(node)
        rows.append({
            "node_id": node.id,
            "name": node.name,
            "math_lane": lane.value,
            "lane_priority": _LANE_ORDER[lane],
            "math_bottleneck": bottleneck.label,
            "bottleneck_priority": bottleneck.priority,
            "math_bottleneck_source": bottleneck.source,
            "math_bottleneck_reason": bottleneck.reason,
            "obstruction_rank": rank,
            "eligible": rank == 0 and (job_ids is None or node.id in job_ids),
            "repair_contract": node.metadata.get("frontier_repair_contract"),
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
        bottleneck = explain_math_bottleneck(node)
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
            "math_bottleneck": bottleneck.label,
            "bottleneck_priority": bottleneck.priority,
            "math_bottleneck_source": bottleneck.source,
            "math_bottleneck_reason": bottleneck.reason,
            "blocker": blocker,
            "evidence_hash": _evidence_hash(node),
            "priority": _LANE_ORDER[lane],
            "repair_contract": node.metadata.get("frontier_repair_contract"),
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
