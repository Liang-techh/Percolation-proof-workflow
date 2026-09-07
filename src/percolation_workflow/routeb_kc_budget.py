"""Exact arithmetic checker for the isolated Route-B ``kc`` budget.

This module deliberately checks only the normalized-to-force coordinate map
and the block-domain bound for that one residual channel. It does not bind
the Julia source, prove trajectory coverage, or admit a Route-B certificate.
"""
from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction


@dataclass(frozen=True)
class RouteBKcBudget:
    status: str
    normalized_kc: Fraction
    force_coefficients: tuple[Fraction, Fraction]
    q_squared_cap: Fraction
    squared_force_bound: Fraction
    formal_certificate_allowed: bool = False
    registry_eligible: bool = False


def derive_routeb_kc_budget(
    *,
    normalized_kc: Fraction = Fraction(1, 20),
    inertia4: Fraction = Fraction(1, 5),
    inertia5: Fraction = Fraction(1, 10),
    position_weight: Fraction = Fraction(3, 2),
    block_energy_cap: Fraction = Fraction(28, 5),
) -> RouteBKcBudget:
    """Return the exact one-channel budget under the current block domain."""
    force_coefficients = (inertia4 * normalized_kc, inertia5 * normalized_kc)
    if position_weight <= 0 or block_energy_cap < 0:
        return RouteBKcBudget(
            status="OPEN_FAIL_CLOSED",
            normalized_kc=normalized_kc,
            force_coefficients=force_coefficients,
            q_squared_cap=Fraction(0),
            squared_force_bound=Fraction(0),
        )
    q_squared_cap = block_energy_cap / position_weight
    max_squared_coefficient = max(c * c for c in force_coefficients)
    return RouteBKcBudget(
        status="EXACT_ARITHMETIC_CANDIDATE",
        normalized_kc=normalized_kc,
        force_coefficients=force_coefficients,
        q_squared_cap=q_squared_cap,
        squared_force_bound=max_squared_coefficient * q_squared_cap,
    )


__all__ = ["RouteBKcBudget", "derive_routeb_kc_budget"]
