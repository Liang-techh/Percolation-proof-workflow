"""Read-only source audit; exact rational FD force budget. Standard library only.

Run: python -B examples/routeb_fd_force_budget/recompute.py [--source PATH]
Only this script's own directory receives generated artifacts. No source main()
is invoked, and bytecode writes are disabled before loading the Fourier builder.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import runpy
import sys
from fractions import Fraction as Q
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
DEFAULT = HERE.parents[2] / "6dof_sos_optimized/6dof_sos_optimized/routeB_dense_Mq"
H = Q(1, 100000)
D = list(map(Q, ("13/10", "11/10", "19/20", "4/5", "13/20", "1/2")))
G = list(map(Q, ("1", "1/2", "3/10", "1/5", "1/10", "1/20")))


def rows(path):
    with path.open(encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


def polynomial(records):
    out = {}
    for row in records:
        nu = tuple(int(row[f"nu{k}"]) for k in range(1, 7))
        assert nu not in out, ("duplicate Fourier frequency", nu)
        out[nu] = (Q(int(row["real_num"]), int(row["real_den"])),
                   Q(int(row["imag_num"]), int(row["imag_den"])))
    return out


def derivative_bound(poly, k):
    return sum(((abs(ar) + abs(ai)) * abs(nu[k])**3 * H**2 / 6
                for nu, (ar, ai) in poly.items()), Q(0))


def verify_real(poly):
    for nu, (ar, ai) in poly.items():
        assert poly.get(tuple(-n for n in nu)) == (ar, -ai)


def weighted_poly(slopes, beta):
    # R(x) = r2*x^2 + r1*x + r0, given |e_i| <= slopes_i*x+beta_i.
    return dict(r2=sum(a*a/(2*d) for a, d in zip(slopes, D)),
                r1=sum(a*b/d for a, b, d in zip(slopes, beta, D)),
                r0=sum(b*b/(2*d) for b, d in zip(beta, D)))


def at(poly, x):
    return poly["r2"]*x*x + poly["r1"]*x + poly["r0"]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, default=DEFAULT)
    args = parser.parse_args()
    source = args.source.resolve()
    mass_file = source / "routeB_fourier_mass_full_rational.csv"
    potential_file = source / "routeB_fourier_potential_rational.csv"
    mr = rows(mass_file)
    mass = [[polynomial([r for r in mr if int(r["row"]) == i+1 and
                        int(r["col"]) == j+1]) for j in range(6)] for i in range(6)]
    potential = polynomial(rows(potential_file))
    assert all(1 <= int(r["row"]) <= 6 and 1 <= int(r["col"]) <= 6 for r in mr)
    for i in range(6):
        for j in range(6):
            verify_real(mass[i][j])
            assert mass[i][j] == mass[j][i]
    verify_real(potential)
    # Pure-real conjugate pairs make U(-q)=U(q), hence G_an(0)=G_fd(0)=0.
    assert all(ai == 0 for ar, ai in potential.values())

    # Re-evaluate only the small exact constructor; no target script main/writes.
    builder_path = source / "routeB_fourier_rational_probe.py"
    builder = runpy.run_path(str(builder_path), run_name="fd_budget_source")
    built_mass, built_potential = builder["build"]()
    unpack = lambda p: {nu: (a.r, a.i) for nu, a in p.items()}
    assert unpack(built_potential) == potential
    assert all(unpack(built_mass[i][j]) == mass[i][j]
               for i in range(6) for j in range(6))

    # Check the actual controller decimal vectors as intended exact-real values.
    controller = (source / "dhport_lib.jl").read_text(encoding="utf-8")
    def vector(name):
        match = re.search(r"\b" + name + r"\s*=\s*\[([^\]]+)\]", controller)
        assert match, name
        return [Q(x.strip()) for x in match[1].split(",")]
    assert [a+b for a,b in zip(vector("Kd"), vector("b_fr"))] == D
    assert vector("gw_coef") == G  # numerator of ./ I_val, then .* I_val
    assert vector("m") == builder["MASS"] and vector("I_val") == builder["IVAL"]
    assert "const CG_FINITE_DIFF_STEP = 1e-5" in controller
    assert "const MASS_REGULARIZER = 1e-6" in controller
    gamma = sum(g*g/(2*d) for g,d in zip(G,D))
    assert gamma == Q(631227, 1086800)

    dm = [[[derivative_bound(mass[i][j], k) for k in range(6)]
           for j in range(6)] for i in range(6)]
    beta = [derivative_bound(potential, k) for k in range(6)]
    expected = {("mass_derivative", i+1,j+1,k+1): dm[i][j][k]
                for i in range(6) for j in range(6) for k in range(6)}
    expected.update({("gravity_derivative", i+1,0,i+1): beta[i] for i in range(6)})
    ledger_path = source / "routeB_fourier_fd_error_bounds.csv"
    ledger = rows(ledger_path)
    recorded = {(r["kind"], int(r["row"]), int(r["col"]), int(r["coordinate"])):
                Q(int(r["num"]), int(r["den"])) for r in ledger}
    assert len(ledger) == len(recorded) == 222 and recorded == expected
    tensor = [[[(dm[i][j][k]+dm[i][k][j]+dm[j][k][i])/2
                for k in range(6)] for j in range(6)] for i in range(6)]
    assert all(tensor[i][j][k] == tensor[i][k][j]
               for i in range(6) for j in range(6) for k in range(6))
    alpha = [sum(sum(row) for row in matrix) for matrix in tensor]
    bnorm = [max(sum(row) for row in matrix) for matrix in tensor]
    old_path = source / "routeB_compact_fd_remainder_energy_audit.csv"
    old = {r["metric"]: r["value"] for r in rows(old_path)}
    assert sum(alpha) == Q(old["mass_derivative_christoffel_sum"])
    assert sum(b*b/d for b,d in zip(beta,D)) == Q(old["gravity_error_dinv_energy"])

    # Small exact LDL check of the structural prefix bound (not a solver run).
    weights = [x/3 for x in builder["IVAL"]]
    mu = Q(47, 5000)
    gram = [[sum(weights[max(i,j):])-(mu if i==j else 0)
             for j in range(6)] for i in range(6)]
    L = [[Q(i==j) for j in range(6)] for i in range(6)]
    pivots = []
    for i in range(6):
        p = gram[i][i]-sum(L[i][k]**2*pivots[k] for k in range(i))
        assert p > 0
        pivots.append(p)
        for j in range(i+1,6):
            L[j][i] = (gram[j][i]-sum(L[j][k]*L[i][k]*pivots[k]
                                    for k in range(i)))/p
    kinetic_lower = (mu+Q(1,1000000))/2
    assert kinetic_lower == Q(9401,2000000)
    energy_slopes = [b/kinetic_lower for b in bnorm]
    pbox = weighted_poly(alpha, beta)  # x=r^2
    pnorm = weighted_poly(bnorm, beta)  # x=||v||^2 cap
    penergy = weighted_poly(energy_slopes, beta)  # x=Vcap
    pround = dict(r2=Q(3103,10**21), r1=Q(152,10**21), r0=Q(4,10**21))
    assert all(penergy[k] <= pround[k] for k in penergy)
    cases = {"Vcap_0": at(penergy,Q(0)), "Vcap_1": at(penergy,Q(1)),
             "Vcap_2": at(penergy,Q(2)), "all_six_component_cap_15": at(pbox,Q(225)),
             "all_six_component_cap_2_conditional": at(pbox,Q(4)),
             "all_six_component_cap_8_over_3_conditional": at(pbox,Q(64,9))}
    inputs = [mass_file,potential_file,builder_path,ledger_path,old_path,
              source/"routeB_analytic_fourier_dynamics_probe.py",
              source/"routeB_compact_fd_remainder_energy_audit.py",
              source/"routeB_compact_rotational_mass_lower_certificate.py",
              source/"dhport_lib.jl"]
    result = dict(status="EXACT_RATIONAL_CONDITIONAL_FD_FORCE_BUDGET",
                  source=str(source), formal_certificate_allowed=False,
                  float64_error_enclosed=False, h=H, damping=D, disturbance=G,
                  supply_coefficient=gamma, all_222_ledger_rows_equal=True,
                  exact_constructor_matches_csv=True,
                  exact_reference_gravity_zero=True, mass_fourier_terms=len(mr),
                  potential_fourier_terms=len(potential), alpha=alpha,beta=beta,
                  norm_coefficients=bnorm, energy_force_slopes=energy_slopes,
                  christoffel_sum=sum(alpha), kinetic_lower=kinetic_lower,
                  prefix_ldl_pivots=pivots, R_box_in_r_squared=pbox,
                  R_norm_in_velocity_norm_squared=pnorm, R_energy_in_Vcap=penergy,
                  R_energy_rational_upper=pround,
                  cases=cases, sha256={p.name:hashlib.sha256(p.read_bytes()).hexdigest()
                                      for p in inputs})
    (HERE/"results.json").write_text(json.dumps(result,default=str,indent=2)+"\n",encoding="utf-8")
    with (HERE/"component_bounds.csv").open("w",newline="",encoding="utf-8") as fh:
        w=csv.writer(fh)
        w.writerow(["component","D","G","alpha_box","beta_gravity","b_norm","a_energy"])
        w.writerows((i+1,D[i],G[i],alpha[i],beta[i],bnorm[i],energy_slopes[i]) for i in range(6))
    with (HERE/"christoffel_bounds.csv").open("w",newline="",encoding="utf-8") as fh:
        w=csv.writer(fh)
        w.writerow(["i","j","k","bound"])
        w.writerows((i+1,j+1,k+1,tensor[i][j][k])
                    for i in range(6) for j in range(6) for k in range(6))
    print("222 exact ledger rows and source constructor agree; prefix LDL positive.")
    for i in range(6):
        print(f"i={i+1}: alpha={alpha[i]}, beta={beta[i]}, b={bnorm[i]}, a={energy_slopes[i]}")
    print("R(Vcap) coefficients:", {k:str(v) for k,v in penergy.items()})
    print("R(Vcap) decimal display:", {k:float(v) for k,v in penergy.items()})
    for name,value in cases.items():
        print(name, str(value), f"(~{float(value):.12e})")


if __name__ == "__main__":
    main()
