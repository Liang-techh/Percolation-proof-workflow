import csv
import tempfile
import unittest
from pathlib import Path

import check_fold


class FixedLambdaFoldTests(unittest.TestCase):
    def test_declared_partitions_fold_without_dense_global_labels(self):
        result = check_fold.audit()
        self.assertEqual(result["status"], "PASS_EXACT_DECLARED_FINITE_FOLD_ONLY")
        self.assertEqual(result["fold"]["witness_count"], 577)
        self.assertEqual(result["partitions"]["2.7"]["distinct_boxes"], 256)
        self.assertEqual(result["partitions"]["5.6"]["distinct_boxes"], 321)
        self.assertFalse(result["partitions"]["5.6"]["dense_box_ids"])
        self.assertFalse(result["true_dh_coverage_proven"])

    def test_duplicate_selected_box_is_rejected(self):
        with check_fold.LEDGER.open(newline="", encoding="utf-8") as handle:
            rows = list(csv.DictReader(handle))
        selected = next(row for row in rows
                        if row["eta"] == "5.6" and row["lambda"] == "2.0"
                        and row.get("theta") == "1.0")
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "ledger.csv"
            with path.open("w", newline="", encoding="utf-8") as handle:
                writer = csv.DictWriter(handle, fieldnames=rows[0].keys())
                writer.writeheader()
                writer.writerows(rows)
                writer.writerow(selected)
            result = check_fold.audit(path)
        self.assertEqual(result["status"], "FAIL")
        self.assertTrue(any("duplicate_box_id" in error for error in result["errors"]))


if __name__ == "__main__":
    unittest.main()
