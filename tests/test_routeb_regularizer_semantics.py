from fractions import Fraction

import pytest

from percolation_workflow.routeb_regularizer_semantics import (
    EXACT_MU,
    FLOAT64_MU,
    MU_DELTA,
    RouteBExactResolventPremise,
    audit_routeb_regularizer_inclusion,
    convert_routeb_infinity_port_bound_to_weighted_l2,
    convert_routeb_port_bound_to_weighted_metric,
    consume_routeb_schur_margin,
    derive_routeb_root_witness,
    derive_routeb_zero_shift_weighted_perturbation,
    derive_routeb_general_resolvent_port_propagation,
    derive_routeb_resolvent_port_propagation,
    propagate_routeb_regularizer_diagonal,
    routeb_regularizer_fact,
)
from percolation_workflow.routeb_o0_r3_receipt import (
    O0_R3_CANONICAL_RECEIPT_SCHEMA,
    audit_routeb_o0_r3_canonical_receipt,
    audit_routeb_o0_r3_receipt,
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


def test_resolvent_numeric_premise_is_not_authoritative_by_default() -> None:
    result = derive_routeb_resolvent_port_propagation(
        RouteBExactResolventPremise("mass:D", "induced_2", Fraction(1)),
        mbd_norm_bound=Fraction(2),
        delta_m_db_norm_bound=Fraction(3),
        source_key="mass:D",
    )

    assert result.status == "OPEN_FAIL_CLOSED"
    assert result.inverse_difference_bound is None
    assert "exact_real_inverse_bound_not_authoritatively_supplied" in result.errors


def test_resolvent_rejects_float_bound() -> None:
    result = derive_routeb_resolvent_port_propagation(
        RouteBExactResolventPremise("mass:D", "induced_2", Fraction(1), True),
        mbd_norm_bound=1.0,
        delta_m_db_norm_bound=Fraction(1),
    )
    assert result.status == "OPEN_FAIL_CLOSED"
    assert result.port_difference_bound is None


def test_resolvent_can_produce_conditional_bound_with_exact_premises() -> None:
    result = derive_routeb_resolvent_port_propagation(
        RouteBExactResolventPremise("mass:D", "induced_2", Fraction(1), True),
        mbd_norm_bound=Fraction(2),
        delta_m_db_norm_bound=Fraction(3),
        source_key="mass:D",
    )
    assert result.status == "CONDITIONAL_RESOLVENT_PORT_BOUND"
    assert result.inverse_difference_bound == MU_DELTA / (1 - MU_DELTA)
    assert result.port_difference_bound == 6 * result.inverse_difference_bound


def test_resolvent_rejects_couplings_without_matching_source_key() -> None:
    result = derive_routeb_resolvent_port_propagation(
        RouteBExactResolventPremise("mass:D", "induced_2", Fraction(1), True),
        mbd_norm_bound=Fraction(2),
        delta_m_db_norm_bound=Fraction(3),
    )
    assert result.status == "OPEN_FAIL_CLOSED"
    assert result.port_difference_bound is None
    assert "coupling_source_key_missing" in result.errors
    assert result.errors.count("coupling_source_key_missing") == 1


def test_general_resolvent_keeps_independent_block_errors_in_three_term_bound() -> None:
    result = derive_routeb_general_resolvent_port_propagation(
        RouteBExactResolventPremise("mass:D", "induced_2", Fraction(1), True),
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
        RouteBExactResolventPremise("mass:D", "induced_2", Fraction(1), True),
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


def test_infinity_to_l2_weighted_conversion_requires_explicit_output_norm_proof() -> None:
    result = convert_routeb_infinity_port_bound_to_weighted_l2(
        Fraction(3, 10), Fraction(2), Fraction(1, 5),
        source_key="cell", metric_source_key="cell",
    )
    assert result.status == "OPEN_FAIL_CLOSED"
    assert "output_norm_conversion_not_authoritatively_supplied" in result.errors
    assert result.weighted_l2_bound is None

    result = convert_routeb_infinity_port_bound_to_weighted_l2(
        Fraction(3, 10), Fraction(2), Fraction(1, 5),
        source_key="cell", metric_source_key="cell",
        output_norm_conversion_proven=True, metric_lower_bound_proven=True,
    )
    assert result.status == "CONDITIONAL_INFINITY_TO_L2_WEIGHTED_BOUND"
    assert result.weighted_l2_bound == Fraction(3)
    assert result.formal_certificate_allowed is False
    assert result.registry_eligible is False


def test_infinity_to_l2_weighted_conversion_keeps_key_mismatch_fail_closed() -> None:
    result = convert_routeb_infinity_port_bound_to_weighted_l2(
        Fraction(1), Fraction(2), Fraction(1, 5),
        source_key="cell-a", metric_source_key="cell-b",
        output_norm_conversion_proven=True,
    )
    assert result.status == "OPEN_FAIL_CLOSED"
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


def test_root_witness_keeps_squared_candidate_distinct_from_root() -> None:
    result = derive_routeb_root_witness(
        Fraction(4227, 500000), Fraction(9195, 100000),
        source_key="compact:eta27",
    )

    assert result.status == "CONDITIONAL_ROOT_WITNESS"
    assert result.root_bound == Fraction(9195, 100000)
    assert result.slack == Fraction(321, 400000000)
    assert result.squared_bound_proven is False
    assert result.formal_certificate_allowed is False


def test_root_witness_rejects_a_root_below_the_squared_candidate() -> None:
    result = derive_routeb_root_witness(
        Fraction(1, 4), Fraction(1, 3), source_key="compact"
    )

    assert result.status == "OPEN_FAIL_CLOSED"
    assert result.slack is not None and result.slack < 0
    assert "root_bound_squared_below_squared_bound" in result.errors


def test_zero_shift_reduction_derives_weighted_perturbation_exactly() -> None:
    result = derive_routeb_zero_shift_weighted_perturbation(
        Fraction(1, 10), Fraction(1, 2), Fraction(2), Fraction(3), Fraction(1, 5),
        source_key="canonical", metric_source_key="canonical",
        exact_inverse_proven=True, zero_offdiagonal_shift_proven=True,
        metric_lower_bound_proven=True,
    )

    assert result.status == "CONDITIONAL_ZERO_SHIFT_WEIGHTED_PORT_BOUND"
    assert result.inverse_difference_bound == Fraction(1, 38)
    assert result.unweighted_bound == Fraction(3, 19)
    assert result.weighted_bound == Fraction(15, 19)
    assert result.formal_certificate_allowed is False


def test_zero_shift_reduction_rejects_unproven_zero_shift() -> None:
    result = derive_routeb_zero_shift_weighted_perturbation(
        Fraction(1, 10), Fraction(1, 2), Fraction(2), Fraction(3), Fraction(1, 5),
        source_key="canonical", metric_source_key="canonical",
        exact_inverse_proven=True, metric_lower_bound_proven=True,
    )

    assert result.status == "OPEN_FAIL_CLOSED"
    assert "zero_offdiagonal_shift_not_authoritatively_supplied" in result.errors


def _o0_r3_receipt(**overrides):
    receipt = {
        "source_key": "physical:B45:cell-01",
        "metric_source_key": "physical:B45:cell-01",
        "margin_source_key": "physical:B45:cell-01",
        "rho_baseline": "1/2",
        "epsilon_port": "1/10",
        "theta": "1/4",
        "remaining_schur_margin": "1",
        "baseline_bound_proven": True,
        "perturbation_bound_proven": True,
        "metric_lower_bound_proven": True,
        "semantic_binding_proven": True,
        "port_binding_proven": True,
        "coverage_complete": True,
        "source_artifact_hashes": {"dhport_lib.jl": "ABC"},
    }
    receipt.update(overrides)
    return receipt


def test_o0_r3_receipt_validator_checks_exact_budget_and_provenance() -> None:
    result = audit_routeb_o0_r3_receipt(_o0_r3_receipt())

    assert result.status == "READY_FOR_COORDINATOR_ADMISSION"
    assert result.added_young_charge == Fraction(11, 20)
    assert result.leftover_margin == Fraction(9, 20)
    assert result.formal_certificate_allowed is False
    assert result.registry_eligible is False


def test_o0_r3_receipt_validator_is_pending_until_all_proof_flags_are_explicit() -> None:
    result = audit_routeb_o0_r3_receipt(
        _o0_r3_receipt(semantic_binding_proven=False)
    )

    assert result.status == "PENDING_PROOF_FIELDS"
    assert "semantic_binding_proven_not_proven" in result.errors
    assert result.added_young_charge is None


def test_o0_r3_receipt_validator_rejects_float_and_nonpositive_leftover() -> None:
    float_result = audit_routeb_o0_r3_receipt(_o0_r3_receipt(rho_baseline=0.5))
    margin_result = audit_routeb_o0_r3_receipt(
        _o0_r3_receipt(remaining_schur_margin="11/20")
    )

    assert float_result.status == "REJECTED"
    assert "exact integer/rational value required" in " ".join(float_result.errors)
    assert margin_result.status == "REJECTED"
    assert margin_result.leftover_margin == 0


def _canonical_o0_r3_receipt(**overrides):
    receipt = {
        "schema": O0_R3_CANONICAL_RECEIPT_SCHEMA,
        "status": "PENDING",
        "receipt_id": "receipt-01",
        "source_key": "canonical-K",
        "state_key": "canonical-K:cell-01:state-01",
        "domain": {
            "cell_id": "cell-01",
            "q_lo": ["0", "0", "0", "0", "0", "0"],
            "q_hi": ["1", "1", "1", "1", "1", "1"],
            "axis_order": ["q1", "q2", "q3", "q4", "q5", "q6"],
            "coverage": "complete-for-this-receipt",
        },
        "semantics": {
            "exact_real_mu": "1/1000000",
            "deployed_mu_literal": "1e-6",
            "fd_step": "1/1000",
            "force_scale": "canonical-force",
            "coefficient_version": "v1",
            "rounding_or_interval_mode": "outward",
        },
        "metric": {
            "orientation": "left_output",
            "norm": "induced_2",
            "B_up_identity": "B_up = S^T S",
            "beta": "1/2",
            "s": "1/4",
            "s_positive": True,
            "s_sq_le_beta": True,
            "B_up_ge_beta_I_proved": True,
        },
        "inverse": {
            "matrix": "M_DD(mu_exact)",
            "K": "1",
            "norm": "induced_2",
            "proves_exact_real_bound": True,
            "proof_receipt": "lean-K",
            "epsilon_A": "1/100",
            "epsilon_A_times_K_lt_one": True,
        },
        "weighted_baseline": {
            "map": "R_r",
            "rho_r": "1/2",
            "rho_r_nonnegative": True,
            "statement": "forall a_B, ||R_r a_B||_2^2 <= rho_r^2 * (a_B^T B_up a_B)",
            "proof_receipt": "baseline-K",
        },
        "weighted_perturbation": {
            "map": "R_f - R_r",
            "epsilon_R": "1/10",
            "statement": "||(R_f-R_r)a_B||_2 <= epsilon_R*sqrt(a_B^T B_up a_B)",
            "proof_receipt": "perturb-K",
        },
        "schur_baseline": {
            "theta": "1/4",
            "lambda": "1 + 1/theta",
            "remaining_margin_m_r": "1",
            "m_r_positive": True,
            "same_normalization_as_metric": True,
            "proof_receipt": "schur-K",
        },
        "physical_binding": {
            "statement": "R_port a_B = r_B",
            "proof_receipt": "binding-K",
        },
        "admission": {
            "all_source_keys_equal": True,
            "all_state_keys_equal": True,
            "registry_promoted": False,
            "formal_certificate_allowed": False,
        },
    }
    receipt.update(overrides)
    return receipt


def test_canonical_o0_r3_receipt_enforces_nested_same_key_contract() -> None:
    result = audit_routeb_o0_r3_canonical_receipt(_canonical_o0_r3_receipt())

    assert result.status == "READY_FOR_COORDINATOR_ADMISSION"
    assert result.added_young_charge == Fraction(11, 20)
    assert result.leftover_margin == Fraction(9, 20)
    assert result.formal_certificate_allowed is False
    assert result.registry_eligible is False


def test_canonical_o0_r3_receipt_keeps_missing_physical_proof_pending() -> None:
    receipt = _canonical_o0_r3_receipt()
    receipt["physical_binding"] = {"statement": "R_port a_B = r_B"}
    result = audit_routeb_o0_r3_canonical_receipt(receipt)

    assert result.status == "PENDING_REQUIRED_FIELDS"
    assert "physical_binding.proof_receipt" in result.missing


def test_canonical_o0_r3_receipt_rejects_float_and_key_boundary_violation() -> None:
    receipt = _canonical_o0_r3_receipt()
    receipt["weighted_baseline"]["rho_r"] = 0.5
    result = audit_routeb_o0_r3_canonical_receipt(receipt)
    assert result.status == "REJECTED"
    assert "exact integer/rational value required" in " ".join(result.errors)

    receipt = _canonical_o0_r3_receipt()
    receipt["admission"]["all_state_keys_equal"] = False
    result = audit_routeb_o0_r3_canonical_receipt(receipt)
    assert result.status == "REJECTED"
    assert "admission.state_keys_not_equal" in result.errors
