from fractions import Fraction

from scripts.check_routeb_p3_rotational_coercivity import audit_source


SOURCE = """
DH = [0.0 0.19 0.0 -pi/2;]
I_val = [1.0, 0.6, 0.35, 0.2, 0.1, 0.05]
Jv[:, jj] = cross(z[:, jj], pcom - o[:, jj])
Jw[:, jj] = z[:, jj]
Ii = (I_val[ii] / 3) .* Matrix{Float64}(I, 3, 3)
M += m[ii] .* (Jv' * Jv) + Jw' * (Ri * Ii * Ri') * Jw
return M + Float64(regularization) .* Matrix{Float64}(I, 6, 6)
"""


def test_structural_source_shape_and_exact_bounds():
    result = audit_source(SOURCE)
    assert result["status"] == "SOURCE_SHAPE_PASS"
    assert result["unregularized_inverse_norm_upper"] == "20"
    assert result["regularized_inverse_norm_upper"] == "20000000/1000001"
    assert result["formal_certificate_allowed"] is False


def test_wrong_inertia_or_missing_regularizer_fails_closed():
    broken = SOURCE.replace("0.2, 0.1, 0.05", "0.2, 0.2, 0.05")
    result = audit_source(broken)
    assert result["status"] == "OPEN_FAIL_CLOSED"
    assert "link_4_5_6_inertia_constants_not_bound" in result["errors"]
