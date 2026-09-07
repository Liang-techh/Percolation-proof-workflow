"""Read-only exact check of the 23-row mathematical attempt; never executes Lean.

Parses literal rows from the new standalone Core and compares exact Laurent
coefficients with the pinned CSV column and the stated trigonometric formula.
The formula transcription below is a Python check, not a Lean proof receipt.
"""
from __future__ import annotations

import csv
import hashlib
import json
import re
from fractions import Fraction as F
from pathlib import Path

HERE = Path(__file__).resolve().parent
ZERO = (F(0), F(0))
PINS = {
    "NEW_BODY6_SLICE_20260907.csv":
        "46f59e5db4d74a03d5106cee4bd501090dbeec51cc897edcfd68e559ac939c7c",
    "NEW_BODY6_SLICE_20260907Data.lean":
        "e26bb7bbed18325eee215060d37a16b2a5e71762e2689f464874a1aa1fe5a657",
    "NEW_BODY6_SLICE_20260907.lean":
        "8c7bf133203f0d5104c1ba36e433d117388c36309bed18ad91fac47506542cea",
}


def require(ok, message):
    if not ok:
        raise ValueError(message)


def add(*polys):
    out = {}
    for poly in polys:
        for key, (a, b) in poly.items():
            c, d = out.get(key, ZERO)
            out[key] = a + c, b + d
    return {k: v for k, v in out.items() if v != ZERO}


def scale(poly, s):
    return {k: (s * a, s * b) for k, (a, b) in poly.items() if (s*a, s*b) != ZERO}


def mul(p, q):
    terms = []
    for k, (a, b) in p.items():
        for l, (c, d) in q.items():
            terms.append({tuple(x+y for x, y in zip(k, l)): (a*c-b*d, a*d+b*c)})
    return add(*terms)


def trig(k):
    e = tuple(int(i == k) for i in range(3))
    ne = tuple(-x for x in e)
    return ({e: (F(1, 2), F(0)), ne: (F(1, 2), F(0))},
            {e: (F(0), F(-1, 2)), ne: (F(0), F(1, 2))})


def main():
    for name, expected in PINS.items():
        require(hashlib.sha256((HERE / name).read_bytes()).hexdigest() == expected, name)
    core_path = HERE / "NEW_BODY6_SLICE_STEP6_Core20260907.lean"
    core = core_path.read_text(encoding="utf-8")
    require(re.findall(r"^import (.+)$", core, re.M) == ["Mathlib"], "source-independent import")
    block = core.split("def rows23 : List Row :=", 1)[1].split("def columnFormula", 1)[0]
    parsed = re.findall(r"⟨(\d+),\s*(-?\d+),\s*(-?\d+),\s*(-?\d+),\s*(-?\d+) / (\d+)⟩", block)
    require(len(parsed) == block.count("⟨") == 23, "complete literal parse")
    rows = {}
    ordered = []
    for fields in parsed:
        i, x, y, z, num, den = map(int, fields)
        key = i, x, y, z
        require(0 <= i < 6 and den > 0 and key not in rows, "range/duplicate")
        rows[key] = F(num, den), F(0)
        ordered.append((key, rows[key]))
    selected = []
    with (HERE / "NEW_BODY6_SLICE_20260907.csv").open(encoding="utf-8", newline="") as handle:
        for r in csv.DictReader(handle):
            if r["col"] != "6":
                continue
            require(r["body"] == "6", "wrong source label")
            ns = tuple(int(r[f"nu{k}"]) for k in range(1, 7))
            require(ns[0] == ns[5] == 0 and ns[1] == ns[2], "phase compression")
            key = int(r["row"])-1, ns[1], ns[3], ns[4]
            value = F(int(r["real_num"]), int(r["real_den"])), F(int(r["imag_num"]), int(r["imag_den"]))
            selected.append((key, value))
    require(ordered == selected, "ordered complete CSV column mismatch")
    cx, sx = trig(0)
    cy, sy = trig(1)
    cz, sz = trig(2)
    formulas = [add(mul(cx, cz), scale(mul(mul(sx, cy), sz), -1)),
                mul(sy, sz), mul(sy, sz), cz, {}, {(0, 0, 0): (F(1), F(0))}]
    for i, expression in enumerate(formulas):
        actual = {key[1:]: value for key, value in rows.items() if key[0] == i}
        require(actual == scale(expression, F(1, 60)), f"scalar formula {i}")
    counts = [sum(key[0] == i for key in rows) for i in range(6)]
    require(counts == [12, 4, 4, 2, 0, 1], "counts")
    files = sorted(HERE.glob("NEW_BODY6_SLICE_STEP6_*.lean"))
    for path in files:
        text = path.read_text(encoding="utf-8")
        require(not re.search(r"^\s*(axiom|opaque)\s|\bsorry\b|\badmit\b", text, re.M), "proof placeholder")
    bridge = (HERE / "NEW_BODY6_SLICE_STEP6_Bridge20260907.lean").read_text(encoding="utf-8")
    require("(hall : AllEntriesGramFourierTarget) (hzero : EmptyFourierTarget)" in bridge,
            "global/zero-complement premise removed")
    report = {
        "status": "EXACT_23_ROW_CHECK_PASSED_LEAN_ATTEMPTS_UNCOMPILED",
        "checks": {"core_imports_mathlib_only": True, "csv_column_exact_ordered_match": True,
                   "exact_laurent_formula_match_all_six_rows": True, "counts": counts,
                   "all_36_and_zero_complement_premises_present_as_text": True},
        "new_lean_sha256": {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in files},
        "lean_lake_run": False, "source_endpoint_proven": False,
        "source_binding_proven": False, "source_coverage_proven": False,
        "lean_literal_binding_proven": False, "registry_eligible": False,
        "registry_status": "pending", "formal_certificate_allowed": False,
    }
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
