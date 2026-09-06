"""Fail-closed statement identity gate used before comparator-child admission."""
from __future__ import annotations

from dataclasses import dataclass
from collections.abc import Mapping, Iterable
import hashlib
import re
from typing import Any


def _normalise(value: Any) -> str | None:
    return re.sub(r"\s+", " ", value).strip() if isinstance(value, str) else None


def _digest(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


@dataclass(frozen=True)
class StatementComparatorGate:
    accepted: bool
    reasons: tuple[str, ...] = ()

    def __bool__(self) -> bool:
        return self.accepted


def check_statement_comparator_gate(*, source_identity: Mapping[str, Any] | None,
                                    source_statement: str | None,
                                    candidate_statement: str | None,
                                    covered_source: Iterable[str] | Mapping[str, Any] | None,
                                    target_theorem_identity: Mapping[str, Any] | None) -> StatementComparatorGate:
    """Check the four coordinator-owned bindings required for child admission.

    This is deliberately a pure structural gate: it neither proves equivalence nor
    invokes Lean. Missing context is rejected, so callers cannot accidentally turn
    an incomplete comparison into admission.
    """
    reasons: list[str] = []
    if not isinstance(source_identity, Mapping) or not source_identity:
        reasons.append("missing source identity")
    if not isinstance(target_theorem_identity, Mapping) or not target_theorem_identity:
        reasons.append("missing target theorem identity")
    left, right = _normalise(source_statement), _normalise(candidate_statement)
    if left is None or right is None:
        reasons.append("missing statement for normalization")
    elif left != right:
        reasons.append("normalized statement mismatch")
    if isinstance(source_identity, Mapping) and left is not None:
        expected = source_identity.get("statement_sha256")
        if not isinstance(expected, str) or expected != _digest(left):
            reasons.append("source identity does not bind normalized statement")
    if covered_source is None:
        reasons.append("missing source coverage")
    else:
        covered = (set(covered_source) if not isinstance(covered_source, Mapping)
                   else set(covered_source))
        source_key = source_identity.get("source") if isinstance(source_identity, Mapping) else None
        if not covered or (source_key is not None and source_key not in covered):
            reasons.append("source coverage is incomplete")
    if isinstance(source_identity, Mapping) and isinstance(target_theorem_identity, Mapping):
        for key in ("module", "name"):
            if source_identity.get(key) != target_theorem_identity.get(key):
                reasons.append(f"target theorem identity mismatch: {key}")
    return StatementComparatorGate(not reasons, tuple(dict.fromkeys(reasons)))


compare_statement_gate = check_statement_comparator_gate
