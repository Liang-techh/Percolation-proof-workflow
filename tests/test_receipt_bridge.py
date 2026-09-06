import unittest

from percolation_workflow.receipt_bridge import receipt_to_frontier_outcome


class ReceiptBridgeTests(unittest.TestCase):
    def test_maps_supported_statuses_to_advisory_scheduler_outcomes(self):
        expected = {
            "validated": "advisory_validated",
            "failed": "advisory_failed",
            "missing": "advisory_missing",
            "needs_manual_review": "advisory_needs_manual_review",
        }
        for status, outcome in expected.items():
            with self.subTest(status=status):
                result = receipt_to_frontier_outcome({"status": status, "extra": object()})
                self.assertEqual(result["outcome"], outcome)
                self.assertEqual(result["receipt_status"], status)
                self.assertTrue(result["advisory"])
                self.assertFalse(result["verified"])

    def test_only_retryable_receipts_are_dispatchable(self):
        self.assertTrue(receipt_to_frontier_outcome({"status": "failed"})["dispatchable"])
        self.assertTrue(receipt_to_frontier_outcome({"status": "missing"})["dispatchable"])
        self.assertFalse(receipt_to_frontier_outcome({"status": "validated"})["dispatchable"])
        self.assertTrue(receipt_to_frontier_outcome({"status": "needs_manual_review"})["requires_manual_review"])

    def test_rejects_unknown_status_without_promoting_anything(self):
        with self.assertRaises(ValueError):
            receipt_to_frontier_outcome({"status": "verified"})


if __name__ == "__main__":
    unittest.main()

