"""Exact coefficient check for the M33 lower-bound factorization.

This is a pre-Lean algebra sanity check.  It uses rational coefficients only;
it is not a replacement for the scheduled pinned Lean compilation.
"""
from __future__ import annotations

from fractions import Fraction as F


def add(*terms):
    result = {}
    for scale, poly in terms:
        for monomial, value in poly.items():
            result[monomial] = result.get(monomial, F(0)) + scale * value
    return {key: value for key, value in result.items() if value}


def mul(left, right):
    result = {}
    for (u1, x1), a in left.items():
        for (u2, x2), b in right.items():
            key = (u1 + u2, x1 + x2)
            result[key] = result.get(key, F(0)) + a * b
    return {key: value for key, value in result.items() if value}


def main() -> int:
    A = F(12159703, 48000000)
    B = F(399, 200000)
    C = F(147, 3200000)
    lower = F(3016537, 12000000)
    u = {(1, 0): F(1)}
    x = {(0, 1): F(1)}
    const = {(0, 0): F(1)}
    doubled_u_sq_minus_one = add((2, mul(u, u)), (-1, const))
    bracket = add(
        (1, x),
        (1, doubled_u_sq_minus_one),
        (-1, mul(x, doubled_u_sq_minus_one)),
    )
    formula = add(
        (A, const),
        (B, u),
        (C, bracket),
    )
    lhs = add((F(1), formula), (-lower, const))
    inner = add(
        (B, const),
        (-2 * C, mul(add((1, const), (-1, u)),
                     add((1, const), (-1, x)))),
    )
    rhs = mul(add((1, u), (1, const)), inner)
    if lhs != rhs:
        raise SystemExit(f"IDENTITY_FAIL lhs={lhs} rhs={rhs}")
    gap = B - 8 * C
    if gap <= 0 or A - B + C != lower:
        raise SystemExit("RATIONAL_BOUND_FAIL")
    print({"status": "PASS", "identity": True,
           "lower": f"{lower.numerator}/{lower.denominator}",
           "endpoint_gap": f"{gap.numerator}/{gap.denominator}"})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
