"""Read-only obligation-plan audit. Not an exporter or a theorem verifier.

Only prints JSON. Exit 3 = pending, 2 = malformed input or source drift.
No source values, graph nodes, Julia traces or proof certificates are generated.
"""
from __future__ import annotations

import argparse
from hashlib import sha256
import json
from pathlib import Path
import sys

sys.dont_write_bytecode = True
import NEW_SEAM_source as seam

base, intake = seam.base, seam.intake
HERE = Path(__file__).resolve().parent
SCHEMA = "routeb.o0.h_acc.source_seam.obligation_plan.v1"

# This dependency list is a proof PLAN, not the exported E_star scalar DAG.
# Each premise is to be proved under the same independently specified bundle K.
RULES = [
    ("K", [], "Independent source idealization, target, input and environment definitions; bind G/O/U separately."),
    ("EVAL", ["K"], "Total Real evaluator equations for all nine ops; equal node IDs imply equal values at the same q."),
    ("SOURCE_ARRAY", ["K"], "Source-token binding, A/Tc/o/COM/cross/Ii semantics, frame and inner-loop invariants; no graph-defined source state."),
    ("USE", ["EVAL", "SOURCE_ARRAY"], "Instance-indexed z/Ri/Jw reads and inactive zeros denote the mapped nodes and persist to their consumers."),
    ("OPERANDS", ["EVAL", "SOURCE_ARRAY", "USE"], "Scalar lowerings of translation and unsimplified rotation equal independently interpreted line-58 operands for every b,r,c."),
    ("BODY", ["EVAL", "OPERANDS"], "Checked B=add(translation,rotation) gives eval(B)=Lsrc+Rsrc; cannot produce operand premises."),
    ("SOURCE_LOOP", ["K"], "Independent M source-state recurrence from allocation and six += steps, including binding preservation and termination before line 60."),
    ("FOLD", ["EVAL", "BODY", "SOURCE_LOOP"], "Checked zero, ordered predecessor additions, update bindings and final alias imply eval(Sb)=Msrc_b by induction."),
    ("TARGET", ["SOURCE_ARRAY", "SOURCE_LOOP"], "Identify independently defined M_NE^0 with Msrc_6; no rename of the source or graph result as target."),
    ("H_ACC_EXPR", ["FOLD", "TARGET"], "For each admitted input, E_star=M_NE^0, conditional on all preceding proved instances; no rounding conclusion."),
]


def rule_plan():
    seen, out = set(), []
    for name, dependencies, conclusion in RULES:
        base.require(name not in seen and all(d in seen for d in dependencies),
                     "duplicate, forward or cyclic obligation dependency")
        seen.add(name)
        out.append({"id": name, "depends_on": dependencies, "required_conclusion": conclusion,
                    "artifact": None, "verified": False})
    return out


def use_families(sites):
    """Quantified required uses, never a synthetic array_mapping or node list."""
    specs = [
        ("z", "axis_parent", "fk_frames: ii=j; j=1..6,k=1..3", 18,
         "pre-push read, post-copy value", "Tc has j frames; last frame is j-1",
         "N_z(j,k)=N_Tc(j-1,k,3)", "preserve Tc old entries and z column j through return and its mass_matrix consumers"),
        ("Ri", "rotation_alias", "mass_matrix: ii=b; b=1..6,k,l=1..3", 54,
         "post-slice value", "fk_frames returned; Julia Tc[b+1] is frame b",
         "N_Ri(b,k,l)=N_Tc(b,k,l)", "preserve selected block value until rotation RHS evaluation"),
        ("Jw_active", "angular_alias", "mass_matrix: ii=b,jj=j; 1<=j<=b<=6,k=1..3", 63,
         "post-column-copy value", "same-call z; current body has fresh Jw",
         "N_Jw(b,k,j)=N_z(j,k)", "later jj writes other columns; preserve column j until line 58"),
        ("Jw_inactive", "angular_initial", "mass_matrix: ii=b; 1<=b<j<=6,k=1..3", 45,
         "post-allocation through RHS", "inner loop visits only 1..b",
         "mapped node is explicit rat zero", "no line-56 assignment instance for this j"),
        ("Jv_inactive", "linear_initial", "mass_matrix: ii=b; 1<=b<j<=6,k=1..3", 45,
         "post-allocation through RHS", "inner loop visits only 1..b",
         "mapped node is explicit rat zero", "no line-55 assignment instance for this j"),
    ]
    return [{"family": name, "site": site, "source_location": sites[site],
             "quantifier": quantifier, "required_coordinate_count": count,
             "phase": phase, "source_state_premise": premise,
             "existing_candidate_predicate": predicate, "preservation_obligation": preservation,
             "actual_node_binding": None, "semantic_witness": None, "verified": False}
            for name, site, quantifier, count, phase, premise, predicate, preservation in specs]


def inspect(raw, source):
    original = seam.inspect(raw, source)
    doc = base.decode(raw)
    sites = original["source_locations"]
    # Distinguish four occurrences that v1 deliberately gives the same line span.
    a, b, total, update = [sites[k] for k in
                          ("translation", "rotation", "body_sum", "accumulator_update")]
    base.require(update["byte_start"] < total["byte_start"] == a["byte_start"] <
                 a["byte_end_exclusive"] < b["byte_start"] < b["byte_end_exclusive"] ==
                 total["byte_end_exclusive"] == update["byte_end_exclusive"],
                 "line-58 occurrence nesting mismatch")
    # Null is deliberately not hash(null) and is not a claim of an observed export.
    bindings = {key: None if doc[key] is None else base.digest(doc[key])
                for key in ("source_export", "array_mapping", "source_updates")}
    return {
        "schema": SCHEMA, "status": "pending", "checker_exit_code": 3,
        "scope": "static_source_locations_and_proposed_semantic_obligations_only",
        "source_sha256": original["source_sha256"],
        "submission_sha256": original["submission_sha256"],
        "canonical_component_bindings": bindings,
        "unprovided_semantic_bindings": {k: None for k in
            ("real_evaluator", "source_idealization", "target_definition", "input_interpretation",
             "source_environment", "proof_dependency_manifest")},
        "candidate_checks": original["candidate_checks"],
        "occurrence_line_gaps": original["occurrence_line_gaps"],
        "use_key_fields": ["bundle_K", "procedure", "site_fragment", "loop_indices", "phase", "coordinate", "node_id"],
        "use_families": use_families(sites),
        "line58_sites": {k: sites[k] for k in ("translation", "rotation", "body_sum", "accumulator_update")},
        "body_fold_coverage": {"translation": 216, "rotation": 216, "body": 216,
                               "accumulator": 216, "final": 36, "source_updates": 6},
        "obligation_plan": rule_plan(),
        "blockers": original["blockers"],
        "admission": intake.template()["admission"],
        "generated_source_export": None, "generated_constants": None,
        "runtime_evidence": None, "proof_evidence": None,
        "execution": {"julia": False, "lean_lake": False, "files_written": 0},
    }


def audit(path=HERE / "NEW_INTAKE.json", source_path=base.SOURCE):
    try:
        result = inspect(path.read_bytes(), source_path.read_bytes())
    except FileNotFoundError as exc:
        result = {"schema": SCHEMA, "status": "pending", "checker_exit_code": 3,
                  "blockers": ["MISSING_ARTIFACT: " + str(exc)], "admission": intake.template()["admission"]}
    except (OSError, ValueError, TypeError, KeyError, IndexError, ZeroDivisionError,
            OverflowError, RecursionError) as exc:
        result = {"schema": SCHEMA, "status": "rejected", "checker_exit_code": 2,
                  "blockers": [str(exc)], "admission": intake.template()["admission"]}
    result["implementation_sha256"] = {p.name: sha256(p.read_bytes()).hexdigest()
        for p in (Path(__file__), Path(seam.__file__), Path(intake.__file__), Path(base.__file__),
                  HERE / "NEW_INTAKE_SCHEMA.json", HERE / "NEW_REVIEW.md")}
    return result, result["checker_exit_code"]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("submission", nargs="?", type=Path, default=HERE / "NEW_INTAKE.json")
    result, code = audit(parser.parse_args().submission)
    print(json.dumps(result, indent=2, ensure_ascii=False))
    raise SystemExit(code)
