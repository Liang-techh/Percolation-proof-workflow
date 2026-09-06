"""Minimal, side-effect-free guard for comparator handoff review.

This module is intentionally below registry/admission.  It only decides whether
the handoff packet is reviewable; it never promotes, admits, or executes it.
"""
from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
import re
from typing import Any

_SHA256 = re.compile(r"^[0-9a-f]{64}$")


@dataclass(frozen=True)
class ComparatorHandoffResult:
    status: str
    blockers: tuple[dict[str, str], ...] = ()

    @property
    def reviewable(self) -> bool:
        return self.status == "reviewable"

    def to_dict(self) -> dict[str, Any]:
        return {"status": self.status, "reviewable": self.reviewable,
                "blockers": [dict(item) for item in self.blockers]}

    def __bool__(self) -> bool:
        return self.reviewable


def _missing(blockers: list[dict[str, str]], evidence: str, reason: str) -> None:
    blockers.append({"code": f"missing_{evidence}", "evidence": evidence, "reason": reason})


def check_comparator_handoff(
    *,
    statement_identity: Mapping[str, Any] | None = None,
    source_hash: str | None = None,
    coverage: Mapping[str, Any] | None = None,
    numeric_receipt: Mapping[str, Any] | None = None,
    kernel_evidence: Mapping[str, Any] | None = None,
) -> ComparatorHandoffResult:
    """Return ``reviewable`` iff all five required evidence classes are complete.

    The checks are deliberately structural.  In particular, this function does
    not call a registry or an admission gate, and does not treat numeric output
    as kernel evidence.
    """
    blockers: list[dict[str, str]] = []
    if not isinstance(statement_identity, Mapping) or not statement_identity:
        _missing(blockers, "statement_identity", "non-empty statement identity is required")
    if not isinstance(source_hash, str) or not _SHA256.fullmatch(source_hash):
        _missing(blockers, "source_hash", "a lowercase SHA-256 source hash is required")
    if not isinstance(coverage, Mapping) or not coverage or coverage.get("complete") is not True:
        _missing(blockers, "coverage", "coverage.complete must be true")
    if not isinstance(numeric_receipt, Mapping) or not numeric_receipt:
        _missing(blockers, "numeric_receipt", "non-empty numeric receipt is required")
    if not isinstance(kernel_evidence, Mapping) or not kernel_evidence:
        _missing(blockers, "kernel_evidence", "non-empty kernel evidence is required")
    return ComparatorHandoffResult("blocked" if blockers else "reviewable", tuple(blockers))


guard_comparator_handoff = check_comparator_handoff
