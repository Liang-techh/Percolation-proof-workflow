import csv
import io
from itertools import product

from percolation_workflow.routeb_nominal_distal_contract import (
    audit_routeb_nominal_distal_bridge,
    audit_routeb_physical_rational_gram,
    audit_routeb_physical_rational_tail,
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


def bridge_metadata_csv():
    rows = [
        ("block_B", "4,5"),
        ("D_coordinates", "1,2,3,6"),
        ("r_hat", "0,1,-6377/6250,0"),
        ("rho_num", "10616159325566083327957"),
        ("rho_den", "39062500000000000000000"),
        ("orthogonality_entries", "3"),
        ("retained_polynomial_terms", "46"),
        ("retained_max_total_cs_degree", "5"),
        ("full_MBB_12", "153080849893419/50000000000000000000000000000000"),
        ("full_MBB_21", "153080849893419/50000000000000000000000000000000"),
        ("evidence_level", "algebraic_subcertificate"),
    ]
    output = io.StringIO()
    writer = csv.writer(output, lineterminator="\n")
    writer.writerow(["metric", "value"])
    writer.writerows(rows)
    return output.getvalue()


def tail_meta_csv():
    rows = [
        ("pmi_dimension", "3"),
        ("schur_scalar_dimension", "1"),
        ("scalar_terms", "27"),
        ("scalar_max_total_cs_degree", "6"),
        ("rho", "10616159325566083327957/39062500000000000000000"),
        ("delta_sq", "1/160000"),
        ("active_variables", "c3;s3;c4;s4;c5;s5"),
        ("energy_accounting", "tail_only_no_double_count"),
        ("evidence_level", "algebraic_sos_input_candidate"),
    ]
    return "metric,value\n" + "\n".join(f"{k},{v}" for k, v in rows) + "\n"


def scalar_csv():
    header = "row,col," + ",".join(f"e{k}" for k in range(1, 13)) + ",num,den\n"
    zero = "0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1\n"
    return header + "1,1,0,0,0,0,1,0,0,0,0,0,0,0,1,1\n" + zero


def valid_scalar_csv():
    output = io.StringIO()
    writer = csv.writer(output, lineterminator="\n")
    writer.writerow(["row", "col", *[f"e{k}" for k in range(1, 13)], "num", "den"])
    monomials = []
    for total in range(3):
        monomials.extend(
            exponents for exponents in product(range(3), repeat=6)
            if sum(exponents) == total
        )
    monomials = monomials[:26] + [(6, 0, 0, 0, 0, 0)]
    for exponents in monomials:
        writer.writerow([1, 1, *([0] * 4), *exponents, 0, 0, 1, 1])
    return output.getvalue()


def test_exact_rational_tail_candidate_is_pending():
    # Keep the fixture small: duplicate rows combine, while the production
    # artifact is checked for its full 27-term canonical polynomial.
    scalar = scalar_csv().replace(
        "1,1,0,0,0,0,1,0,0,0,0,0,0,0,1,1\n",
        "1,1,0,0,0,0,1,0,0,0,0,0,0,0,1,1\n" * 27
    )
    result = audit_routeb_physical_rational_tail(
        bridge_metadata_csv(), tail_meta_csv(), scalar,
    )
    assert result.status == "OPEN_FAIL_CLOSED"
    assert "scalar_polynomial_term_count_mismatch" in result.errors


def test_exact_rational_tail_shape_can_pass_without_proving_psd():
    result = audit_routeb_physical_rational_tail(
        bridge_metadata_csv(), tail_meta_csv(), valid_scalar_csv(),
    )
    assert result.status == "EXACT_RATIONAL_TAIL_CANDIDATE"
    assert result.scalar_terms == 27
    assert result.scalar_max_total_cs_degree == 6
    assert result.formal_certificate_allowed is False


def test_exact_rational_tail_rejects_active_variable_drift():
    scalar = scalar_csv().replace(
        "1,1,0,0,0,0,1,0,0,0,0,0,0,0,1,1",
        "1,1,1,0,0,0,1,0,0,0,0,0,0,0,1,1",
    )
    result = audit_routeb_physical_rational_tail(
        bridge_metadata_csv(), tail_meta_csv(), scalar,
    )
    assert result.status == "OPEN_FAIL_CLOSED"
    assert "scalar_polynomial_active_variable_mismatch" in result.errors


def test_rational_gram_rejects_asymmetric_block_fail_closed():
    audit = "metric,value\nformal_certificate_allowed,false\n"
    gram = (
        "kind,clique,constraint,block,row,col,num,den\n"
        "gram,1,1,1,1,1,1,1\n"
        "gram,1,1,1,1,2,1,1\n"
        "gram,1,1,1,2,1,0,1\n"
        "gram,1,1,1,2,2,1,1\n"
    )
    basis = (
        "kind,clique,constraint,block,block_row,basis_index,exponents\n"
        "gram,1,1,1,1,1,\n"
        "gram,1,1,1,2,2,1\n"
    )
    result = audit_routeb_physical_rational_gram(audit, gram, basis)
    assert result.status == "OPEN_FAIL_CLOSED"
    assert "gram_matrix_not_symmetric:('1', '1', '1')" in result.errors


def test_tail_identity_check_requires_both_source_inputs():
    result = audit_routeb_physical_rational_tail(
        bridge_metadata_csv(), tail_meta_csv(), scalar_csv(),
        tail_cs_csv_text="not-used",
    )
    assert result.status == "OPEN_FAIL_CLOSED"
    assert "tail_identity_inputs_incomplete" in result.errors
