"""Exact storage obstruction and shifted coercivity; standard library only.

Run with python -B. Reads existing Fourier coefficients and actual Kp; writes
only storage_results.json beside this script. No target modules are executed.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
from fractions import Fraction as Q
from pathlib import Path

HERE = Path(__file__).resolve().parent
DEFAULT = HERE.parents[2] / "6dof_sos_optimized/6dof_sos_optimized/routeB_dense_Mq"


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def quadratic(matrix, vector):
    return sum(matrix[i][j]*vector[i]*vector[j]
               for i in range(len(vector)) for j in range(len(vector)))


def ldl(matrix):
    n = len(matrix)
    lower = [[Q(i == j) for j in range(n)] for i in range(n)]
    pivots = []
    for i in range(n):
        d = matrix[i][i] - sum(lower[i][k]**2*pivots[k] for k in range(i))
        assert d != 0, "zero pivot: this fixed-order LDL needs a different pivot"
        pivots.append(d)
        for j in range(i+1, n):
            lower[j][i] = (matrix[j][i] - sum(lower[j][k]*lower[i][k]*pivots[k]
                                            for k in range(i)))/d
    assert all(matrix[i][j] == sum(lower[i][k]*pivots[k]*lower[j][k]
                                  for k in range(n))
               for i in range(n) for j in range(n))
    return dict(L=lower, pivots=pivots,
                inertia=dict(positive=sum(d > 0 for d in pivots),
                             negative=sum(d < 0 for d in pivots), zero=0))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, default=DEFAULT)
    args = parser.parse_args()
    source = args.source.resolve()
    potential_file = source / "routeB_fourier_potential_rational.csv"
    controller_file = source / "dhport_lib.jl"
    preserved = {str(p): sha(p) for p in HERE.iterdir()
                 if p.is_file() and not p.name.startswith("storage_")}
    inputs = {str(p): sha(p) for p in (potential_file, controller_file)}
    with potential_file.open(encoding="utf-8", newline="") as fh:
        rows = list(csv.DictReader(fh))
    coeff = {}
    for row in rows:
        nu = tuple(int(row[f"nu{i}"]) for i in range(1, 7))
        assert nu not in coeff
        assert Q(int(row["imag_num"]), int(row["imag_den"])) == 0
        coeff[nu] = Q(int(row["real_num"]), int(row["real_den"]))
    assert all(coeff.get(tuple(-x for x in nu)) == a for nu,a in coeff.items())
    controller = controller_file.read_text(encoding="utf-8")
    match = re.search(r"\bKp\s*=\s*\[([^\]]+)\]", controller)
    assert match
    kp = [Q(x.strip()) for x in match[1].split(",")]
    assert kp == list(map(Q, ("1", "4/5", "7/10", "3/5", "1/2", "2/5")))
    zero = (0,)*6
    nonzero = {nu:a for nu,a in coeff.items() if nu != zero}
    positive = {nu:a for nu,a in nonzero.items() if a > 0}
    # Each conjugate row is included once, with its original coefficient.
    positive_moment = [[sum(a*nu[i]*nu[j] for nu,a in positive.items())
                        for j in range(6)] for i in range(6)]
    signed_moment = [[sum(a*nu[i]*nu[j] for nu,a in nonzero.items())
                      for j in range(6)] for i in range(6)]
    H = [[(kp[i] if i == j else 0)-positive_moment[i][j]
          for j in range(6)] for i in range(6)]
    J = [[(kp[i] if i == j else 0)-signed_moment[i][j]
          for j in range(6)] for i in range(6)]
    h_ldl, j_ldl = ldl(H), ldl(J)
    e2 = [Q(i == 1) for i in range(6)]
    assert quadratic(H,e2) < 0 and quadratic(J,e2) < 0
    assert J[0][0] > 0  # Together with e2, a direct indefiniteness witness.
    # Along q=t e2, every nonconstant frequency has |nu_2|=1.
    assert all(abs(nu[1]) == 1 for nu in nonzero)
    A = sum(nonzero.values())
    assert A > 0 and J[1][1] == kp[1]-A
    # cos(t)-1 <= -t^2/2+t^4/24; hence for |t|<=1:
    local_negative_coefficient = kp[1]/2-Q(11,24)*A
    assert local_negative_coefficient < 0
    t = Q(1,10)
    witness_upper = (kp[1]-A)*t*t/2+A*t**4/24
    assert witness_upper < 0
    # Bounded trigonometric potential plus actual positive proportional gains.
    B = 2*sum(positive.values())
    q_coercivity = min(kp)/2
    assert q_coercivity == Q(1,5)
    # The q4,q5 slice is only a restricted configuration statement.
    slice_H = [[H[i][j] for j in (3,4)] for i in (3,4)]
    slice_mu = Q(2,5)
    slice_shift = [[slice_H[i][j]-(slice_mu if i==j else 0)
                    for j in range(2)] for i in range(2)]
    slice_ldl = ldl(slice_shift)
    assert all(d > 0 for d in slice_ldl["pivots"])
    mass_kinetic = Q(9401,2000000)  # Previously checked exact mass premise.
    p45_factor = max(Q(3,2)/q_coercivity, Q(4,5)/mass_kinetic)
    result = dict(status="EXACT_HESSIAN_NEGATIVE_STORAGE_OBSTRUCTION",
                  model="exact rational Fourier DH; no Float64 enclosure",
                  Kp=kp, potential_terms=len(coeff), positive_nonzero_rows=len(positive),
                  negative_nonzero_rows=sum(a < 0 for a in nonzero.values()),
                  conjugate_accounting="all original rows once; no extra factor of two",
                  U0=sum(coeff.values()), positive_frequency_moment=positive_moment,
                  signed_frequency_moment=signed_moment,
                  global_lower_matrix_H=H, H_LDL=h_ldl,
                  actual_Hessian_at_zero=J, Hessian_LDL=j_ldl,
                  witness=dict(direction=e2,H_quadratic=quadratic(H,e2),
                               Hessian_quadratic=quadratic(J,e2),
                               exact_slice="W(t e2)=A*(cos(t)-1)+(2/5)*t^2",
                               A=A, negative_coefficient_on_abs_t_le_1=local_negative_coefficient,
                               t=t, W_at_t_upper=witness_upper),
                  W_globally_nonnegative=False,
                  W_positive_quadratic_lower_bound=False,
                  W_coercive_at_infinity=True,
                  shifted_coercivity=dict(B=B,q_norm_squared_coefficient=q_coercivity,
                                         inequality="W(q)+B >= ||q||^2/5",
                                         kinetic_lower_premise=mass_kinetic,
                                         full_energy="E=kinetic+W",
                                         energy_cap_to_fd_cap="E<=Ecap implies Vcap=Ecap+B",
                                         p45_factor=p45_factor,
                                         p45_bound="p45 <= p45_factor*(E+B)"),
                  restricted_q45_slice=dict(H=slice_H,mu=slice_mu,
                                            shifted_LDL=slice_ldl,
                                            W_lower="W >= (q4^2+q5^2)/5 when q1=q2=q3=q6=0",
                                            invariance_proved=False),
                  input_sha256=inputs,preserved_output_sha256=preserved)
    (HERE/"storage_results.json").write_text(json.dumps(result,default=str,indent=2)+"\n",
                                             encoding="utf-8")
    assert all(sha(Path(p)) == h for p,h in {**inputs, **preserved}.items())
    for name,matrix in (("H",H),("Hessian",J)):
        print(name)
        for row in matrix:
            print(" ", " ".join(map(str,row)))
    print("H LDL:", [str(d) for d in h_ldl["pivots"]],h_ldl["inertia"])
    print("Hessian LDL:", [str(d) for d in j_ldl["pivots"]],j_ldl["inertia"])
    print("A=",A,"H_e2=",H[1][1],"Hessian_e2=",J[1][1])
    print("W(te2)<=",local_negative_coefficient,"*t^2 for |t|<=1")
    print("W(e2/10)<=",witness_upper)
    print("shift B=",B,"q coercivity=",q_coercivity,"p45 factor=",p45_factor)
    print("slice LDL:", [str(d) for d in slice_ldl["pivots"]])
    print("Source and existing outputs unchanged; exact checks passed.")


if __name__ == "__main__":
    main()
