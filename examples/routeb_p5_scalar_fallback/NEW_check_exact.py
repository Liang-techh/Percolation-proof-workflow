"""Independent exact-rational checker for the P5-027 scalar sidecar.

This checker verifies the rational matrix, all four leading principal minors,
the LDL identity as a matrix identity, the division-free constant arithmetic,
and the explicit lower witness.  It is an algebraic certificate checker only;
it does not inspect or bind a source Jacobian, K_path, P8, coverage, or the
Route-B registry.
"""

from fractions import Fraction as F


def matmul(a, b):
    return [
        [sum(a[i][k] * b[k][j] for k in range(len(b))) for j in range(len(b[0]))]
        for i in range(len(a))
    ]


def transpose(a):
    return [list(row) for row in zip(*a)]


def determinant(m):
    a = [row[:] for row in m]
    n = len(a)
    out = F(1)
    for col in range(n):
        pivot = next((row for row in range(col, n) if a[row][col]), None)
        assert pivot is not None, "singular matrix in exact determinant"
        if pivot != col:
            a[col], a[pivot] = a[pivot], a[col]
            out = -out
        pivot_value = a[col][col]
        out *= pivot_value
        for row in range(col + 1, n):
            factor = a[row][col] / pivot_value
            for j in range(col + 1, n):
                a[row][j] -= factor * a[col][j]
    return out


def main():
    alpha = F(75, 106)
    alpha_inv = F(106, 75)
    c = F(47984317, 10000000)

    p = [
        [F(3, 4), -F(3, 400), F(0), F(1, 800)],
        [-F(3, 400), F(29, 50), -F(1, 800), F(0)],
        [F(0), -F(1, 800), F(2049997, 3000000), F(0)],
        [F(1, 800), F(0), F(0), F(2399261, 4000000)],
    ]
    r = [
        [F(1), F(0), F(1), F(0)],
        [F(0), F(1), F(0), F(1)],
        [F(1), F(0), F(1), F(0)],
        [F(0), F(1), F(0), F(1)],
    ]
    identity = [[F(int(i == j)) for j in range(4)] for i in range(4)]
    h = [
        [c * p[i][j] - alpha * r[i][j] - alpha_inv * identity[i][j]
         for j in range(4)]
        for i in range(4)
    ]
    expected_h = [
        [F(9399719209, 6360000000), -F(143952951, 4000000000),
         -F(75, 106), F(47984317, 8000000000)],
        [-F(143952951, 4000000000), F(52645685687, 79500000000),
         -F(47984317, 8000000000), -F(75, 106)],
        [-F(75, 106), -F(47984317, 8000000000),
         F(613762804181199, 530000000000000), F(0)],
        [F(47984317, 8000000000), -F(75, 106), F(0),
         F(4816377161968183, 6360000000000000)],
    ]
    assert h == expected_h, "weighted-gap matrix mismatch"

    minors = [determinant([row[:k] for row in h[:k]]) for k in range(1, 5)]
    expected_minors = [
        F(9399719209, 6360000000),
        F(395359846106875447280719, 404496000000000000000000),
        F(359556829343316384950230880641180953,
          449440000000000000000000000000000000),
        F(1337085894390964667090754208081695830761861,
          17977600000000000000000000000000000000000000000000),
    ]
    assert minors == expected_minors, "principal-minor value mismatch"
    assert all(value > 0 for value in minors), "Sylvester positivity failed"

    l = [
        [F(1), F(0), F(0), F(0)],
        [-F(22888519209, 939971920900), F(1), F(0), F(0)],
        [-F(4500000000, 9399719209),
         -F(13885594538623379761350, 395359846106875447280719), F(1), F(0)],
        [F(7629506403, 1879943841800),
         -F(845800100706139746004773, 790719692213750894561438),
         -F(3217560789628848699300752572801875,
            119852276447772128316743626880393651), F(1)],
    ]
    d = [
        F(9399719209, 6360000000),
        F(395359846106875447280719, 597822141692400000000000),
        F(3236011464089847464552077925770628577,
          3953598461068754472807190000000000000),
        F(1337085894390964667090754208081695830761861,
          14382273173732655398009235225647238120000000000000),
    ]
    ld = [[sum(l[i][k] * d[k] * l[j][k] for k in range(4))
           for j in range(4)] for i in range(4)]
    assert ld == h, "LDL matrix identity mismatch"
    assert all(value > 0 for value in d), "LDL weights are not positive"
    assert [d[0], d[0] and minors[1] / minors[0],
            minors[2] / minors[1], minors[3] / minors[2]] == d

    new_constant = c * c / 4
    assert new_constant == F(2302494677956489, 400000000000000)
    assert F(144, 25) - new_constant == F(1505322043511, 400000000000000)
    assert (new_constant - F(11512473, 2000000) ==
            F(77956489, 400000000000000))

    x4, x5, y4, y5 = 2379, 73046, 1832, 68229
    u = (x4 + y4) ** 2 + (x5 + y5) ** 2
    n = x4 ** 2 + x5 ** 2 + y4 ** 2 + y5 ** 2
    q = (F(3, 4) * x4 ** 2 + F(29, 50) * x5 ** 2 -
         F(3, 200) * x4 * x5 + F(2049997, 3000000) * y4 ** 2 +
         F(2399261, 4000000) * y5 ** 2 + F(1, 400) * x4 * y5 -
         F(1, 400) * x5 * y4)
    assert (u, n, q) == (19976358146, 9999930422,
                         F(14138344959005123, 2400000))
    cross = (10000000 * u * n * 2400000 ** 2 -
             57562365 * 14138344959005123 ** 2)
    assert cross == 23290832775682489880381695029915
    assert cross > 0

    print("P5_027_EXACT_RATIONAL_CHECK=PASS")
    print("SYLVESTER_PRINCIPAL_MINORS=PASS")
    print("LDL_MATRIX_IDENTITY=PASS")
    print("DIVISION_FREE_CONSTANT=2302494677956489/400000000000000")
    print("LOWER_WITNESS_THRESHOLD=11512473/2000000")
    print("SOURCE_BINDING=OPEN")
    print("P8_COVERAGE_AND_CLOSURE=OPEN")


if __name__ == "__main__":
    main()
