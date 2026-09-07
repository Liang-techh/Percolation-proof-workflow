"""Independent P5 closed-cone geometry and SPN arithmetic audit (stdlib only).

Read-only at runtime, including imports. No Lean execution or source admission.
Unlike a state grid, the coverage checks use exact inverse/Farkas identities;
universal polynomial identities are checked by sparse rational coefficients.
The optional certificate interface is T-P5-026-rational-spn-v1, still unbound.
"""

from __future__ import annotations

import argparse
import ast
import copy
from fractions import Fraction as F
import hashlib
import itertools
import json
from pathlib import Path
import re
import runpy
import sys

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parent
NAMES = ("pp", "nn", "pnPos", "pnNeg", "npPos", "npNeg")
G = [list(map(list, g)) for g in (
    ((1, 0), (0, 1)), ((-1, 0), (0, -1)),
    ((1, 1), (-1, 0)), ((1, 0), (-1, -1)),
    ((-1, 0), (1, 1)), ((-1, -1), (1, 0)),
)]
J = [list(map(list, g)) for g in (
    ((1, 0), (0, 1)), ((-1, 0), (0, -1)),
    ((0, -1), (1, 1)), ((1, 0), (-1, -1)),
    ((-1, 0), (1, 1)), ((0, 1), (-1, -1)),
)]
SIGNS = ((1, 1, 1), (-1, -1, -1), (1, -1, 1),
         (1, -1, -1), (-1, 1, 1), (-1, 1, -1))
REVERSE = (1, 0, 5, 4, 3, 2)
REPS = tuple(itertools.product((0, 2, 3), range(6)))
ALL_CONES = tuple(itertools.product(range(6), repeat=2))
L = [[1, 0, 1, 0], [0, 1, 0, 1]]
P = [list(map(F, row)) for row in (
    ("3/4", "-3/400", "0", "1/800"),
    ("-3/400", "29/50", "-1/800", "0"),
    ("0", "-1/800", "2049997/3000000", "0"),
    ("1/800", "0", "0", "2399261/4000000"),
)]
BOUNDARY = dict(lean_status="not_run", kernel_verified=False,
                concrete_K_path_bound=False, source_coverage_verified=False,
                source_authentication="not_checked", registry_eligible=False,
                registry_mutated=False, P5_P8_M4_closed=False)
# Freeze the reviewed executable before using it ONLY as a comparison/fixture.
LEGACY_SHA256 = "d887aade11edf9adf1e7f532d8b173a089aac9e2fadba2e25fbc2f169e1e4211"


class Rejected(ValueError):
    pass


def need(condition, message):
    if not condition:  # Remains active with python -O.
        raise Rejected(message)


class Poly:
    """Q[variables], monomials are sorted tuples of variable names."""

    def __init__(self, value=0):
        if isinstance(value, Poly):
            self.terms = dict(value.terms)
        elif isinstance(value, dict):
            self.terms = {m: F(c) for m, c in value.items() if c}
        else:
            need(type(value) is int or isinstance(value, F), "non-rational polynomial scalar")
            self.terms = {(): F(value)} if value else {}

    @staticmethod
    def var(name):
        return Poly({(name,): F(1)})

    def __add__(self, other):
        out = dict(self.terms)
        for m, c in Poly(other).terms.items():
            out[m] = out.get(m, F(0)) + c
        return Poly(out)

    __radd__ = __add__

    def __neg__(self):
        return Poly({m: -c for m, c in self.terms.items()})

    def __sub__(self, other):
        return self + -Poly(other)

    def __rsub__(self, other):
        return Poly(other) + -self

    def __mul__(self, other):
        out = {}
        for m, a in self.terms.items():
            for n, b in Poly(other).terms.items():
                key = tuple(sorted(m + n))
                out[key] = out.get(key, F(0)) + a * b
        return Poly(out)

    __rmul__ = __mul__

    def __eq__(self, other):
        return self.terms == Poly(other).terms


def shape(a):
    need(isinstance(a, list) and a and isinstance(a[0], list) and a[0], "empty matrix")
    n = len(a[0])
    need(all(isinstance(row, list) and len(row) == n for row in a), "ragged matrix")
    return len(a), n


def tr(a):
    m, n = shape(a)
    return [[a[i][j] for i in range(m)] for j in range(n)]


def mm(a, b):
    m, n = shape(a)
    p, q = shape(b)
    need(n == p, "matrix multiplication shape mismatch")
    return [[sum(a[i][k] * b[k][j] for k in range(n)) for j in range(q)] for i in range(m)]


def mv(a, v):
    m, n = shape(a)
    need(n == len(v), "matrix/vector shape mismatch")
    return [sum(a[i][j] * v[j] for j in range(n)) for i in range(m)]


def add(a, b):
    need(shape(a) == shape(b), "matrix addition shape mismatch")
    m, n = shape(a)
    return [[a[i][j] + b[i][j] for j in range(n)] for i in range(m)]


def scale(s, a):
    return [[s * x for x in row] for row in a]


def eye(n):
    return [[int(i == j) for j in range(n)] for i in range(n)]


def quad(a, v):
    need(shape(a) == (len(v), len(v)), "quadratic shape mismatch")
    return sum(v[i] * a[i][j] * v[j] for i in range(len(v)) for j in range(len(v)))


def congr(a, t):
    return mm(tr(t), mm(a, t))


def interleave(table, c):
    t = [[0] * 4 for _ in range(4)]
    for channel, slots in zip(c, ((0, 2), (1, 3))):
        for i in range(2):
            for j in range(2):
                t[slots[i]][slots[j]] = table[channel][i][j]
    return t


def cone_data(c):
    a, b = c
    return (interleave(G, c),
            [SIGNS[a][0], SIGNS[b][0], SIGNS[a][1], SIGNS[b][1]],
            [SIGNS[a][2], SIGNS[b][2]])


def matrices(k, mu, c):
    need(shape(k) == (2, 4), "gain shape mismatch")
    t, sigma, tau = cone_data(c)
    a = [[sum(L[h][i] * tau[h] * k[h][j] * sigma[j] for h in range(2))
          for j in range(4)] for i in range(4)]
    b = scale(F(1, 2), add(a, tr(a)))
    return b, congr(add(scale(mu, P), scale(-1, b)), t)


def dissipation(z):
    x, v, y, w = z
    return (F(3, 4)*x*x + F(29, 50)*v*v - F(3, 200)*x*v
            + F(2049997, 3000000)*y*y + F(2399261, 4000000)*w*w
            + F(1, 400)*x*w - F(1, 400)*v*y)


def halfspaces(signs):
    x, y, s = signs
    return [[x, 0], [0, y], [s, s]]


def check_chart(g, inv, signs, rows):
    d = halfspaces(signs)
    w = [[int(k == row) for k in range(3)] for row in rows]
    need(mm(inv, g) == eye(2) and mm(g, inv) == eye(2), "chart inverse identity")
    need(mm(w, d) == inv, "inverse Farkas identity J = W D")
    need(all(x >= 0 for row in w for x in row), "negative Farkas coefficient")
    need(all(x >= 0 for row in mm(d, g) for x in row), "forward weak signs")


def geometry_checks():
    selectors = ((0, 1), (0, 1), (1, 2), (0, 2), (0, 2), (1, 2))
    for c in range(6):
        check_chart(G[c], J[c], SIGNS[c], selectors[c])
        need(REVERSE[REVERSE[c]] == c and REVERSE[c] != c, "free cone involution")
        need(G[REVERSE[c]] == scale(-1, G[c]), "reversed forward map")
        need(SIGNS[REVERSE[c]] == tuple(-s for s in SIGNS[c]), "reversed signs")
    # All sign choices occur for arbitrary real x,y,x+y using weak signs.
    # The two omitted choices force all three signed forms to zero, hence x=y=0.
    exceptional = set(itertools.product((-1, 1), repeat=3)) - set(SIGNS)
    need(exceptional == {(1, 1, -1), (-1, -1, 1)}, "sign-case coverage")
    for signs in exceptional:
        d = halfspaces(signs)
        need([sum(row[j] for row in d) for j in range(2)] == [0, 0], "zero-sum Farkas forms")
        need(d[0][0]*d[1][1] - d[0][1]*d[1][0] != 0, "origin-only rank certificate")
    need(mv(G[0], [0, 0]) == [0, 0], "origin covered")
    flipped = {(REVERSE[a], REVERSE[b]) for a, b in REPS}
    need(len(REPS) == len(set(REPS)) == 18, "representative count")
    need(set(REPS).isdisjoint(flipped) and set(REPS) | flipped == set(ALL_CONES), "orbit coverage")
    for c in ALL_CONES:
        t = interleave(G, c)
        inv = interleave(J, c)
        need(mm(t, inv) == eye(4) and mm(inv, t) == eye(4), "interleaved inverse")
    return dict(closed_cone_inverse_Farkas_certificates=6, weak_sign_cases=8,
                exceptional_sign_cases_origin_only=2, product_maps_with_two_sided_inverse=36,
                disjoint_global_sign_orbits=18, state_samples_used=0)


def restricted_expr(text, env=None):
    """Tiny arithmetic reader, never eval/exec; NOT a Lean parser/elaborator."""
    env = {} if env is None else env

    def visit(node):
        if isinstance(node, ast.Constant) and type(node.value) is int:
            return F(node.value)
        if isinstance(node, ast.Name) and node.id in env:
            return env[node.id]
        if isinstance(node, ast.List):
            return [visit(x) for x in node.elts]
        if isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.USub):
            return -visit(node.operand)
        if isinstance(node, ast.BinOp):
            a, b = visit(node.left), visit(node.right)
            if isinstance(node.op, ast.Add):
                return a + b
            if isinstance(node.op, ast.Sub):
                return a - b
            if isinstance(node.op, ast.Mult):
                return a * b
            if isinstance(node.op, ast.Div) and isinstance(a, F) and isinstance(b, F) and b:
                return a / b
        raise Rejected("unsupported restricted expression: " + text)

    return visit(ast.parse(text, mode="eval").body)


def lean_table_checks(source):
    def body(name):
        matches = re.findall(r"^def " + re.escape(name) + r" [^\n]*\n(.*?)(?=\n\n)", source, re.M | re.S)
        need(len(matches) == 1, "missing/ambiguous Lean table: " + name)
        return matches[0].strip()

    a, b = Poly.var("a"), Poly.var("b")
    for name, row in (("cx", 0), ("cy", 1)):
        lines = body(name).splitlines()
        need(len(lines) == 6, "unexpected channel branch count")
        seen = set()
        for line in lines:
            m = re.fullmatch(r"\s*\| \.(\w+), (a|_), (b|_) => (.+)", line)
            need(m is not None and m[1] in NAMES and m[1] not in seen, "unsupported Lean channel branch")
            seen.add(m[1])
            env = {key: val for key, val in ((m[2], a), (m[3], b)) if key != "_"}
            actual = restricted_expr(m[4], env)
            c = NAMES.index(m[1])
            need(actual == G[c][row][0]*a + G[c][row][1]*b, "Lean channel map mismatch")
    for name, pos in (("sx", 0), ("sy", 1), ("ss", 2)):
        seen = set()
        for line in body(name).splitlines():
            lhs, rhs = line.split("=>")
            need(re.fullmatch(r"\s*(?:\|\s*\.\w+\s*)+", lhs) is not None, "unsupported sign branch")
            value = restricted_expr(rhs.strip())
            for cname in re.findall(r"\.(\w+)", lhs):
                need(cname in NAMES and cname not in seen, "duplicate/unknown sign branch")
                seen.add(cname)
                need(value == SIGNS[NAMES.index(cname)][pos], "Lean sign mismatch")
        need(seen == set(NAMES), "Lean sign coverage")
    branches = re.findall(r"\| \.(\w+) => \.(\w+)", body("reverse"))
    need(len(branches) == 6 and {x for x, _ in branches} == set(NAMES), "Lean reverse branches")
    for x, y in branches:
        need(y == NAMES[REVERSE[NAMES.index(x)]], "Lean reverse mismatch")
    # P is multiline; L is a one-line literal in the frozen source.
    ptext = re.sub(r"\(([^():]+) : ℝ\)", r"\1", body("P")).replace("![", "[")
    need(restricted_expr(ptext) == P, "Lean P literal mismatch")
    lm = re.findall(r"^def L : [^\n]+ := (.+)$", source, re.M)
    need(len(lm) == 1 and restricted_expr(lm[0].replace("![", "[")) == L, "Lean L literal mismatch")
    return ["cx", "cy", "sx", "sy", "ss", "reverse", "P", "L"]


def polynomial_checks(legacy):
    u = [Poly.var("u" + str(i)) for i in range(4)]
    k = [[Poly.var(f"K{a}{j}") for j in range(4)] for a in range(2)]
    mu = Poly.var("mu")
    all_h = {}
    for c in ALL_CONES:
        t, sigma, tau = cone_data(c)
        need(legacy["cone_data"](c) == (t, sigma, tau), "legacy sign/map differs")
        z = mv(t, u)
        # Scalar route explicitly uses physical channel sums and the frozen Q polynomial.
        sums = [z[0] + z[2], z[1] + z[3]]
        envelope = sum(tau[a]*sums[a]*k[a][j]*sigma[j]*z[j]
                       for a in range(2) for j in range(4))
        b, h = matrices(k, mu, c)
        need(quad(P, z) == dissipation(z), "frozen dissipation cross coefficients")
        need(quad(b, z) == envelope, "signed power/symmetrization identity")
        need(quad(h, u) == mu*dissipation(z) - envelope, "cone gap polynomial identity")
        need(h == tr(h), "symbolic H symmetry")
        need(legacy["matrices"](k, mu, c) == (b, h), "legacy full symbolic matrices differ")
        fc = (REVERSE[c[0]], REVERSE[c[1]])
        need(matrices(k, mu, fc) == (b, h), "symbolic global sign pair")
        all_h[c] = h
    # Independent generic identities: arbitrary nonsymmetric M and arbitrary U.
    m = [[Poly.var(f"M{i}{j}") for j in range(4)] for i in range(4)]
    t = [[Poly.var(f"T{i}{j}") for j in range(4)] for i in range(4)]
    need(quad(congr(m, t), u) == quad(m, mv(t, u)), "generic congruence identity")
    d = [Poly.var(f"d{i}") for i in range(4)]
    diag = [[d[i] if i == j else 0 for j in range(4)] for i in range(4)]
    tu = mv(t, u)
    need(quad(congr(diag, t), u) == sum(d[i]*tu[i]*tu[i] for i in range(4)), "generic factor sum of squares")
    # At symbolic K,mu these 18 matrices really differ; specialization can merge them.
    distinct = {tuple(tuple(sorted(Poly(x).terms.items())) for row in all_h[c] for x in row)
                for c in REPS}
    return dict(full_symbolic_cone_gap_identities=36, full_symbolic_legacy_comparisons=36,
                full_symbolic_flip_identities=36, generic_congruence_identity=True,
                generic_diagonal_factor_identity=True, distinct_symbolic_representatives=len(distinct))


def scalar(x):
    need(type(x) is int or (isinstance(x, str) and re.fullmatch(r"-?(?:0|[1-9][0-9]*)(?:/[1-9][0-9]*)?", x)),
         "expected exact integer or fraction string")
    return F(x)


def read_matrix(x, dims=(4, 4)):
    need(shape(x) == dims, "certificate matrix dimensions")
    return [[scalar(v) for v in row] for row in x]


def keys(obj, wanted):
    need(isinstance(obj, dict) and set(obj) == set(wanted.split()), "certificate object fields")


def check_spn(h, item):
    s, n, r = (read_matrix(item[key]) for key in ("S", "N", "R"))
    need(isinstance(item["d"], list) and len(item["d"]) == 4, "factor diagonal length")
    d = [scalar(x) for x in item["d"]]
    need(s == tr(s) and n == tr(n), "SPN symmetry")
    need(all(x >= 0 for row in n for x in row) and all(x >= 0 for x in d), "SPN signs")
    # Compute Gram entries directly; independent of congr() and legacy LDL construction.
    gram = [[sum(d[a]*r[a][i]*r[a][j] for a in range(4)) for j in range(4)] for i in range(4)]
    need(s == gram, "S != R^T diag(d) R")
    need(h == add(s, n), "H != S+N")


def check_certificate(payload):
    keys(payload, "schema scope mu K certificates")
    need(payload["schema"] == "T-P5-026-rational-spn-v1", "certificate schema")
    need(payload["scope"] == "source-independent-unbound", "unsupported source scope")
    k, mu = read_matrix(payload["K"], (2, 4)), scalar(payload["mu"])
    need(mu >= 0 and all(x >= 0 for row in k for x in row), "negative gain/budget")
    items = payload["certificates"]
    need(isinstance(items, list) and len(items) == 18, "exactly 18 certificate items required")
    seen = set()
    for item in items:
        keys(item, "cone S N R d")
        c = item["cone"]
        need(isinstance(c, list) and len(c) == 2 and all(type(x) is int for x in c), "cone index type")
        c = tuple(c)
        need(c in REPS and c not in seen, "duplicate/nonrepresentative cone")
        seen.add(c)
        check_spn(matrices(k, mu, c)[1], item)
        check_spn(matrices(k, mu, (REVERSE[c[0]], REVERSE[c[1]]))[1], item)
    need(seen == set(REPS), "certificate orbit coverage")
    return dict(certificate_arithmetic_valid=True, representatives_checked=18,
                matrices_checked_including_flips=36, mu=str(mu), mu_lt_one=mu < 1,
                **BOUNDARY)


def pairs_no_duplicates(pairs):
    out = {}
    for key, value in pairs:
        need(key not in out, "duplicate JSON key")
        out[key] = value
    return out


def negative_controls(fixture, lean):
    rejected = []

    def reject(label, action):
        try:
            action()
        except Rejected:
            rejected.append(label)
        else:
            raise Rejected("negative control unexpectedly accepted: " + label)

    reject("inverse_transpose", lambda: check_chart(G[2], tr(J[2]), SIGNS[2], (1, 2)))
    reject("wrong_sum_sign", lambda: check_chart(G[2], J[2], (1, -1, -1), (1, 2)))
    reject("wrong_Farkas_selector", lambda: check_chart(G[2], J[2], SIGNS[2], (0, 2)))
    reject("Lean_map_tamper", lambda: lean_table_checks(lean.replace(".pnPos, a, b => a + b", ".pnPos, a, b => a - b", 1)))
    reject("Lean_sign_tamper", lambda: lean_table_checks(lean.replace("| .pp | .pnPos | .npPos => 1", "| .pp | .pnPos | .npPos => -1", 1)))
    reject("Lean_P_tamper", lambda: lean_table_checks(lean.replace("2049997/3000000", "2049998/3000000", 1)))
    k = [[F(i*4+j+1, 1000) for j in range(4)] for i in range(2)]
    t, sigma, tau = cone_data((2, 4))
    b, h = matrices(k, F(1, 2), (2, 4))
    m = add(scale(F(1, 2), P), scale(-1, b))
    reject("congruence_transpose", lambda: need(h == mm(t, mm(m, tr(t))), "wrong congruence orientation"))
    reject("missing_sym_half", lambda: need(h == congr(add(scale(F(1, 2), P), scale(-2, b)), t), "missing factor 1/2"))
    permuted = [t[i] for i in (0, 2, 1, 3)]
    reject("state_order_permutation", lambda: need(h == congr(m, permuted), "wrong state order"))
    reject("ragged_matrix", lambda: mm([[1, 2], [3]], [[1], [2]]))
    mutations = (
        ("missing_representative", lambda p: p["certificates"].pop()),
        ("duplicate_representative", lambda p: p["certificates"][1].update(cone=[0, 0])),
        ("bool_cone", lambda p: p["certificates"][0].update(cone=[False, 0])),
        ("negative_K", lambda p: p["K"][0].__setitem__(0, "-1")),
        ("float_mu", lambda p: p.update(mu=0.5)),
        ("decimal_mu", lambda p: p.update(mu="0.5")),
        ("zero_denominator", lambda p: p.update(mu="1/0")),
        ("bool_K", lambda p: p["K"][0].__setitem__(0, True)),
        ("negative_d", lambda p: p["certificates"][0]["d"].__setitem__(0, "-1")),
        ("negative_N", lambda p: p["certificates"][0]["N"][0].__setitem__(0, "-1")),
        ("R_transpose", lambda p: p["certificates"][0].update(R=tr(p["certificates"][0]["R"]))),
        ("false_source_binding", lambda p: p.update(scope="source-bound")),
        ("admission_field", lambda p: p.update(registry_eligible=True)),
    )
    for label, mutate in mutations:
        changed = copy.deepcopy(fixture)
        mutate(changed)
        reject(label, lambda: check_certificate(changed))
    reject("duplicate_JSON_key", lambda: json.loads('{"mu":1,"mu":2}', object_pairs_hook=pairs_no_duplicates))
    return rejected


def run(certificate_path=None):
    original_bytes = (ROOT / "check_exact.py").read_bytes()
    need(hashlib.sha256(original_bytes).hexdigest() == LEGACY_SHA256, "reviewed legacy checker changed; re-audit required")
    # Fixture construction and comparison only. All acceptance checks above are independent.
    legacy = runpy.run_path(str(ROOT / "check_exact.py"), run_name="p5_comparison_only")
    lean = (ROOT / "P5FeasibleConeSPN.lean").read_text(encoding="utf-8")
    result = dict(geometry=geometry_checks(),
                  Lean_tables_checked_as_restricted_text_only=lean_table_checks(lean),
                  polynomial=polynomial_checks(legacy))
    fixture = legacy["toy_fixture"]()
    result["toy_only_unbound_certificate"] = check_certificate(fixture)
    # Singular PSD factor and a genuinely non-PSD SPN matrix must also be accepted.
    zero = [[0]*4 for _ in range(4)]
    gap = copy.deepcopy(zero)
    gap[0][1] = gap[1][0] = 1
    check_spn(gap, dict(S=zero, N=gap, R=zero, d=[0]*4))
    need(quad(gap, [1, -1, 0, 0]) == -2, "SPN strict matrix-class witness")
    result["singular_SPN_non_PSD_witness"] = True
    result["negative_controls_rejected"] = negative_controls(fixture, lean)
    if certificate_path is not None:
        raw = sys.stdin.buffer.read() if str(certificate_path) == "-" else Path(certificate_path).read_bytes()
        payload = json.loads(raw.decode("utf-8"), object_pairs_hook=pairs_no_duplicates)
        result["supplied_unbound_certificate"] = check_certificate(payload)
        result["supplied_certificate_bytes_sha256"] = hashlib.sha256(raw).hexdigest()
    result["sha256"] = {name: hashlib.sha256((ROOT / name).read_bytes()).hexdigest()
                        for name in ("P5FeasibleConeSPN.lean", "check_exact.py", Path(__file__).name)}
    return dict(result="pass", check_type="exact_rational_geometry_and_polynomial_arithmetic_only",
                **result, **BOUNDARY)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--self-test", action="store_true")
    group.add_argument("--certificate", type=Path, help="exact JSON file, or - to read stdin without writing a file")
    args = parser.parse_args()
    try:
        result = run(args.certificate)
    except (Rejected, OSError, ValueError, TypeError, KeyError, SyntaxError) as exc:
        print(json.dumps(dict(result="rejected_or_uncheckable", reason=str(exc),
                              meaning="no acceptance; not a copositivity counterexample", **BOUNDARY), indent=2))
        return 1
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
