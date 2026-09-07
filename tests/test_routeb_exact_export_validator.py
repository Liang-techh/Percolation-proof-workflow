import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "artifacts/task_BD_exact_coefficient_gram_validator_20260906/validate_exact_export.py"
if not SCRIPT.is_file():
    raise unittest.SkipTest(f"optional local artifact is not checked in: {SCRIPT}")
spec = importlib.util.spec_from_file_location("exact_export_validator", SCRIPT)
validator = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(validator)


class RouteBExactExportValidatorTests(unittest.TestCase):
    def test_existing_float64_missing_export_is_fail_closed(self):
        contract = json.loads((ROOT / "artifacts/task_AU_routeb_pmi_export_v2/contract.json").read_text())
        result = validator.validate(ROOT / "artifacts/task_AU_routeb_pmi_export_v2", contract)
        self.assertEqual(result["result"], "FAIL_CLOSED")
        self.assertFalse(result["exact_coefficients"])
        self.assertFalse(result["exact_gram"])
        self.assertTrue(any("missing file" in error for error in result["errors"]))

    def test_float64_sentinel_cannot_be_relabelled_exact(self):
        with tempfile.TemporaryDirectory() as directory:
            package = Path(directory)
            contract = json.loads((ROOT / "artifacts/task_AU_routeb_pmi_export_v2/contract.json").read_text())
            (package / "export_manifest.json").write_text(json.dumps({
                "schema_version": "routeB-pmi-export-v2", "variable_order": list(validator.VARIABLES),
                "exact_coefficients": True, "exact_gram": True,
                "promotion_allowed": False, "registry_promoted": False,
                "formal_certificate_allowed": False,
            }))
            for name, columns in validator.REQUIRED.items():
                content = ",".join(columns) + "\n"
                if name == "polynomial_coefficients.csv":
                    values = {column: "0" for column in columns}
                    values.update({"object": "D0", "term_id": "t0", "coefficient_exact": validator.SENTINEL})
                    content += ",".join(values[column] for column in columns) + "\n"
                (package / name).write_text(content)
            result = validator.validate(package, contract)
            self.assertEqual(result["result"], "FAIL_CLOSED")
            self.assertTrue(any("sentinel" in error for error in result["errors"]))


if __name__ == "__main__":
    unittest.main()
