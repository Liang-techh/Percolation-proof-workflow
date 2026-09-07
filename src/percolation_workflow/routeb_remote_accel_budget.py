"""Exact conditional budget for the Route-B remote acceleration block.

The compiled ``RouteBRotationalDual`` sidecar proves a scalar full-state
coercivity consequence ``||a||^2 / 90 <= mass`` under its dual premise.  The
remote coordinates are a restriction of the full vector, so the same bound
gives ``||a_D||^2 <= 90 * mass``.  This module records that arithmetic seam for
the P4 remote contract; it does not bind ``mass`` to the deployed Float64 DH
evaluator or bound ``M_BD`` itself.
"""
from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction


REMOTE_ACCELERATION_COEFFICIENT = Fraction(90)
WEAKER_COORDINATEWISE_COEFFICIENT = Fraction(802, 7)


@dataclass(frozen=True)
class RouteBRemoteAccelerationBudget:
    status: str
    remote_coordinates: tuple[int, ...]
    euclidean_squared_coefficient: Fraction
    coordinatewise_reference_coefficient: Fraction
    assumptions: tuple[str, ...]
    formal_certificate_allowed: bool = False
    registry_eligible: bool = False


def derive_routeb_remote_acceleration_budget() -> RouteBRemoteAccelerationBudget:
    """Return the exact full-state-to-remote budget candidate.

    The 90 coefficient is inherited from the full-state scalar dual lemma;
    the 802/7 value is retained as a cross-check from the four coordinate
    force-metric coefficients ``3, 8, 95/7, 90``.
    """
    coordinatewise = Fraction(3) + Fraction(8) + Fraction(95, 7) + Fraction(90)
    return RouteBRemoteAccelerationBudget(
        status="CONDITIONAL_EXACT_ARITHMETIC_CANDIDATE",
        remote_coordinates=(1, 2, 3, 6),
        euclidean_squared_coefficient=REMOTE_ACCELERATION_COEFFICIENT,
        coordinatewise_reference_coefficient=coordinatewise,
        assumptions=(
            "RouteBRotationalDual.coercivity_from_dual",
            "mass_is_full_state_kinetic_budget",
            "a_and_aD_share_one_full_state_key",
            "remote_coordinates_are_exactly_(1,2,3,6)",
        ),
    )


__all__ = [
    "REMOTE_ACCELERATION_COEFFICIENT",
    "WEAKER_COORDINATEWISE_COEFFICIENT",
    "RouteBRemoteAccelerationBudget",
    "derive_routeb_remote_acceleration_budget",
]
