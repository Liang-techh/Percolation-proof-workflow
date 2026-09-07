from fractions import Fraction

import pytest

from percolation_workflow.routeb_regularizer_semantics import (
    EXACT_MU,
    FLOAT64_MU,
    MU_DELTA,
    RouteBExactResolventPremise,
    audit_routeb_regularizer_inclusion,
    derive_routeb_resolvent_port_propagation,
    propagate_routeb_regularizer_diagonal,
    routeb_regularizer_fact,
)


def test_scalar_fact_keeps_float64_below_exact_rational() -> None:
    fact = routeb_regularizer_fact()
    assert fact.mu_float64 == FLOAT64_MU
    assert fact.mu_exact_real == EXACT_MU
    assert fact.delta_exact == MU_DELTA
    assert fact.formal_certificate_allowed is False
    assert fact.registry_eligible is False


def test_matrix_inclusion_requires_exact_rational_inputs() -> None:
    result = audit_routeb_regularizer_inclusion([[1.0]], [[1]])
    assert result.status == "OPEN_FAIL_CLOSED"
    assert result.formal_certificate_allowed is False


def test_common_base_propagates_only_diagonal_delta() -> None:
    base = [[Fraction(i == j) for j in range(4)] for i in range(4)]
    result = propagate_routeb_regularizer_diagonal(
        base, block_coords=(1, 2), remote_coords=(3, 4)
    )
    assert result.status == "CONDITIONAL_COMMON_BASE_OUTWARD_INCLUSION"
    assert result.inclusion.status == "EXACT_OUTWARD_INCLUSION"
    assert result.float64_BD == result.exact_real_BD
    assert result.float64_DB == result.exact_real_DB
    assert result.exact_real_DD[0][0] - result.float64_DD[0][0] == MU_DELTA


def test_resolvent_without_premise_stays_pending() -> None:
    result = derive_routeb_resolvent_port_propagation(None)
    assert result.status == "PENDING_RESOLVENT_PREMISE"
    assert result.inverse_difference_bound is None


def test_resolvent_rejects_float_bound() -> None:
    result = derive_routeb_resolvent_port_propagation(
        RouteBExactResolventPremise("mass:D", "induced_2", Fraction(1)),
        mbd_norm_bound=1.0,
        delta_m_db_norm_bound=Fraction(1),
    )
    assert result.status == "OPEN_FAIL_CLOSED"
    assert result.port_difference_bound is None


def test_resolvent_can_produce_conditional_bound_with_exact_premises() -> None:
    result = derive_routeb_resolvent_port_propagation(
        RouteBExactResolventPremise("mass:D", "induced_2", Fraction(1)),
        mbd_norm_bound=Fraction(2),
        delta_m_db_norm_bound=Fraction(3),
        source_key="mass:D",
    )
    assert result.status == "CONDITIONAL_RESOLVENT_PORT_BOUND"
    assert result.inverse_difference_bound == MU_DELTA / (1 - MU_DELTA)
    assert result.port_difference_bound == 6 * result.inverse_difference_bound


def test_resolvent_rejects_couplings_without_matching_source_key() -> None:
    result = derive_routeb_resolvent_port_propagation(
        RouteBExactResolventPremise("mass:D", "induced_2", Fraction(1)),
        mbd_norm_bound=Fraction(2),
        delta_m_db_norm_bound=Fraction(3),
    )
    assert result.status == "OPEN_FAIL_CLOSED"
    assert result.port_difference_bound is None
    assert "coupling_source_key_missing" in result.errors
    assert result.errors.count("coupling_source_key_missing") == 1
