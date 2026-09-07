from fractions import Fraction

from percolation_workflow.routeb_kc_budget import derive_routeb_kc_budget


def test_exact_canonical_force_budget():
    result = derive_routeb_kc_budget()
    assert result.status == "EXACT_ARITHMETIC_CANDIDATE"
    assert result.force_coefficients == (Fraction(1, 100), Fraction(1, 200))
    assert result.q_squared_cap == Fraction(56, 15)
    assert result.squared_force_bound == Fraction(7, 18750)
    assert result.formal_certificate_allowed is False


def test_invalid_domain_premise_fails_closed():
    result = derive_routeb_kc_budget(position_weight=Fraction(0))
    assert result.status == "OPEN_FAIL_CLOSED"
    assert result.registry_eligible is False
