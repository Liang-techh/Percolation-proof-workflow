"""Read-only source-theorem seam inventory, never an exporter or proof verifier.

python -B NEW_SEAM_source.py [intake.json]
Exit 3: pending, including complete candidates. Exit 2: malformed input/source.
Only stdout is produced. No Julia, numeric evaluation, constants export or writes.
"""
from __future__ import annotations

import argparse
from hashlib import sha256
import json
from pathlib import Path
import sys

sys.dont_write_bytecode = True
import NEW_source_intake as intake

base = intake.base
HERE = Path(__file__).resolve().parent
SCHEMA = "routeb.o0.h_acc.source_theorem_seam.review.v1"

# These are literal source selectors, not exported scalar expressions or values.
# Byte ranges are zero-based, half-open, in the raw source file (including CRLF).
SITES = {
    "frame_initial": (32, "Matrix{Float64}(I, 4, 4)"),
    "origin_initial": (33, "zeros(3, 7)"),
    "axis_initial": (34, "zeros(3, 6)"),
    "frame_loop": (35, "for ii in 1:6"),
    "axis_parent": (36, "z[:, ii] = Tc[end][1:3, 3]"),
    "joint_angle": (37, "th = q[ii] + DH[ii, 1]"),
    "dh_bindings": (37, "d = DH[ii, 2]; a = DH[ii, 3]; al = DH[ii, 4]"),
    "trig": (38, "ct, st, ca, sa = cos(th), sin(th), cos(al), sin(al)"),
    "dh_transform": (39, "A = [ct -st*ca st*sa a*ct; st ct*ca -ct*sa a*st; 0 sa ca d; 0 0 0 1]"),
    "frame_push": (40, "push!(Tc, Tc[end] * A)"),
    "origin_current": (41, "o[:, ii+1] = Tc[end][1:3, 4]"),
    "frame_call": (47, "Tc, o, z = fk_frames(q)"),
    "accumulator_initial": (48, "M = zeros(6, 6)"),
    "body_loop": (49, "for ii in 1:6"),
    "com": (50, "pcom = 0.5 .* (o[:, ii] + o[:, ii+1])"),
    "rotation_alias": (51, "Ri = Tc[ii+1][1:3, 1:3]"),
    "inertia": (52, "Ii = (I_val[ii] / 3) .* Matrix{Float64}(I, 3, 3)"),
    "linear_initial": (53, "Jv = zeros(3, 6)"),
    "angular_initial": (53, "Jw = zeros(3, 6)"),
    "active_prefix": (54, "for jj in 1:ii"),
    "linear_column": (55, "Jv[:, jj] = cross(z[:, jj], pcom - o[:, jj])"),
    "angular_alias": (56, "Jw[:, jj] = z[:, jj]"),
    "translation": (58, "m[ii] .* (Jv' * Jv)"),
    "rotation": (58, "Jw' * (Ri * Ii * Ri') * Jw"),
    "body_sum": (58, "m[ii] .* (Jv' * Jv) + Jw' * (Ri * Ii * Ri') * Jw"),
    "accumulator_update": (58, "M += m[ii] .* (Jv' * Jv) + Jw' * (Ri * Ii * Ri') * Jw"),
    "body_loop_end": (59, "end"),
}

OBLIGATIONS = {
    "SEAM_SOURCE": "Pinned-source idealization, binding/lifetime and selected expression semantics; spans alone insufficient.",
    "SEAM_EVAL": "Total topological Real evaluator with the nine op equations and same-input node identity congruence.",
    "SEAM_ARRAY": "Source literals, DH entries, frame products, origins, COM, cross and inertia scalarization.",
    "SEAM_ALIAS": "Parent/current frame and active-prefix occurrences denote their referenced scalar nodes.",
    "SEAM_BODY": "Every translation/rotation node evaluates to the unsimplified indexed matrix term; then B addition.",
    "SEAM_FOLD": "S0, ordered coordinatewise six-step fold and final S6 alias imply target equality, conditional on body refinement.",
}


def source_sites(source):
    base.require(sha256(source).hexdigest() == base.SOURCE_SHA, "pinned source bytes mismatch")
    lines = source.splitlines(keepends=True)
    offsets, offset = [], 0
    for line in lines:
        offsets.append(offset)
        offset += len(line)
    result = {}
    for name, (line, token) in SITES.items():
        encoded = token.encode("utf-8")
        raw_line = lines[line - 1]
        base.require(raw_line.count(encoded) == 1, "source selector not unique: " + name)
        column = raw_line.index(encoded)
        start = offsets[line - 1] + column
        end = start + len(encoded)
        result[name] = {
            "source_span": base.span(source, line, line),
            "byte_start": start, "byte_end_exclusive": end,
            "byte_column_start": column, "byte_column_end_exclusive": column + len(encoded),
            "fragment_sha256": sha256(source[start:end]).hexdigest(),
            "source_text": token,
        }
    return result


def occurrence_line(stage, coordinate):
    """Required defining/use line of a *final mapped entry*, not its scalar node."""
    if stage == "Tc":
        return 32 if coordinate[0] == 0 else 40
    if stage == "o":
        return 33 if coordinate[0] == 0 else 41
    if stage in ("Jv", "Jw"):
        return 53 if coordinate[2] > coordinate[0] else (55 if stage == "Jv" else 56)
    return {"A": 39, "z": 36, "COM": 50, "Ri": 51, "Ii": 52,
            "translation": 58, "rotation": 58}[stage]


def occurrence_gaps(mapping):
    """Call only after intake.inspect. A seam gap is not a new v1 rejection rule."""
    if mapping is None:
        return None
    gaps = []
    for stage, rows in mapping.items():
        for row in rows:
            line = occurrence_line(stage, row["coordinate"])
            span = row["source_span"]
            if not span["start_line"] <= line <= span["end_line"]:
                gaps.append({"stage": stage, "coordinate": row["coordinate"],
                             "required_line": line, "submitted_span": span})
    return gaps


def inspect(raw, source):
    # Strict duplicate/nonfinite parsing and the unchanged v1 semantic validator.
    doc = base.decode(raw)
    checks, blockers = intake.inspect(doc, source)
    sites = source_sites(source)
    gaps = occurrence_gaps(doc["array_mapping"])
    if gaps:
        blockers.append("SEAM_REQUIRED_OCCURRENCE_LINES_NOT_COVERED")
    blockers.extend(OBLIGATIONS)
    return {
        "schema": SCHEMA, "status": "pending", "theorem_status": "OPEN_H_ACC",
        "checker_exit_code": 3,
        "scope": "raw_source_locations_and_existing_candidate_consistency_only",
        "source_sha256": sha256(source).hexdigest(),
        "submission_sha256": sha256(raw).hexdigest(),
        "admission": intake.template()["admission"],
        "candidate_checks": checks,
        "source_export_sha256": doc["source_export_sha256"],
        "source_locations": sites,
        "constant_declaration_spans": {
            "DH": base.span(source, 6, 11), "m": base.span(source, 12, 12),
            "I_val": base.span(source, 13, 13)},
        "occurrence_line_gaps": gaps,
        "required_witnesses": {key: {"obligation": value, "artifact": None, "verified": False}
                               for key, value in OBLIGATIONS.items()},
        "blockers": list(dict.fromkeys(blockers)),
        "execution": {"julia": False, "lean_lake": False, "files_written": 0},
        "generated_source_export": None, "generated_constant_values": None,
        "generated_runtime_observation": None,
    }


def audit(path, source_path=base.SOURCE):
    try:
        report = inspect(path.read_bytes(), source_path.read_bytes())
    except FileNotFoundError as exc:
        report = {"schema": SCHEMA, "status": "pending", "checker_exit_code": 3,
                  "blockers": ["MISSING_ARTIFACT: " + str(exc)],
                  "admission": intake.template()["admission"]}
    except (OSError, ValueError, TypeError, KeyError, IndexError, ZeroDivisionError,
            OverflowError, RecursionError) as exc:
        report = {"schema": SCHEMA, "status": "rejected", "checker_exit_code": 2,
                  "blockers": [str(exc)], "admission": intake.template()["admission"]}
    report["implementation_sha256"] = {
        path.name: sha256(path.read_bytes()).hexdigest()
        for path in (Path(__file__), Path(intake.__file__), Path(base.__file__),
                     HERE / "NEW_INTAKE_SCHEMA.json")}
    return report, report["checker_exit_code"]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("submission", nargs="?", type=Path, default=HERE / "NEW_INTAKE.json")
    args = parser.parse_args()
    report, code = audit(args.submission)
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return code


if __name__ == "__main__":
    raise SystemExit(main())
