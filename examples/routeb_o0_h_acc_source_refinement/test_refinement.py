"""Focused intake checks. No invented Julia DAG, constants, or root fixture."""
import copy
import json
import subprocess
import sys
import unittest

import check_refinement as checker


class IntakeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source = checker.SOURCE.read_bytes()

    def test_missing_export_is_pending(self):
        receipt, code = checker.audit(checker.HERE / "intake.json")
        self.assertEqual((receipt["status"], code), ("pending", 3))
        self.assertFalse(receipt["source_export_present"])
        self.assertFalse(receipt["formal_certificate_allowed"])
        self.assertEqual(receipt["structural_check"], "NOT_RUN_NO_SOURCE_EXPORT")

    def test_missing_file_is_pending(self):
        receipt, code = checker.audit(checker.HERE / "not-a-source-export.json")
        self.assertEqual((receipt["status"], code), ("pending", 3))

    def test_cli_pending_exit_is_nonzero(self):
        run = subprocess.run([sys.executable, "-B", str(checker.HERE / "check_refinement.py")],
                             capture_output=True, text=True, check=False)
        self.assertEqual(run.returncode, 3)
        self.assertEqual(json.loads(run.stdout)["status"], "pending")

    def test_cli_malformed_submission_is_rejected(self):
        # Existing Python source is deliberately not JSON; no fabricated export fixture.
        run = subprocess.run([sys.executable, "-B", str(checker.HERE / "check_refinement.py"),
                              str(checker.HERE / "check_refinement.py")],
                             capture_output=True, text=True, check=False)
        self.assertEqual(run.returncode, 2)
        self.assertEqual(json.loads(run.stdout)["status"], "rejected")

    def test_template_has_no_manufactured_evidence(self):
        doc = checker.decode((checker.HERE / "intake.json").read_bytes())
        self.assertEqual(doc, checker.template())
        self.assertIsNone(doc["source_export"])
        self.assertIsNone(doc["source_export_sha256"])
        self.assertIsNone(doc["runtime_policy"]["runtime_evidence"])

    def test_contract_tampering_rejected(self):
        mutations = [
            lambda d: d.update(source_sha256="0" * 64),
            lambda d: d.update(source_export_sha256="0" * 64),
            lambda d: d.update(verified=True),
            lambda d: d["admission"].update(h_acc_expr_proven=True),
            lambda d: d["admission"].update(h_acc_round_proven=0),
            lambda d: d["semantic_layers"].update(E_loaded=d["semantic_layers"]["E_star"]),
            lambda d: d["index_contract"].update(final="row major"),
            lambda d: d["runtime_policy"].update(runtime_evidence={}),
            lambda d: d["runtime_policy"].update(quantifier="sampled inputs"),
            lambda d: d.update(source_export={}),
        ]
        for mutation in mutations:
            with self.subTest(mutation=mutations.index(mutation)):
                doc = copy.deepcopy(checker.template())
                mutation(doc)
                with self.assertRaises(ValueError):
                    checker.inspect(doc, self.source)

    def test_empty_submitted_export_is_rejected_even_with_matching_hash(self):
        doc = checker.template()
        doc.update(source_export={}, source_export_sha256=checker.digest({}))
        with self.assertRaisesRegex(ValueError, "source export: exact fields"):
            checker.inspect(doc, self.source)

    def test_source_drift_rejected(self):
        with self.assertRaisesRegex(ValueError, "source bytes mismatch"):
            checker.inspect(checker.template(), self.source + b"\n")

    def test_dense_orders_and_slots(self):
        final, body = checker.coords(), checker.coords(True)
        self.assertEqual((len(final), len(body)), (36, 216))
        for slot, (r, c) in enumerate(final):
            self.assertEqual(slot, (c - 1) * 6 + r - 1)
        for slot, (b, r, c) in enumerate(body):
            self.assertEqual(slot, (b - 1) * 36 + (c - 1) * 6 + r - 1)

    def test_missing_duplicate_transposed_reordered_and_boolean_coordinates(self):
        for expected in (checker.coords(), checker.coords(True)):
            bad_boolean = copy.deepcopy(expected)
            bad_boolean[0][0] = True
            variants = [expected[:-1], [expected[0]] + expected[:-1], list(reversed(expected)),
                        [row[:-2] + row[-2:][::-1] for row in expected], bad_boolean]
            for actual in variants:
                with self.assertRaises(ValueError):
                    checker.check_coordinates(actual, expected)

    def test_duplicate_nonfinite_and_malformed_json_rejected(self):
        for raw in (b'{"source_export":null,"source_export":{}}', b'{"x":NaN}', b'{'):
            with self.assertRaises(ValueError):
                checker.decode(raw)

    def test_spans_are_byte_bound_and_regularizer_excluded(self):
        for role, bounds in checker.SPANS.items():
            item = checker.span(self.source, *bounds)
            checker.check_span(item, self.source, role)
            item["sha256"] = "0" * 64
            with self.assertRaises(ValueError):
                checker.check_span(item, self.source, role)
        with self.assertRaises(ValueError):
            checker.check_span(checker.span(self.source, 60, 60), self.source, "pre_regularizer")


if __name__ == "__main__":
    unittest.main()
