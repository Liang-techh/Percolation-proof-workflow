import copy

import pytest

from percolation_workflow.initial_binding_contract import (
    InitialBindingContractError,
    SCHEMA_VERSION,
    validate_initial_binding_contract,
)


H = "a" * 64


def _contract():
    return {
        "schema_version": SCHEMA_VERSION,
        "registry_eligible": False,
        "formal_certificate_allowed": False,
        "function": {
            "certificate_sha256": H,
            "coefficient_interpretation": "literal_decimal",
            "variable_order": ["q4", "q5", "v4", "v5", "t"],
            "t0": 0,
        },
        "domain": {
            "x0_key": "block45_X0",
            "constraint": "9/400-(q4^2+q5^2+v4^2+v5^2)>=0",
            "remote_coordinates_zero": True,
        },
        "upper": {
            "artifact_sha256": "b" * 64,
            "metric_selector": "initial_storage_upper",
            "value": "492033745203/25600000000000",
            "unique_row_count": 1,
        },
        "initial_witness": {
            "representation": "sos_plus_domain_multiplier",
            "artifact_sha256": "c" * 64,
            "monomial_basis": ["1", "q4", "q5", "v4", "v5"],
            "exact_coefficient_identity_checked": True,
            "psd_factorization_checked": True,
        },
        "producer_event": {
            "event_id": "producer-1",
            "execution_status": "planned",
            "output_hashes": {"upper": "b" * 64, "witness": "c" * 64},
            "execution_record": "pending-receipt.json",
        },
        "consumer_event": {
            "event_id": "consumer-1",
            "execution_status": "planned",
            "producer_event_ref": "producer-1",
            "function_key": "certificate.literal_decimal",
            "input_hashes": {"upper": "b" * 64, "witness": "c" * 64},
        },
    }


def test_initial_binding_is_structurally_consistent_but_pending():
    result = validate_initial_binding_contract(_contract())
    assert result["structural_consistency"] is True
    assert result["status"] == "PENDING"
    assert "missing_exact_finite_checker_receipt" in result["pending_reasons"]
    assert result["registry_eligible"] is False


def test_initial_binding_rejects_cross_run_hash_mismatch():
    data = _contract()
    data["consumer_event"]["input_hashes"]["upper"] = "d" * 64
    with pytest.raises(InitialBindingContractError, match="input hashes"):
        validate_initial_binding_contract(data)


@pytest.mark.parametrize(
    ("path", "value"),
    [
        (("function", "variable_order"), ["q4", "q5"]),
        (("upper", "unique_row_count"), 2),
        (("initial_witness", "exact_coefficient_identity_checked"), False),
    ],
)
def test_initial_binding_rejects_incomplete_finite_contract(path, value):
    data = _contract()
    cursor = data
    for key in path[:-1]:
        cursor = cursor[key]
    cursor[path[-1]] = value
    with pytest.raises(InitialBindingContractError):
        validate_initial_binding_contract(data)
