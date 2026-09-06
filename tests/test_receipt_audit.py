import hashlib
import json
import unittest

from percolation_workflow.comparator import (
    build_comparator_manifest,
    validate_candidate_receipt,
)


def digest(value):
    return hashlib.sha256(json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")).hexdigest()


class CandidateReceiptAuditTests(unittest.TestCase):
    def fixture(self):
        snapshot = {"nodes": {
            "child": {"node_id": "child", "parent_id": "parent",
                       "child_ids": [], "dependency_ids": ["dep"]},
            "dep": {"node_id": "dep", "parent_id": None,
                     "child_ids": [], "dependency_ids": []},
            "parent": {"node_id": "parent", "parent_id": None,
                        "child_ids": ["child"], "dependency_ids": []},
        }}
        statement_identity = {
            "module": "Challenge",
            "name": "Namespace.child",
            "statement_sha256": "a" * 64,
            "challenge_sha256": "b" * 64,
        }
        receipt = {
            "schema_version": 1,
            "status": "compiled_candidate",
            "statement_identity": statement_identity,
            "dag_binding": snapshot["nodes"]["child"],
            "dag_snapshot_sha256": digest(snapshot),
            "source_hashes": {"Challenge.lean": "c" * 64},
            "olean_hashes": {"Namespace.child.olean": "d" * 64},
            "lean_toolchain": "leanprover/lean4:v4.33.1",
            "mathlib_commit": "m" * 40,
            "axioms": {"Namespace.child": ["propext"]},
            "strict_admission": {
                "accepted": True,
                "axioms": {"Namespace.child": ["propext"]},
                "toolchain": "leanprover/lean4:v4.33.1",
            },
            "comparator_status": "accepted",
            "comparator_command": ["trusted-comparator"],
            "comparator_stdout": "Your solution is okay!\n",
            "comparator_stderr": "",
        }
        receipt["receipt_sha256"] = digest(receipt)
        return receipt, snapshot, statement_identity

    def bound(self, receipt, snapshot, statement_identity):
        return dict(
            expected_statement_identity=statement_identity,
            expected_dag_snapshot_sha256=receipt["dag_snapshot_sha256"],
            expected_source_hashes=receipt["source_hashes"],
            expected_olean_hashes=receipt["olean_hashes"],
            expected_lean_toolchain=receipt["lean_toolchain"],
            expected_mathlib_commit=receipt["mathlib_commit"],
            expected_axioms=receipt["axioms"],
            dag_snapshot=snapshot,
        )

    def test_valid_candidate_is_accepted_but_comparator_remains_pending(self):
        receipt, snapshot, identity = self.fixture()
        audit = validate_candidate_receipt(receipt, **self.bound(receipt, snapshot, identity))
        self.assertTrue(audit.accepted)
        manifest = build_comparator_manifest(receipt, **self.bound(receipt, snapshot, identity))
        self.assertEqual(manifest["status"], "compiled_candidate")
        self.assertEqual(manifest["candidate_status"], "compiled_candidate")
        self.assertEqual(manifest["comparator_status"], "accepted")
        self.assertEqual(manifest["registry_status"], "pending")

    def test_legacy_receipt_is_explicitly_pending(self):
        receipt, _, _ = self.fixture()
        legacy = {"source_hashes": receipt["source_hashes"]}
        audit = validate_candidate_receipt(legacy)
        self.assertTrue(audit.pending)
        self.assertFalse(audit.accepted)
        manifest = build_comparator_manifest(legacy)
        self.assertEqual(manifest["status"], "pending")
        self.assertEqual(manifest["comparator_status"], "pending")

    def test_hash_and_identity_drift_is_rejected(self):
        receipt, snapshot, identity = self.fixture()
        receipt["source_hashes"] = {"Challenge.lean": "e" * 64}
        audit = validate_candidate_receipt(receipt, **self.bound(receipt, snapshot, identity))
        self.assertTrue(audit.rejected)
        self.assertIn("receipt self-hash mismatch", audit.reasons)

        receipt, snapshot, identity = self.fixture()
        identity = dict(identity, statement_sha256="f" * 64)
        audit = validate_candidate_receipt(receipt, **self.bound(receipt, snapshot, identity))
        self.assertTrue(audit.rejected)
        self.assertIn("statement_identity mismatch: statement_sha256", audit.reasons)

    def test_missing_or_bad_comparator_and_strict_evidence_cannot_pass(self):
        receipt, snapshot, identity = self.fixture()
        del receipt["strict_admission"]
        receipt["receipt_sha256"] = digest({k: v for k, v in receipt.items()
                                             if k != "receipt_sha256"})
        audit = validate_candidate_receipt(receipt, **self.bound(receipt, snapshot, identity))
        self.assertTrue(audit.pending)
        self.assertIn("missing strict_admission report", audit.reasons)

        receipt, snapshot, identity = self.fixture()
        receipt["comparator_stdout"] = "build succeeded\n"
        receipt["receipt_sha256"] = digest({k: v for k, v in receipt.items()
                                             if k != "receipt_sha256"})
        audit = validate_candidate_receipt(receipt, **self.bound(receipt, snapshot, identity))
        self.assertTrue(audit.rejected)
        self.assertIn("comparator output lacks the exact acceptance line", audit.reasons)

    def test_duplicate_unsorted_and_dangling_edges_are_rejected(self):
        receipt, snapshot, identity = self.fixture()
        receipt["dag_binding"] = dict(receipt["dag_binding"], dependency_ids=["dep", "dep"])
        receipt["receipt_sha256"] = digest({k: v for k, v in receipt.items()
                                             if k != "receipt_sha256"})
        audit = validate_candidate_receipt(receipt, **self.bound(receipt, snapshot, identity))
        self.assertTrue(audit.rejected)
        self.assertTrue(any("duplicate" in reason for reason in audit.reasons))

        receipt, snapshot, identity = self.fixture()
        receipt["dag_binding"] = dict(receipt["dag_binding"], dependency_ids=["missing"])
        receipt["receipt_sha256"] = digest({k: v for k, v in receipt.items()
                                             if k != "receipt_sha256"})
        audit = validate_candidate_receipt(receipt, **self.bound(receipt, snapshot, identity))
        self.assertTrue(audit.rejected)
        self.assertTrue(any("dangling" in reason for reason in audit.reasons))


if __name__ == "__main__":
    unittest.main()
