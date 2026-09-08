"""Construct one exact toy PSD-slack packet; stdout only, no Lean or regression.
All input code hashes are pinned. Output is source-independent-unbound.
"""
import hashlib
import json
from fractions import Fraction as F
from pathlib import Path
import runpy
import sys

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parent
PINS = {
    "check_exact.py": "d887aade11edf9adf1e7f532d8b173a089aac9e2fadba2e25fbc2f169e1e4211",
    "NEW_exact_geometry_spn.py": "263fac727c1c3068043c02a63dade5995a22e1e7e9a879682ac3e69bafd54f42",
}


def need(ok, label):
    if not ok:
        raise ValueError(label)


def load(name):
    need(hashlib.sha256((ROOT / name).read_bytes()).hexdigest() == PINS[name], "input hash " + name)
    return runpy.run_path(str(ROOT / name), run_name="capacity_dependency")


def inverse(a):
    n = len(a)
    b = [list(row) + [F(i == j) for j in range(n)] for i, row in enumerate(a)]
    for j in range(n):
        k = next((k for k in range(j, n) if b[k][j]), None)
        need(k is not None, "singular factor")
        b[j], b[k] = b[k], b[j]
        pivot = b[j][j]
        b[j] = [x / pivot for x in b[j]]
        for i in range(n):
            if i != j:
                q = b[i][j]
                b[i] = [x - q * y for x, y in zip(b[i], b[j])]
    return [row[n:] for row in b]


def main():
    old, geo = load("check_exact.py"), load("NEW_exact_geometry_spn.py")
    mm, tr, add, scale = (old[k] for k in ("mm", "transpose", "add", "scale"))
    mat, encode = old["matrix"], old["encode"]
    baseline = old["toy_fixture"]()
    baseline_result = geo["check_certificate"](baseline)
    k0, mu = mat(baseline["K"], 2, 4), F(baseline["mu"])
    direction = [[F(1)] * 4 for _ in range(2)]
    records, limits = [], []
    for item in baseline["certificates"]:
        c = tuple(item["cone"])
        s, n, r = (mat(item[k]) for k in ("S", "N", "R"))
        d = [F(x) for x in item["d"]]
        ri = inverse(r)
        need(mm(r, ri) == old["identity"]() == mm(ri, r), "factor inverse identity")
        dmin = min(d)
        frob2 = sum(x*x for row in ri for x in row)
        exact_delta = dmin / frob2
        # Rational downward rounding keeps report entries readable.
        delta = F((exact_delta * 1000000).__floor__(), 1000000)
        need(0 < delta <= exact_delta, "positive rational coercivity")
        # A second, direct LDL certificate verifies S - delta I is PSD.
        shifted = add(s, scale(-delta, old["identity"]()))
        rshift, dshift = old["ldlt_positive"](shifted)
        old["validate_spn"](shifted, encode({"S": shifted, "N": old["zero"](), "R": rshift, "d": dshift}))
        chart, sigma, tau = old["cone_data"](c)
        aabs = [[sigma[i] * chart[i][j] for j in range(4)] for i in range(4)]
        lt = mm(old["L"], chart)
        babs = [[tau[i] * lt[i][j] for j in range(4)] for i in range(2)]
        need(all(x >= 0 for m in (aabs, babs) for row in m for x in row), "absolute maps nonnegative")

        def correction(e):
            raw = mm(mm(tr(babs), e), aabs)
            return scale(F(1, 2), add(raw, tr(raw)))

        cd = correction(direction)
        rows = [sum(row, F(0)) for row in cd]
        need(all(x >= 0 for x in rows), "direction row sums")
        limits.extend((delta / v, list(c), i) for i, v in enumerate(rows) if v > 0)
        # Exact 72-by-8 nonnegative coefficients of the capacity polytope.
        coefficients = [[] for _ in range(4)]
        for a in range(2):
            for k in range(4):
                basis = [[F(0)] * 4 for _ in range(2)]
                basis[a][k] = F(1)
                cc = correction(basis)
                for i in range(4):
                    coefficients[i].append(sum(cc[i], F(0)))
        need([sum(v, F(0)) for v in coefficients] == rows, "polytope direction contraction")
        records.append({"cone": list(c), "R_inverse": ri, "d_min": dmin,
                        "inverse_frobenius_squared": frob2, "delta_raw": exact_delta,
                        "delta": delta, "shifted_R": rshift, "shifted_d": dshift,
                        "A_abs": aabs, "B_abs": babs, "correction_direction": cd,
                        "capacity_rows": coefficients, "direction_row_sums": rows})
    cap, active_cone, active_row = min(limits)
    t = F(1)
    while t > cap / 2:
        t /= 10
    need(t > 0, "nonzero ray witness")
    knew = add(k0, scale(t, direction))
    updated = []
    for item, rec in zip(baseline["certificates"], records):
        correction = scale(t, rec["correction_direction"])
        slack = [rec["delta"] - t*v for v in rec["direction_row_sums"]]
        need(min(slack) >= 0, "capacity violation")
        rec["capacity_slack"] = slack
        snew = add(mat(item["S"]), scale(-1, correction))
        rnew, dnew = old["ldlt_positive"](snew)
        _, hnew = old["matrices"](knew, mu, tuple(item["cone"]))
        need(hnew == add(snew, mat(item["N"])), "new gap identity")
        updated.append({"cone": item["cone"], "S": snew, "N": mat(item["N"]), "R": rnew, "d": dnew})
    payload = encode({"schema": baseline["schema"], "scope": baseline["scope"],
                      "mu": mu, "K": knew, "certificates": updated})
    # Two targeted validators only, not self-test/regression suites.
    legacy_result = old["check_certificate"](payload)
    geometry_result = geo["check_certificate"](payload)
    for name, expected in PINS.items():
        need(hashlib.sha256((ROOT / name).read_bytes()).hexdigest() == expected, "input changed")
    result = {"schema": "P5-toy-PSD-capacity-v1", "scope": "source-independent-unbound",
              "input_code_sha256": PINS, "chart_table": old["G"], "sign_table": old["SIGNS"],
              "reverse": old["REVERSE"], "Q_matrix": old["P"], "L": old["L"],
              "gain_slot_order": [[a, k] for a in range(2) for k in range(4)],
              "baseline_certificate": baseline, "capacity_records": records,
              "direction": direction, "t_cap": cap, "active_cone": active_cone,
              "active_row": active_row, "t": t, "updated_certificate": payload,
              "checks": {"baseline_geometry": baseline_result, "updated_legacy": legacy_result,
                         "updated_geometry": geometry_result, "shifted_psd_factors": 18,
                         "capacity_inequalities": 72, "regression_run": False},
              "lean_run": False, "concrete_K_path_bound": False, "registry_eligible": False,
              "source_binding": False, "P5_closed": False}
    print(json.dumps(encode(result), separators=(",", ":"), sort_keys=True))


if __name__ == "__main__":
    main()
