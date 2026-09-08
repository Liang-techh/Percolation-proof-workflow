"""Focused development checks; no manufactured DAGs, constants or runtime bits."""
import json
import unittest
from unittest.mock import patch

import NEW_SEAM_contract_audit as audit


class ContractAuditTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.raw = (audit.HERE / "NEW_INTAKE.json").read_bytes()
        cls.source = audit.base.SOURCE.read_bytes()

    def test_real_empty_intake_remains_pending(self):
        result = audit.inspect(self.raw, self.source)
        self.assertEqual(result["checker_exit_code"], 3)
        self.assertTrue(all(v is None for v in result["canonical_component_bindings"].values()))
        self.assertIsNone(result["occurrence_line_gaps"])
        self.assertIsNone(result["runtime_evidence"])
        self.assertIsNone(result["generated_source_export"])
        self.assertFalse(result["admission"]["h_acc_expr_proven"])
        self.assertTrue(all(not r["verified"] and r["artifact"] is None for r in result["obligation_plan"]))

    def test_fragment_ranges_use_actual_raw_bytes(self):
        sites = audit.seam.source_sites(self.source)
        families = audit.use_families(sites)
        for row in families:
            s = row["source_location"]
            self.assertEqual(self.source[s["byte_start"]:s["byte_end_exclusive"]].decode(), s["source_text"])
        self.assertEqual([r["required_coordinate_count"] for r in families], [18, 54, 63, 45, 45])
        self.assertEqual(families[2]["source_location"]["source_span"]["start_line"], 56)
        self.assertEqual(families[3]["source_location"]["source_span"]["start_line"], 53)
        self.assertTrue(all(r["actual_node_binding"] is None for r in families))

    def test_same_line_does_not_identify_same_expression(self):
        sites = audit.inspect(self.raw, self.source)["line58_sites"]
        self.assertEqual(len({s["source_span"]["sha256"] for s in sites.values()}), 1)
        self.assertEqual(len({s["fragment_sha256"] for s in sites.values()}), 4)

    def test_obligation_dependencies_are_non_circular(self):
        rules = {r["id"]: r for r in audit.rule_plan()}
        self.assertEqual(rules["BODY"]["depends_on"], ["EVAL", "OPERANDS"])
        self.assertEqual(rules["FOLD"]["depends_on"], ["EVAL", "BODY", "SOURCE_LOOP"])
        with patch.object(audit, "RULES", [("K", ["H_ACC_EXPR"], "invalid plan")]):
            with self.assertRaises(ValueError):
                audit.rule_plan()

    def test_source_drift_rejected(self):
        with self.assertRaisesRegex(ValueError, "pinned source"):
            audit.inspect(self.raw, self.source + b" ")

    def test_duplicate_key_rejected(self):
        with self.assertRaisesRegex(ValueError, "duplicate"):
            audit.inspect(b'{"source_export":null,"source_export":null}', self.source)

    def test_promotion_rejected_without_graph(self):
        doc = audit.base.decode(self.raw)
        doc["admission"]["h_acc_expr_proven"] = True
        with self.assertRaisesRegex(ValueError, "promotion"):
            audit.inspect(json.dumps(doc).encode(), self.source)

    def test_missing_file_pending(self):
        with patch.object(audit, "inspect", side_effect=FileNotFoundError("absent")):
            result, code = audit.audit()
            self.assertEqual((result["status"], code), ("pending", 3))

    def test_malformed_audit_exit(self):
        with patch.object(audit, "inspect", side_effect=ValueError("malformed")):
            result, code = audit.audit()
            self.assertEqual((result["status"], code), ("rejected", 2))


if __name__ == "__main__":
    unittest.main()
