import sys
import tempfile
import unittest
from percolation_workflow.comparator import run_comparator


class AcceptanceTests(unittest.TestCase):
    def test_both_exact_acceptance_and_exit_zero_required(self):
        with tempfile.TemporaryDirectory() as directory:
            for code, expected in [
                ("print('build succeeded')", False),
                ("print('prefix Your solution is okay!')", False),
                ("print('Your solution is okay!'); raise SystemExit(1)", False),
                ("print('Your solution is okay!')", True),
            ]:
                with self.subTest(code=code):
                    ok, _, _ = run_comparator(directory, [sys.executable, '-c', code])
                    self.assertEqual(ok, expected)
