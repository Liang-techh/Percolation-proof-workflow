"""Body-6-only exact construction. Default: read-only verification; --emit: new files.

Uses the pinned Fourier arithmetic, but never calls build/main, sums bodies,
subtracts other bodies, invokes Lean/Lake/Julia, or reads/writes state/registry.
This is coefficient evidence and uncompiled reification, not a source proof.
"""
from __future__ import annotations

import csv
import hashlib
import importlib.util
import io
import json
import re
import sys
from collections import Counter
from fractions import Fraction as F
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
BASE = ROOT / "artifacts/task_routeb_body_trace_sink_current"
STEM = "NEW_BODY6_SLICE_20260907"
FIELDS = ["body", "row", "col", *[f"nu{k}" for k in range(1, 7)],
          "real_num", "real_den", "imag_num", "imag_den"]
ZERO = (F(0), F(0))
PINS = {
    BASE / "source_snapshot/routeB_fourier_rational_probe.py":
        "9460181770e47be0ecbde43a8a29ef285da1168c3121fab18d5378c671401a7b",
    BASE / "source_snapshot/routeB_fourier_mass_full_rational.csv":
        "a986a208b62f585c6ca1b9c81b958710d2043e5bf786ddc930a6fa29f7a232b8",
    BASE / "outputs/routeB_fourier_mass_body_trace.csv":
        "ae1f9cd7978c4cf23626b5c097eaaf4a2c70de9c8b86a31a61db12997cf4c3b9",
    HERE / "O1_BODY_6_CANONICAL_SLICE.csv":
        "46f59e5db4d74a03d5106cee4bd501090dbeec51cc897edcfd68e559ac939c7c",
    HERE / "O1_BODY_6_CANONICAL_EXPORT_CONTRACT.json":
        "0e03ea7e7a216574f3f76ae433a0b3bef1463675d490739da94a5635aba2eeb1",
    HERE / "O1_BODY_6_SUPPORT_TARGET.json":
        "379d3d4cb91119fb5553ad718908001681ae30477272a6efe6b5ab7526ecfff9",
    HERE / "BodyTraceEvaluator.lean":
        "b9845d37b5dcd16e1f9e142cb2e4d0e5571452993e843c85ac8cd643f6ba5dea",
    HERE / "RouteBO1PerBodyExactSource.lean":
        "c09b84677adef121488b3ceb53e886d0ef0b028c7979d91f8a7f9ba0fbfcd553",
}


def require(ok, message):
    if not ok:
        raise ValueError(message)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def read_rows(path, *, labelled=True, selected=False):
    """Strict integer/rational intake; filtering is explicit, never label rewriting."""
    result = {}
    with path.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        require(reader.fieldnames == (FIELDS if labelled else FIELDS[1:]), "header")
        for row in reader:
            require(all(isinstance(x, str) and re.fullmatch(r"0|-?[1-9][0-9]*", x)
                        for x in row.values()), "integer spelling")
            if labelled:
                require(1 <= int(row["body"]) <= 6, "body range")
                if selected and row["body"] != "6":
                    continue
                require(row["body"] == "6", "wrong body label")
            key = tuple(int(row[f]) for f in FIELDS[1:9])
            rn, rd, im, den = (int(row[f]) for f in FIELDS[9:])
            require(all(1 <= v <= 6 for v in key[:2]), "matrix range")
            require(rd > 0 and den > 0, "denominator sign")
            value = F(rn, rd), F(im, den)
            require((value[0].numerator, value[0].denominator,
                     value[1].numerator, value[1].denominator) == (rn, rd, im, den),
                    "unreduced rational")
            require(value != ZERO and key not in result, "zero/duplicate key")
            result[key] = value
    return result


def independent_body6(p):
    """Direct body-6 Gram: no body loop and no aggregate accumulator."""
    require(p.MASS[5] == F(3, 20) and p.IVAL[5] / 3 == F(1, 60), "inertia")
    require(p.DH_A[5] == 0 and p.DH_D[5] == F(7, 100), "endpoint")
    T = p.eye()
    origins = [[p.const(0) for _ in range(3)]]
    axes = []
    for j in range(6):
        axes.append([T[k][2] for k in range(3)])
        c, s = p.trig(j, p.DH_OFF[j])
        ca, sa = [p.const(v) for v in {-1: (0, -1), 0: (1, 0), 1: (0, 1)}[p.DH_ALPHA[j]]]
        A = [[c, p.scale(p.mul(s, ca), -1), p.mul(s, sa), p.scale(c, p.DH_A[j])],
             [s, p.mul(c, ca), p.scale(p.mul(c, sa), -1), p.scale(s, p.DH_A[j])],
             [p.const(0), sa, ca, p.const(p.DH_D[j])],
             [p.const(0), p.const(0), p.const(0), p.const(1)]]
        T = p.matmul(T, A)
        origins.append([T[k][3] for k in range(3)])
    center = [p.add(origins[5][a], p.scale(axes[5][a], F(7, 200))) for a in range(3)]
    for a in range(3):
        midpoint = p.scale(p.add(origins[5][a], origins[6][a]), F(1, 2))
        require(not p.add(midpoint, p.dneg(center[a])), "endpoint/center identity")
    velocity = [p.cross(axes[i], [p.add(center[a], p.dneg(origins[i][a]))
                                for a in range(3)]) for i in range(6)]
    require(all(not v for v in velocity[5]), "sixth velocity must vanish")
    result, coverage = {}, []
    for i in range(6):
        for j in range(6):
            coverage.append((i + 1, j + 1))
            linear = p.add(*(p.mul(velocity[i][a], velocity[j][a]) for a in range(3)))
            angular = p.add(*(p.mul(axes[i][a], axes[j][a]) for a in range(3)))
            term = p.add(p.scale(linear, F(3, 20)), p.scale(angular, F(1, 60)))
            for nu, value in term.items():
                result[(i + 1, j + 1, *nu)] = (value.r, value.i)
    # Small analytical sixth-column leaf, verified by exact Fourier arithmetic.
    c2, s2 = p.trig(1, 0)
    c3, s3 = p.trig(2, 0)
    c4, s4 = p.trig(3, 0)
    c5, s5 = p.trig(4, 0)
    cp = p.add(p.mul(c2, c3), p.dneg(p.mul(s2, s3)))
    sp = p.add(p.mul(s2, c3), p.mul(c2, s3))
    formulas = [p.add(p.mul(cp, c5), p.dneg(p.mul(p.mul(sp, c4), s5))),
                p.mul(s4, s5), p.mul(s4, s5), c5, {}, p.const(1)]
    for i, expression in enumerate(formulas, 1):
        expected = {nu: (v.r, v.i) for nu, v in p.scale(expression, F(1, 60)).items()}
        actual = {k[2:]: v for k, v in result.items() if k[:2] == (i, 6)}
        require(actual == expected, f"sixth-column scalar formula {i}")
    return result, coverage


def serialize(rows):
    stream = io.StringIO(newline="")
    writer = csv.writer(stream, lineterminator="\n")
    writer.writerow(FIELDS)
    for k, (a, b) in sorted(rows.items()):
        writer.writerow([6, *k, a.numerator, a.denominator, b.numerator, b.denominator])
    return stream.getvalue().encode("utf-8")


def lean_data(rows, digest):
    lines = ["import RouteBO1Body6CanonicalExportTargets", "", "set_option autoImplicit false", "",
             f"namespace {STEM}Data", "", "noncomputable section", "",
             "open RouteBO1PerBodyTraceGenerated RouteBO1Body6CanonicalExportTargets", "",
             "/- UNCOMPILED data candidate. No Lean/Lake invocation or proof receipt.",
             f"   Independently constructed body-6 CSV SHA-256: {digest}",
             "   Each Fin index is range-checked explicitly; numerator/denominator labels survive. -/", "",
             "def mkRow (i j : Fin 6) (nu : Fin 6 → ℤ) (rn rd im den : ℤ) : BodyTraceRow :=",
             "  { body := ⟨5, by decide⟩, row := i, col := j, frequency := nu,",
             "    realCoeff := ⟨rn, rd⟩, imagCoeff := ⟨im, den⟩ }", "",
             "def taggedRows : List BodyTraceRow :=", "  ["]
    for n, (k, (a, b)) in enumerate(sorted(rows.items())):
        nu = ", ".join(f"({v} : ℤ)" for v in k[2:])
        values = " ".join(f"({v})" for v in (a.numerator, a.denominator, b.numerator, b.denominator))
        comma = "," if n + 1 < len(rows) else ""
        lines.append(f"    mkRow ⟨{k[0]-1}, by decide⟩ ⟨{k[1]-1}, by decide⟩ ![{nu}] {values}{comma}")
    lines += ["  ]", "", "def toCanonical (r : BodyTraceRow) : CanonicalRow :=",
              "  { row := r.row, col := r.col, frequency := r.frequency,",
              "    realCoeff := r.realCoeff.toRat, imagCoeff := r.imagCoeff.toRat }", "",
              "def canonicalRows : List CanonicalRow := taggedRows.map toCanonical", "",
              "def sixthColumnRows : List CanonicalRow :=",
              "  canonicalRows.filter (fun r => decide (r.col = (5 : Fin 6)))", "",
              "end", f"end {STEM}Data", ""]
    return "\n".join(lines).encode("utf-8")


def main():
    require(sys.argv[1:] in ([], ["--emit"]), "usage: script [--emit]")
    for path, digest in PINS.items():
        require(sha(path.read_bytes()) == digest, f"pinned input drift: {path.name}")
    spec = importlib.util.spec_from_file_location("body6_slice_exact_arithmetic", next(iter(PINS)))
    require(spec is not None and spec.loader is not None, "loader")
    p = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(p)
    rows, coverage = independent_body6(p)
    canonical = read_rows(HERE / "O1_BODY_6_CANONICAL_SLICE.csv")
    legacy = read_rows(BASE / "outputs/routeB_fourier_mass_body_trace.csv", selected=True)
    aggregate = read_rows(BASE / "source_snapshot/routeB_fourier_mass_full_rational.csv", labelled=False)
    require(rows == canonical == legacy, "independent body-6 coefficient mismatch")
    differences = sorted(k for k in rows.keys() | aggregate.keys()
                         if rows.get(k, ZERO) != aggregate.get(k, ZERO))
    require(rows.keys() == aggregate.keys() and len(differences) == 57, "negative control drift")
    require(len(rows) == 610 and len(set(coverage)) == 36, "coverage drift")
    require(all(rows.get((k[1], k[0], *k[2:])) == v for k, v in rows.items()), "transpose")
    require(all(rows.get((*k[:2], *[-x for x in k[2:]])) == (v[0], -v[1])
                for k, v in rows.items()), "conjugacy")
    require(all(k[2] == k[7] == 0 for k in rows), "q1/q6 frequencies")
    payload = serialize(rows)
    require(payload == (HERE / "O1_BODY_6_CANONICAL_SLICE.csv").read_bytes(), "canonical bytes")
    data = lean_data(rows, sha(payload))
    # Decode every emitted literal back to CSV labels; no Lean elaboration claim.
    decoded = []
    for line in data.decode().splitlines():
        if line.startswith("    mkRow "):
            indices, rest = line.split("![", 1)
            i, j = map(int, re.findall(r"⟨([0-9]+),", indices))
            ns, coeff = rest.split("]", 1)
            decoded.append((6, i + 1, j + 1, *map(int, re.findall(r"\((-?[0-9]+) : ℤ\)", ns)),
                            *map(int, re.findall(r"\((-?[0-9]+)\)", coeff))))
    expected = [tuple(map(int, row)) for row in list(csv.reader(io.StringIO(payload.decode())))[1:]]
    require(decoded == expected, "generated Lean literal roundtrip")
    counts = Counter(k[:2] for k in rows)
    contract = json.loads((HERE / "O1_BODY_6_CANONICAL_EXPORT_CONTRACT.json").read_text())
    support = [{"row": i, "col": j, "count": counts[i, j],
                "frequencies": [list(k[2:]) for k in sorted(rows) if k[:2] == (i, j)]}
               for i, j in coverage]
    report = {
        "schema": "routeb.o1.NEW_BODY6_SLICE.v1",
        "status": "EXACT_BODY6_COEFFICIENTS_AND_UNCOMPILED_REIFICATION_SOURCE_OPEN",
        "construction": "Direct body-6 Gram; pinned arithmetic only; no build/main or aggregate subtraction",
        "source_authority": "artifact-local rational Python DH construction, not Lean or deployed Julia",
        "source_key": contract["identity"]["source_key"],
        "state_key": contract["identity"]["state_key"],
        "state_key_role": "inherited consumer context only; state not read or changed",
        "body6_export_key": f"routeb-human-body-fourier:body=6|sha256={sha(payload)}|contract=exp(i*nu*q)|regularizer=excluded",
        "contract": {**contract["source_semantics"], **contract["canonical_csv"],
                     "emission_point": "Direct body-6-only Gram loop in NEW_BODY6_SLICE_20260907.py",
                     "requested_theorem_domain": "forall q : Fin 6 -> Real; all i,j : Fin 6"},
        "input_sha256": {str(k.relative_to(ROOT)).replace("\\", "/"): v for k, v in PINS.items()},
        "generator_sha256": sha(Path(__file__).read_bytes()),
        "payload_sha256": sha(payload), "lean_data_sha256": sha(data),
        "checks": {"independent_equals_canonical_and_legacy_csv": True,
                   "python_literal_roundtrip": True, "canonical_sorted_unique_keys": True,
                   "all_36_entry_constructions": True, "row_count": len(rows),
                   "nonempty_entries": len(counts), "transpose_and_conjugacy": True,
                   "nu1_nu6_zero": True, "sixth_column_scalar_formulas_exact": True,
                   "sixth_column_rows": sum(k[1] == 6 for k in rows),
                   "sixth_column_equals_aggregate": all(v == aggregate[k] for k, v in rows.items() if k[1] == 6)},
        "negative_control": {
            "aggregate_admissible_as_body6": False,
            "legacy_aggregate_shaped_bucket_admissible_as_source_proof": False,
            "same_support": True, "different_coefficient_keys": len(differences),
            "interpretation": "610-row count/support is not source binding; legacy bucket equals direct body-6 data but is not a theorem",
            "witness": {"row_col_nu": differences[0], "body6": list(map(str, rows[differences[0]])),
                        "aggregate": list(map(str, aggregate[differences[0]]))}},
        "support_all_36_entries": support,
        "admission": {"source_binding_proven": False, "source_support_coverage_proven": False,
                      "lean_reification_proven": False, "h_body_6_proven": False,
                      "lean_lake_run": False, "compile_status": "NOT_RUN",
                      "comparator_accepted": False, "registry_status": "pending",
                      "registry_eligible": False, "formal_certificate_allowed": False},
        "minimal_missing": ["Lean endpoint/center source witness and source-to-Gram bridge",
                            "Gram-to-canonical-Fourier proof over all 36 entries including four empty entries",
                            "Lean list/label binding and canonical-to-existing-trace proof",
                            "Future authorized pinned compile/axiom and same-key comparator receipts"],
    }
    outputs = {HERE / f"{STEM}.csv": payload, HERE / f"{STEM}Data.lean": data,
               HERE / f"{STEM}.json": (json.dumps(report, indent=2) + "\n").encode()}
    if sys.argv[1:] == ["--emit"]:
        require(all(not path.exists() for path in outputs), "refusing to overwrite existing output")
        for path, content in outputs.items():
            require(path.parent == HERE and path.name.startswith("NEW_BODY6_SLICE_"), "write scope")
            with path.open("xb") as handle:
                handle.write(content)
    else:
        for path, content in outputs.items():
            require(path.read_bytes() == content, f"artifact drift: {path.name}")
    print(json.dumps({"status": report["status"], "checks": report["checks"],
                      "negative_control": report["negative_control"],
                      "payload_sha256": sha(payload), "lean_data_sha256": sha(data),
                      "lean_lake_run": False}, indent=2))


if __name__ == "__main__":
    main()
