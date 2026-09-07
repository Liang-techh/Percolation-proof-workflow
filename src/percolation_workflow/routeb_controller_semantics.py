"""Fail-closed comparison of the deployed and lifted Route-B damping laws.

The two source files use different names and numeric syntaxes, so a textual
"both contain Kd and friction" check is not enough.  This module parses the
small, deliberately supported Julia vector forms into exact ``Fraction``
values and compares the coefficient of each ``dq[i]`` in the torque law.

This is a source-semantics audit, not a dynamics theorem.  A matching vector
still needs an authoritative-source decision and the ordinary Lean/source
binding gates before registry admission.
"""
from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
import re


@dataclass(frozen=True)
class ControllerDampingAudit:
    status: str
    deployed_kd: tuple[Fraction, ...] | None
    deployed_friction: tuple[Fraction, ...] | None
    deployed_sum: tuple[Fraction, ...] | None
    lifted_kd: tuple[Fraction, ...] | None
    lifted_friction: tuple[Fraction, ...] | None
    lifted_sum: tuple[Fraction, ...] | None
    mismatched_indices: tuple[int, ...]
    difference: tuple[Fraction, ...] | None
    errors: tuple[str, ...] = ()
    formal_certificate_allowed: bool = False
    registry_eligible: bool = False


_Q_VECTOR = re.compile(
    r"(?m)^\s*(?P<name>Kd|Bfr)\s*=\s*Q\[(?P<body>[^\]]+)\]"
    r"\s*(?:\./\s*(?P<scale>[0-9]+))?"
)
_PLAIN_VECTOR = re.compile(
    r"(?m)^\s*(?P<name>Kd|b_fr)\s*=\s*\[(?P<body>[^\]]+)\]"
)


def _atom(raw: str) -> Fraction:
    token = raw.strip()
    q = re.fullmatch(r"Q\(\s*([+-]?\d+)\s*,\s*([1-9]\d*)\s*\)", token)
    if q:
        return Fraction(int(q.group(1)), int(q.group(2)))
    if re.fullmatch(r"[+-]?\d+", token):
        return Fraction(int(token), 1)
    if re.fullmatch(r"[+-]?(?:\d+(?:\.\d*)?|\.\d+)", token):
        return Fraction(token)
    raise ValueError(f"unsupported Julia rational atom: {token!r}")


def _split_vector(body: str) -> list[str]:
    """Split commas while preserving nested ``Q(a,b)`` atoms."""
    pieces: list[str] = []
    start = 0
    depth = 0
    for index, char in enumerate(body):
        if char == "(":
            depth += 1
        elif char == ")":
            depth -= 1
            if depth < 0:
                raise ValueError("unbalanced parentheses in coefficient vector")
        elif char == "," and depth == 0:
            pieces.append(body[start:index].strip())
            start = index + 1
    if depth != 0:
        raise ValueError("unbalanced parentheses in coefficient vector")
    pieces.append(body[start:].strip())
    return pieces


def _vector(body: str, scale: str | None = None) -> tuple[Fraction, ...]:
    pieces = _split_vector(body)
    values = tuple(_atom(item) for item in pieces)
    if not values or any(item == "" for item in pieces):
        raise ValueError("empty or malformed coefficient vector")
    if scale is not None:
        denominator = int(scale)
        values = tuple(value / denominator for value in values)
    return values


def _extract(source: str, *, deployed: bool) -> tuple[tuple[Fraction, ...], tuple[Fraction, ...]]:
    pattern = _PLAIN_VECTOR if deployed else _Q_VECTOR
    found: dict[str, tuple[Fraction, ...]] = {}
    for match in pattern.finditer(source):
        name = match.group("name")
        key = "friction" if name in {"b_fr", "Bfr"} else "kd"
        found[key] = _vector(match.group("body"), match.groupdict().get("scale"))
    missing = [key for key in ("kd", "friction") if key not in found]
    if missing:
        raise ValueError("missing damping vectors: " + ",".join(missing))
    if len(found["kd"]) != len(found["friction"]):
        raise ValueError("Kd and friction vectors have different dimensions")
    return found["kd"], found["friction"]


def audit_controller_damping_semantics(
    deployed_source: str,
    lifted_source: str,
) -> ControllerDampingAudit:
    """Compare exact per-coordinate ``dq`` damping coefficients."""
    errors: list[str] = []
    deployed_kd = deployed_friction = lifted_kd = lifted_friction = None
    try:
        deployed_kd, deployed_friction = _extract(deployed_source, deployed=True)
    except ValueError as exc:
        errors.append(f"deployed_parse:{exc}")
    try:
        lifted_kd, lifted_friction = _extract(lifted_source, deployed=False)
    except ValueError as exc:
        errors.append(f"lifted_parse:{exc}")

    if errors:
        return ControllerDampingAudit(
            status="OPEN_MALFORMED_CONTROLLER_DAMPING_SOURCE",
            deployed_kd=deployed_kd, deployed_friction=deployed_friction,
            deployed_sum=None, lifted_kd=lifted_kd,
            lifted_friction=lifted_friction, lifted_sum=None,
            mismatched_indices=(), difference=None, errors=tuple(errors),
        )

    assert deployed_kd is not None and deployed_friction is not None
    assert lifted_kd is not None and lifted_friction is not None
    deployed_sum = tuple(kd + fr for kd, fr in zip(deployed_kd, deployed_friction))
    lifted_sum = tuple(kd + fr for kd, fr in zip(lifted_kd, lifted_friction))
    if len(deployed_sum) != len(lifted_sum):
        errors.append("damping_vector_dimension_mismatch")
        return ControllerDampingAudit(
            status="OPEN_CONTROLLER_DAMPING_DIMENSION_MISMATCH",
            deployed_kd=deployed_kd, deployed_friction=deployed_friction,
            deployed_sum=deployed_sum, lifted_kd=lifted_kd,
            lifted_friction=lifted_friction, lifted_sum=lifted_sum,
            mismatched_indices=(), difference=None, errors=tuple(errors),
        )

    difference = tuple(a - b for a, b in zip(deployed_sum, lifted_sum))
    mismatches = tuple(index + 1 for index, delta in enumerate(difference) if delta)
    status = ("OPEN_CONTROLLER_DAMPING_VECTOR_MISMATCH"
              if mismatches else "MATCHED_CONTROLLER_DAMPING_VECTOR_PENDING_AUTHORITY")
    return ControllerDampingAudit(
        status=status,
        deployed_kd=deployed_kd, deployed_friction=deployed_friction,
        deployed_sum=deployed_sum, lifted_kd=lifted_kd,
        lifted_friction=lifted_friction, lifted_sum=lifted_sum,
        mismatched_indices=mismatches, difference=difference,
        errors=tuple(errors),
    )


__all__ = ["ControllerDampingAudit", "audit_controller_damping_semantics"]
