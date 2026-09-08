"""Read-only inverse/finite-cover audit; optional Lean stdin check, no output files.

Only literal geometry tables are read from the old Python source (never executed).
Arithmetic probes do not prove coverage over all reals; Lean proves that separately.
"""
from __future__ import annotations

import argparse
import ast
from collections import Counter
from fractions import Fraction as F
import hashlib
from itertools import product
import json
import os
from pathlib import Path
import re
import subprocess
import sys

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parent
NEW = "NEW_CONE_INDEX_InverseCover20260908.lean"
PINS = {
    "P5FeasibleConeSPN.lean": "fa9d990cfb2adb6fce049b4c6feb9ab2dfed3c2bcd14b059a0a8332138e1e824",
    "NEW_exact_geometry_spn.py": "263fac727c1c3068043c02a63dade5995a22e1e7e9a879682ac3e69bafd54f42",
    "NEW_CONE_INDEX_Core.lean": "b0e154716a2ba71058b7996b8d85f982a12326ce117f8127cf9895286bd80602",
}
AUDITS = ("coordinates_chart", "chart_coordinates", "chartEquiv", "parameter_unique",
          "member_iff_coordinates", "witnessLabelEquiv", "memberLabelEquiv",
          "coveringLabels_spec", "coveringLabels_nonempty", "coveringLabels_card",
          "inverse_cover_multiplicity", "origin_coveringLabels_card")


def need(ok, message):
    if not ok:
        raise ValueError(message)


def hashes():
    return {name: hashlib.sha256((ROOT / name).read_bytes()).hexdigest()
            for name in (*PINS, NEW, Path(__file__).name)}


def literals():
    tree = ast.parse((ROOT / "NEW_exact_geometry_spn.py").read_text(encoding="utf-8"))
    out = {}
    for node in tree.body:
        if isinstance(node, ast.Assign) and len(node.targets) == 1:
            name = getattr(node.targets[0], "id", None)
            if name in ("NAMES", "REVERSE"):
                out[name] = ast.literal_eval(node.value)
            elif name in ("G", "J"):
                need(isinstance(node.value, ast.ListComp), "geometry table structure changed")
                out[name] = ast.literal_eval(node.value.generators[0].iter)
    need(set(out) == {"NAMES", "REVERSE", "G", "J"}, "missing literal tables")
    return out


def linear_value(expression, x, y):
    def visit(n):
        if isinstance(n, ast.Name) and n.id in ("x", "y"):
            return {"x": x, "y": y}[n.id]
        if isinstance(n, ast.UnaryOp) and isinstance(n.op, ast.USub):
            return -visit(n.operand)
        if isinstance(n, ast.BinOp) and isinstance(n.op, (ast.Add, ast.Sub)):
            return visit(n.left) + (1 if isinstance(n.op, ast.Add) else -1) * visit(n.right)
        raise ValueError("unsupported non-linear inverse expression")
    return visit(ast.parse(expression, mode="eval").body)


def inverse_table(source, names):
    tables = []
    for name in ("invA", "invB"):
        matches = re.findall(r"^def " + name + r"[^\n]*\n(.*?)(?=\n\n)", source, re.M | re.S)
        need(len(matches) == 1, "inverse definition missing/ambiguous")
        rows = {}
        for line in matches[0].splitlines():
            m = re.fullmatch(r"\s*\| \.(\w+), (x|_), (y|_) => (.+)", line)
            need(m is not None and m[1] in names and m[1] not in rows, "invalid branch")
            used = {n.id for n in ast.walk(ast.parse(m[4], mode="eval")) if isinstance(n, ast.Name)}
            need(used <= ({m[2], m[3]} - {"_"}), "expression uses unbound coordinate")
            rows[m[1]] = (linear_value(m[4], F(1), F(0)), linear_value(m[4], F(0), F(1)))
        need(set(rows) == set(names), "missing inverse branch")
        tables.append(rows)
    return tuple(tuple(t[n] for t in tables) for n in names)


def mm(a, b):
    return tuple(tuple(sum(x * y for x, y in zip(row, col)) for col in zip(*b)) for row in a)


def interleave(table, c):
    out = [[F(0)] * 4 for _ in range(4)]
    for cone, slots in zip(c, ((0, 2), (1, 3))):
        for i, j in product(range(2), repeat=2):
            out[slots[i]][slots[j]] = table[cone][i][j]
    return tuple(map(tuple, out))


def mv(a, u):
    return tuple(sum(x * y for x, y in zip(row, u)) for row in a)


def arithmetic():
    data = literals()
    source = (ROOT / NEW).read_text(encoding="utf-8")
    inv = inverse_table(source, data["NAMES"])
    need(inv == data["J"], "new inverse differs from reviewed J table")
    cones = tuple(product(range(6), repeat=2))
    reps = tuple(product((0, 2, 3), range(6)))
    flip = lambda c: tuple(data["REVERSE"][i] for i in c)
    expanded = tuple(c for r in reps for c in (r, flip(r)))
    need(Counter(expanded) == Counter(cones), "36-to-18 signed multiplicity")
    forward = {c: interleave(data["G"], c) for c in cones}
    inverse = {c: interleave(inv, c) for c in cones}
    identity = tuple(tuple(F(i == j) for j in range(4)) for i in range(4))
    for c in cones:
        need(mm(forward[c], inverse[c]) == identity, "right inverse")
        need(mm(inverse[c], forward[c]) == identity, "left inverse")
    histogram = Counter()
    for z in product(map(F, (-2, -1, 0, 1, 2)), repeat=4):
        def witnesses(labels):
            return Counter((c, mv(inverse[c], z)) for c in labels
                           if all(v >= 0 for v in mv(inverse[c], z)))
        full = witnesses(cones)
        need(full and full == witnesses(expanded), "lost label/parameter witness")
        for (c, u) in full:
            need(mv(forward[c], u) == z, "witness reconstruction")
        histogram[sum(full.values())] += 1
    rejected = []

    def reject(label, action):
        try:
            action()
        except ValueError:
            rejected.append(label)
        else:
            raise ValueError("negative control accepted: " + label)

    reject("wrong_inverse_sign", lambda: need(inverse_table(source.replace(
        ".pnPos, _, y => -y", ".pnPos, _, y => y", 1), data["NAMES"]) == data["J"], "inverse mismatch"))
    reject("missing_orientation", lambda: need(Counter(reps) == Counter(cones), "lost labels"))
    reject("duplicate_label", lambda: need(Counter(expanded[:-1] + expanded[:1]) == Counter(cones), "duplicate"))
    reject("matrix_value_dedup_at_origin", lambda: need(len({mv(forward[c], (0, 0, 0, 0)) for c in cones}) == 36, "lost origin labels"))
    reject("fixed_state_sign_invariance", lambda: need(
        all(v >= 0 for v in mv(inverse[(0, 0)], (1, 1, 1, 1))) ==
        all(v >= 0 for v in mv(inverse[flip((0, 0))], (1, 1, 1, 1))), "membership is not even per label"))
    return dict(two_sided_inverse_products=36, signed_labels=36, representative_pairs=18,
                rational_probes=625, multiplicity_histogram=dict(sorted(histogram.items())),
                negative_controls=rejected, universal_real_coverage_proved_by_python=False)


def lean_check(executable, packages):
    imports, bodies = [], []
    for name in ("NEW_CONE_INDEX_Core.lean", NEW):
        body = []
        for line in (ROOT / name).read_text(encoding="utf-8").splitlines():
            if line.startswith("import "):
                module = line.removeprefix("import ")
                need(module == "NEW_CONE_INDEX_Core" or module.startswith("Mathlib."), "unexpected import")
                if module.startswith("Mathlib.") and line not in imports:
                    imports.append(line)
            else:
                body.append(line)
        bodies.append("\n".join(body))
    bundle = "\n".join(imports) + "\n\n" + "\n\n".join(bodies) + "\n"
    paths = sorted(p / ".lake/build/lib/lean" for p in packages.resolve().iterdir()
                   if (p / ".lake/build/lib/lean").is_dir())
    need(any((p / "Mathlib.olean").is_file() for p in paths), "missing cached Mathlib")
    env = dict(os.environ, LEAN_PATH=os.pathsep.join(map(str, paths)))
    proc = subprocess.run([str(executable.resolve()), "--stdin"], input=bundle,
                          encoding="utf-8", capture_output=True, env=env, timeout=180)
    output = proc.stdout + proc.stderr
    print(output)
    need(proc.returncode == 0, "Lean failed")
    need("sorryAx" not in output and "warning:" not in output, "axiom/warning audit failed")
    reports = re.findall(r"depends on axioms:\s*\[([^\]]*)\]", output)
    allowed = {"propext", "Classical.choice", "Quot.sound"}
    need(reports and all({a.strip() for a in r.split(",") if a.strip()} <= allowed
                         for r in reports), "unexpected axiom dependency")
    for name in AUDITS:
        need("RouteBP5ConeIndexInverseCover." + name + "' depends on axioms:" in output,
             "missing audit: " + name)
    return dict(lean_status="stdin_source_bundle_pass", standalone_imports_verified=False,
                source_bundle_sha256=hashlib.sha256(bundle.encode()).hexdigest())


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--lean", type=Path)
    parser.add_argument("--mathlib-packages", type=Path)
    args = parser.parse_args()
    need(args.self_test or args.lean, "request --self-test or --lean")
    need(bool(args.lean) == bool(args.mathlib_packages), "Lean and packages required together")
    before = hashes()
    need(all(before[n] == h for n, h in PINS.items()), "input changed; re-audit required")
    result = dict(arithmetic=arithmetic(), lean_status="not_run")
    if args.lean:
        result.update(lean_check(args.lean, args.mathlib_packages))
    need(before == hashes(), "input changed during verification")
    print(json.dumps(dict(result="pass", **result, input_sha256=before,
                         concrete_K_path_bound=False, P5_closed=False,
                         source_coverage_verified=False, registry_eligible=False), indent=2))


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError, subprocess.SubprocessError) as exc:
        print(json.dumps(dict(result="rejected_or_uncheckable", reason=str(exc))))
        sys.exit(1)
