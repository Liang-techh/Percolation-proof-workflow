import copy

from percolation_workflow.residual_ledger import audit_residual_ledger
from percolation_workflow.residual_ledger import audit_full_state_binding


def skeleton():
    channels = {
        name: {"source_field": name, "bound": {"lo": 0, "hi": 1}, "status": "open"}
        for name in ("rho_C", "rho_G", "rho_mgl", "rho_kc", "rho_mass", "rho_remote")
    }
    return {
        "schema": "routeb.residual_ledger.v1",
        "cell_id": "cell-0", "q_box": [0, 1], "dq_box": [0, 1],
        "t_box": [0, 1], "w_box": [0, 1], "source_sha256": "a" * 64,
        "norm_convention": "induced_2", "outward_rounding_mode": "directed",
        "channels": channels,
        "remainder_total": {
            "bound": {"lo": 0, "hi": 1}, "charged_once": True,
            "components": ["fd_remainder", "rounding_remainder", "solve_remainder"],
        },
        "charged_channels": ["rho_C", "rho_G", "rho_mgl", "rho_kc", "rho_mass", "rho_remote", "remainder_total"],
    }


def test_structural_pass_never_opens_formal_admission():
    result = audit_residual_ledger(skeleton())
    assert result["status"] == "STRUCTURAL_PASS"
    assert result["formal_certificate_allowed"] is False
    assert result["registry_eligible"] is False


def test_repeated_remainder_charge_fails_closed():
    receipt = skeleton()
    receipt["charged_channels"].append("fd_remainder")
    result = audit_residual_ledger(receipt)
    assert result["status"] == "OPEN_FAIL_CLOSED"
    assert "charged_channels_not_exactly_once" in result["errors"]


def test_missing_remote_or_remainder_fields_fail_closed():
    receipt = copy.deepcopy(skeleton())
    del receipt["channels"]["rho_remote"]
    receipt["remainder_total"]["charged_once"] = False
    result = audit_residual_ledger(receipt)
    assert result["status"] == "OPEN_FAIL_CLOSED"
    assert "missing_channel:rho_remote" in result["errors"]
    assert "remainder_not_charged_once" in result["errors"]


def full_state_binding_skeleton():
    source = {"routeB_interval_bounds.jl": "a" * 64}
    key = "cell-0/point-0"
    payloads = {}
    for name, value in {
        "q": [0] * 6, "dq": [0] * 6, "t": 0, "w": 0,
        "a": [0] * 6, "aB": [0, 0], "aD": [0] * 4,
        "MBD": [[0] * 4, [0] * 4], "MBD_aD": [0, 0],
        "B": [4, 5], "D": [1, 2, 3, 6], "rhs_B": [0, 0], "rhs_D": [0] * 4,
    }.items():
        payloads[name] = {"value": value, "full_state_key": key,
                          "source_snapshot": source}
    return {
        "schema": "routeb.full_state_binding.v1",
        "full_state_key": key, "source_snapshot": source,
        "norm_convention": "induced_2", "action_semantics": "MBD_times_aD",
        "payloads": payloads,
    }


def test_full_state_binding_requires_one_keyed_physical_payload():
    result = audit_full_state_binding(full_state_binding_skeleton())
    assert result["status"] == "STRUCTURAL_PASS"
    assert result["formal_certificate_allowed"] is False
    assert result["registry_eligible"] is False


def test_full_state_binding_rejects_key_or_norm_drift():
    receipt = full_state_binding_skeleton()
    receipt["payloads"]["MBD_aD"]["full_state_key"] = "other-cell"
    receipt["norm_convention"] = "induced_1"
    result = audit_full_state_binding(receipt)
    assert result["status"] == "OPEN_FAIL_CLOSED"
    assert "payload_key_mismatch:MBD_aD" in result["errors"]
    assert "unsupported_norm_convention" in result["errors"]
