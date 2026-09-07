"""Read-only extension of check_refinement: candidate consistency, never admission.

Run with python -B. Exit 3 = pending, 2 = rejected; --template prints no evidence.
The closed schema is implemented below. No exporter, Julia call, or file writes.
"""
from __future__ import annotations

import argparse
from fractions import Fraction
from hashlib import sha256
import json
from pathlib import Path
import re
import sys

# Also suppress bytecode when imported by a caller that forgot -B.
sys.dont_write_bytecode = True
import check_refinement as base

HERE = Path(__file__).resolve().parent
SCHEMA = "routeb.o0.h_acc.source_export_extension.v1"
LIMIT = Fraction(1, 1000)
BRIDGES = ["C0_SOURCE_REFINEMENT_UNCHECKED", "C1_REAL_EVALUATOR_UNCHECKED",
           "C2_C5_ARRAY_AND_BODY_SEMANTICS_UNCHECKED", "R0_RUNTIME_PROVENANCE_UNCHECKED",
           "R1_INTERVAL_SOUNDNESS_UNCHECKED", "R2_FORMAL_COVERAGE_WITNESS_UNCHECKED"]
require, fields = base.require, base.fields


def exact(actual, expected, where):
    require(base.canonical(actual) == base.canonical(expected), where)


def identifier(value):
    require(type(value) is str and bool(value.strip()), "nonempty identifier required")
    return value


def hash_string(value):
    require(type(value) is str and re.fullmatch(r"[0-9a-f]{64}", value), "SHA256 syntax")


def rational(value):
    require(type(value) is str and re.fullmatch(r"-?(0|[1-9][0-9]*)(/[1-9][0-9]*)?", value),
            "canonical rational string required")
    result = Fraction(value)
    require(str(result) == value, "noncanonical rational")
    return result


def interval(value):
    require(type(value) is list and len(value) == 2, "interval pair required")
    lo, hi = map(rational, value)
    require(lo <= hi, "reversed interval")
    return lo, hi


def plus(a, b):
    return a[0] + b[0], a[1] + b[1]


def contains(outer, inner):
    require(outer[0] <= inner[0] <= inner[1] <= outer[1], "enclosure too narrow")


def matrix_coords(n, m):
    return [[r, c] for c in range(1, m + 1) for r in range(1, n + 1)]


def layouts():
    """Coordinate obligations only: no constants, node IDs, or runtime data."""
    shapes = {"A": (range(1, 7), 4, 4), "Tc": (range(7), 4, 4),
              "Ri": (range(1, 7), 3, 3), "Ii": (range(1, 7), 3, 3),
              "Jv": (range(1, 7), 3, 6), "Jw": (range(1, 7), 3, 6),
              "translation": (range(1, 7), 6, 6), "rotation": (range(1, 7), 6, 6)}
    out = {k: [[b, r, c] for b in bs for r, c in matrix_coords(n, m)]
           for k, (bs, n, m) in shapes.items()}
    out.update(o=[[f, r] for f in range(7) for r in range(1, 4)],
               z=[[j, r] for j in range(1, 7) for r in range(1, 4)],
               COM=[[b, r] for b in range(1, 7) for r in range(1, 4)])
    return out


def check_records(records, coordinates, keys):
    require(type(records) is list, "dense records must be array")
    for record in records:
        fields(record, "coordinate " + keys, "dense record")
    base.check_coordinates([r["coordinate"] for r in records], coordinates)


def output_ids(export, role, body=None):
    records = export["roots"][role]
    if body is not None:
        records = records[(body - 1) * 36:body * 36]
    return [r["node_id"] for r in records]


def check_export(export, source):
    """Occurrence-aware graph: node definition spans do not label every use."""
    fields(export, "layer source_sha256 nodes roots", "source export")
    exact(export["layer"], "E_star", "only ideal real graph supported")
    exact(export["source_sha256"], base.SOURCE_SHA, "export source mismatch")
    require(type(export["nodes"]) is list and export["nodes"], "nonempty DAG required")
    nodes, inputs = {}, set()
    for node in export["nodes"]:
        fields(node, "id op args payload semantic_role source_span", "node")
        name = identifier(node["id"])
        require(name not in nodes, "duplicate node id")
        op, args, payload = node["op"], node["args"], node["payload"]
        require(type(op) is str and op in base.ARITIES, "unsupported operation")
        require(type(args) is list and len(args) == base.ARITIES[op], "operation arity")
        require(all(type(a) is str and a in nodes for a in args), "forward/dangling reference")
        if op == "input":
            fields(payload, "joint", "input payload")
            joint = payload["joint"]
            require(type(joint) is int and 1 <= joint <= 6, "joint range/type")
            require(joint not in inputs, "one input node per joint required")
            inputs.add(joint)
        elif op == "rat":
            fields(payload, "numerator denominator", "rational payload")
            n, d = payload["numerator"], payload["denominator"]
            require(type(n) is str and type(d) is str, "rational integer strings required")
            value = Fraction(int(n), int(d))
            exact([n, d], [str(value.numerator), str(value.denominator)], "noncanonical rational payload")
        elif op == "div_nat":
            fields(payload, "divisor", "division payload")
            require(type(payload["divisor"]) is int and payload["divisor"] > 0, "positive divisor")
        else:
            fields(payload, "", "empty payload")
        require(type(node["semantic_role"]) is str, "semantic role string")
        base.check_span(node["source_span"], source, node["semantic_role"])
        nodes[name] = node
    require(inputs == set(range(1, 7)), "six input joints required")
    roots = export["roots"]
    fields(roots, "initial_zero pre_regularizer body_contribution accumulator_after_body", "roots")
    zero = identifier(roots["initial_zero"])
    require(zero in nodes and nodes[zero]["op"] == "rat" and
            nodes[zero]["payload"] == {"numerator": "0", "denominator": "1"}, "S0 exact zero required")
    base.check_span(nodes[zero]["source_span"], source, "initial_zero")
    for role in ("pre_regularizer", "body_contribution", "accumulator_after_body"):
        check_records(roots[role], base.coords(role != "pre_regularizer"), "node_id")
        for row in roots[role]:
            require(identifier(row["node_id"]) in nodes, "dangling output root")
            base.check_span(nodes[row["node_id"]]["source_span"], source, role)
    acc = output_ids(export, "accumulator_after_body")
    terms = output_ids(export, "body_contribution")
    for slot, ref in enumerate(acc):
        prior = zero if slot < 36 else acc[slot - 36]
        require(nodes[ref]["op"] == "add" and nodes[ref]["args"] == [prior, terms[slot]], "six ordered additions required")
    exact(output_ids(export, "pre_regularizer"), acc[-36:], "final roots must alias S6")


def check_mapping(mapping, export, source):
    expected = layouts()
    fields(mapping, " ".join(expected), "array mapping")
    nodes = {n["id"]: n for n in export["nodes"]}
    for stage, coordinates in expected.items():
        check_records(mapping[stage], coordinates, "node_id source_span")
        for row in mapping[stage]:
            ref = identifier(row["node_id"])
            require(ref in nodes, "array mapping dangling node")
            base.check_span(row["source_span"], source, stage)
            coord = row["coordinate"]
            literal = None
            if stage == "Tc" and coord[0] == 0:
                literal = int(coord[1] == coord[2])
            elif stage == "o" and coord[0] == 0:
                literal = 0
            elif stage in ("Jv", "Jw") and coord[2] > coord[0]:
                literal = 0
            if literal is not None:
                node = nodes[ref]
                require(node["op"] == "rat" and node["payload"] ==
                        {"numerator": str(literal), "denominator": "1"},
                        "explicit initial identity/zero or inactive Jacobian zero required")
    tables = {stage: {tuple(row["coordinate"]): row["node_id"] for row in rows}
              for stage, rows in mapping.items()}
    for j in range(1, 7):
        for r in range(1, 4):
            exact(tables["z"][j, r], tables["Tc"][j - 1, r, 3], "parent axis must alias previous frame")
            exact(tables["o"][j, r], tables["Tc"][j, r, 4], "origin must alias frame column 4")
    for b in range(1, 7):
        for r, col in matrix_coords(3, 3):
            exact(tables["Ri"][b, r, col], tables["Tc"][b, r, col], "Ri must alias body frame block")
        for j in range(1, b + 1):
            for r in range(1, 4):
                exact(tables["Jw"][b, r, j], tables["z"][j, r], "active Jw must alias parent axis")
    for root in export["roots"]["body_contribution"]:
        coord = tuple(root["coordinate"])
        node = nodes[root["node_id"]]
        require(node["op"] == "add" and node["args"] ==
                [tables["translation"][coord], tables["rotation"][coord]], "body must add translation and rotation")


def check_updates(updates, export, source):
    require(type(updates) is list and len(updates) == 6, "six source updates required")
    zero = export["roots"]["initial_zero"]
    nodes = {n["id"]: n for n in export["nodes"]}
    for body, row in enumerate(updates, 1):
        fields(row, "body source_span before body_roots after", "source update")
        exact(row["body"], body, "source update order/type")
        base.check_span(row["source_span"], source, "accumulator_after_body")
        prior = [zero] * 36 if body == 1 else output_ids(export, "accumulator_after_body", body - 1)
        terms = output_ids(export, "body_contribution", body)
        after = output_ids(export, "accumulator_after_body", body)
        exact(row["before"], prior, "source update predecessor")
        exact(row["body_roots"], terms, "source update body roots")
        exact(row["after"], after, "source update accumulator roots")
        for a, p, term in zip(after, prior, terms):
            require(nodes[a]["op"] == "add" and nodes[a]["args"] == [p, term],
                    "literal six-step fold required")
    exact(output_ids(export, "pre_regularizer"), updates[-1]["after"], "final must alias sixth update")


def decode_bits(value):
    require(type(value) is str and re.fullmatch(r"[0-9a-f]{16}", value), "binary64 bit string")
    word = int(value, 16)
    exponent, mantissa = (word >> 52) & 2047, word & ((1 << 52) - 1)
    require(exponent != 2047, "nonfinite binary64")
    # Integer operations and exact fractions; no host Float64 conversion.
    significand = mantissa if exponent == 0 else mantissa + (1 << 52)
    power = -1074 if exponent == 0 else exponent - 1023 - 52
    value = Fraction(significand) * Fraction(2) ** power
    return -value if word >> 63 else value


def bit_table(records, coordinates):
    check_records(records, coordinates, "bits")
    for row in records:
        decode_bits(row["bits"])
    return [row["bits"] for row in records]


def check_runtime(runtime, export_hash, source):
    fields(runtime, "source_sha256 source_export_sha256 provenance qhat_bits loaded_constants updates final observation", "runtime")
    exact(runtime["source_sha256"], base.SOURCE_SHA, "runtime source mismatch")
    exact(runtime["source_export_sha256"], export_hash, "runtime graph mismatch")
    fields(runtime["provenance"], "language exporter_sha256 instrumentation_sha256 environment_sha256 stdout_sha256 stderr_sha256 exit_code", "provenance")
    p = runtime["provenance"]
    exact(p["language"], "Julia", "runtime language")
    exact(p["exit_code"], 0, "runtime execution did not succeed")
    for key in p.keys() - {"language", "exit_code"}:
        hash_string(p[key])
    bits = runtime["qhat_bits"]
    require(type(bits) is list and len(bits) == 6, "six actual input bits required")
    require(all(-LIMIT <= decode_bits(v) <= LIMIT for v in bits), "runtime input outside Q1000")
    fields(runtime["loaded_constants"], "DH m I_val", "loaded constants")
    for name, coordinates in {"DH": matrix_coords(6, 4), "m": [[i] for i in range(1, 7)],
                              "I_val": [[i] for i in range(1, 7)]}.items():
        item = runtime["loaded_constants"][name]
        fields(item, "julia_type records", "loaded array")
        exact(item["julia_type"], "Matrix{Float64}" if name == "DH" else "Vector{Float64}", "loaded type")
        bit_table(item["records"], coordinates)
    check_runtime_updates(runtime["updates"], runtime["final"], source)
    exact(runtime["observation"], "after_line_58_body_6_before_line_60", "runtime observation point")


def check_runtime_updates(updates, final, source):
    """Validate recorded bit-table continuity, not actual Julia arithmetic."""
    require(type(updates) is list and len(updates) == 6, "six runtime updates required")
    prior = ["0000000000000000"] * 36  # source zeros(6,6), not invented observations
    for body, event in enumerate(updates, 1):
        fields(event, "body source_span kind before body_value after", "runtime event")
        exact(event["body"], body, "runtime update order/type")
        exact(event["kind"], "observed_source_update", "runtime must observe source update")
        base.check_span(event["source_span"], source, "accumulator_after_body")
        before = bit_table(event["before"], base.coords())
        bit_table(event["body_value"], base.coords())
        after = bit_table(event["after"], base.coords())
        exact(before, prior, "runtime update chain mismatch")
        prior = after
    exact(bit_table(final, base.coords()), prior, "runtime final mismatch")


def check_partition(tree):
    """Exact finite binary box partition, shared closed split faces permitted."""
    leaves, seen = {}, set()
    stack = [(tree, [(-LIMIT, LIMIT)] * 6)]
    while stack:
        node, box = stack.pop()
        require(type(node) is dict, "partition node object required")
        kind = node.get("kind")
        if kind == "leaf":
            fields(node, "kind id", "partition leaf")
            key = identifier(node["id"])
            require(key not in seen, "duplicate leaf id")
            seen.add(key)
            leaves[key] = box
        else:
            fields(node, "kind axis cut left right", "partition split")
            exact(kind, "split", "partition node kind")
            axis = node["axis"]
            require(type(axis) is int and 1 <= axis <= 6, "partition axis")
            cut = rational(node["cut"])
            lo, hi = box[axis - 1]
            require(lo < cut < hi, "partition cut must be strictly interior")
            left, right = list(box), list(box)
            left[axis - 1], right[axis - 1] = (lo, cut), (cut, hi)
            stack.extend([(node["right"], right), (node["left"], left)])
    return leaves


def check_real_rule(node, records, box):
    """Necessary rational enclosure rules; no trig or pi witness is trusted."""
    row = records[node["id"]]
    actual = interval(row["real"])
    args = [interval(records[arg]["real"]) for arg in node["args"]]
    op, payload = node["op"], node["payload"]
    expected = None
    if op == "input":
        expected = box[payload["joint"] - 1]
    elif op == "rat":
        value = Fraction(int(payload["numerator"]), int(payload["denominator"]))
        expected = value, value
    elif op == "neg":
        expected = -args[0][1], -args[0][0]
    elif op == "add":
        expected = plus(*args)
    elif op == "mul":
        products = [a * b for a in args[0] for b in args[1]]
        expected = min(products), max(products)
    elif op == "div_nat":
        expected = tuple(a / payload["divisor"] for a in args[0])
    if expected is not None:
        contains(actual, expected)
    # sin/cos/pi ranges and all error propagation remain external soundness obligations.


def check_intervals(candidate, export, runtime, export_hash):
    fields(candidate, "source_export_sha256 runtime_sha256 partition leaves final_36_error_bounds", "interval candidate")
    exact(candidate["source_export_sha256"], export_hash, "interval graph mismatch")
    exact(candidate["runtime_sha256"], base.digest(runtime), "interval runtime mismatch")
    boxes = check_partition(candidate["partition"])
    leaves = candidate["leaves"]
    require(type(leaves) is list, "interval leaves array")
    keys = []
    for leaf in leaves:
        fields(leaf, "box_id node_enclosures body_enclosures accumulator_enclosures final_36_error_bounds", "interval leaf")
        keys.append(identifier(leaf["box_id"]))
    exact(keys, list(boxes), "one certificate per partition leaf in left-first order")
    nodes = export["nodes"]
    global_rows = candidate["final_36_error_bounds"]
    check_records(global_rows, base.coords(), "epsilon")
    global_eps = [rational(row["epsilon"]) for row in global_rows]
    require(all(e >= 0 for e in global_eps), "negative final error bound")
    for leaf in leaves:
        rows = leaf["node_enclosures"]
        require(type(rows) is list, "node enclosures array")
        for row in rows:
            fields(row, "node_id real constant_error execution_error local_rounding rule_witness", "node enclosure")
            identifier(row["node_id"])
            for name in ("real", "constant_error", "execution_error", "local_rounding"):
                interval(row[name])
            require(row["rule_witness"] is None, "witness verification unsupported; submit no proof claims")
        exact([r["node_id"] for r in rows], [n["id"] for n in nodes], "all nodes exactly once in DAG order")
        by_id = {r["node_id"]: r for r in rows}
        for node in nodes:
            check_real_rule(node, by_id, boxes[leaf["box_id"]])
        for field, role in (("body_enclosures", "body_contribution"),
                            ("accumulator_enclosures", "accumulator_after_body")):
            table = leaf[field]
            check_records(table, base.coords(True), "node_id real constant_error execution_error")
            for row, root in zip(table, export["roots"][role]):
                exact(row["node_id"], root["node_id"], "root enclosure binding")
                ref = by_id[root["node_id"]]
                for key in ("real", "constant_error", "execution_error"):
                    exact(row[key], ref[key], "root enclosure must alias node enclosure")
        final = leaf["final_36_error_bounds"]
        check_records(final, base.coords(), "node_id epsilon")
        for slot, (row, root) in enumerate(zip(final, export["roots"]["pre_regularizer"])):
            exact(row["node_id"], root["node_id"], "final error binding")
            ref = by_id[root["node_id"]]
            total = plus(interval(ref["constant_error"]), interval(ref["execution_error"]))
            epsilon = rational(row["epsilon"])
            require(0 <= max(abs(total[0]), abs(total[1])) <= epsilon <= global_eps[slot],
                    "final epsilon must dominate both error bridges on every leaf")


def template():
    return {"schema": SCHEMA, "source_sha256": base.SOURCE_SHA,
            "constant_policy": "source_decimal_rational_and_exact_pi",
            "input_policy": "decoded_finite_binary64_in_Q1000",
            "source_export": None, "source_export_sha256": None, "array_mapping": None,
            "source_updates": None, "runtime_observation": None, "interval_candidate": None,
            "admission": {"status": "pending", "source_binding_proven": False,
                          "h_acc_expr_proven": False, "h_acc_round_proven": False,
                          "registry_eligible": False, "formal_certificate_allowed": False}}


def inspect(doc, source):
    fields(doc, " ".join(template()), "extension")
    exact(doc["schema"], SCHEMA, "extension schema")
    exact(doc["admission"], template()["admission"], "promotion prohibited")
    for key in ("source_sha256", "constant_policy", "input_policy"):
        exact(doc[key], template()[key], "contract mismatch: " + key)
    require(sha256(source).hexdigest() == base.SOURCE_SHA, "pinned source bytes mismatch")
    export, export_hash = doc["source_export"], doc["source_export_sha256"]
    blockers = []
    if export is None:
        require(export_hash is None, "hash without export")
        checks = {"expression": "NOT_RUN_NO_SOURCE_EXPORT"}
        blockers.append("REAL_SOURCE_EXPORT_ABSENT")
    else:
        exact(export_hash, base.digest(export), "canonical export hash mismatch")
        check_export(export, source)
        checks = {"expression": "PASS_CANDIDATE_CONSISTENCY_ONLY"}
    for field in ("array_mapping", "source_updates", "runtime_observation", "interval_candidate"):
        value = doc[field]
        if value is None:
            checks[field] = "NOT_RUN_ABSENT"
            blockers.append(field.upper() + "_ABSENT")
        else:
            # v1 is a bundle protocol. References without their graph are malformed;
            # an absent whole component is pending. Do not silently ignore payloads.
            require(export is not None, field + ": orphan component without source export")
            if field == "array_mapping":
                check_mapping(value, export, source)
            elif field == "source_updates":
                check_updates(value, export, source)
            elif field == "runtime_observation":
                check_runtime(value, export_hash, source)
            else:
                require(doc["runtime_observation"] is not None, "interval requires runtime binding")
                check_intervals(value, export, doc["runtime_observation"], export_hash)
            checks[field] = "PASS_CANDIDATE_CONSISTENCY_ONLY"
    return checks, list(dict.fromkeys(blockers + BRIDGES))


def audit(path, source_path=base.SOURCE):
    receipt = {"schema": SCHEMA + ".review", "status": "pending", "checker_exit_code": 3,
               "scope": "candidate_structure_exact_cover_and_rational_consistency_only",
               "admission": template()["admission"], "execution": {"julia": False, "lean_lake": False, "files_written": 0},
               "checker_sha256": sha256(Path(__file__).read_bytes()).hexdigest(),
               "base_checker_sha256": sha256(Path(base.__file__).read_bytes()).hexdigest()}
    try:
        raw = path.read_bytes()
        receipt["submission_sha256"] = sha256(raw).hexdigest()
        source = source_path.read_bytes()
        receipt["source_sha256"] = sha256(source).hexdigest()
        checks, blockers = inspect(base.decode(raw), source)
        receipt.update(checks=checks, blockers=blockers)
    except FileNotFoundError as exc:
        receipt["blockers"] = ["MISSING_ARTIFACT: " + str(exc)]
    except (OSError, ValueError, TypeError, KeyError, ZeroDivisionError, OverflowError, RecursionError) as exc:
        receipt.update(status="rejected", checker_exit_code=2, blockers=[str(exc)])
    return receipt, receipt["checker_exit_code"]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("submission", type=Path, nargs="?", default=HERE / "NEW_INTAKE.json")
    parser.add_argument("--template", action="store_true")
    args = parser.parse_args()
    if args.template:
        print(json.dumps(template(), indent=2, ensure_ascii=False))
        return 0
    receipt, code = audit(args.submission)
    print(json.dumps(receipt, indent=2, ensure_ascii=False))
    return code


if __name__ == "__main__":
    raise SystemExit(main())
