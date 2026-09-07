from percolation_workflow.routeb_nominal_distal_contract import (
    audit_routeb_nominal_distal_bridge,
)


def audit_csv():
    rows = [
        ("status", "DH_NOMINAL_DISTAL_BRIDGE_AUDIT"),
        ("mass_regularizer", "1//1000000"),
        ("full_D_descriptor_rows", "4"),
        ("nominal_equation_rows", "4"),
        ("reduced_equation_rows", "4"),
        ("retained_port_rows", "2"),
        ("split_identity_exact", "true"),
        ("nominal_equation_max_degree", "10"),
        ("reduced_equation_max_degree", "9"),
        ("port_max_degree", "6"),
        ("full_DH_rhs_semantics", "true"),
        ("formal_certificate_allowed", "false"),
    ]
    return "metric,value\n" + "\n".join(f"{k},{v}" for k, v in rows) + "\n"


def interface_csv():
    rows = [
        ("block_B", "4;5"),
        ("block_D", "1;2;3;6"),
        ("inverse_substitution", "false"),
        ("nominal_remote_equation", "M_DD(q)^(-1)*(b_D-M0_DB*a_B)"),
        ("v_descriptor_equation", "M_DD(q)*v+DeltaM_DB(q)*a_B=0"),
        ("force_port_equation", "r_B-M_BD(q)*v=0"),
    ]
    return "field,value\n" + "\n".join(f"{k},{v}" for k, v in rows) + "\n"


def test_exact_nominal_bridge_shape_is_pending_candidate():
    result = audit_routeb_nominal_distal_bridge(
        audit_csv(), interface_csv(),
        artifact_sha256="a" * 64, source_sha256="b" * 64,
    )
    assert result.status == "EXACT_DESCRIPTOR_BRIDGE_CANDIDATE"
    assert result.block_coordinates == (4, 5)
    assert result.remote_coordinates == (1, 2, 3, 6)
    assert result.formal_certificate_allowed is False
    assert result.registry_eligible is False


def test_nominal_bridge_rejects_inverses_or_coordinate_drift():
    interface = interface_csv().replace("M_DD(q)^(-1)", "inverse(M_DD(q))")
    interface = interface.replace("1;2;3;6", "1;2;3;5")
    result = audit_routeb_nominal_distal_bridge(audit_csv(), interface)
    assert result.status == "OPEN_FAIL_CLOSED"
    assert "interface_mismatch:nominal_remote_equation" in result.errors
    assert "remote_coordinate_order_mismatch" in result.errors
