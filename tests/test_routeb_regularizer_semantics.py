from fractions import Fraction

import pytest

from percolation_workflow.routeb_regularizer_semantics import (
    EXACT_MU,
    FLOAT64_MU,
    MU_DELTA,
    RouteBExactResolventPremise,
    audit_routeb_regularizer_inclusion,
    convert_routeb_port_bound_to_weighted_metric,
    consume_routeb_schur_margin,
    derive_routeb_general_resolvent_port_propagation,
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


def test_general_resolvent_keeps_independent_block_errors_in_three_term_bound() -> None:
    result = derive_routeb_general_resolvent_port_propagation(
        RouteBExactResolventPremise("mass:D", "induced_2", Fraction(1)),
        epsilon_a=MU_DELTA,
        b_r_norm_bound=Fraction(2),
        b_difference_norm_bound=Fraction(1, 10),
        c_f_norm_bound=Fraction(3),
        c_difference_norm_bound=Fraction(1, 5),
        source_key="mass:D",
    )

    assert result.status == "CONDITIONAL_GENERAL_RESOLVENT_PORT_BOUND"
    assert result.inverse_norm_bound_float64 == 1 / (1 - MU_DELTA)
    assert result.inverse_difference_bound == MU_DELTA / (1 - MU_DELTA)
    expected = (
        Fraction(1, 10) * result.inverse_norm_bound_float64 * 3
        + 2 * result.inverse_difference_bound * 3
        + 2 * Fraction(1, 5)
    )
    assert result.port_difference_bound == expected
    assert result.weighted_port_bound_required is True


def test_general_resolvent_rejects_missing_epsilon_and_source_key_fail_closed() -> None:
    result = derive_routeb_general_resolvent_port_propagation(
        RouteBExactResolventPremise("mass:D", "induced_2", Fraction(1)),
        b_r_norm_bound=Fraction(2),
        b_difference_norm_bound=Fraction(1),
        c_f_norm_bound=Fraction(1),
        c_difference_norm_bound=Fraction(1),
    )

    assert result.status == "OPEN_FAIL_CLOSED"
    assert result.port_difference_bound is None
    assert "epsilon_a_missing" in result.errors
    assert result.errors.count("coupling_source_key_missing") == 1


def test_weighted_metric_conversion_requires_same_key_and_positive_root() -> None:
    result = convert_routeb_port_bound_to_weighted_metric(
        Fraction(3), Fraction(2), source_key="schur:B45", metric_source_key="schur:B45",
        metric_lower_bound_proven=True,
    )

    assert result.status == "CONDITIONAL_WEIGHTED_PORT_BOUND"
    assert result.weighted_port_bound == Fraction(3, 2)
    assert result.schur_margin_consumed is False


def test_weighted_metric_conversion_rejects_unproven_or_mismatched_metric() -> None:
    result = convert_routeb_port_bound_to_weighted_metric(
        Fraction(3), Fraction(2), source_key="port:A", metric_source_key="metric:B",
        metric_lower_bound_proven=False,
    )

    assert result.status == "OPEN_FAIL_CLOSED"
    assert result.weighted_port_bound is None
    assert "metric_source_key_mismatch" in result.errors
    assert "metric_lower_bound_not_authoritatively_supplied" in result.errors


def test_schur_margin_consumer_computes_added_young_charge_exactly() -> None:
    result = consume_routeb_schur_margin(
        Fraction(1, 2), Fraction(1, 10), Fraction(1, 4), Fraction(1),
        source_key="ledger:B45", margin_source_key="ledger:B45",
        baseline_bound_proven=True, perturbation_bound_proven=True,
    )

    assert result.status == "CONDITIONAL_SCHUR_MARGIN_CONSUMED"
    assert result.rho_rounded == Fraction(3, 5)
    assert result.added_young_charge == Fraction(11, 20)
    assert result.remaining_margin == Fraction(9, 20)
    assert result.margin_consumed is True


def test_schur_margin_consumer_rejects_mismatch_and_insufficient_budget() -> None:
    mismatch = consume_routeb_schur_margin(
        Fraction(1), Fraction(1, 2), Fraction(1), Fraction(1),
        source_key="port", margin_source_key="stale-ledger",
        baseline_bound_proven=True, perturbation_bound_proven=True,
    )
    insufficient = consume_routeb_schur_margin(
        Fraction(1), Fraction(1), Fraction(1), Fraction(1),
        source_key="ledger", margin_source_key="ledger",
        baseline_bound_proven=True, perturbation_bound_proven=True,
    )

    assert mismatch.status == "OPEN_FAIL_CLOSED"
    assert "schur_source_key_mismatch" in mismatch.errors
    assert insufficient.status == "OPEN_SCHUR_MARGIN_INSUFFICIENT"
    assert insufficient.margin_consumed is False


def test_schur_margin_consumer_rejects_unproven_numeric_bounds_by_default() -> None:
    result = consume_routeb_schur_margin(
        Fraction(1, 2), Fraction(1, 10), Fraction(1, 4), Fraction(1),
        source_key="ledger", margin_source_key="ledger",
    )

    assert result.status == "OPEN_FAIL_CLOSED"
    assert result.margin_consumed is False
    assert "baseline_port_bound_not_authoritatively_supplied" in result.errors
    assert "weighted_port_perturbation_not_authoritatively_supplied" in result.errors
