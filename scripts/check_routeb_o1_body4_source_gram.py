"""Read-only exact polynomial check of the proposed body-4 source formulas.

Mirrors the four source DH parameter rows; does not parse/elaborate Lean,
read Fourier CSV, run Lean/Lake, write receipts, or establish source admission.
Run: python scripts/check_routeb_o1_body4_source_gram.py
Requires SymPy. All arithmetic is rational polynomial arithmetic.
"""
from __future__ import annotations

import json
import sympy as sp


def main() -> None:
    rat = sp.Rational
    s0, c0, s1, c1, s2, c2, s3, c3 = sp.symbols("s0 c0 s1 c1 s2 c2 s3 c3")
    variables = (s0, c0, s1, c1, s2, c2, s3, c3)
    circle = sp.groebner(
        [s0**2 + c0**2 - 1, s1**2 + c1**2 - 1,
         s2**2 + c2**2 - 1, s3**2 + c3**2 - 1],
        *variables, domain=sp.QQ,
    )
    counts: dict[str, int] = {}

    def check(group: str, actual: sp.MatrixBase, expected: sp.MatrixBase) -> None:
        assert actual.shape == expected.shape, group
        for index, difference in enumerate(actual - expected):
            remainder = circle.reduce(sp.expand(difference))[1]
            if remainder != 0:
                raise AssertionError(f"{group}[{index}]: {remainder}")
        counts[group] = counts.get(group, 0) + len(actual)

    def dh(ct, st, ca, sa, a, d):
        return sp.Matrix([
            [ct, -st * ca, st * sa, ct * a],
            [st, ct * ca, -ct * sa, st * a],
            [0, sa, ca, d], [0, 0, 0, 1],
        ])

    # RealDHStep + FourierNormalForm exact rows, k = 0,1,2,3.
    steps = [
        dh(c0, s0, 0, -1, rat(2, 25), rat(1, 10)),
        dh(s1, -c1, 1, 0, rat(21, 100), 0),
        dh(-s2, c2, 0, 1, 0, rat(1, 20)),
        dh(c3, s3, 0, -1, 0, rat(19, 100)),
    ]
    frames = [sp.eye(4)]
    for step in steps:
        frames.append(frames[-1] * step)
    origins = [frame[:3, 3] for frame in frames]
    axes = [frame[:3, 2] for frame in frames[:4]]
    er, et, ez = sp.Matrix([c0, s0, 0]), sp.Matrix([-s0, c0, 0]), sp.Matrix([0, 0, 1])
    sp_, cp = s1 * c2 + c1 * s2, c1 * c2 - s1 * s2
    b, c, d, e = rat(21, 100) * s1, rat(21, 100) * c1, rat(1, 20), rat(19, 200)
    a, p, q = rat(2, 25) + b + e * sp_, c + e * cp, b + e * sp_
    z3 = sp_ * er + cp * ez
    expected_origins = [
        sp.zeros(3, 1), rat(2, 25) * er + rat(1, 10) * ez,
        (rat(2, 25) + b) * er + (rat(1, 10) + c) * ez,
        (rat(2, 25) + b) * er + d * et + (rat(1, 10) + c) * ez,
        (rat(2, 25) + b + 2 * e * sp_) * er + d * et
        + (rat(1, 10) + c + 2 * e * cp) * ez,
    ]
    prefix_xyz = [
        (sp.eye(3)[:, 0], sp.eye(3)[:, 1], ez),
        (er, -ez, et),
        (s1 * er + c1 * ez, c1 * er - s1 * ez, et),
        (cp * er - sp_ * ez, et, z3),
    ]
    for k in range(4):
        check("prefix_spatial_columns", frames[k][:3, :],
              sp.Matrix.hstack(*prefix_xyz[k], expected_origins[k]))
    check("slot4_translation", origins[4] - origins[3], 2 * e * axes[3])
    for k in range(5):
        check("origins", origins[k], expected_origins[k])
    for k, z in enumerate([ez, et, et, z3]):
        check("axes", axes[k], z)
    com = (origins[3] + origins[4]) / 2
    check("com", com, a * er + d * et + (rat(1, 10) + p) * ez)
    for j, r in enumerate([
        a * er + d * et + (rat(1, 10) + p) * ez,
        q * er + d * et + p * ez, d * et + e * z3, e * z3,
    ]):
        check("displacements", com - origins[j], r)
    zero = sp.zeros(3, 1)
    jv = sp.Matrix.hstack(*[axes[j].cross(com - origins[j]) for j in range(4)], zero, zero)
    jw = sp.Matrix.hstack(*axes, zero, zero)
    check("Jv", jv, sp.Matrix.hstack(a * et - d * er, p * er - q * ez,
                                    e * (cp * er - sp_ * ez), zero, zero, zero))
    check("Jw", jw, sp.Matrix.hstack(ez, et, et, z3, zero, zero))
    gv, gw = sp.zeros(6), sp.zeros(6)
    gv[0, 0], gv[1, 1], gv[2, 2] = a**2 + d**2, p**2 + q**2, e**2
    gv[0, 1] = gv[1, 0] = -d * p
    gv[0, 2] = gv[2, 0] = -d * e * cp
    gv[1, 2] = gv[2, 1] = e * (p * cp + q * sp_)
    for i, j in [(0, 0), (1, 1), (1, 2), (2, 1), (2, 2), (3, 3)]:
        gw[i, j] = 1
    gw[0, 3] = gw[3, 0] = cp
    check("linear_Gram", jv.T * jv, gv)
    check("angular_Gram", jw.T * jw, gw)
    target = sp.zeros(6)
    target[0, 0] = (
        rat(48511, 600000) + rat(42, 3125) * s1 + rat(19, 3125) * sp_
        - rat(441, 50000) * (c1**2 - s1**2) + rat(399, 50000) * c2
        - rat(399, 50000) * ((c1**2 - s1**2) * c2 - 2 * s1 * c1 * s2)
        - rat(361, 200000) * (cp**2 - sp_**2)
    )
    target[0, 1] = target[1, 0] = -rat(19, 10000) * cp - rat(21, 5000) * c1
    target[0, 2] = target[2, 0] = -rat(19, 10000) * cp
    target[0, 3] = target[3, 0] = rat(1, 15) * cp
    target[1, 1] = rat(211, 2400) + rat(399, 25000) * c2
    target[1, 2] = target[2, 1] = rat(21083, 300000) + rat(399, 50000) * c2
    target[2, 2], target[3, 3] = rat(21083, 300000), rat(1, 15)
    check("weighted_Gram_to_piecewise", rat(2, 5) * gv + rat(1, 15) * gw, target)
    check("direct_source_mass_to_piecewise", rat(2, 5) * jv.T * jv + rat(1, 15) * jw.T * jw, target)
    print(json.dumps({
        "status": "EXACT_POLYNOMIAL_IDENTITIES_CHECKED_NOT_A_LEAN_PROOF",
        "sympy_version": sp.__version__, "scalar_identity_counts": counts,
        "scalar_identity_count": sum(counts.values()),
        "arithmetic": "QQ polynomial remainders modulo four unit-circle equations",
        "lean_parsed_or_compiled": False, "lean_lake_run": False,
        "source_binding_proven": False, "formal_certificate_allowed": False,
    }, indent=2))


if __name__ == "__main__":
    main()
