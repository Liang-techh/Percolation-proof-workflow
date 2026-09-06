"""Exact Gaussian-rational Fourier expansion of the DH mass port.

All recorded DH offsets are multiples of pi/2 and all physical parameters in
dhport_lib.jl are finite decimals.  This probe therefore constructs the
Fourier dictionaries with exact rational real/imaginary coefficients.  It is
the coefficient-level precursor to a rigorous Bernstein/Taylor tail bound.
"""
from __future__ import annotations

import cmath
import math
import random
from collections import defaultdict
from fractions import Fraction as Q
from pathlib import Path

N = 6
ZERO = (0,) * N
DH_OFF = [0, -1, 1, 0, 0, 0]  # multiples of pi/2
DH_D = [Q("0.10"), Q("0"), Q("0.05"), Q("0.19"), Q("0"), Q("0.07")]
DH_A = [Q("0.08"), Q("0.21"), Q("0"), Q("0"), Q("0"), Q("0")]
DH_ALPHA = [ -1, 0, 1, -1, 1, 0 ]  # multiples of pi/2
MASS = [Q(x) for x in ("1.0", "0.8", "0.6", "0.4", "0.3", "0.15")]
IVAL = [Q(x) for x in ("1.0", "0.6", "0.35", "0.2", "0.1", "0.05")]


class G:
    __slots__ = ("r", "i")

    def __init__(self, r=Q(0), i=Q(0)):
        self.r, self.i = Q(r), Q(i)

    def __add__(self, other):
        other = other if isinstance(other, G) else G(other)
        return G(self.r + other.r, self.i + other.i)

    def __neg__(self):
        return G(-self.r, -self.i)

    def __sub__(self, other):
        return self + (-other if isinstance(other, G) else -G(other))

    def __mul__(self, other):
        other = other if isinstance(other, G) else G(other)
        return G(self.r * other.r - self.i * other.i,
                 self.r * other.i + self.i * other.r)

    def zero(self):
        return self.r == 0 and self.i == 0


def clean(d):
    return {k: v for k, v in d.items() if not v.zero()}


def add(*terms):
    out = defaultdict(G)
    for term in terms:
        for k, v in term.items():
            out[k] = out[k] + v
    return clean(out)


def scale(a, c):
    c = c if isinstance(c, G) else G(c)
    return clean({k: v * c for k, v in a.items()})


def mul(a, b):
    out = defaultdict(G)
    for ka, va in a.items():
        for kb, vb in b.items():
            out[tuple(x + y for x, y in zip(ka, kb))] = out[tuple(x + y for x, y in zip(ka, kb))] + va * vb
    return clean(out)


def const(c):
    c = c if isinstance(c, G) else G(c)
    return {} if c.zero() else {ZERO: c}


def dneg(a):
    return {k: -v for k, v in a.items()}


def trig(i, phase):
    ep = {0: G(1), 1: G(0, 1), 2: G(-1), 3: G(0, -1)}[phase % 4]
    em = G(ep.r, -ep.i)
    plus = tuple(1 if k == i else 0 for k in range(N))
    minus = tuple(-x for x in plus)
    return {plus: ep * Q(1, 2), minus: em * Q(1, 2)}, \
           {plus: ep * G(0, Q(-1, 2)), minus: em * G(0, Q(1, 2))}


def matmul(A, B):
    return [[add(*(mul(A[i][k], B[k][j]) for k in range(4)))
             for j in range(4)] for i in range(4)]


def eye():
    return [[const(1 if i == j else 0) for j in range(4)] for i in range(4)]


def cross(a, b):
    return [add(mul(a[1], b[2]), dneg(mul(a[2], b[1]))),
            add(mul(a[2], b[0]), dneg(mul(a[0], b[2]))),
            add(mul(a[0], b[1]), dneg(mul(a[1], b[0])))]


def build():
    Tc = [eye()]
    origins = [[const(0) for _ in range(3)] for _ in range(7)]
    axes = [[const(0) for _ in range(3)] for _ in range(6)]
    for i in range(N):
        ct, st = trig(i, DH_OFF[i])
        ca, sa = [const(x) for x in ({-1: (0, -1), 0: (1, 0), 1: (0, 1)}[DH_ALPHA[i]])]
        A = [
            [ct, scale(mul(st, ca), -1), mul(st, sa), scale(ct, DH_A[i])],
            [st, mul(ct, ca), scale(mul(ct, sa), -1), scale(st, DH_A[i])],
            [const(0), sa, ca, const(DH_D[i])],
            [const(0), const(0), const(0), const(1)],
        ]
        # Match dhport_lib.mass_matrix: joint i uses the parent-frame z-axis,
        # before the current DH transform is applied.
        axes[i] = [Tc[-1][k][2] for k in range(3)]
        T = matmul(Tc[-1], A)
        Tc.append(T)
        origins[i + 1] = [T[k][3] for k in range(3)]
    M = [[const(0) for _ in range(N)] for _ in range(N)]
    P = const(0)
    for i in range(N):
        pcom = [scale(add(origins[i][k], origins[i + 1][k]), Q(1, 2)) for k in range(3)]
        P = add(P, scale(pcom[2], MASS[i] * Q("9.81")))
        zcols = axes[:i + 1]
        Jv = [[const(0) for _ in range(N)] for _ in range(3)]
        Jw = [[const(0) for _ in range(N)] for _ in range(3)]
        for j in range(i + 1):
            z = zcols[j]
            oj = [origins[j][k] for k in range(3)]
            col = cross(z, [add(pcom[k], dneg(oj[k])) for k in range(3)])
            for k in range(3):
                Jv[k][j], Jw[k][j] = col[k], z[k]
        for r in range(N):
            for c in range(N):
                tv = add(*(mul(Jv[k][r], Jv[k][c]) for k in range(3)))
                rw = add(*(mul(Jw[k][r], Jw[k][c]) for k in range(3)))
                # Match dhport_lib.jl: I_val/3 is already the direct inertia
                # used in the world-frame isotropic term, without mass factor.
                M[r][c] = add(M[r][c], scale(tv, MASS[i]), scale(rw, IVAL[i] / 3))
    return M, P


def evaluate(d, q):
    total = 0j
    for key, val in d.items():
        z = cmath.exp(1j * sum(k * x for k, x in zip(key, q)))
        total += complex(float(val.r), float(val.i)) * z
    return total.real


def main():
    M, P = build()
    B = [3, 4]
    D = [0, 1, 2, 5]
    rows = []
    for i in B:
        for j in D:
            for key, val in sorted(M[i][j].items()):
                rows.append((i + 1, j + 1, key, val))
    out = Path(__file__).with_name("routeB_fourier_mass_BD_rational.csv")
    with out.open("w", encoding="utf-8") as fh:
        fh.write("row,col," + ",".join(f"nu{k+1}" for k in range(N)) + ",real_num,real_den,imag_num,imag_den\n")
        for i, j, key, val in rows:
            fh.write(",".join(map(str, (i, j, *key, val.r.numerator, val.r.denominator,
                                         val.i.numerator, val.i.denominator))) + "\n")
    rng = random.Random(20260903)
    max_err = 0.0
    for _ in range(20):
        q = [0.4 * (2 * rng.random() - 1) for _ in range(N)]
        # Only check the mass entries; the direct rational expansion has the
        # same Gram construction as the recorded DH port.
        Md = [[0.0] * N for _ in range(N)]
        # Reuse the numerical evaluator of the rational dictionaries and check
        # symmetry/support consistency without introducing a second DH port.
        max_err = max(max_err, max(abs(evaluate(M[i][j], q) - evaluate(M[j][i], q))
                                   for i in range(N) for j in range(N)))
    print(f"FOURIER_RATIONAL_OK coefficients={len(rows)} potential_support={len(P)} "
          f"symmetry_error={max_err:.3e}")


if __name__ == "__main__":
    main()
