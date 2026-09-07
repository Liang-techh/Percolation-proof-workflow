from fractions import Fraction

from percolation_workflow.routeb_mbd_obstruction import audit_routeb_mbd_projection


CSV = """row,col,nu1,nu2,nu3,nu4,nu5,nu6,real_num,real_den,imag_num,imag_den
4,1,0,0,0,0,0,0,7,60,0,1
5,1,0,0,0,0,0,0,-21,80000,0,1
4,2,0,0,0,0,0,0,1,10,0,1
5,2,0,0,0,0,0,0,2,10,0,1
"""


def test_exact_projection_obstruction():
    result = audit_routeb_mbd_projection(CSV)
    assert result.status == "PROJECTION_OBSTRUCTION_EXACT"
    assert result.first_column_vector == (Fraction(7, 60), Fraction(-21, 80000))
    assert result.projection_factor == Fraction(784003969, 57600000000)
    assert result.formal_certificate_allowed is False


def test_malformed_or_zero_projection_fails_closed():
    result = audit_routeb_mbd_projection("row,col\n4,1\n")
    assert result.status == "OPEN_FAIL_CLOSED"
    assert result.registry_eligible is False
