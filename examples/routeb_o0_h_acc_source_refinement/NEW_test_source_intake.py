"""Targeted protocol tests. All toy records are in-memory unit-test data only.

No complete Julia export fixture exists here. Toy graphs omit mandatory source
fields and cannot pass base.check_export; their numbers are arithmetic test
operands, never observed constants or certified H_acc bounds. Tests write nothing.
"""
import copy
from fractions import Fraction
import json
import subprocess
import sys
from types import SimpleNamespace
import unittest

import NEW_source_intake as c


class IntakeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source = c.base.SOURCE.read_bytes()
        cls.fixture = c.base.decode((c.HERE / "NEW_LAYOUT_FIXTURE.json").read_bytes())

    def test_empty_template_and_cli_stay_pending(self):
        doc = c.base.decode((c.HERE / "NEW_INTAKE.json").read_bytes())
        self.assertEqual(doc, c.template())
        checks, blockers = c.inspect(doc, self.source)
        self.assertEqual(checks["expression"], "NOT_RUN_NO_SOURCE_EXPORT")
        self.assertIn("REAL_SOURCE_EXPORT_ABSENT", blockers)
        result = subprocess.run([sys.executable, "-B", str(c.HERE / "NEW_source_intake.py")],
                                capture_output=True, text=True, check=False)
        self.assertEqual(result.returncode, 3)
        receipt = json.loads(result.stdout)
        self.assertEqual(receipt["status"], "pending")
        self.assertFalse(receipt["admission"]["registry_eligible"])

    def test_malformed_file_rejected_missing_file_pending(self):
        for path, code in ((c.HERE / "NEW_source_intake.py", 2),
                           (c.HERE / "NEW_nonexistent_test_input.json", 3)):
            with self.subTest(path=path.name):
                receipt, got = c.audit(path)
                self.assertEqual(got, code)
                self.assertFalse(receipt["admission"]["formal_certificate_allowed"])

    def test_unknown_promotion_orphan_and_hash_attacks(self):
        mutations = [lambda d: d.update(verified=True),
                     lambda d: d["admission"].update(h_acc_expr_proven=True),
                     lambda d: d["admission"].update(h_acc_round_proven=0),
                     lambda d: d.update(source_updates=[]),
                     lambda d: d.update(interval_candidate={}),
                     lambda d: d.update(source_export={}),
                     lambda d: d.update(source_export_sha256="0" * 64)]
        for mutate in mutations:
            doc = c.template()
            mutate(doc)
            with self.subTest(mutation=mutations.index(mutate)), self.assertRaises(ValueError):
                c.inspect(doc, self.source)

    def test_source_drift_and_duplicate_json(self):
        with self.assertRaisesRegex(ValueError, "source bytes mismatch"):
            c.inspect(c.template(), self.source + b"\n")
        for raw in (b'{"x":1,"x":2}', b'{"x":NaN}', b'{"x":Infinity}'):
            with self.assertRaises(ValueError):
                c.base.decode(raw)

    def test_final_template_named_duplicates_reject_before_schema(self):
        raw = (c.HERE / "NEW_INTAKE.json").read_bytes()
        self.assertEqual(c.base.decode(raw), c.template())
        for key in ("source_updates", "runtime_observation"):
            token = ('"' + key + '": null').encode()
            self.assertEqual(raw.count(token), 1)
            for second in (b"null", b"{}"):
                duplicate = token + b', "' + key.encode() + b'": ' + second
                ambiguous = raw.replace(token, duplicate, 1)
                with self.subTest(key=key, second=second):
                    with self.assertRaisesRegex(ValueError, "duplicate JSON key: " + key):
                        c.base.decode(ambiguous)
                    # Exercise the actual audit boundary without writing a file.
                    receipt, code = c.audit(SimpleNamespace(read_bytes=lambda: ambiguous))
                    self.assertEqual((receipt["status"], code), ("rejected", 2))
                    self.assertIn("duplicate JSON key: " + key, receipt["blockers"][0])

    def test_coordinate_fixture_is_only_geometry(self):
        for key in ("source_export", "runtime_observation", "interval_candidate"):
            self.assertIsNone(self.fixture[key])
        with self.assertRaises(ValueError):
            c.inspect(self.fixture, self.source)
        for key, body in (("final_coordinates", False), ("body_coordinates", True),
                          ("accumulator_coordinates", True)):
            actual = self.fixture[key]
            c.base.check_coordinates(actual, c.base.coords(body))
            self.assertEqual(len(actual), 216 if body else 36)
            for slot, row in enumerate(actual):
                b, r, col = row if body else [1] + row
                self.assertEqual(slot, (b - 1) * 36 + (col - 1) * 6 + r - 1)
        for b, row in enumerate(self.fixture["source_update_slots"]):
            self.assertEqual(row["body"], b + 1)
            self.assertEqual(row["after_accumulator_slots"], list(range(b * 36, (b + 1) * 36)))
            self.assertEqual(row["before_accumulator_slots"], None if b == 0 else list(range((b-1)*36, b*36)))

    def test_all_dense_orders_reject_omission_duplication_transpose_bool(self):
        for expected in [c.base.coords(), c.base.coords(True), *c.layouts().values()]:
            boolean = copy.deepcopy(expected)
            boolean[0][0] = True
            variants = [expected[:-1], expected + [expected[-1]], list(reversed(expected)), boolean,
                        [row[:-2] + row[-2:][::-1] for row in expected]]
            for actual in variants:
                with self.assertRaises(ValueError):
                    c.base.check_coordinates(actual, expected)

    def test_intermediate_counts_and_frame_endpoints(self):
        layout = c.layouts()
        self.assertEqual({k: len(v) for k, v in layout.items()},
                         {"A": 96, "Tc": 112, "Ri": 54, "Ii": 54, "Jv": 108, "Jw": 108,
                          "translation": 216, "rotation": 216, "o": 21, "z": 18, "COM": 18})
        self.assertEqual(layout["Tc"][0], [0, 1, 1])
        self.assertEqual(layout["Tc"][-1], [6, 4, 4])
        self.assertEqual(layout["z"][0], [1, 1])

    def test_spans_preserve_bytes_and_exclude_line60(self):
        for role, bounds in c.base.SPANS.items():
            span = c.base.span(self.source, *bounds)
            c.base.check_span(span, self.source, role)
            span["sha256"] = "0" * 64
            with self.assertRaises(ValueError):
                c.base.check_span(span, self.source, role)
        for role in ("accumulator_after_body", "body_contribution", "pre_regularizer"):
            with self.assertRaises(ValueError):
                c.base.check_span(c.base.span(self.source, 60, 60), self.source, role)

    def test_canonical_rationals(self):
        for raw in ("0", "-1/1000", "7/3", "-2"):
            self.assertEqual(c.rational(raw), Fraction(raw))
        for raw in (True, 0, 0.0, "-0", "+1", "01", "1/1", "2/4", "1/0", "1/-2", "1e-3", "NaN"):
            with self.assertRaises(ValueError):
                c.rational(raw)
        for pair in (["1", "0"], ["0"], [0, 1]):
            with self.assertRaises(ValueError):
                c.interval(pair)

    def test_binary64_decoding_is_exact_including_subnormals(self):
        self.assertEqual(c.decode_bits("0000000000000001"), Fraction(1, 2**1074))
        self.assertEqual(c.decode_bits("8000000000000000"), 0)
        self.assertEqual(c.decode_bits("3ff0000000000000"), 1)
        for bad in (True, "0", "7ff0000000000000", "7ff8000000000000", "FFF0000000000000"):
            with self.assertRaises(ValueError):
                c.decode_bits(bad)

    def test_partition_geometry_is_exact_and_complete(self):
        boxes = c.check_partition(self.fixture["partition_geometry_only"])
        self.assertEqual(list(boxes), ["geometry-left", "geometry-right"])
        self.assertEqual(boxes["geometry-left"][0], (-c.LIMIT, 0))
        self.assertEqual(boxes["geometry-right"][0], (0, c.LIMIT))
        self.assertEqual(c.check_partition({"kind": "leaf", "id": "whole"})["whole"], [(-c.LIMIT, c.LIMIT)] * 6)
        volume = sum((b[0][1] - b[0][0]) * (2*c.LIMIT)**5 for b in boxes.values())
        self.assertEqual(volume, (2*c.LIMIT)**6)

    def test_partition_attacks(self):
        for mutate in (lambda t: t.update(axis=True), lambda t: t.update(axis=0),
                       lambda t: t.update(cut="1/1000"), lambda t: t.update(cut="2/1000"),
                       lambda t: t.update(cut="0.0"), lambda t: t.pop("right"),
                       lambda t: t["right"].update(id="geometry-left"),
                       lambda t: t.update(box=[["0", "1"]] * 6)):
            tree = copy.deepcopy(self.fixture["partition_geometry_only"])
            mutate(tree)
            with self.assertRaises(ValueError):
                c.check_partition(tree)

    def test_rational_interval_rules(self):
        # Generic arithmetic unit operands; deliberately not a source export.
        records = {"a": {"real": ["-2", "3"]}, "b": {"real": ["-4", "5"]}}
        cases = [("add", ["a", "b"], {}, ["-6", "8"]),
                 ("mul", ["a", "b"], {}, ["-12", "15"]),
                 ("neg", ["a"], {}, ["-3", "2"]),
                 ("div_nat", ["a"], {"divisor": 2}, ["-1", "3/2"]),
                 ("input", [], {"joint": 1}, ["-1/1000", "1/1000"])]
        for op, args, payload, enclosure in cases:
            node = {"id": "result", "op": op, "args": args, "payload": payload}
            records["result"] = {"real": enclosure}
            c.check_real_rule(node, records, [(-c.LIMIT, c.LIMIT)] * 6)
            records["result"] = {"real": ["0", "0"]}
            with self.assertRaisesRegex(ValueError, "too narrow"):
                c.check_real_rule(node, records, [(-c.LIMIT, c.LIMIT)] * 6)


class BindingTests(unittest.TestCase):
    """Metadata-only stand-ins: intentionally incomplete, never source exports."""
    def setUp(self):
        self.source = c.base.SOURCE.read_bytes()

    def test_definition_and_occurrence_spans_allow_slice_aliases(self):
        # Only a generic occurrence-map unit object. No export schema or real DAG.
        nodes = {"unit:zero": {"id": "unit:zero", "op": "rat", "payload": {"numerator": "0", "denominator": "1"}},
                 "unit:one": {"id": "unit:one", "op": "rat", "payload": {"numerator": "1", "denominator": "1"}}}
        mapping, tables = {}, {}
        for stage, coords in c.layouts().items():
            rows, table = [], {}
            for coord in coords:
                ref = "unit:" + stage + ":" + str(coord)
                if stage == "Tc" and coord[0] == 0:
                    ref = "unit:one" if coord[1] == coord[2] else "unit:zero"
                elif stage == "o" and coord[0] == 0:
                    ref = "unit:zero"
                elif stage in ("Jv", "Jw") and coord[2] > coord[0]:
                    ref = "unit:zero"
                nodes.setdefault(ref, {"id": ref, "op": "input", "payload": {}})
                row = {"coordinate": coord, "node_id": ref, "source_span": c.base.span(self.source, *c.base.SPANS[stage])}
                rows.append(row)
                table[tuple(coord)] = row
            mapping[stage], tables[stage] = rows, table
        for j in range(1, 7):
            for r in range(1, 4):
                tables["z"][j, r]["node_id"] = tables["Tc"][j-1, r, 3]["node_id"]
                tables["o"][j, r]["node_id"] = tables["Tc"][j, r, 4]["node_id"]
        for b in range(1, 7):
            for r, col in c.matrix_coords(3, 3):
                tables["Ri"][b, r, col]["node_id"] = tables["Tc"][b, r, col]["node_id"]
            for j in range(1, b+1):
                for r in range(1, 4):
                    tables["Jw"][b, r, j]["node_id"] = tables["z"][j, r]["node_id"]
        roots = []
        for coord in c.base.coords(True):
            ref = "unit:body:" + str(coord)
            nodes[ref] = {"id": ref, "op": "add", "args": [tables[s][tuple(coord)]["node_id"] for s in ("translation", "rotation")]}
            roots.append({"coordinate": coord, "node_id": ref})
        partial = {"nodes": list(nodes.values()), "roots": {"body_contribution": roots}}
        with self.assertRaises(ValueError):
            c.check_export(partial, self.source)
        c.check_mapping(mapping, partial, self.source)
        for stage, slot, replacement in (("Ri", 0, "unit:zero"), ("z", 0, "unit:one"),
                                          ("Jw", 0, "unit:one"), ("Jv", 3, "unit:one")):
            bad = copy.deepcopy(mapping)
            bad[stage][slot]["node_id"] = replacement
            with self.subTest(stage=stage), self.assertRaises(ValueError):
                c.check_mapping(bad, partial, self.source)

    def test_runtime_bit_chain_unit_data_is_not_execution_evidence(self):
        # Generic bit patterns exercise the protocol only; no provenance supplied.
        def table(bits):
            return [{"coordinate": rc, "bits": bits} for rc in c.base.coords()]
        updates = []
        for b in range(1, 7):
            updates.append({"body": b, "source_span": c.base.span(self.source, 58, 58),
                            "kind": "observed_source_update", "before": table("0000000000000000"),
                            "body_value": table("0000000000000000"), "after": table("0000000000000000")})
        final = table("0000000000000000")
        c.check_runtime_updates(updates, final, self.source)
        for mutate in (lambda u: u.reverse(), lambda u: u.pop(),
                       lambda u: u[0].update(kind="post_hoc_sum"),
                       lambda u: u[1]["before"][0].update(bits="8000000000000000"),
                       lambda u: u[3]["after"][0].update(bits="7ff0000000000000"),
                       lambda u: u[2]["body_value"].pop(),
                       lambda u: u[5].update(source_span=c.base.span(self.source, 60, 60))):
            bad = copy.deepcopy(updates)
            mutate(bad)
            with self.assertRaises(ValueError):
                c.check_runtime_updates(bad, final, self.source)
        final[0]["bits"] = "8000000000000000"
        with self.assertRaisesRegex(ValueError, "final mismatch"):
            c.check_runtime_updates(updates, final, self.source)

    def fold_metadata(self):
        roots = {"initial_zero": "unit-test:S0", "body_contribution": [], "accumulator_after_body": []}
        nodes, updates = [], []
        for b in range(1, 7):
            before = ["unit-test:S0"] * 36 if b == 1 else updates[-1]["after"]
            terms = [f"unit-test:B:{b}:{i}" for i in range(36)]
            after = [f"unit-test:S:{b}:{i}" for i in range(36)]
            for i, (r, col) in enumerate(c.base.coords()):
                roots["body_contribution"].append({"coordinate": [b, r, col], "node_id": terms[i]})
                roots["accumulator_after_body"].append({"coordinate": [b, r, col], "node_id": after[i]})
                nodes.append({"id": after[i], "op": "add", "args": [before[i], terms[i]]})
            updates.append({"body": b, "source_span": c.base.span(self.source, 58, 58),
                            "before": before, "body_roots": terms, "after": after})
        roots["pre_regularizer"] = [{"coordinate": rc, "node_id": ref}
                                    for rc, ref in zip(c.base.coords(), updates[-1]["after"])]
        return {"roots": roots, "nodes": nodes}, updates

    def test_six_source_update_bindings_and_attacks(self):
        partial, updates = self.fold_metadata()
        with self.assertRaises(ValueError):
            c.base.check_export(partial, self.source)
        c.check_updates(updates, partial, self.source)
        for mutate in (lambda u: u.reverse(), lambda u: u.pop(),
                       lambda u: u[0].update(body=True),
                       lambda u: u[2]["before"].reverse(),
                       lambda u: u[5]["after"].pop(),
                       lambda u: u[0].update(source_span=c.base.span(self.source, 60, 60))):
            bad = copy.deepcopy(updates)
            mutate(bad)
            with self.assertRaises(ValueError):
                c.check_updates(bad, partial, self.source)
        bad = copy.deepcopy(partial)
        bad["nodes"][0]["args"].reverse()
        with self.assertRaisesRegex(ValueError, "literal six-step"):
            c.check_updates(updates, bad, self.source)

    def interval_metadata(self):
        # Single input toy, no DH values or Julia observations, no source fields.
        graph = {"nodes": [{"id": "unit-test:x", "op": "input", "args": [], "payload": {"joint": 1}}],
                 "roots": {k: [{"coordinate": rc, "node_id": "unit-test:x"} for rc in c.base.coords(body)]
                           for k, body in (("pre_regularizer", False), ("body_contribution", True),
                                           ("accumulator_after_body", True))}}
        row = {"node_id": "unit-test:x", "real": ["-1/1000", "1/1000"],
               "constant_error": ["-1", "2"], "execution_error": ["-3", "4"],
               "local_rounding": ["0", "0"], "rule_witness": None}
        leaf = {"box_id": "unit-test:whole", "node_enclosures": [row]}
        for table, role in (("body_enclosures", "body_contribution"),
                            ("accumulator_enclosures", "accumulator_after_body")):
            leaf[table] = [{**root, **{k: row[k] for k in ("real", "constant_error", "execution_error")}}
                           for root in graph["roots"][role]]
        leaf["final_36_error_bounds"] = [{**root, "epsilon": "6"} for root in graph["roots"]["pre_regularizer"]]
        # Content hashes bind these explicitly invalid unit objects, not a runtime.
        runtime = {"unit_test_only": True}
        candidate = {"source_export_sha256": c.base.digest(graph), "runtime_sha256": c.base.digest(runtime),
                     "partition": {"kind": "leaf", "id": "unit-test:whole"}, "leaves": [leaf],
                     "final_36_error_bounds": [{"coordinate": rc, "epsilon": "6"} for rc in c.base.coords()]}
        return candidate, graph, runtime

    def test_interval_binding_pipeline_on_nonexport_unit_data(self):
        candidate, graph, runtime = self.interval_metadata()
        with self.assertRaises(ValueError):
            c.base.check_export(graph, self.source)
        c.check_intervals(candidate, graph, runtime, c.base.digest(graph))
        attacks = [lambda v: v["leaves"].clear(),
                   lambda v: v["leaves"].append(copy.deepcopy(v["leaves"][0])),
                   lambda v: v["leaves"][0]["node_enclosures"].clear(),
                   lambda v: v["leaves"][0]["body_enclosures"].pop(),
                   lambda v: v["leaves"][0]["accumulator_enclosures"].reverse(),
                   lambda v: v["leaves"][0]["body_enclosures"][0].update(node_id="dangling"),
                   lambda v: v["leaves"][0]["body_enclosures"][0].update(real=["0", "0"]),
                   lambda v: v["leaves"][0]["node_enclosures"][0].update(rule_witness={"verified": True}),
                   lambda v: v["leaves"][0]["final_36_error_bounds"][0].update(epsilon="4"),
                   lambda v: v["final_36_error_bounds"][0].update(epsilon="5"),
                   lambda v: v.update(runtime_sha256="0" * 64)]
        for mutate in attacks:
            bad = copy.deepcopy(candidate)
            mutate(bad)
            with self.subTest(attack=attacks.index(mutate)), self.assertRaises(ValueError):
                c.check_intervals(bad, graph, runtime, c.base.digest(graph))


if __name__ == "__main__":
    unittest.main()
