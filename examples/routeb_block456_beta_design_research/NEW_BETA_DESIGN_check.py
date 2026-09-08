"""Bounded exact beta-design research, stdout only; NOT source/Lean verification.

Reuses the nominal metric to evaluate a NONZERO q6 / zero-acceleration ray.
Does not recompute the supplied origin inertia/definiteness audit, run Julia,
solve an SDP, scan partitions, or mutate source/state/registry.
"""

from __future__ import annotations

import argparse
import csv
from fractions import Fraction as F
import hashlib
import io
import json
from pathlib import Path
import sys

sys.dont_write_bytecode = True
DEFAULT_SOURCE = Path(
    "C:/Users/z5242/Desktop/重构版/6dof_sos_optimized/6dof_sos_optimized/routeB_dense_Mq"
)
FILES = (
    "routeB_analytic_mass_full_cs_polynomial.csv",
    "routeB_factorized_descriptor_model.jl",
    "routeB_compact_block456_descriptor_structure_audit.jl",
    "routeB_compact_block456_residual_schur_interface_audit.jl",
    "routeB_compact_block456_fd_stacked_pmi_structure_audit.jl",
    "routeB_compact_block456_stacked_pmi_schur_reduction_audit.jl",
    "routeB_compact_block456_manual_sparse_gram_probe.jl",
)


def need(ok, message):
    if not ok:
        raise ValueError(message)


def inverse(a):
    n = len(a)
    out = [list(row) + [F(i == j) for j in range(n)] for i, row in enumerate(a)]
    for i in range(n):
        p = next((j for j in range(i, n) if out[j][i]), None)
        need(p is not None, "singular metric")
        out[i], out[p] = out[p], out[i]
        pivot = out[i][i]
        out[i] = [v / pivot for v in out[i]]
        for j in range(n):
            if j != i:
                scale = out[j][i]
                out[j] = [x - scale * y for x, y in zip(out[j], out[i])]
    return [row[n:] for row in out]


def run(root):
    raw = {name: (root / name).read_bytes() for name in FILES}
    source = {name: data.decode("utf-8") for name, data in raw.items()}
    snippets = {
        FILES[1]: ["Kp = Q[1, Q(4, 5), Q(7, 10), Q(3, 5), Q(1, 2), Q(2, 5)]"],
        FILES[2]: ["const MU456 = Q(1, 1_000_000)",
                   "MGL_C456 = Q[Q(3, 20), Q(2, 25), Q(3, 100)]",
                   "-(Kp[6] + MGL_C456[3]) / IVAL[6] * q[6]"],
        FILES[3]: ["Q(1, 100) * sum(aC456[i]^2", "Q(1, 10) * sum(q[CIDX456[i]]^2",
                   "Q(1, 20) * w^2", "direct_total456 = betaC456 - direct_total_quad456"],
        FILES[4]: ["const SRES = Q(5)", "SRES * sum(lpoly[i]^2 for i in 1:3) - SRES * beta_poly"],
        FILES[5]: ["SRES * beta_poly", "sum(h_eff[i]^2 / Q(22) for i in 1:3)"],
    }
    for name, tokens in snippets.items():
        for token in tokens:
            need(token in source[name], "reviewed source pattern changed: " + name)

    # Rational coefficient table, not the rounded routeB_Mq_M0.csv.
    m = [[F(0) for _ in range(3)] for _ in range(3)]
    for row in csv.DictReader(io.StringIO(source[FILES[0]])):
        i, j = int(row["row"]) - 4, int(row["col"]) - 4
        if 0 <= i < 3 and 0 <= j < 3:
            need(all(int(row[f"e{k}"]) == 0 for k in (1, 2, 11, 12)),
                 "unexpected q1/q6 mass dependence")
            if all(int(row[f"e{k}"]) == 0 for k in (2, 4, 6, 8, 10, 12)):
                m[i][j] += F(int(row["num"]), int(row["den"]))
    for i in range(3):
        m[i][i] += F(1, 1000000)
    w = inverse(m)
    need(all(sum(m[i][k] * w[k][j] for k in range(3)) == int(i == j)
             for i in range(3) for j in range(3)), "metric inverse identity")
    need(w[2][2] == F(350003000000, 5000400003), "nominal W66 changed")

    beta0, beta1, sres, beta_x, stiffness = F(1, 100), F(3, 25), F(5), F(1, 10), F(43, 100)
    delta = beta1 - beta0
    lower_x = stiffness**2 * w[2][2]
    upper_x = stiffness**2
    ray = beta_x - lower_x
    need(ray == -F(642155146997, 50004000030) and ray < 0, "q6 direct-ray obstruction")
    need(lower_x > upper_x, "direct/Dbase beta_x interval should be empty on this ray")
    need(sres * delta == F(11, 20), "beta migration charge")
    # For a free coefficient A=||a_C||^2, these exact changes have opposite signs.
    need(delta > 0 and -sres * delta < 0, "beta sign orientation")
    # S-lemma common-mode completion is independent of beta; its change is identical.
    need(-sres * delta == -F(11, 20), "stacked scalar migration")
    need(beta0 * 0 + ray == beta1 * 0 + ray, "beta cannot repair a=0 ray")

    # In-memory negative controls, with no solver or new origin test.
    controls = []
    for label, false_claim in (
        ("beta_alone_repairs_zero_acceleration_ray", ray >= 0),
        ("Dbase_improves_with_beta", -sres * delta > 0),
        ("Euclidean_and_nominal_metrics_identical", w[2][2] == 1),
        ("beta_x_intervals_overlap_on_ray", lower_x <= upper_x),
    ):
        need(not false_claim, "negative control unexpectedly passed: " + label)
        controls.append(label)

    need(all((root / name).read_bytes() == raw[name] for name in FILES), "input changed during check")
    return {
        "result": "pass", "evidence": "bounded rational research only",
        "delta_beta_a": str(delta), "direct_target_delta_coefficient": str(delta),
        "Dbase_delta_coefficient": str(-sres * delta),
        "stacked_Schur_delta_coefficient": str(-sres * delta),
        "W66": str(w[2][2]), "q6_ray_target_coefficient": str(ray),
        "q6_one_thousandth_target": str(ray / 1000000),
        "q6_ray_Dbase_coefficient_at_current_beta_x": str(sres * (upper_x - beta_x)),
        "q6_ray_necessary_beta_x_lower_direct": str(lower_x),
        "q6_ray_necessary_beta_x_upper_Euclidean_Dbase": str(upper_x),
        "negative_controls_rejected": controls,
        "source_sha256": {name: hashlib.sha256(data).hexdigest() for name, data in raw.items()},
        "origin_definiteness_audit_repeated": False,
        "all_descriptor_rows_machine_reified": False,
        "physical_acceleration_graph_bound": False,
        "kernel_verified": False, "registry_eligible": False, "closure": False,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-root", type=Path, default=DEFAULT_SOURCE)
    parser.add_argument("--self-test", action="store_true", required=True)
    args = parser.parse_args()
    try:
        output = run(args.source_root)
    except (OSError, ValueError, KeyError, StopIteration) as exc:
        print(json.dumps({"result": "rejected_or_uncheckable", "reason": str(exc),
                          "registry_eligible": False, "closure": False}, indent=2))
        return 1
    print(json.dumps(output, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
