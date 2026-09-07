"""Independent, read-only H_acc structural intake. No execution or proof admission.

Exit 3: pending (including structurally valid but unproved exports).
Exit 2: rejected malformed/mismatched submission. Never returns admission success.
The Python validators below are the executable closed schema, not a Julia exporter.
"""
from __future__ import annotations

import argparse
from fractions import Fraction
from hashlib import sha256
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "examples/routeb_source_binding_audit/snapshots/original_target/dhport_lib.jl"
SOURCE_SHA = "aebe6db09b2d943448c5d701631109dba8f5eeb070cc66593e5dbaca26485936"
HERE = Path(__file__).resolve().parent
ARITIES = {"input": 0, "rat": 0, "pi": 0, "neg": 1, "add": 2,
           "mul": 2, "div_nat": 1, "sin": 1, "cos": 1}
# Inclusive, one-based source lines. These are text anchors, not refinement proofs.
SPANS = {"constants": [6, 13], "input": [31, 37], "angle": [37, 37],
         "trig": [38, 38], "A": [39, 39], "Tc": [32, 40],
         "o": [33, 41], "z": [34, 36], "COM": [50, 50],
         "Ri": [51, 51], "Ii": [52, 52], "Jv": [53, 55],
         "Jw": [53, 56], "translation": [58, 58], "rotation": [58, 58],
         "initial_zero": [48, 48], "body_contribution": [58, 58],
         "accumulator_after_body": [58, 58], "pre_regularizer": [58, 59]}
LAYERS = {
    "E_star": "unrounded real graph; source decimal tokens as rationals; pi exact; div_nat retained",
    "E_loaded": "unrounded real graph with actual exported Float64 constants decoded as dyadics; absent",
    "J_acc": "actual machine accumulator after body 6 line 58, before line 60; absent",
    "bridges": "E_star=M_NE^0; E_loaded-E_star constant error; J_acc-E_loaded execution error: all OPEN",
}
RUNTIME = {
    "input_type": "Vector{Float64} of length 6, finite entries",
    "quantifier": "all finite binary64 qhat with Decode(qhat) in [-1/1000,1/1000]^6",
    "all_real_extension": "requires RN64 input-conversion error and expanded input cover separately",
    "globals": "isolated include; export full DH,m,I_val shapes/types/raw bits; no intervening mutation",
    "environment": "pin Julia version, platform, methods, compiler, BLAS kernels/threads, trig implementation",
    "arithmetic": "bind reductions, FMA/folding, rounding, overflow, subnormal and underflow behavior",
    "observation": "six actual accumulator updates; final after body 6, before line 60",
    "instrumentation": "own source hash, patch and refinement evidence; stdout/stderr hashes and exit code",
    "forbidden_substitutes": "no triangle copying, post-hoc body sum, regularizer subtraction or zero-regularizer return",
    "interval": "complete rational partition of Q1000; intermediate/body/accumulator enclosures and 36 errors; soundness witnesses",
    "runtime_evidence": None,
}
INDEX = {
    "human_body_joint_row_column": [1, 2, 3, 4, 5, 6],
    "frames": [0, 1, 2, 3, 4, 5, 6],
    "final": "36: column outer, row inner; slot=(column-1)*6+(row-1)",
    "body": "216: body outer, column middle, row inner; slot=(body-1)*36+(column-1)*6+(row-1)",
    "accumulator": "216: body outer, column middle, row inner; slot=(body-1)*36+(column-1)*6+(row-1)",
    "frame_mapping": "Tc[frame+1],o[:,frame+1]; z[:,joint] from frame joint-1 before transform",
    "jacobian": "joint<=body active; remaining columns explicit zero; COM frames body-1 and body",
    "fin_mapping": "human index minus 1; frame already zero-based",
    "coverage": "both triangles and all zeros mandatory; S0 exact zero; six ordered additions; final aliases S6",
}


def require(ok, message):
    if not ok:
        raise ValueError(message)


def fields(obj, names, where):
    require(type(obj) is dict and set(obj) == set(names.split()), f"{where}: exact fields required")


def canonical(obj):
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False).encode("utf-8")


def digest(obj):
    return sha256(canonical(obj)).hexdigest()


def no_duplicates(pairs):
    obj = {}
    for key, value in pairs:
        require(key not in obj, f"duplicate JSON key: {key}")
        obj[key] = value
    return obj


def decode(raw):
    return json.loads(raw.decode("utf-8"), object_pairs_hook=no_duplicates,
                      parse_constant=lambda value: require(False, f"nonfinite JSON: {value}"))


def span(source, start, end):
    # Preserve original newline bytes in inclusive line slices; no text normalization.
    return {"start_line": start, "end_line": end,
            "sha256": sha256(b"".join(source.splitlines(keepends=True)[start - 1:end])).hexdigest()}


def template():
    return {"schema": "routeb.o0.h_acc.source_refinement_intake.v1",
            "source_sha256": SOURCE_SHA, "semantic_layers": LAYERS,
            "index_contract": INDEX, "runtime_policy": RUNTIME,
            "source_export": None, "source_export_sha256": None,
            "admission": {"h_acc_expr_proven": False, "h_acc_round_proven": False,
                          "source_binding_proven": False, "registry_eligible": False,
                          "formal_certificate_allowed": False}}


def coords(body=False):
    if body:
        return [[b, r, c] for b in range(1, 7) for c in range(1, 7) for r in range(1, 7)]
    return [[r, c] for c in range(1, 7) for r in range(1, 7)]


def check_coordinates(actual, expected):
    require(type(actual) is list, "coordinate list required")
    require(all(type(row) is list and all(type(i) is int for i in row) for row in actual),
            "integer coordinates required (booleans forbidden)")
    require(actual == expected, "dense coordinates/order mismatch")


def check_span(item, source, role):
    fields(item, "start_line end_line sha256", "source span")
    lo, hi = item["start_line"], item["end_line"]
    require(type(lo) is int and type(hi) is int, "integer source lines required")
    require(role in SPANS, "unknown semantic role")
    a, b = SPANS[role]
    require(a <= lo <= hi <= b, f"span outside {role} anchor")
    require(item == span(source, lo, hi), "source span hash mismatch")


def check_export(export, source):
    """Only graph syntax, coordinate coverage and literal fold shape, never semantics."""
    fields(export, "layer source_sha256 nodes roots source_map", "source export")
    require(export["layer"] == "E_star", "only ideal E_star structural intake supported")
    require(export["source_sha256"] == SOURCE_SHA, "export source mismatch")
    require(type(export["nodes"]) is list and export["nodes"], "nonempty exported DAG required")
    nodes = {}
    inputs = set()
    for node in export["nodes"]:
        fields(node, "id op args payload semantic_role source_span", "node")
        name, op, args, payload = node["id"], node["op"], node["args"], node["payload"]
        require(type(name) is str and bool(name.strip()) and name not in nodes, "unique nonempty node id required")
        require(type(op) is str and op in ARITIES, "unsupported operation")
        require(type(args) is list and len(args) == ARITIES[op], "operation arity mismatch")
        require(all(type(arg) is str and arg in nodes for arg in args), "forward/dangling/cyclic reference")
        if op == "input":
            fields(payload, "joint", "input payload")
            require(type(payload["joint"]) is int and 1 <= payload["joint"] <= 6, "joint range/type")
            inputs.add(payload["joint"])
        elif op == "rat":
            fields(payload, "numerator denominator", "rational payload")
            n, d = payload["numerator"], payload["denominator"]
            require(type(n) is str and type(d) is str, "rational integer strings required")
            value = Fraction(int(n), int(d))
            require(n == str(value.numerator) and d == str(value.denominator), "noncanonical rational")
        elif op == "div_nat":
            fields(payload, "divisor", "division payload")
            require(type(payload["divisor"]) is int and payload["divisor"] > 0, "positive divisor required")
        else:
            fields(payload, "", "empty payload")
        require(type(node["semantic_role"]) is str, "semantic role string required")
        check_span(node["source_span"], source, node["semantic_role"])
        nodes[name] = node
    require(inputs == set(range(1, 7)), "six input joints required")
    fields(export["roots"], "initial_zero pre_regularizer body_contribution accumulator_after_body", "roots")
    zero = export["roots"]["initial_zero"]
    require(type(zero) is str and zero in nodes, "initial zero root missing")
    require(nodes[zero]["op"] == "rat" and nodes[zero]["payload"] == {"numerator": "0", "denominator": "1"}, "S0 must be exact zero")
    tables = {}
    for name in ("pre_regularizer", "body_contribution", "accumulator_after_body"):
        records = export["roots"][name]
        require(type(records) is list, "root array required")
        for record in records:
            fields(record, "coordinate node_id", "root record")
            require(type(record["node_id"]) is str and record["node_id"] in nodes, "dangling root")
        check_coordinates([r["coordinate"] for r in records], coords(name != "pre_regularizer"))
        tables[name] = [r["node_id"] for r in records]
    acc, body = tables["accumulator_after_body"], tables["body_contribution"]
    for slot, root in enumerate(acc):
        prior = zero if slot < 36 else acc[slot - 36]
        require(nodes[root]["op"] == "add" and nodes[root]["args"] == [prior, body[slot]],
                "six ordered accumulator additions required")
    require(tables["pre_regularizer"] == acc[-36:], "final roots must alias S6")
    # Map stage -> nonempty node-id list, including intermediate scalar products.
    # Full array/index refinement remains a proof obligation even with this coverage.
    fields(export["source_map"], " ".join(SPANS), "source map stages")
    for role, refs in export["source_map"].items():
        require(type(refs) is list and bool(refs), f"missing stage: {role}")
        require(all(type(ref) is str and ref in nodes for ref in refs), "dangling source map node")
        for ref in refs:
            check_span(nodes[ref]["source_span"], source, role)
    for name, node in nodes.items():
        require(name in export["source_map"][node["semantic_role"]], "unmapped node")
    for role, roots in tables.items():
        require(export["source_map"][role] == roots, "source map/output root mismatch")
    require(export["source_map"]["initial_zero"] == [zero], "source map/S0 mismatch")


def inspect(doc, source):
    base = template()
    fields(doc, " ".join(base), "intake")
    for key in base.keys() - {"source_export", "source_export_sha256"}:
        require(canonical(doc[key]) == canonical(base[key]), f"contract mismatch: {key}")
    require(sha256(source).hexdigest() == SOURCE_SHA, "pinned source bytes mismatch")
    export = doc["source_export"]
    if export is None:
        require(doc["source_export_sha256"] is None, "hash without export")
        return "NOT_RUN_NO_SOURCE_EXPORT", ["REAL_SOURCE_EXPORT_ABSENT", "SOURCE_REFINEMENT_WITNESS_ABSENT", "RUNTIME_AND_INTERVAL_EVIDENCE_ABSENT"]
    require(doc["source_export_sha256"] == digest(export), "canonical export hash mismatch")
    check_export(export, source)
    return "PASS_STRUCTURE_ONLY", ["SOURCE_REFINEMENT_AND_EVALUATOR_PROOFS_UNCHECKED", "ARRAY_INDEX_AND_UNSIMPLIFIED_BODY_SEMANTICS_UNPROVEN", "RUNTIME_AND_INTERVAL_EVIDENCE_ABSENT"]


def audit(path, source_path=SOURCE):
    receipt = {"schema": "routeb.o0.h_acc.source_refinement_review.v1",
               "status": "pending", "theorem_status": "OPEN_H_ACC",
               "checker_scope": "intake_schema_and_structural_consistency_only",
               "checker_exit_code": 3,
               "formal_certificate_allowed": False, "source_binding_proven": False,
               "h_acc_expr_proven": False, "h_acc_round_proven": False,
               "registry_eligible": False, "expected_roots": {"final": 36, "body": 216, "accumulator": 216},
               "execution": {"julia": False, "lean_lake": False, "files_written": 0},
               "checker_sha256": sha256(Path(__file__).read_bytes()).hexdigest()}
    try:
        submission = path.read_bytes()
        receipt["submission_sha256"] = sha256(submission).hexdigest()
        source = source_path.read_bytes()
        receipt["source_sha256"] = sha256(source).hexdigest()
        receipt["source_spans"] = {role: span(source, *bounds) for role, bounds in SPANS.items()}
        doc = decode(submission)
        result, missing = inspect(doc, source)
        receipt.update(structural_check=result, blockers=missing,
                       source_export_present=doc["source_export"] is not None)
        return receipt, 3
    except FileNotFoundError as exc:
        receipt.update(structural_check="NOT_RUN_MISSING_ARTIFACT", blockers=[str(exc)])
        return receipt, 3
    except (OSError, ValueError, TypeError, KeyError, ZeroDivisionError, OverflowError, RecursionError) as exc:
        receipt.update(status="rejected", checker_exit_code=2,
                       structural_check="REJECTED", blockers=[str(exc)])
        return receipt, 2


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("submission", nargs="?", type=Path, default=HERE / "intake.json")
    parser.add_argument("--template", action="store_true", help="print empty intake; contains no Julia constants or roots")
    args = parser.parse_args()
    if args.template:
        print(json.dumps(template(), indent=2, ensure_ascii=False))
        return 0
    receipt, code = audit(args.submission)
    print(json.dumps(receipt, indent=2, ensure_ascii=False))
    return code


if __name__ == "__main__":
    raise SystemExit(main())
