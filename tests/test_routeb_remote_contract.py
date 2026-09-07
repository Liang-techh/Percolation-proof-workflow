from percolation_workflow.routeb_remote_contract import audit_routeb_remote_binding


def full_state_receipt():
    return {
        "schema": "routeb.remote_binding.v1",
        "full_state_key": "cell-0/point-0",
        "source_snapshot": {"dhport_lib.jl": "a" * 64},
        "block_coords": [4, 5],
        "remote_coords": [1, 2, 3, 6],
        "norm_convention": "induced_2",
        "action_semantics": "MBD_times_aD",
        "binding_mode": "full_state",
        "aD_bound": {"squared": "finite"},
        "MBD_operator_bound": {"squared": "finite"},
        "remote_action_bound": {"squared": "finite"},
        "descriptor_identity": "source_force_B=MBB*aB+MBD*aD+remainder",
    }


def test_full_state_remote_contract_is_structural_only():
    result = audit_routeb_remote_binding(full_state_receipt())
    assert result.status == "STRUCTURAL_PASS"
    assert result.mode == "full_state"
    assert result.formal_certificate_allowed is False
    assert result.registry_eligible is False


def test_block_only_remote_bound_is_rejected_even_with_a_mode():
    receipt = full_state_receipt()
    receipt.pop("aD_bound")
    receipt["block_only_remote_bound"] = {"squared": "finite"}
    result = audit_routeb_remote_binding(receipt)
    assert result.status == "OPEN_FAIL_CLOSED"
    assert "block_only_remote_bound_forbidden" in result.errors
    assert "missing_mode_field:full_state:aD_bound" in result.errors


def test_schur_mode_requires_d_row_elimination_premises():
    receipt = full_state_receipt()
    receipt["binding_mode"] = "d_row_schur"
    for field in ("aD_bound", "remote_action_bound", "descriptor_identity"):
        receipt.pop(field)
    receipt["d_row_residual_bound"] = {"squared": "finite"}
    receipt["MDD_regularized_inverse_bound"] = {"squared": "finite"}
    receipt["schur_elimination_identity"] = "MBD*aD=K*(rhsD-MDB*aB)"
    result = audit_routeb_remote_binding(receipt)
    assert result.status == "STRUCTURAL_PASS"
    assert result.required_fields == (
        "d_row_residual_bound",
        "MDD_regularized_inverse_bound",
        "MBD_operator_bound",
        "schur_elimination_identity",
    )


def test_coordinate_or_semantics_drift_fails_closed():
    receipt = full_state_receipt()
    receipt["remote_coords"] = [1, 2, 3, 5]
    receipt["action_semantics"] = "aD_only"
    result = audit_routeb_remote_binding(receipt)
    assert result.status == "OPEN_FAIL_CLOSED"
    assert "remote_coordinate_order_mismatch" in result.errors
    assert "remote_action_semantics_not_explicit" in result.errors
