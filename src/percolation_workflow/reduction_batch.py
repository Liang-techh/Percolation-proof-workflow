"""Read-only batch projection for an optional reduction coordinator adapter."""
from __future__ import annotations

import hashlib
from collections.abc import Mapping
from typing import Any

from .model import NodeStatus, WorkflowState
from .registry import audit_registry


def _selected_proposal(parent: Any) -> Mapping[str, Any] | None:
    proposals = parent.metadata.get("reduction_proposals", [])
    if not isinstance(proposals, list):
        raise ValueError("reduction_proposals must be a list")
    for proposal in reversed(proposals):
        if (isinstance(proposal, Mapping)
                and proposal.get("reduction_status") == "accepted"
                and proposal.get("status") in {"sketch_checked", "sketch_accepted"}):
            return proposal
    return None


def reduction_closure_batch(state: WorkflowState, parent_id: str) -> dict[str, Any] | None:
    """Project an accepted reduction's child closure inputs without mutation.

    The projection is deliberately independent of scheduling and receipt
    promotion.  Child order comes from the proposal when valid; otherwise IDs
    are sorted, so completion order cannot affect the closure identity.
    """
    parent = state.nodes.get(parent_id)
    if parent is None:
        raise ValueError(f"missing parent: {parent_id}")
    proposal = _selected_proposal(parent)
    if proposal is None:
        return None                         # legacy proposals: caller fallback
    proposal_id = proposal.get("proposal_id")
    children = proposal.get("children")
    if not isinstance(proposal_id, str) or not proposal_id:
        raise ValueError("reduction proposal has no proposal_id")
    if not isinstance(children, list) or not children or any(
            not isinstance(child_id, str) or not child_id for child_id in children):
        raise ValueError("reduction proposal has no child IDs")
    if len(set(children)) != len(children):
        raise ValueError("reduction proposal contains duplicate child IDs")
    ordered = proposal.get("child_order", children)
    if not isinstance(ordered, list) or set(ordered) != set(children) or len(ordered) != len(children):
        ordered = sorted(children)

    statements: dict[str, str] = {}
    statuses: dict[str, str] = {}
    registry_status: dict[str, str] = {}
    try:
        freshness = audit_registry(state)
    except (AttributeError, OSError, TypeError, ValueError):
        freshness = {}
    for child_id in ordered:
        child = state.nodes.get(child_id)
        if child is None or not isinstance(child.statement, str) or not child.statement:
            raise ValueError(f"missing child/statement data: {child_id}")
        digest = hashlib.sha256(child.statement.encode("utf-8")).hexdigest()
        statements[child_id] = digest
        statuses[child_id] = child.status.value
        receipt = state.registry.get(child_id)
        audit = freshness.get(child_id, {})
        registry_status[child_id] = (
            "verified" if child.status == NodeStatus.VERIFIED
            and isinstance(receipt, Mapping)
            and receipt.get("statement") == child.statement
            and isinstance(audit, Mapping)
            and audit.get("status") == "current"
            else (audit.get("status") if isinstance(audit, Mapping)
                  and audit.get("status") in {"stale", "unavailable"}
                  else "missing_or_mismatched"))

    pairs = "".join(f"{child_id}:{statements[child_id]}\0" for child_id in ordered)
    closure_key = hashlib.sha256((proposal_id + "\0" + pairs).encode("utf-8")).hexdigest()
    return {
        "schema_version": 1,
        "proposal_id": proposal_id,
        "ordered_child_ids": list(ordered),
        "child_statement_sha256": dict(statements),
        "child_status": dict(statuses),
        "registry_status": dict(registry_status),
        "closure_key": closure_key,
    }


__all__ = ["reduction_closure_batch"]
