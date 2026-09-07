"""Targeted tests of source locations and fail-closed seam status; no fake export."""
import copy
from hashlib import sha256
import sys
import unittest

sys.dont_write_bytecode = True
import NEW_SEAM_source as seam


class SourceSeamTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source = seam.base.SOURCE.read_bytes()
        cls.raw = (seam.HERE / "NEW_INTAKE.json").read_bytes()

    def test_real_empty_intake_stays_pending(self):
        report = seam.inspect(self.raw, self.source)
        self.assertEqual(report["checker_exit_code"], 3)
        self.assertEqual(report["status"], "pending")
        self.assertIn("REAL_SOURCE_EXPORT_ABSENT", report["blockers"])
        self.assertIsNone(report["source_export_sha256"])
        self.assertIsNone(report["occurrence_line_gaps"])
        for name in ("generated_source_export", "generated_constant_values",
                     "generated_runtime_observation"):
            self.assertIsNone(report[name])
        for witness in report["required_witnesses"].values():
            self.assertIsNone(witness["artifact"])
            self.assertFalse(witness["verified"])
        self.assertEqual(report["admission"], seam.intake.template()["admission"])

    def test_every_fragment_roundtrips_raw_bytes(self):
        sites = seam.source_sites(self.source)
        self.assertEqual(set(sites), set(seam.SITES))
        for site in sites.values():
            raw = self.source[site["byte_start"]:site["byte_end_exclusive"]]
            self.assertEqual(raw.decode("utf-8"), site["source_text"])
            self.assertEqual(sha256(raw).hexdigest(), site["fragment_sha256"])
            line = site["source_span"]["start_line"]
            self.assertLess(line, 60)
            self.assertEqual(site["source_span"], seam.base.span(self.source, line, line))

    def test_line58_roles_are_distinct_and_nested(self):
        sites = seam.source_sites(self.source)
        translation, rotation, body, update = [sites[k] for k in
            ("translation", "rotation", "body_sum", "accumulator_update")]
        self.assertLessEqual(translation["byte_end_exclusive"], rotation["byte_start"])
        self.assertEqual(translation["source_span"], rotation["source_span"])
        self.assertNotEqual(translation["fragment_sha256"], rotation["fragment_sha256"])
        self.assertLess(update["byte_start"], body["byte_start"])
        for child in (translation, rotation):
            self.assertLessEqual(body["byte_start"], child["byte_start"])
            self.assertLessEqual(child["byte_end_exclusive"], body["byte_end_exclusive"])
        self.assertEqual(body["byte_end_exclusive"], update["byte_end_exclusive"])

    def test_source_mutation_and_newline_normalization_rejected(self):
        changed = self.source.replace(b"Ri * Ii * Ri'", b"Ri * Ri' * Ii", 1)
        self.assertNotEqual(changed, self.source)
        with self.assertRaisesRegex(ValueError, "source bytes mismatch"):
            seam.inspect(self.raw, changed)
        newline_changed = (self.source.replace(b"\r\n", b"\n") if b"\r\n" in self.source
                           else self.source.replace(b"\n", b"\r\n"))
        with self.assertRaisesRegex(ValueError, "source bytes mismatch"):
            seam.source_sites(newline_changed)

    def test_occurrence_initial_parent_current_and_prefix(self):
        for stage, coord, expected in (
            ("Tc", [0, 1, 1], 32), ("Tc", [1, 1, 1], 40),
            ("o", [0, 1], 33), ("o", [1, 1], 41),
            ("z", [1, 1], 36), ("Ri", [6, 1, 1], 51),
            ("Jw", [1, 1, 1], 56), ("Jw", [1, 1, 2], 53),
            ("Jv", [6, 1, 6], 55), ("Jv", [1, 1, 2], 53)):
            self.assertEqual(seam.occurrence_line(stage, coord), expected)

    def test_valid_v1_anchor_can_leave_a_semantic_occurrence_gap(self):
        # Location-only records for this helper, not a graph or intake/export.
        records = {"z": [{"coordinate": [1, 1],
                          "source_span": seam.base.span(self.source, 34, 34)}]}
        seam.base.check_span(records["z"][0]["source_span"], self.source, "z")
        self.assertEqual(seam.occurrence_gaps(records)[0]["required_line"], 36)
        for start in (34, 36):
            records["z"][0]["source_span"] = seam.base.span(self.source, start, 36)
            self.assertEqual(seam.occurrence_gaps(records), [])

    def test_duplicate_keys_even_null_rejected(self):
        for key in ("source_export", "source_updates", "runtime_observation"):
            token = ('"' + key + '": null').encode()
            self.assertEqual(self.raw.count(token), 1)
            with self.assertRaisesRegex(ValueError, "duplicate JSON key"):
                seam.inspect(self.raw.replace(token, token + b", " + token), self.source)

    def test_promotion_or_fabricated_export_envelope_rejected(self):
        doc = seam.base.decode(self.raw)
        changed = copy.deepcopy(doc)
        changed["admission"]["h_acc_expr_proven"] = True
        with self.assertRaisesRegex(ValueError, "promotion prohibited"):
            seam.inspect(seam.base.canonical(changed), self.source)
        changed = copy.deepcopy(doc)
        changed["source_export"] = {}
        with self.assertRaisesRegex(ValueError, "export hash mismatch"):
            seam.inspect(seam.base.canonical(changed), self.source)

    def test_audit_reports_three_and_two_without_writes(self):
        report, code = seam.audit(seam.HERE / "NEW_INTAKE.json")
        self.assertEqual(code, 3)
        self.assertEqual(report["execution"]["files_written"], 0)
        # The existing Python file is invalid JSON; no malformed fixture is saved.
        report, code = seam.audit(seam.HERE / "NEW_source_intake.py")
        self.assertEqual(code, 2)
        self.assertEqual(report["status"], "rejected")
        report, code = seam.audit(seam.HERE / "NEW_SEAM_intentionally_absent.json")
        self.assertEqual(code, 3)
        self.assertTrue(report["blockers"][0].startswith("MISSING_ARTIFACT:"))


if __name__ == "__main__":
    unittest.main()
