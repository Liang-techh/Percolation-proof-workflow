"""Small numerical adversarial-direction screen; never certificate evidence.

Linearization coefficients come from exact Fourier M(0) and Hessian U(0).
Matrix exponentials, eigensolvers and the maximizing direction are Float64.
The original nonlinear Julia-FD RHS must separately evaluate the candidate.
"""
import csv
from fractions import Fraction as Q
import hashlib
import json
from pathlib import Path

import numpy as np
from scipy.linalg import expm
from scipy.optimize import brentq

HERE = Path(__file__).resolve().parent
SOURCE = HERE.parents[2] / "6dof_sos_optimized/6dof_sos_optimized/routeB_dense_Mq"


def main():
    paths = [SOURCE / "routeB_fourier_mass_full_rational.csv",
             SOURCE / "routeB_fourier_potential_rational.csv", SOURCE / "dhport_lib.jl"]
    hashes = {str(p): hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}
    mass = [[Q(0) for _ in range(6)] for _ in range(6)]
    mass_imag = [[Q(0) for _ in range(6)] for _ in range(6)]
    with paths[0].open(encoding="utf-8", newline="") as fh:
        for row in csv.DictReader(fh):
            i, j = int(row["row"]) - 1, int(row["col"]) - 1
            mass[i][j] += Q(int(row["real_num"]), int(row["real_den"]))
            mass_imag[i][j] += Q(int(row["imag_num"]), int(row["imag_den"]))
    assert all(x == 0 for row in mass_imag for x in row)
    # CSV constructor returns the unregularized mass (probe.py build return).
    # dhport_lib.jl mass_matrix adds MASS_REGULARIZER=1e-6 to every diagonal.
    for i in range(6):
        mass[i][i] += Q(1, 1000000)
    assert mass[3][3] == Q(350003, 3000000) and mass[4][4] == Q(200739, 4000000)
    hess = [[Q(0) for _ in range(6)] for _ in range(6)]
    with paths[1].open(encoding="utf-8", newline="") as fh:
        for row in csv.DictReader(fh):
            nu = [int(row[f"nu{i}"]) for i in range(1, 7)]
            a = Q(int(row["real_num"]), int(row["real_den"]))
            for i in range(6):
                for j in range(6):
                    hess[i][j] -= a * nu[i] * nu[j]
    M = np.array(mass, dtype=float)
    kp = np.array([1, .8, .7, .6, .5, .4])
    damp = np.array([1.3, 1.1, .95, .8, .65, .5])
    inp = np.array([1, .5, .3, .2, .1, .05])
    A = np.block([[np.zeros((6, 6)), np.eye(6)],
                  [-np.linalg.solve(M, np.diag(kp) + np.array(hess, dtype=float)),
                   -np.linalg.solve(M, np.diag(damp))]])
    b = np.r_[np.zeros(6), np.linalg.solve(M, inp)]
    # Augmented coordinates (x[12],w,c), with w'=c and c'=0.
    aug = np.zeros((14, 14)); aug[:12, :12] = A; aug[:12, 12] = b; aug[12, 13] = 1
    out = np.zeros((2, 14))
    for axis, j in enumerate((3, 4)):
        out[axis] = M[j, j] * aug[6+j]
        out[axis, j] += kp[j]; out[axis, 6+j] += damp[j]; out[axis, 12] -= inp[j]
    cost = out.T @ np.diag([5/8, 10/13]) @ out
    # Positive quadrature avoids the exponentially growing inverse transition
    # in a Van Loan block exponential for fast stable modes. Still un-enclosed.
    nodes, weights = np.polynomial.legendre.leggauss(96)
    gram = np.zeros((14,14))
    for node, weight in zip(nodes, weights):
        transition = expm(aug*((node+1)/2))
        gram += weight/2 * (transition.T @ cost @ transition)
    asymmetry = float(np.max(np.abs(gram-gram.T)))
    gram = (gram + gram.T)/2
    idx = list(range(12))+[13]
    reduced = gram[np.ix_(idx,idx)]
    P, f = reduced[:12,:12], reduced[:12,12]*1.7
    vals, vecs = np.linalg.eigh(P)
    v = vecs.T @ f
    radius = .149
    def secular(mu):
        return np.sum((v/(mu-vals))**2)-radius**2
    lo = vals[-1] + max(1e-12, abs(vals[-1])*1e-12)
    hi = max(lo+1, 2*lo)
    while secular(hi)>0:
        hi *= 2
    mu = brentq(secular,lo,hi,xtol=1e-14)
    x = vecs @ (v/(mu-vals))
    x *= radius/np.linalg.norm(x)
    assert np.dot(x,x)<.15**2 and 1.7**2<3
    z = np.r_[x,1.7]
    # Loose finite-dimensional upper screen for the ENTIRE original initial
    # ball and ramp interval, but not a rigorous inequality due to rounding.
    screen_upper = vals[-1]*.15**2 + 2*np.sqrt(3)*.15*np.linalg.norm(reduced[:12,12]) + 3*reduced[12,12]
    result = dict(evidence="E1_LINEARIZED_FLOAT64_SCREEN_ONLY", original_nonlinear_budget_proved=False,
        mass_zero=[[str(v) for v in row] for row in mass],
        potential_hessian=[[str(v) for v in row] for row in hess],
        spectral_abscissa=float(max(np.linalg.eigvals(A).real)),
        gram_asymmetry=asymmetry, gram_min_eigenvalue=float(min(np.linalg.eigvalsh(gram))),
        linear_predicted_R=float(z@reduced@z), linear_original_set_upper_screen=float(screen_upper),
        candidate_initial=x.tolist(), candidate_c=1.7, candidate_norm_squared=float(x@x),
        source_sha256=hashes,
        caveat="Exact-real Fourier linearization, not original FD/Float64 Jacobian; matrix exponential and eigenvalues un-enclosed.")
    output=HERE / "linear_output"
    output.mkdir(exist_ok=False)
    (output / "result.json").write_text(json.dumps(result,indent=2)+"\n",encoding="utf-8")
    with (output / "candidate.csv").open("w",newline="",encoding="utf-8") as fh:
        writer=csv.writer(fh)
        writer.writerow([*[f"x{i}" for i in range(1,13)],"c"])
        writer.writerow([*x,1.7])
    assert all(hashlib.sha256(Path(p).read_bytes()).hexdigest()==h for p,h in hashes.items())
    print(json.dumps({k:result[k] for k in ("linear_predicted_R","linear_original_set_upper_screen","spectral_abscissa","gram_asymmetry","candidate_norm_squared")}))


if __name__=="__main__":
    main()
