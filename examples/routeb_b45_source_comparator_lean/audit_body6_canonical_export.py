"""Read-only body-6 export audit; print a proposed artifact bundle to stdout.

No Lean, Lake, Julia, state writer, or exporter main() is invoked. The pinned
artifact-local Python sink is replayed at its pre-accumulation callback.
This is exact coefficient/provenance evidence, never a source theorem.
"""
from __future__ import annotations

import csv
import hashlib
import importlib.util
import io
import json
import sys
from fractions import Fraction as F
from pathlib import Path

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[2]
BASE = ROOT / "artifacts/task_routeb_body_trace_sink_current"
HERE = Path(__file__).resolve().parent
FIELDS = ["body", "row", "col", *[f"nu{k}" for k in range(1, 7)],
          "real_num", "real_den", "imag_num", "imag_den"]
ZERO = (F(0), F(0))
PINS = {
    "outputs/routeB_fourier_mass_body_trace.csv":
        "ae1f9cd7978c4cf23626b5c097eaaf4a2c70de9c8b86a31a61db12997cf4c3b9",
    "source_snapshot/routeB_fourier_mass_full_rational.csv":
        "a986a208b62f585c6ca1b9c81b958710d2043e5bf786ddc930a6fa29f7a232b8",
    "source_snapshot/routeB_fourier_rational_probe.py":
        "9460181770e47be0ecbde43a8a29ef285da1168c3121fab18d5378c671401a7b",
    "source_snapshot/dhport_lib.jl":
        "aebe6db09b2d943448c5d701631109dba8f5eeb070cc66593e5dbaca26485936",
    "routeB_fourier_rational_probe_trace_sink.py":
        "ffd7e06f49fc52e44bfbcbb5cb1be967f909fd4c55ef5b4147c9f9a3141a5f75",
}


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def require(ok, message):
    if not ok:
        raise ValueError(message)


def read_map(path, *, body6=False):
    result = {}
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        require(reader.fieldnames == (FIELDS if body6 else FIELDS[1:]),
                f"invalid headers: {path.name}")
        for row in reader:
            if body6 and row["body"] != "6":
                continue
            key = tuple(int(row[f]) for f in FIELDS[1:9])
            require(all(1 <= x <= 6 for x in key[:2]), "invalid matrix index")
            nums = [int(row[f]) for f in FIELDS[9:]]
            rn, rd, im, den = nums
            require(rd > 0 and den > 0, "nonpositive denominator")
            value = F(rn, rd), F(im, den)
            require((value[0].numerator, value[0].denominator,
                     value[1].numerator, value[1].denominator) == tuple(nums),
                    "noncanonical rational")
            require(value != ZERO and key not in result, "zero or duplicate row")
            result[key] = value
    return result


def csv_bytes(coeff):
    buffer = io.StringIO(newline="")
    writer = csv.writer(buffer, lineterminator="\n")
    writer.writerow(FIELDS)
    for key, (real, imag) in sorted(coeff.items()):
        writer.writerow([6, *key, real.numerator, real.denominator,
                         imag.numerator, imag.denominator])
    return buffer.getvalue()


def main():
    for name, expected in PINS.items():
        require(digest(BASE / name) == expected, f"pinned input drift: {name}")
    body6 = read_map(BASE / "outputs/routeB_fourier_mass_body_trace.csv", body6=True)
    aggregate = read_map(BASE / "source_snapshot/routeB_fourier_mass_full_rational.csv")
    support = json.loads((HERE / "O1_BODY_6_SUPPORT_TARGET.json").read_text())
    state_path = ROOT / "artifacts/routeb_6dof/state.json"
    state_bytes = state_path.read_bytes()
    state = json.loads(state_bytes)
    node = state["nodes"]["3ad9bd4fa1d040da995906fc487913fd"]

    # Only the selected body's callback values are retained. Never execute main().
    spec = importlib.util.spec_from_file_location("body6_pinned_sink",
                                                  BASE / "routeB_fourier_rational_probe_trace_sink.py")
    require(spec is not None and spec.loader is not None, "missing sink loader")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    require(module.MASS[5] == F(3, 20) and module.IVAL[5] / 3 == F(1, 60),
            "body-6 mass/inertia contract drift")
    require(module.DH_A[5] == 0 and module.DH_D[5] == F(7, 100),
            "body-6 endpoint geometry contract drift")
    emitted, callbacks = {}, []

    def sink(body, row, col, term):
        if body != 6:
            return
        callbacks.append((row, col))
        for nu, value in term.items():
            key = (row, col, *nu)
            require(key not in emitted, "duplicate callback coefficient")
            emitted[key] = (value.r, value.i)

    module.build(body_trace_sink=sink)
    require(len(callbacks) == 36 and len(set(callbacks)) == 36,
            "body-6 callback must cover all 36 entries, including empty entries")
    require(emitted == body6, "pre-accumulation body-6 replay differs from CSV")
    require(len(body6) == 610 and len(aggregate) == 610, "snapshot row count drift")
    different = [k for k in sorted(body6.keys() | aggregate.keys())
                 if body6.get(k, ZERO) != aggregate.get(k, ZERO)]
    require(body6.keys() == aggregate.keys() and len(different) == 57,
            "snapshot support/coefficient observation drift")
    require(all(body6.get((k[0], k[1], *[-n for n in k[2:]]), ZERO) == (v[0], -v[1])
                for k, v in body6.items()), "missing conjugate symmetry")
    require(all(body6.get((k[1], k[0], *k[2:]), ZERO) == v
                for k, v in body6.items()), "matrix symmetry failed")
    require(all(k[2] == 0 and k[7] == 0 for k in body6), "q1/q6 support changed")
    diagonal6 = {k[2:]: v for k, v in body6.items() if k[:2] == (6, 6)}
    require(diagonal6 == {(0,) * 6: (F(1, 60), F(0))}, "sixth diagonal drift")

    canonical = csv_bytes(emitted)
    sha = hashlib.sha256(canonical.encode("utf-8")).hexdigest()
    entries = set(k[:2] for k in emitted)
    report = {
        "schema": "routeb.o1.body6.canonical_export_audit.v1",
        "status": "COEFFICIENT_REPLAY_MATCH_SOURCE_THEOREM_OPEN",
        "source_key": support["source_key"], "state_key": support["state_key"],
        "body6_export_key": f"routeb-human-body-fourier:body=6|sha256={sha}|contract=exp(i*nu*q)|regularizer=excluded",
        "replay": {"command": "python -B examples/routeb_b45_source_comparator_lean/audit_body6_canonical_export.py",
                   "callable": "build(body_trace_sink=sink)", "selected_callback_body": 6,
                   "capture_point": "body_term before M[r][c] = add(M[r][c], body_term)",
                   "source_authority": "pinned artifact-local Python copy only",
                   "stdout_only": True, "runtime_julia_run": False},
        "state_snapshot": {"revision": state["revision"],
                           "sha256": hashlib.sha256(state_bytes).hexdigest(),
                           "node_id": node["id"], "node_status": node["status"],
                           "mutated": False},
        "pinned_inputs": {str((BASE / k).relative_to(ROOT)).replace('\\', '/'): v
                          for k, v in PINS.items()},
        "support_artifact": {"sha256": digest(HERE / "O1_BODY_6_SUPPORT_TARGET.json"),
                             "recorded_status": support["status"],
                             "interpretation": "same support alone does not establish aggregate mislabelling"},
        "checks": {"selected_body_rows": len(body6), "frozen_aggregate_rows": len(aggregate),
                   "same_support": True, "different_coefficient_keys": len(different),
                   "pre_accumulation_callback_entries": len(callbacks),
                   "pre_accumulation_replay_equals_selected_csv": True,
                   "nonempty_entries": len(entries),
                   "zero_entries_one_based": [[i, j] for i in range(1, 7) for j in range(1, 7)
                                              if (i, j) not in entries],
                   "conjugate_symmetry": True, "matrix_symmetry": True,
                   "frequency_nu1_nu6_zero": True, "sixth_diagonal_constant": "1/60"},
        "discriminating_coefficient": {"key_row_col_nu": different[0],
                                       "body6": [str(x) for x in body6[different[0]]],
                                       "aggregate": [str(x) for x in aggregate[different[0]]]},
        "payload": {"path": "examples/routeb_b45_source_comparator_lean/O1_BODY_6_CANONICAL_SLICE.csv",
                    "sha256": sha, "encoding": "UTF-8 without BOM; LF",
                    "row_count": len(emitted), "kind": "artifact_local_pre_accumulation_body_slice"},
        "evidence_files": {name: digest(HERE / name) for name in
                           ("audit_body6_canonical_export.py", "RouteBO1Body6CanonicalExportTargets.lean",
                            "RouteBO1PerBodyExactSource.lean", "BodyTraceEvaluator.lean",
                            "RouteBO1PerBodyTraceAdapter.lean", "O1_BODY_6_CANONICAL_EXPORT_CONTRACT.json")},
        "admission": {"source_binding_proven": False, "trace_reification_proven": False,
                      "h_body_6_proven": False, "aggregate_function_lift_proven": False,
                      "compile_status": "NOT_RUN", "lean_lake_run": False,
                      "comparator_accepted": False, "registry_eligible": False,
                      "registry_status": "pending", "formal_certificate_allowed": False},
        "missing_evidence": {"canonical_csv_to_lean_reification": None,
                             "body6_source_to_real_fourier_proof": None,
                             "pinned_compile_and_axiom_receipt": None,
                             "downstream_comparator_receipt": None},
    }
    print(json.dumps({"receipt": report, "canonical_csv": canonical}, indent=2))


if __name__ == "__main__":
    main()
