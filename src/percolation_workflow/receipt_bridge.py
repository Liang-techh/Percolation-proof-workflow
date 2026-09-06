"""Pure projection from an external receipt to a scheduler advisory outcome.

The projection is deliberately not a verification boundary.  In particular,
no receipt status can produce ``verified`` or alter workflow state.
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any


_OUTCOME_BY_STATUS = {
    "validated": "advisory_validated",
    "failed": "advisory_failed",
    "missing": "advisory_missing",
    "needs_manual_review": "advisory_needs_manual_review",
}


def receipt_to_frontier_outcome(receipt: Mapping[str, Any]) -> dict[str, Any]:
    """Return a scheduler-readable, advisory projection of ``receipt``.

    ``receipt`` must contain one of the four supported status values.  The
    returned dictionary is new and contains no reference to mutable receipt
    data.  ``verified`` is always false: this function only describes what the
    scheduler may do next and never grants formal admission.
    """
    if not isinstance(receipt, Mapping):
        raise TypeError("receipt must be a mapping")
    status = receipt.get("status")
    if status not in _OUTCOME_BY_STATUS:
        supported = ", ".join(_OUTCOME_BY_STATUS)
        raise ValueError(f"unsupported receipt status {status!r}; expected one of: {supported}")

    return {
        "schema_version": 1,
        "outcome": _OUTCOME_BY_STATUS[status],
        "receipt_status": status,
        "advisory": True,
        "verified": False,
        "dispatchable": status in {"failed", "missing"},
        "requires_manual_review": status == "needs_manual_review",
    }

