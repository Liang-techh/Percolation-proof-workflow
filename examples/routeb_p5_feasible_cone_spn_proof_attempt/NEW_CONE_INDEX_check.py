"""Read-only exact audit of the P5 36-to-18 INDEX interface (stdlib only).

Finite exhaustive checks and exact boundary probes are not Lean verification.
No K_path, certificate acceptance, source artifact, state or registry output.
Run with python -B NEW_CONE_INDEX_check.py --self-test; output is stdout only.
"""

from __future__ import annotations

import argparse
from collections import Counter
from fractions import Fraction
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
POSITIVE = (0, 2, 3)
REVERSE = (1, 0, 5, 4, 3, 2)
CONES = tuple(itertools.product(range(6), repeat=2))
REPS = tuple(itertools.product(range(3), range(6)))
SIGNED = tuple(itertools.product(REPS, (False, True)))
FROZEN = {
    "P5FeasibleConeSPN.lean": "fa9d990cfb2adb6fce049b4c6feb9ab2dfed3c2bcd14b059a0a8332138e1e824",
    "NEW_exact_geometry_spn.py": "263fac727c1c3068043c02a63dade5995a22e1e7e9a879682ac3e69bafd54f42",
}


class Rejected(ValueError):
    pass


def need(ok, message):
    if not ok:
        raise Rejected(message)


def pair(value, bounds):
    need(isinstance(value, tuple) and len(value) == 2, "index must be a pair")
    need(all(type(x) is int and 0 <= x < n for x, n in zip(value, bounds)),
         "index out of range or not an exact integer")
    return value


def flip(c):
    a, b = pair(c, (6, 6))
    return REVERSE[a], REVERSE[b]


def representative_cone(r):
    a, b = pair(r, (3, 6))
    return POSITIVE[a], b


def select(c):
    a, _ = pair(c, (6, 6))
    reversed_sign = a not in POSITIVE
    oriented = flip(c) if reversed_sign else c
    return (POSITIVE.index(oriented[0]), oriented[1]), reversed_sign


def expand(p):
    need(isinstance(p, tuple) and len(p) == 2 and type(p[1]) is bool,
         "signed index requires a representative and a Bool")
    c = representative_cone(p[0])
    return flip(c) if p[1] else c


def check_expansion_table(table):
    need(isinstance(table, dict) and set(table) == set(SIGNED), "signed domain must have all 36 keys")
    for c in table.values():
        pair(c, (6, 6))
    need(Counter(table.values()) == Counter(CONES), "multiplicity-preserving label cover failed")
    for p, c in table.items():
        need(select(c) == p, "canonical orientation/representative mismatch")


def finite_checks():
    table = {p: expand(p) for p in SIGNED}
    check_expansion_table(table)
    for c in CONES:
        need(flip(flip(c)) == c and flip(c) != c, "global sign involution not free")
        need(expand(select(c)) == c, "left inverse")
        r, sign = select(c)
        need(select(flip(c)) == (r, not sign), "global sign must toggle orientation")
        for d in CONES:
            need((select(c)[0] == select(d)[0]) == (c == d or c == flip(d)),
                 "representative equality not exactly a sign orbit")
    fibers = Counter(select(c)[0] for c in CONES)
    need(fibers == Counter({r: 2 for r in REPS}), "fiber cardinality")
    # Free additive-monoid basis identity: compares every coefficient, for any weights.
    lhs = Counter(CONES)
    rhs = Counter(c for r in REPS for c in (representative_cone(r), flip(representative_cone(r))))
    need(lhs == rhs, "universal indexed-sum coefficient identity")
    # All object values may coincide: still retain the 18 representative labels.
    constant_objects = [(r, "same-object") for r in REPS]
    need(len(constant_objects) == 18 and len({v for _, v in constant_objects}) == 1,
         "specialization collision fixture")
    return dict(cone_indices=36, representatives=18, orientations_per_representative=2,
                left_inverse_cases=36, right_inverse_cases=36, orbit_relation_pairs=1296,
                arbitrary_weight_identity="all 36 free-monoid coefficients equal",
                coincident_object_values=1, retained_representative_labels=18)


def lean_text_checks(old, new, geometry):
    # Reuse the reviewed restricted reader for the OLD table, not its proof bodies.
    geometry["lean_table_checks"](old)

    def definition(source, name):
        found = re.findall(r"^def " + name + r"\b[^\n]*\n(.*?)(?=\n\n)", source, re.M | re.S)
        need(len(found) == 1, "missing/ambiguous definition " + name)
        return found[0].strip()

    for name in ("cx", "cy", "reverse"):
        need(definition(old, name) == definition(new, name), "reviewed table mismatch: " + name)
    rep = re.findall(r"^def representativeFirst[^\n]*:= (.+)$", new, re.M)
    need(rep == ["![.pp, .pnPos, .pnNeg] i"], "representative first-channel order")
    branches = re.findall(
        r"^  \| \.(\w+) => \(\(([012]), (c\.2|reverse c\.2)\), (true|false)\)$", new, re.M
    )
    need(len(branches) == 6 and {b[0] for b in branches} == set(NAMES), "selection branch syntax")
    for name, rank, second, orientation in branches:
        for b in range(6):
            parsed = ((int(rank), REVERSE[b] if second.startswith("reverse") else b), orientation == "true")
            need(parsed == select((NAMES.index(name), b)), "selection table mismatch")
    chart = definition(new, "chart")
    interleave = definition(old, "interleave")
    need(chart == interleave, "physical/orthant coordinate order")
    return ["cx", "cy", "reverse", "representativeFirst", "select (36 branches)", "chart/interleave"]


def boundary_checks(geometry):
    # 13 strata representatives per channel: origin, six rays, six interiors.
    # Diagnostic probes only. Universal real coverage is proved in the NEW Lean file.
    strata = ((0, 0), (1, 0), (0, 1), (-1, 0), (0, -1), (1, -1), (-1, 1),
              (1, 1), (-1, -1), (2, -1), (1, -2), (-1, 2), (-2, 1))

    def witnesses(z):
        out = []
        for c in CONES:
            inv = geometry["interleave"](geometry["J"], c)
            u = tuple(geometry["mv"](inv, z))
            if all(v >= 0 for v in u):
                t = geometry["interleave"](geometry["G"], c)
                need(tuple(geometry["mv"](t, u)) == z, "exact witness reconstruction")
                out.append((c, u))
        return out

    histogram = Counter()
    for v4, v5 in itertools.product(strata, repeat=2):
        z = tuple(map(Fraction, (v4[0], v5[0], v4[1], v5[1])))
        original = witnesses(z)
        need(original, "uncovered boundary probe")
        signed = [(select(c), u) for c, u in original]
        recovered = [(expand(p), u) for p, u in signed]
        need(Counter(original) == Counter(recovered), "boundary witness multiplicity changed")
        need(len(set(signed)) == len(original), "boundary witness collision")
        histogram[len(original)] += 1
    origin = witnesses((Fraction(0),) * 4)
    need(len(origin) == 36, "origin must keep all 36 labels")
    return dict(exact_boundary_probes=169, probes_are_not_a_universal_proof=True,
                multiplicity_histogram=dict(sorted(histogram.items())), origin_labels=36)


def negative_controls(new, old, geometry):
    rejected = []

    def reject(label, action):
        try:
            action()
        except Rejected:
            rejected.append(label)
        else:
            raise Rejected("negative control accepted: " + label)

    good = {p: expand(p) for p in SIGNED}
    missing = dict(good)
    missing.pop(((0, 0), True))
    reject("missing_orientation", lambda: check_expansion_table(missing))
    duplicate = dict(good)
    duplicate[((0, 0), True)] = duplicate[((0, 0), False)]
    reject("duplicate_index_in_cover", lambda: check_expansion_table(duplicate))
    one_channel = {p: ((REVERSE[representative_cone(p[0])[0]], representative_cone(p[0])[1])
                       if p[1] else representative_cone(p[0])) for p in SIGNED}
    reject("only_first_channel_flipped", lambda: check_expansion_table(one_channel))
    reject("bool_cone_index", lambda: select((False, 0)))
    reject("negative_cone_index", lambda: select((-1, 0)))
    reject("out_of_range_representative", lambda: expand(((3, 0), False)))
    reject("integer_orientation", lambda: expand(((0, 0), 1)))
    reject("discard_orientation_at_origin", lambda: need(Counter(representative_cone(r) for r in REPS)
                                                         == Counter(CONES), "lost origin labels"))
    reject("deduplicate_equal_object_values", lambda: need(len(set(["same-object"] * 18)) == len(REPS),
                                                         "lost representative labels"))
    altered = new.replace("| .npPos => ((2, reverse c.2), true)", "| .npPos => ((1, reverse c.2), true)", 1)
    need(altered != new, "selection mutation did not apply")
    reject("Lean_wrong_representative", lambda: lean_text_checks(old, altered, geometry))
    altered_map = new.replace(".pnPos, a, b => a + b", ".pnPos, a, b => a - b", 1)
    reject("Lean_wrong_chart", lambda: lean_text_checks(old, altered_map, geometry))
    return rejected


def run():
    before = {name: hashlib.sha256((ROOT / name).read_bytes()).hexdigest() for name in FROZEN}
    need(before == FROZEN, "reviewed input changed; re-audit required")
    geometry = runpy.run_path(str(ROOT / "NEW_exact_geometry_spn.py"), run_name="p5_geometry_read_only")
    old = (ROOT / "P5FeasibleConeSPN.lean").read_text(encoding="utf-8")
    new = (ROOT / "NEW_CONE_INDEX_Core.lean").read_text(encoding="utf-8")
    need(geometry["ALL_CONES"] == CONES and geometry["REVERSE"] == REVERSE,
         "reviewed cone enumeration mismatch")
    need(tuple(representative_cone(r) for r in REPS) == geometry["REPS"],
         "Fin3-to-original-cone representative correspondence")
    result = dict(finite=finite_checks(),
                  restricted_Lean_text_checks=lean_text_checks(old, new, geometry),
                  boundaries=boundary_checks(geometry),
                  negative_controls_rejected=negative_controls(new, old, geometry))
    after = {name: hashlib.sha256((ROOT / name).read_bytes()).hexdigest() for name in FROZEN}
    need(before == after, "input changed during audit")
    return dict(result="pass", **result, input_sha256=after,
                new_sha256={name: hashlib.sha256((ROOT / name).read_bytes()).hexdigest()
                            for name in ("NEW_CONE_INDEX_Core.lean", Path(__file__).name)},
                check_type="finite_index_arithmetic_and_boundary_probes_only",
                lean_executed_by_this_checker=False, kernel_verified_by_this_checker=False,
                concrete_K_path_bound=False, source_coverage_verified=False,
                registry_eligible=False, registry_mutated=False, P5_P8_M4_closed=False)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--self-test", action="store_true", required=True)
    parser.parse_args()
    try:
        result = run()
    except (Rejected, OSError, ValueError, TypeError, KeyError) as exc:
        print(json.dumps(dict(result="rejected_or_uncheckable", reason=str(exc),
                              registry_eligible=False, concrete_K_path_bound=False,
                              P5_P8_M4_closed=False), indent=2))
        return 1
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
