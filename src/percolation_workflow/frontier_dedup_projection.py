"""Opt-in explanation of existing scheduler deduplication, not a new policy.

Eligibility precedes deduplication. Retention here precedes worker/cost limits
and is not dispatch, verification, or admission. All frontier node IDs survive
in the projection; shared candidate identity does not merge theorem evidence
or CONDITIONAL_PASS reviews. Nothing is persisted or appended to the event log.
"""

from __future__ import annotations

from typing import Any

from .model import WorkflowState
from .scheduler import FrontierJob, explain_frontier, rank_frontier


def project_frontier_dedup(
    state: WorkflowState, jobs: dict[str, FrontierJob]
) -> dict[str, Any]:
    """Explain which eligible leaves the existing scheduler deduplicates.

    Require the actual registered job map, but never call a job. Use the
    existing ranker as the authority for representatives rather than copying
    its ranking policy. Callers must supply a quiescent state, as for the
    existing frontier projections. The result is detached from state.
    """
    rows = explain_frontier(state, jobs)
    ranked = rank_frontier(state, jobs)
    positions = {node_id: i for i, node_id in enumerate(ranked)}
    representatives = {
        row["candidate_identity"]: row["node_id"]
        for row in rows
        if row["node_id"] in positions and row["candidate_identity"] is not None
    }
    for row in rows:
        node_id = row["node_id"]
        retained = node_id in positions
        duplicate = row["eligible"] and not retained
        row.update(
            dedup_status="duplicate" if duplicate else "retained" if retained else "ineligible",
            deduplicated_into=representatives[row["candidate_identity"]] if duplicate else None,
            rank_after_dedup=positions.get(node_id),
        )
    return {
        "schema": "frontier-dedup-projection-v1",
        "formal_admission": "unchanged",
        "selection_scope": "rank_frontier_before_worker_and_cost_limits",
        "ranked_node_ids": ranked,
        "frontier": sorted(rows, key=lambda row: row["node_id"]),
    }
