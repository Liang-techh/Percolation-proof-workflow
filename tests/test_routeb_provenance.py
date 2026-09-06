import importlib.util
import json
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch
import zipfile


spec = importlib.util.spec_from_file_location(
    "routeb_provenance_audit", Path(__file__).resolve().parents[1] / "scripts/audit_routeb_provenance.py")
provenance = importlib.util.module_from_spec(spec)
spec.loader.exec_module(provenance)


class RouteBProvenanceTests(unittest.TestCase):
    def fixture(self, root):
        old = b"# historical source\n"
        sha = provenance.digest(old)
        for folder in ("robot_final", "routeB_dense_Mq", "robot_formal_v1"):
            (root / folder).mkdir(parents=True)
        for folder in ("robot_final", "routeB_dense_Mq"):
            (root / folder / "routeB_interval_bounds.jl").write_bytes(old)
            report = root / folder / "P3_REPORT.md"
            report.write_text(f"- source_sha256: `{sha}`\n", encoding="utf-8")
            Path(str(report) + ".backup_20260905_pre_provenance_sync").write_bytes(report.read_bytes())
        (root / "robot_final/routeB_certificate_manifest.toml").write_text(
            f'interval_candidate_sha256 = "{sha}"\n', encoding="utf-8")
        (root / "robot_formal_v1/manifest.json").write_text(json.dumps({
            "current_gate": {"formal_certificate_allowed": False}, "artifacts": []}), encoding="utf-8")
        with zipfile.ZipFile(root / "routeB_reform_handoff.zip", "w") as archive:
            for folder in ("robot_final", "routeB_dense_Mq"):
                archive.writestr(f"{folder}/routeB_interval_bounds.jl", old)
        return sha

    def test_historical_recovery_is_not_current_replay(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            sha = self.fixture(root)
            (root / "robot_final/routeB_interval_bounds.jl").write_text("# new algorithm\n", encoding="utf-8")
            before = {p.relative_to(root): p.read_bytes() for p in root.rglob("*") if p.is_file()}
            with patch.object(provenance, "HISTORICAL_SOURCE", sha):
                result = provenance.audit(root)
            after = {p.relative_to(root): p.read_bytes() for p in root.rglob("*") if p.is_file()}
            self.assertEqual(before, after)
            self.assertTrue(all(row["historical_source_available"] for row in result["historical_reports"]))
            self.assertFalse(result["current_baseline_complete"])
            self.assertFalse(result["historical_result_replay_performed"])
            self.assertFalse(result["registry_eligible"])
            self.assertIn("current_delivery_source_does_not_match_historical_manifest", result["issues"])

    def test_hash_consistency_without_checker_does_not_complete_baseline(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            sha = self.fixture(root)
            with patch.object(provenance, "HISTORICAL_SOURCE", sha):
                result = provenance.audit(root)
            self.assertEqual(result["issues"], ["current_delivery_checker_not_run"])
            self.assertFalse(result["current_baseline_complete"])

    def test_failed_checker_preserved_even_when_hashes_match(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            sha = self.fixture(root)
            failure = subprocess.CompletedProcess(["checker"], 1, "", "deliberate failure")
            with patch.object(provenance, "HISTORICAL_SOURCE", sha), patch.object(
                    provenance.subprocess, "run", return_value=failure):
                result = provenance.audit(root, run_checker=True)
            self.assertEqual(result["checker"]["exit_code"], 1)
            self.assertEqual(result["checker"]["stderr"], "deliberate failure")
            self.assertFalse(result["current_baseline_complete"])


if __name__ == "__main__":
    unittest.main()
