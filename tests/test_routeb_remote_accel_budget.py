from fractions import Fraction

from percolation_workflow.routeb_remote_accel_budget import (
    WEAKER_COORDINATEWISE_COEFFICIENT,
    derive_routeb_remote_acceleration_budget,
)


def test_remote_budget_uses_full_state_scalar_bound():
    result = derive_routeb_remote_acceleration_budget()
    assert result.status == "CONDITIONAL_EXACT_ARITHMETIC_CANDIDATE"
    assert result.remote_coordinates == (1, 2, 3, 6)
    assert result.euclidean_squared_coefficient == Fraction(90)
    assert result.coordinatewise_reference_coefficient == Fraction(802, 7)
    assert result.euclidean_squared_coefficient < WEAKER_COORDINATEWISE_COEFFICIENT


def test_remote_budget_never_opens_admission():
    result = derive_routeb_remote_acceleration_budget()
    assert result.formal_certificate_allowed is False
    assert result.registry_eligible is False
    assert "mass_is_full_state_kinetic_budget" in result.assumptions

