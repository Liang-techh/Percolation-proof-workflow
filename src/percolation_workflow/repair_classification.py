"""Read-only repair-loop classification and request planning.

This module is deliberately disjoint from the durable workflow writer.  It
projects existing attempts and coordinator events into repair records and
request-shaped dictionaries without changing nodes, attempts, events, the
registry, or the state revision.
"""
from __future__ import annotations

import hashlib
import json
from typing import Any

from .model import WorkflowState


ERROR_CLASSES = ("syntax", "api", "semantic", "comparator", "coverage")
_REPAIR_STATUSES = {
    "compile_error", "verification_error", "provenance_rejected",
    "verification_rejected", "strict_admission_rejected", "agent_error",
    "agent_timeout",
}
_SIGNALS = {
    "syntax": ("unexpected token", "unexpected identifier", "invalid syntax",
               "parser error", "unexpected end of input"),
    "api": ("unknown identifier", "unknown constant", "unknown tactic",
            "invalid field", "unknown namespace", "declaration has metavariables"),
    "semantic": ("type mismatch", "application type mismatch", "failed to synthesize",
                 "tactic failed", "unsolved goals", "cannot close goal"),
    "coverage": ("coverage=false", "coverage false", "missing domain case",
                 "uncovered branch", "initial set not covered", "terminal condition not covered",
                 "flowpipe gap"),
}


def _text(value: Any) -> str:
    if isinstance(value, str):
        return value
    if value is None:
        return ""
    return json.dumps(value, ensure_ascii=False, sort_keys=True)


def classify_diagnostic(diagnostic: str, *, source: str = "lean_compile") -> tuple[str | None, str]:
    """Classify one diagnostic conservatively; conflicting matches need review."""
    haystack = diagnostic.casefold()
    matches = [name for name, signals in _SIGNALS.items()
               if any(signal in haystack for signal in signals)]
    if len(matches) == 1:
        return matches[0], "high"
    if len(matches) > 1:
        return None, "low"
    if source in {"comparator", "provenance", "verification"}:
        return "comparator", "medium"
    return None, "low"


def _digest(value: dict[str, Any]) -> str:
    encoded = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(encoded.encode()).hexdigest()


def _owner(state: WorkflowState, explicit: Any) -> str | None:
    if isinstance(explicit, str) and explicit in state.nodes:
        return explicit
    return state.root_id if state.root_id in state.nodes else None


def _failed_attempt_records(state: WorkflowState) -> list[dict[str, Any]]:
    records = []
    for attempt in state.attempts.values():
        if attempt.status not in _REPAIR_STATUSES:
            continue
        diagnostic = "\n".join(part for part in (attempt.stderr, attempt.stdout) if part)
        source = "verification" if attempt.status in {
            "verification_error", "provenance_rejected", "verification_rejected",
            "strict_admission_rejected"} else "lean_compile"
        error_class, confidence = classify_diagnostic(diagnostic, source=source)
        if error_class is None and source == "verification":
            error_class, confidence = "comparator", "medium"
        records.append({
            "schema_version": 1, "class": error_class or "manual_review",
            "confidence": confidence, "source": source, "node_id": attempt.node_id,
            "attempt_id": attempt.id, "parent_id": state.nodes[attempt.node_id].parent_id,
            "raw_diagnostic": diagnostic, "evidence_status": "diagnostic_only",
            "next_action": "repair_same_node" if error_class else "manual_review",
            "status": attempt.status,
        })
    return records


def _event_records(state: WorkflowState) -> list[dict[str, Any]]:
    records = []
    for event in state.events:
        kind = str(event.get("kind", ""))
        if kind not in {"controller_final_comparator", "comparator_finished",
                        "verification_rejected"} and "coverage" not in kind.casefold():
            continue
        is_coverage = "coverage" in kind.casefold() or any(
            key in event for key in ("coverage_complete", "coverage_status", "covered"))
        source = "coverage_checker" if is_coverage else "comparator"
        diagnostic = "\n".join(part for part in (
            _text(event.get("stderr")), _text(event.get("stdout")),
            _text(event.get("reason")), _text(event.get("coverage_status"))) if part)
        failed = (event.get("accepted") is False or event.get("comparator_accepted") is False or
                  event.get("source_changed") is True or
                  event.get("coverage_complete") is False or
                  str(event.get("coverage_status", "")).casefold() in {"false", "open", "incomplete"})
        if not failed:
            continue
        error_class = "coverage" if is_coverage else "comparator"
        owner = _owner(state, event.get("node_id") or event.get("owner_node_id"))
        records.append({
            "schema_version": 1, "class": error_class, "confidence": "high",
            "source": source, "node_id": owner, "attempt_id": event.get("attempt_id"),
            "parent_id": state.nodes[owner].parent_id if owner else None,
            "raw_diagnostic": diagnostic, "evidence_status": "diagnostic_only",
            "next_action": "repair_same_node" if owner else "manual_review",
            "event_kind": kind,
        })
    return records


def dry_run_repair_integration(state: WorkflowState, *, max_repair_rounds: int = 3,
                               include_successful_events: bool = False) -> dict[str, Any]:
    """Return classified errors and request-shaped repairs without persistence.

    The output is intentionally not accepted by ``StateStore.save``: callers
    must use the ordinary dispatch API to create a real attempt/request.
    """
    if type(max_repair_rounds) is not int or max_repair_rounds < 1:
        raise ValueError("max_repair_rounds must be a positive integer")
    state.validate()
    records = _failed_attempt_records(state) + _event_records(state)
    records = [record for record in records if record["node_id"] is not None]
    latest_failed: dict[str, Any] = {}
    for attempt in state.attempts.values():
        if attempt.status in _REPAIR_STATUSES:
            latest_failed[attempt.node_id] = attempt
    plans = []
    requests = []
    for record in records:
        owner = record["node_id"]
        prior = latest_failed.get(owner)
        repair_of = prior.id if prior else record.get("attempt_id")
        if repair_of not in state.attempts:
            repair_of = None
        plan_core = {"schema_version": 1, "error_id": "", "owner_node_id": owner,
                     "repair_of_attempt_id": repair_of,
                     "parent_closure": {"parent_id": state.nodes[owner].parent_id,
                                        "required_children": list(state.nodes[owner].dependencies),
                                        "verified_children": [],
                                        "blocked_by_error_id": None,
                                        "closure_action": "retry_child"},
                     "bounded_round": {"round": len(state.nodes[owner].attempts) + 1,
                                       "max_rounds": max_repair_rounds},
                     "acceptance": ["coordinator attempt exits zero",
                                    "class-specific gate passes",
                                    "registry/parent closure uses existing verified gates"]}
        error_id = _digest({k: v for k, v in record.items() if k != "error_id"})
        record["error_id"] = error_id
        plan_core["error_id"] = error_id
        plan_core["plan_id"] = _digest(plan_core)
        plans.append(plan_core)
        node = state.nodes[owner]
        diagnostics = [{"status": record.get("status", record["class"]),
                        "stdout": "", "stderr": record["raw_diagnostic"],
                        "error_record": record}]
        requests.append({"request_id": "dry-run-" + _digest({"error_id": error_id, "node_id": owner})[:16],
                         "node_id": owner, "name": node.name, "statement": node.statement,
                         "proof_sketch": node.proof_sketch, "work_kind": "repair",
                         "repair_of_attempt_id": repair_of, "repair_round": len(node.attempts),
                         "repair_context": record, "diagnostics": diagnostics,
                         "status": "dry_run", "agent_id": None, "repair_plan": plan_core})
    return {"schema_version": 1, "mode": "dry_run", "persisted": False,
            "registry_changed": False, "error_records": records, "repair_plans": plans,
            "repair_requests": requests,
            "ignored_successful_events": (not include_successful_events)}
