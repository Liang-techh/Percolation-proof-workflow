"""T-P5-026 exact rational sidecar checker. Standard library only, read-only.

This checks rational identities, not Lean proofs or source provenance. A valid
certificate file never binds K_path or enables registry admission. No search,
floating-point eigenvalues, source execution, Lean, or Lake is used.
"""

from __future__ import annotations

import argparse
import copy
from fractions import Fraction as F
import hashlib
import itertools
import json
from pathlib import Path
import re
import sys


ROOT = Path(__file__).resolve().parent
NAMES = ("pp", "nn", "pnPos", "pnNeg", "npPos", "npNeg")
G = (
    ((1, 0), (0, 1)), ((-1, 0), (0, -1)),
    ((1, 1), (-1, 0)), ((1, 0), (-1, -1)),
    ((-1, 0), (1, 1)), ((-1, -1), (1, 0)),
)
SIGNS = ((1, 1, 1), (-1, -1, -1), (1, -1, 1),
         (1, -1, -1), (-1, 1, 1), (-1, 1, -1))
REVERSE = (1, 0, 5, 4, 3, 2)
REPS = tuple(itertools.product((0, 2, 3), range(6)))
L = [[F(x) for x in row] for row in ((1, 0, 1, 0), (0, 1, 0, 1))]
P = [list(map(F, row)) for row in (
    ("3/4", "-3/400", "0", "1/800"),
    ("-3/400", "29/50", "-1/800", "0"),
    ("0", "-1/800", "2049997/3000000", "0"),
    ("1/800", "0", "0", "2399261/4000000"),
)]
BOUNDARY = {
    "lean_status": "not_run",
    "proof_status": "proof_attempt_uncompiled",
    "concrete_K_path_bound": False,
    "source_authentication": "not_checked",
    "registry_eligible": False,
    "registry_mutated": False,
    "P5_P8_M4_closed": False,
}


class InvalidCertificate(ValueError):
    pass


def require(condition, message):
    # Explicit checks remain active under python -O.
    if not condition:
        raise InvalidCertificate(message)


def zero(n=4):
    return [[F(0) for _ in range(n)] for _ in range(n)]


def identity(n=4):
    return [[F(i == j) for j in range(n)] for i in range(n)]


def transpose(a):
    return [list(row) for row in zip(*a)]


def mm(a, b):
    return [[sum((x * y for x, y in zip(row, col)), F(0))
             for col in zip(*b)] for row in a]


def mv(a, v):
    return [sum((x * y for x, y in zip(row, v)), F(0)) for row in a]


def add(a, b):
    return [[x + y for x, y in zip(ar, br)] for ar, br in zip(a, b)]


def scale(s, a):
    return [[s * x for x in row] for row in a]


def quadratic(a, v):
    return sum((x * y for x, y in zip(v, mv(a, v))), F(0))


def congruence(a, t):
    return mm(mm(transpose(t), a), t)


def cone_data(c):
    j4, j5 = c
    t = zero()
    for j, slots in ((j4, (0, 2)), (j5, (1, 3))):
        for p, row in enumerate(slots):
            for q, col in enumerate(slots):
                t[row][col] = F(G[j][p][q])
    sigma = [SIGNS[j4][0], SIGNS[j5][0], SIGNS[j4][1], SIGNS[j5][1]]
    tau = [SIGNS[j4][2], SIGNS[j5][2]]
    return t, sigma, tau


def matrices(k, mu, c):
    t, sigma, tau = cone_data(c)
    a = [[sum((L[h][i] * tau[h] * k[h][j] * sigma[j] for h in range(2)), F(0))
          for j in range(4)] for i in range(4)]
    b = scale(F(1, 2), add(a, transpose(a)))
    h = congruence(add(scale(mu, P), scale(-1, b)), t)
    return b, h


def channel_cover(x, y):
    if x >= 0 and y >= 0:
        return 0, x, y
    if x <= 0 and y <= 0:
        return 1, -x, -y
    if x >= 0:
        return (2, -y, x + y) if x + y >= 0 else (3, x, -(x + y))
    return (4, -x, x + y) if x + y >= 0 else (5, y, -(x + y))


def exact_scalar(value):
    # JSON booleans, floats, exponent/decimal strings, NaN are not rationals
    # in this interface. Fraction strings have nonzero positive denominators.
    if type(value) is int:
        return F(value)
    require(isinstance(value, str) and
            re.fullmatch(r"-?(?:0|[1-9][0-9]*)(?:/[1-9][0-9]*)?", value) is not None,
            "scalar must be an integer or an exact integer/fraction string")
    return F(value)


def matrix(value, rows=4, cols=4):
    require(isinstance(value, list) and len(value) == rows, "wrong matrix row count")
    require(all(isinstance(row, list) and len(row) == cols for row in value),
            "wrong matrix column count")
    return [[exact_scalar(x) for x in row] for row in value]


def keys(value, expected):
    require(isinstance(value, dict) and set(value) == set(expected),
            "missing or unexpected object fields")


def validate_spn(h, item):
    s, n, r = (matrix(item[name]) for name in ("S", "N", "R"))
    require(isinstance(item["d"], list) and len(item["d"]) == 4, "wrong d length")
    d = [exact_scalar(x) for x in item["d"]]
    require(s == transpose(s) and n == transpose(n), "S and N must be symmetric")
    require(all(x >= 0 for row in n for x in row), "N has a negative entry")
    require(all(x >= 0 for x in d), "d has a negative entry")
    diagonal = [[d[i] if i == j else F(0) for j in range(4)] for i in range(4)]
    require(s == congruence(diagonal, r), "S != R^T diag(d) R")
    require(h == add(s, n), "recomputed H != S + N")


def check_certificate(payload):
    keys(payload, ("schema", "scope", "mu", "K", "certificates"))
    require(payload["schema"] == "T-P5-026-rational-spn-v1", "unsupported schema")
    require(payload["scope"] == "source-independent-unbound", "source binding is unsupported")
    k = matrix(payload["K"], 2, 4)
    require(all(x >= 0 for row in k for x in row), "K has a negative entry")
    mu = exact_scalar(payload["mu"])
    require(mu >= 0, "certificate budget must be nonnegative")
    items = payload["certificates"]
    require(isinstance(items, list) and len(items) == 18, "exactly 18 certificates required")
    seen = set()
    for item in items:
        keys(item, ("cone", "S", "N", "R", "d"))
        c = item["cone"]
        require(isinstance(c, list) and len(c) == 2 and all(type(j) is int for j in c),
                "cone must contain two integer indices")
        c = tuple(c)
        require(c in REPS and c not in seen, "non-representative or duplicate cone")
        seen.add(c)
        _, h = matrices(k, mu, c)
        validate_spn(h, item)
    require(seen == set(REPS), "representative coverage incomplete")
    return {"certificate_arithmetic_valid": True, "representatives_checked": 18,
            "mu": str(mu), "mu_lt_one": mu < 1, **BOUNDARY}


def encode(value):
    if isinstance(value, F):
        return str(value)
    if isinstance(value, (tuple, list)):
        return [encode(x) for x in value]
    if isinstance(value, dict):
        return {key: encode(val) for key, val in value.items()}
    return value


def ldlt_positive(a):
    """Fixture construction only: strict-positive, exact no-pivot LDL."""
    lower, d = identity(), []
    for j in range(4):
        pivot = a[j][j] - sum((lower[j][p] ** 2 * d[p] for p in range(j)), F(0))
        require(pivot > 0, "fixture LDL pivot is not positive")
        d.append(pivot)
        for i in range(j + 1, 4):
            lower[i][j] = (a[i][j] - sum(
                (lower[i][p] * lower[j][p] * d[p] for p in range(j)), F(0))) / pivot
    return transpose(lower), d


def toy_fixture():
    # Arbitrary nonzero rational K, not K_path and not an application example.
    k, mu = [[F(1, 1000)] * 4 for _ in range(2)], F(1, 2)
    certs = []
    for c in REPS:
        _, h = matrices(k, mu, c)
        n = zero()
        n[0][1] = n[1][0] = F(1, 10000)
        s = add(h, scale(-1, n))
        r, d = ldlt_positive(s)
        certs.append({"cone": list(c), "S": s, "N": n, "R": r, "d": d})
    return encode({"schema": "T-P5-026-rational-spn-v1",
                   "scope": "source-independent-unbound", "mu": mu,
                   "K": k, "certificates": certs})


def reject_duplicate_keys(pairs):
    result = {}
    for key, val in pairs:
        require(key not in result, "duplicate JSON key")
        result[key] = val
    return result


def read_payload(path):
    return json.loads(Path(path).read_text(encoding="utf-8"), object_pairs_hook=reject_duplicate_keys)


def self_test():
    checks = []
    require(P == transpose(P), "frozen P symmetry")
    for c in range(6):
        g = G[c]
        require(abs(g[0][0] * g[1][1] - g[0][1] * g[1][0]) == 1, "unimodularity")
        require(REVERSE[REVERSE[c]] == c and REVERSE[c] != c, "free sign involution")
        require(G[REVERSE[c]] == tuple(tuple(-x for x in row) for row in g), "reverse G")
        # Sign equations for all a,b>=0 follow from coefficient nonnegativity,
        # not from evaluating sample points.
        signed_rows = (g[0], g[1], tuple(x + y for x, y in zip(*g)))
        for row, sign in zip(signed_rows, SIGNS[c]):
            require(all(sign * value >= 0 for value in row), "cone sign coefficients")
    checks.append("six_integer_maps_unimodular_sign_coefficients_and_involution")

    all_cones = set(itertools.product(range(6), repeat=2))
    covered = set(REPS) | {(REVERSE[a], REVERSE[b]) for a, b in REPS}
    require(covered == all_cones and len(covered) == 36 and len(REPS) == 18, "orbit coverage")
    require(not (set(REPS) & {(REVERSE[a], REVERSE[b]) for a, b in REPS}), "orbit overlap")
    checks.append("36_cones_18_disjoint_global_sign_pairs")

    grid = [F(-3), F(-1), F(-1, 2), F(0), F(1, 2), F(1), F(3)]
    for x, y in itertools.product(grid, repeat=2):
        j, a, b = channel_cover(x, y)
        require(a >= 0 and b >= 0 and mv(G[j], [a, b]) == [x, y], "cover witness")
    for z in itertools.product((F(-1), F(0), F(1)), repeat=4):
        j4, a4, b4 = channel_cover(z[0], z[2])
        j5, a5, b5 = channel_cover(z[1], z[3])
        require(mv(cone_data((j4, j5))[0], [a4, a5, b4, b5]) == list(z), "interleave")
    checks.append("49_rational_channel_and_81_product_cover_boundary_samples")

    # Complete coefficient-basis checks: the gap is linear in eight K entries
    # and mu, and quadratic in u. Compare symmetric coefficient matrices.
    parameter_basis = [([[F(0)] * 4 for _ in range(2)], F(1))]
    for a, j in itertools.product(range(2), range(4)):
        k = [[F(0)] * 4 for _ in range(2)]
        k[a][j] = F(1)
        parameter_basis.append((k, F(0)))
    for c in sorted(all_cones):
        t, sigma, tau = cone_data(c)
        abs_t = [[sigma[i] * t[i][j] for j in range(4)] for i in range(4)]
        lt = mm(L, t)
        abs_lt = [[tau[a] * lt[a][j] for j in range(4)] for a in range(2)]
        require(all(x >= 0 for row in abs_t + abs_lt for x in row), "absolute cone maps")
        flipped = (REVERSE[c[0]], REVERSE[c[1]])
        require(cone_data(flipped)[0] == scale(-1, t), "interleaved reversal")
        for k, mu in parameter_basis:
            b, h = matrices(k, mu, c)
            require((b, h) == matrices(k, mu, flipped), "paired B/H identity")
            force = mm(mm(transpose(abs_lt), k), abs_t)
            expected = add(scale(mu, congruence(P, t)), scale(F(-1, 2), add(force, transpose(force))))
            require(h == expected and h == transpose(h), "gap coefficient identity")
    checks.append("324_complete_parameter_basis_gap_and_paired_matrix_identities")

    fixture = toy_fixture()
    require(check_certificate(fixture)["certificate_arithmetic_valid"], "nonzero toy SPN")
    checks.append("18_nonzero_toy_gain_certificates_with_nonzero_N_and_exact_LDL")
    gap = zero()
    gap[0][1] = gap[1][0] = F(1)
    validate_spn(gap, encode({"S": zero(), "N": gap, "R": zero(), "d": [0] * 4}))
    require(quadratic(gap, [F(1), F(-1), F(0), F(0)]) == -2, "SPN non-PSD witness")
    checks.append("singular_zero_PSD_factor_and_SPN_not_PSD_witness")

    mutations = []
    def changed(label, mutate):
        value = copy.deepcopy(fixture)
        mutate(value)
        mutations.append((label, value))
    changed("missing_cone", lambda p: p["certificates"].pop())
    changed("duplicate_cone", lambda p: p["certificates"][1].update(cone=[0, 0]))
    changed("nonrepresentative", lambda p: p["certificates"][0].update(cone=[1, 0]))
    changed("negative_K", lambda p: p["K"][0].__setitem__(0, "-1"))
    changed("float", lambda p: p.update(mu=0.5))
    changed("boolean", lambda p: p["K"][0].__setitem__(0, True))
    changed("decimal_string", lambda p: p.update(mu="0.5"))
    changed("zero_denominator", lambda p: p.update(mu="1/0"))
    changed("negative_mu", lambda p: p.update(mu="-1"))
    changed("wrong_shape", lambda p: p["certificates"][0]["R"].pop())
    changed("negative_N", lambda p: p["certificates"][0]["N"][0].__setitem__(1, "-1"))
    changed("negative_d", lambda p: p["certificates"][0]["d"].__setitem__(0, "-1"))
    changed("factor_mismatch", lambda p: p["certificates"][0]["R"][0].__setitem__(0, "2"))
    changed("decomposition_mismatch", lambda p: p["certificates"][0]["N"][0].__setitem__(0, "1"))
    changed("source_bound_claim", lambda p: p.update(scope="source-bound"))
    changed("admission_field", lambda p: p.update(registry_eligible=True))
    rejected = []
    for label, value in mutations:
        try:
            check_certificate(value)
        except InvalidCertificate:
            rejected.append(label)
        else:
            raise InvalidCertificate("negative control unexpectedly accepted: " + label)
    try:
        json.loads('{"mu": 1, "mu": 2}', object_pairs_hook=reject_duplicate_keys)
    except InvalidCertificate:
        rejected.append("duplicate_json_key")
    else:
        raise InvalidCertificate("duplicate JSON key accepted")
    checks.append("17_malformed_or_tampered_inputs_rejected")

    lean = (ROOT / "P5FeasibleConeSPN.lean").read_text(encoding="utf-8")
    require(not re.search(r"\b(?:sorry|admit|axiom|unsafe|native_decide)\b", lean),
            "forbidden proof escape token in Lean source")
    require("import Mathlib.Data.Real.Basic\nimport Mathlib.Tactic" in lean, "unexpected imports")
    checks.append("Lean_source_token_scan_only_not_elaboration")
    return {"task_id": "T-P5-026", "check_type": "exact_rational_and_static_only",
            "checks": checks, "negative_controls_rejected": rejected,
            "result": "pass", **BOUNDARY}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--self-test", action="store_true")
    group.add_argument("--certificate", type=Path)
    group.add_argument("--print-toy-fixture", action="store_true")
    args = parser.parse_args()
    try:
        if args.self_test:
            result = self_test()
            result["sha256"] = {
                name: hashlib.sha256((ROOT / name).read_bytes()).hexdigest()
                for name in ("P5FeasibleConeSPN.lean", "check_exact.py", "lakefile.toml", "lean-toolchain")
            }
        elif args.certificate:
            result = check_certificate(read_payload(args.certificate))
        else:
            result = toy_fixture()
    except (InvalidCertificate, OSError, ValueError, TypeError, KeyError) as exc:
        print(json.dumps({"result": "rejected_or_uncheckable", "reason": str(exc),
                          "meaning": "no certificate acceptance; not a copositivity counterexample",
                          **BOUNDARY}, indent=2))
        return 1
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
