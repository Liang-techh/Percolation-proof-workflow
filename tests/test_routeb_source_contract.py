from fractions import Fraction

from percolation_workflow.routeb_source_contract import (
    audit_routeb_p4_source_contract,
)


PMI = """
kc = 0.05
f1 = -a[ja] * qa - c[ja] * dqa + kc * qb + gw[ja] * w
f2 = -a[jb] * qb - c[jb] * dqb + kc * qa + gw[jb] * w
"""
DH = """
tau = -Kp .* q - (Kd + b_fr) .* dq + G0v + (gw_coef .* I_val) .* w
return Mq \\ (tau - Cdq - Gq)
"""


def test_canonical_force_scale_and_descriptor_semantics_pass():
    result = audit_routeb_p4_source_contract(PMI, DH)
    assert result.status == "SOURCE_CONTRACT_PASS"
    assert result.kc == Fraction(1, 20)
    assert result.expected_rho_kc == ("q5/20", "q4/20")
    assert result.expected_force_rho_kc == ("q5/100", "q4/200")
    assert result.remote_term_required == "M_BD(q) * a_D"
    assert result.force_acceleration_separated is True
    assert result.formal_certificate_allowed is False


def test_force_scale_adapter_is_accepted_with_explicit_coordinate_label():
    result = audit_routeb_p4_source_contract(
        PMI, DH, "def rhoKc (q) := (q.2 / 100, q.1 / 200)"
    )
    assert result.status == "SOURCE_AND_FORCE_SCALE_PASS"
    assert result.errors == ()
    assert result.observed_adapter_rho_kc == ("q5/100", "q4/200")
    assert result.observed_adapter_coordinate == "force"


def test_normalized_scale_adapter_is_also_accepted_explicitly():
    result = audit_routeb_p4_source_contract(
        PMI, DH, "def rhoKc (q) := (q.2 / 20, q.1 / 20)"
    )
    assert result.status == "SOURCE_AND_NORMALIZED_SCALE_PASS"
    assert result.observed_adapter_coordinate == "normalized_f"


def test_unknown_adapter_scale_is_rejected_fail_closed():
    result = audit_routeb_p4_source_contract(
        PMI, DH, "def rhoKc (q) := (q.2 / 99, q.1 / 99)"
    )
    assert result.status == "OPEN_FAIL_CLOSED"
    assert "adapter_kc_scale_mismatch" in result.errors


def test_hidden_kc_in_deployed_torque_is_a_source_mismatch():
    result = audit_routeb_p4_source_contract(PMI, DH + "\n kc * q[5]")
    assert result.status == "OPEN_FAIL_CLOSED"
    assert "deployed_dh_source_contains_unexpected_kc" in result.errors
