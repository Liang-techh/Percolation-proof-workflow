from fractions import Fraction

from percolation_workflow.routeb_controller_semantics import (
    audit_controller_damping_semantics,
)


DEPLOYED = """
Kd = [0.8, 0.7, 0.6, 0.5, 0.4, 0.3]
b_fr = [0.5, 0.4, 0.35, 0.3, 0.25, 0.2]
"""
LIFTED = """
Kd = Q[4, 5, 3, 1, 2, 3] ./ 5
Bfr = Q[1, Q(2, 5), Q(7, 20), Q(3, 10), Q(1, 4), Q(1, 5)]
"""


def test_damping_audit_reports_exact_mismatch_per_joint():
    result = audit_controller_damping_semantics(DEPLOYED, LIFTED)
    assert result.status == "OPEN_CONTROLLER_DAMPING_VECTOR_MISMATCH"
    assert result.mismatched_indices == (1, 2, 4, 6)
    assert result.deployed_sum == (
        Fraction(13, 10), Fraction(11, 10), Fraction(19, 20),
        Fraction(4, 5), Fraction(13, 20), Fraction(1, 2),
    )
    assert result.lifted_sum == (
        Fraction(9, 5), Fraction(7, 5), Fraction(19, 20),
        Fraction(1, 2), Fraction(13, 20), Fraction(4, 5),
    )
    assert result.formal_certificate_allowed is False


def test_damping_audit_accepts_exactly_matching_vectors_but_stays_pending():
    lifted = LIFTED.replace(
        "Q[1, Q(2, 5), Q(7, 20), Q(3, 10), Q(1, 4), Q(1, 5)]",
        "Q[Q(1, 2), Q(1, 10), Q(7, 20), Q(3, 5), Q(1, 4), Q(-1, 10)]",
    )
    result = audit_controller_damping_semantics(DEPLOYED, lifted)
    assert result.status == "MATCHED_CONTROLLER_DAMPING_VECTOR_PENDING_AUTHORITY"
    assert result.mismatched_indices == ()


def test_damping_audit_rejects_malformed_source():
    result = audit_controller_damping_semantics("Kd = [1]", LIFTED)
    assert result.status == "OPEN_MALFORMED_CONTROLLER_DAMPING_SOURCE"
    assert any(error.startswith("deployed_parse:") for error in result.errors)
