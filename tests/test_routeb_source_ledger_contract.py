import json
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from routeb_source_ledger_contract import (  # noqa: E402
    REQUIRED_NUMERIC_FIELDS,
    build_manifest,
    canonical_sha256,
)


SNAPSHOT = Path(__file__).resolve().parents[1] / "examples" / "routeb_source_binding_audit" / "snapshots"


class RouteBSourceLedgerContractTests(unittest.TestCase):
    def test_missing_receipt_is_fail_closed_and_has_no_synthesized_values(self):
        manifest = build_manifest(SNAPSHOT)
        self.assertEqual(manifest["status"], "FAIL_CLOSED")
        self.assertFalse(manifest["verified"])
        self.assertFalse(manifest["registry_eligible"])
        self.assertEqual(manifest["missing_numeric_fields"], list(REQUIRED_NUMERIC_FIELDS))
        self.assertTrue(all(row["value"] is None for row in manifest["numeric_fields"]))
        self.assertIn("original_target/routeB_interval_bounds.jl", manifest["missing_source_bindings"])

    def test_expected_source_hashes_are_bound(self):
        manifest = build_manifest(SNAPSHOT)
        dh = next(row for row in manifest["sources"] if row["path"] == "original_target/dhport_lib.jl")
        self.assertEqual(dh["sha256"], dh["expected_sha256"])
        self.assertTrue(dh["hash_matches_expected"])
        field = next(row for row in manifest["numeric_fields"] if row["name"] == "Cdq")
        self.assertEqual(field["source"]["path"], "original_target/dhport_lib.jl")
        self.assertEqual(field["source"]["sha256"], dh["sha256"])
        self.assertEqual(field["source"]["line_anchors"], [73, 92])

    def test_receipt_cannot_pass_without_manifest_bound_provenance(self):
        base = build_manifest(SNAPSHOT)
        receipt = {
            "schema": "routeb.source_ledger.numeric_receipt.v1",
            "contract_sha256": base["contract_sha256"],
            "cell": {"cell_id": "cell-0", "q_box": [0, 0], "dq_box": [0, 0], "w_box": [0, 0]},
            "fields": {name: {"value": 1.0} for name in REQUIRED_NUMERIC_FIELDS},
        }
        manifest = build_manifest(SNAPSHOT, receipt=receipt)
        self.assertEqual(manifest["status"], "FAIL_CLOSED")
        self.assertEqual(manifest["missing_numeric_fields"], list(REQUIRED_NUMERIC_FIELDS))
        self.assertTrue(manifest["receipt_rejection_reasons"])
        self.assertIsNone(manifest["numeric_receipt"])

    def test_manifest_hash_is_deterministic_for_same_snapshot(self):
        first = build_manifest(SNAPSHOT)
        second = build_manifest(SNAPSHOT)
        self.assertEqual(first["manifest_sha256"], second["manifest_sha256"])
        self.assertEqual(first["manifest_sha256"], canonical_sha256({k: v for k, v in first.items() if k != "manifest_sha256"}))


if __name__ == "__main__":
    unittest.main()
