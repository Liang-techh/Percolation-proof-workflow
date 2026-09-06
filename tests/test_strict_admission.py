import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from percolation_workflow.lean import LeanResult
from percolation_workflow.strict_admission import _parse_axioms, audit_strict_admission


class StrictAdmissionTests(unittest.TestCase):
    def test_parses_real_lean_axiom_report_with_multiline_values(self):
        output = ("'Target.ok' depends on axioms: [propext,\n"
                  " Classical.choice,\n Quot.sound]\n")
        self.assertEqual(
            _parse_axioms(output, ("Target.ok",))["Target.ok"],
            ("propext", "Classical.choice", "Quot.sound"))

    def test_solution_module_is_imported_and_challenge_can_be_excluded(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.project(root, "theorem Target.ok : True := by trivial\n")
            (root / "Challenge.lean").write_text("theorem Target.ok : True := by sorry\n")
            result = LeanResult(
                True, ["lake", "env", "lean"],
                "'Target.ok' depends on axioms: [propext, Classical.choice]\n", "", 0)
            with patch("percolation_workflow.strict_admission.run_lean", return_value=result) as run:
                audit = audit_strict_admission(
                    root, ["Target.ok"], solution_module="Solution",
                    challenge_module="Challenge")
            self.assertTrue(audit.accepted)
            self.assertEqual(run.call_args.args[1][-1].endswith('.lean'), True)

    def project(self, root: Path, source: str = "theorem Target.ok : True := by trivial\n"):
        (root / "lean-toolchain").write_text("leanprover/lean4:v4.33.1\n")
        (root / "lake-manifest.json").write_text(json.dumps({"packages": []}))
        (root / "Solution.lean").write_text(source)

    def test_accepts_exact_axiom_output_and_records_pins(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.project(root)
            output = "axioms Target.ok uses: propext Classical.choice\n"
            result = LeanResult(True, ["lake", "env", "lean"], output, "", 0)
            with patch("percolation_workflow.strict_admission.run_lean", return_value=result):
                audit = audit_strict_admission(root, ["Target.ok"], expected_toolchain="leanprover/lean4:v4.33.1")
            self.assertTrue(audit.accepted)
            self.assertEqual(audit.axioms["Target.ok"], ("propext", "Classical.choice"))
            self.assertTrue(audit.toolchain_sha256)
            self.assertTrue(audit.lake_manifest_sha256)

    def test_rejects_placeholder_before_running_lean(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.project(root, "theorem Target.ok : True := by sorry\n")
            with patch("percolation_workflow.strict_admission.run_lean") as run:
                audit = audit_strict_admission(root, ["Target.ok"])
            self.assertFalse(audit.accepted)
            self.assertTrue(any("forbidden" in reason for reason in audit.reasons))
            run.assert_not_called()

    def test_rejects_unknown_axiom_and_missing_evidence_fail_closed(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.project(root)
            result = LeanResult(True, ["lake", "env", "lean"], "axioms Target.ok uses: badAx\n", "", 0)
            with patch("percolation_workflow.strict_admission.run_lean", return_value=result):
                audit = audit_strict_admission(root, ["Target.ok"])
            self.assertFalse(audit.accepted)
            self.assertTrue(any("unexpected axioms" in reason for reason in audit.reasons))

            result = LeanResult(True, ["lake", "env", "lean"], "", "", 0)
            with patch("percolation_workflow.strict_admission.run_lean", return_value=result):
                audit = audit_strict_admission(root, ["Target.ok"])
            self.assertFalse(audit.accepted)
            self.assertTrue(any("missing #print axioms" in reason for reason in audit.reasons))
