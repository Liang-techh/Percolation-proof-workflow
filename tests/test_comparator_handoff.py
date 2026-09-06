import hashlib
import unittest

from percolation_workflow.comparator_handoff import check_comparator_handoff


class ComparatorHandoffGuardTests(unittest.TestCase):
    def complete(self):
        return dict(
            statement_identity={"module": "Challenge", "name": "C"},
            source_hash=hashlib.sha256(b"source").hexdigest(),
            coverage={"complete": True},
            numeric_receipt={"status": "accepted"},
            kernel_evidence={"status": "verified"},
        )

    def test_all_five_evidence_classes_are_reviewable(self):
        result = check_comparator_handoff(**self.complete())
        self.assertEqual(result.status, "reviewable")
        self.assertEqual(result.blockers, ())

    def test_each_missing_class_is_a_structured_blocker(self):
        for field in self.complete():
            with self.subTest(field=field):
                packet = self.complete()
                packet[field] = None
                result = check_comparator_handoff(**packet)
                self.assertEqual(result.status, "blocked")
                self.assertIn(f"missing_{field}", {b["code"] for b in result.blockers})

    def test_guard_has_no_registry_or_admission_side_effect(self):
        result = check_comparator_handoff(**self.complete())
        self.assertNotIn("registry_status", result.to_dict())
        self.assertNotIn("admission_status", result.to_dict())


if __name__ == "__main__":
    unittest.main()
