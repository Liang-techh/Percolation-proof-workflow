"""Exact Fourier C/G interface and finite-difference remainder bounds.

The authoritative port currently evaluates C and G by central finite
differences.  The DH mass and potential dictionaries are finite Fourier
polynomials, so their derivatives can be formed exactly in Gaussian-rational
arithmetic.  This probe exports analytic C/G coefficients and a rigorous
coefficient-wise O(h^2) enclosure for the finite-difference port.  It is a
parallel mathematical interface only; it does not silently replace
dhport_lib.jl.
"""
from __future__ import annotations

import csv
import random
from fractions import Fraction as Q
from pathlib import Path

import mpmath as mp

from routeB_fourier_rational_probe import G, N, ZERO, add, build, evaluate, scale


HERE = Path(__file__).resolve().parent
FD_H = Q("0.00001")


def derivative(poly, coordinate):
    """Exact derivative with respect to q_coordinate."""
    out = {}
    for key, value in poly.items():
        if key[coordinate]:
            out[key] = value * G(0, Q(key[coordinate]))
    return {key: value for key, value in out.items() if not value.zero()}


def half(poly):
    return scale(poly, Q(1, 2))


def c_entry(M, i, j, k):
    return half(add(derivative(M[i][j], k),
                    derivative(M[i][k], j),
                    scale(derivative(M[j][k], i), -1)))


def write_gaussian(path, header, rows):
    with path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.writer(fh)
        writer.writerow(header)
        writer.writerows(rows)


def derivative_error(poly, coordinate):
    """Exact rational upper bound for central-difference derivative error.

    For each Fourier term a exp(i nu.q),
    |nu-sin(nu*h)/h| <= |nu|^3 h^2/6.  The Gaussian modulus is bounded by
    |Re(a)|+|Im(a)|, keeping the exported bound rational.
    """
    total = Q(0)
    for key, value in poly.items():
        nu = abs(key[coordinate])
        total += (abs(value.r) + abs(value.i)) * Q(nu**3) * FD_H**2 / 6
    return total


def finite_difference_derivative(poly, q, coordinate):
    qp = list(q); qm = list(q)
    qp[coordinate] += float(FD_H)
    qm[coordinate] -= float(FD_H)
    return (evaluate(poly, qp) - evaluate(poly, qm)) / (2 * float(FD_H))


def evaluate_mp(poly, q):
    total = mp.mpc(0)
    for key, value in poly.items():
        coeff = mp.mpc(mp.mpf(value.r.numerator) / value.r.denominator,
                       mp.mpf(value.i.numerator) / value.i.denominator)
        phase = mp.fsum(key[k] * q[k] for k in range(N))
        total += coeff * mp.exp(1j * phase)
    return mp.re(total)


def finite_difference_derivative_mp(poly, q, coordinate):
    qp = list(q); qm = list(q)
    qp[coordinate] += mp.mpf(FD_H.numerator) / FD_H.denominator
    qm[coordinate] -= mp.mpf(FD_H.numerator) / FD_H.denominator
    h = mp.mpf(FD_H.numerator) / FD_H.denominator
    return (evaluate_mp(poly, qp) - evaluate_mp(poly, qm)) / (2 * h)


def main():
    M, potential = build()
    dM = [[[derivative(M[i][j], k) for k in range(N)]
           for j in range(N)] for i in range(N)]
    C = [[[c_entry(M, i, j, k) for k in range(N)]
          for j in range(N)] for i in range(N)]
    Gq = [derivative(potential, k) for k in range(N)]

    # Full exact Fourier data for a future analytic descriptor/SOS port.
    mass_rows = []
    for i in range(N):
        for j in range(N):
            for key, value in sorted(M[i][j].items()):
                mass_rows.append((i + 1, j + 1, *key, value.r.numerator,
                                  value.r.denominator, value.i.numerator,
                                  value.i.denominator))
    write_gaussian(
        HERE / "routeB_fourier_mass_full_rational.csv",
        ["row", "col", *[f"nu{k+1}" for k in range(N)],
         "real_num", "real_den", "imag_num", "imag_den"],
        mass_rows,
    )

    potential_rows = []
    for key, value in sorted(potential.items()):
        potential_rows.append((*key, value.r.numerator, value.r.denominator,
                               value.i.numerator, value.i.denominator))
    write_gaussian(
        HERE / "routeB_fourier_potential_rational.csv",
        [*[f"nu{k+1}" for k in range(N)], "real_num", "real_den",
         "imag_num", "imag_den"],
        potential_rows,
    )

    coriolis_rows = []
    for i in range(N):
        for j in range(N):
            for k in range(N):
                for key, value in sorted(C[i][j][k].items()):
                    coriolis_rows.append((i + 1, j + 1, k + 1, *key,
                                          value.r.numerator, value.r.denominator,
                                          value.i.numerator, value.i.denominator))
    write_gaussian(
        HERE / "routeB_fourier_coriolis_rational.csv",
        ["row", "dq_j", "dq_k", *[f"nu{k+1}" for k in range(N)],
         "real_num", "real_den", "imag_num", "imag_den"],
        coriolis_rows,
    )

    gravity_rows = []
    for i, poly in enumerate(Gq):
        for key, value in sorted(poly.items()):
            gravity_rows.append((i + 1, *key, value.r.numerator,
                                 value.r.denominator, value.i.numerator,
                                 value.i.denominator))
    write_gaussian(
        HERE / "routeB_fourier_gravity_rational.csv",
        ["row", *[f"nu{k+1}" for k in range(N)], "real_num", "real_den",
         "imag_num", "imag_den"],
        gravity_rows,
    )

    error_rows = []
    for i in range(N):
        for j in range(N):
            for k in range(N):
                value = derivative_error(M[i][j], k)
                error_rows.append(("mass_derivative", i + 1, j + 1, k + 1,
                                   value.numerator, value.denominator))
    for i, poly in enumerate([potential] * N):
        value = derivative_error(poly, i)
        error_rows.append(("gravity_derivative", i + 1, 0, i + 1,
                           value.numerator, value.denominator))
    write_gaussian(
        HERE / "routeB_fourier_fd_error_bounds.csv",
        ["kind", "row", "col", "coordinate", "num", "den"],
        error_rows,
    )

    rng = random.Random(20260903)
    max_c_error = 0.0
    max_g_error = 0.0
    max_c_bound = 0.0
    max_g_bound = 0.0
    mp.mp.dps = 80
    for _ in range(20):
        q = [mp.mpf(str(0.4 * (2 * rng.random() - 1))) for _ in range(N)]
        dq = [0.4 * (2 * rng.random() - 1) for _ in range(N)]
        fd_dM = [[[finite_difference_derivative_mp(M[i][j], q, k)
                   for k in range(N)] for j in range(N)] for i in range(N)]
        for i in range(N):
            for j in range(N):
                for k in range(N):
                    coeff = mp.mpf("0.5") * (fd_dM[i][j][k] + fd_dM[i][k][j] - fd_dM[j][k][i])
                    analytic_coeff = evaluate_mp(C[i][j][k], q)
                    max_c_error = max(max_c_error,
                                      float(abs(analytic_coeff - coeff) * abs(dq[j] * dq[k])))
                    e = (float(derivative_error(M[i][j], k)) +
                         float(derivative_error(M[i][k], j)) +
                         float(derivative_error(M[j][k], i))) / 2
                    max_c_bound = max(max_c_bound, e * abs(dq[j] * dq[k]))
        for i in range(N):
            analytic_g = evaluate_mp(Gq[i], q)
            fd_g = finite_difference_derivative_mp(potential, q, i)
            max_g_error = max(max_g_error, float(abs(analytic_g - fd_g)))
            max_g_bound = max(max_g_bound, float(derivative_error(potential, i)))

    report = HERE / "P5_ANALYTIC_FOURIER_DYNAMICS.md"
    with report.open("w", encoding="utf-8") as fh:
        fh.write("# Exact Fourier C/G interface\n\n")
        fh.write("The current DH port uses central finite differences with `h=1e-5` for C/G. The finite Fourier mass and potential dictionaries now yield exact Gaussian-rational derivatives. The exported Fourier mass is the unregularized structural mass; the authoritative port is `M_fourier + 1e-6 I`. Because the regularizer is constant, it cancels from the mass derivatives and therefore does not alter the analytic C interface. This probe exports a parallel analytic interface and does not replace the authoritative finite-difference port.\n\n")
        fh.write("## Outputs\n\n")
        fh.write("- `routeB_fourier_mass_full_rational.csv`: all 6x6 mass entries.\n")
        fh.write("- `routeB_fourier_potential_rational.csv`: exact potential.\n")
        fh.write("- `routeB_fourier_coriolis_rational.csv`: exact Christoffel coefficients multiplying `dq_j*dq_k`.\n")
        fh.write("- `routeB_fourier_gravity_rational.csv`: exact gravity derivatives.\n")
        fh.write("- `routeB_fourier_fd_error_bounds.csv`: rational coefficient-wise finite-difference error bounds.\n\n")
        fh.write("For every Fourier term, the central-difference derivative error is bounded by `|a| |nu_k|^3 h^2/6`; the exported rational bound uses `|Re(a)|+|Im(a)| >= |a|`. Therefore the analytic port can preserve the finite-difference implementation by adding an explicit remainder instead of enclosing a cancellation-prone difference directly.\n\n")
        fh.write(f"- finite-difference step: `{FD_H}`\n")
        fh.write(f"- sampled max C contribution discrepancy: `{max_c_error:.6e}`\n")
        fh.write(f"- sampled max corresponding coefficient bound: `{max_c_bound:.6e}`\n")
        fh.write(f"- sampled max G discrepancy: `{max_g_error:.6e}`\n")
        fh.write(f"- sampled max corresponding coefficient bound: `{max_g_bound:.6e}`\n")
        fh.write("\nEvidence level: exact algebraic Fourier interface plus an analytic finite-difference remainder formula; no global residual, SOS, flowpipe, or theorem-backed Route-B certificate is claimed.\n")

    print("ANALYTIC_FOURIER_DYNAMICS_OK")
    print("mass_terms=", len(mass_rows), "coriolis_terms=", len(coriolis_rows),
          "gravity_terms=", len(gravity_rows))
    print("sampled_C_error=", f"{max_c_error:.3e}",
          "bound=", f"{max_c_bound:.3e}")
    print("sampled_G_error=", f"{max_g_error:.3e}",
          "bound=", f"{max_g_bound:.3e}")


if __name__ == "__main__":
    main()
