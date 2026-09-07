"""Synthetic arithmetic/format controls ONLY, never concrete source K_path data.

Fixtures stay in memory. No Lean/Lake is invoked; Python CLI probes use stdin.
"""
from copy import deepcopy
from fractions import Fraction as F
import json
from pathlib import Path
import subprocess
import sys
import unittest
from unittest.mock import patch

import NEW_KPATH_INTERFACE_Comparison as C


def synthetic():
    # Hand-derived two-segment, two-raw-force, two-source-coordinate fixture.
    # A has scale 1/10, H scale 1/3, S scale 1/7: total scale 1/210.
    # Unscaled path rows are (20,9,20,15) and (20,17,10,25).
    def table(rows, d):
        return [[str(F(x, d)) for x in row] for row in rows]
    K = table([[20, 9, 20, 15], [20, 17, 10, 25]], 210)
    return {
        "schema": C.SCHEMA, "scope": C.SCOPE, "coordinates": deepcopy(C.COORDINATES),
        "path": {
            "A": table([[-1, 2], [3, -1]], 10),
            "Hjac": [table([[1, 0], [0, 2]], 3), table([[0, 3], [4, 0]], 3)],
            "Scoord": [table([[1, 2, 0, 1], [0, 1, 3, 2]], 7),
                       table([[2, 0, 1, 0], [1, 1, 0, 2]], 7)],
            "K_path": K,
        },
        "K_cert": deepcopy(K),
    }


def raw(p):
    return json.dumps(p, separators=(",", ":")).encode("utf-8")


class ExactComparisonTests(unittest.TestCase):
    def reject(self, p, code):
        with self.assertRaises(C.Rejected) as caught:
            C.check_bytes(raw(p))
        self.assertEqual(caught.exception.code, code)

    def test_independent_golden_and_positive_slack(self):
        p = synthetic()
        result = C.check_bytes(raw(p))
        self.assertEqual([r["slack"] for r in result["entries"]], ["0"] * 8)
        for a in range(2):
            for j in range(4):
                p["K_cert"][a][j] = str(F(p["K_cert"][a][j]) + F(a * 4 + j + 1, 210))
        result = C.check_bytes(raw(p))
        self.assertEqual([r["slack"] for r in result["entries"]],
                         [str(F(k, 210)) for k in range(1, 9)])
        self.assertEqual(result["identity_entries_checked"], 8)
        self.assertEqual(result["comparison_entries_checked"], 8)
        for key, value in C.boundary().items():
            self.assertEqual(result[key], value)

    def test_absolute_force_map(self):
        p = synthetic()
        p["path"]["A"] = [[str(-F(v)) for v in row] for row in p["path"]["A"]]
        self.assertTrue(C.check_bytes(raw(p))["arithmetic_valid"])

    def test_zero_gain_is_arithmetic_only(self):
        p = synthetic()
        p["path"]["A"] = [["0", "0"], ["0", "0"]]
        p["path"]["K_path"] = [["0"] * 4 for _ in range(2)]
        p["K_cert"] = deepcopy(p["path"]["K_path"])
        result = C.check_bytes(raw(p))
        self.assertTrue(result["arithmetic_valid"])
        self.assertFalse(result["source_binding_verified"])

    def test_all_eight_identity_slots(self):
        for a in range(2):
            for j in range(4):
                with self.subTest(a=a, j=j):
                    p = synthetic()
                    p["path"]["K_path"][a][j] = str(F(p["path"]["K_path"][a][j]) - F(1, 1000))
                    self.reject(p, "pathK_identity_mismatch")

    def test_all_eight_comparison_slots_no_tolerance(self):
        for a in range(2):
            for j in range(4):
                with self.subTest(a=a, j=j):
                    p = synthetic()
                    p["K_cert"][a][j] = str(F(p["K_cert"][a][j]) - F(1, 10**40))
                    self.reject(p, "componentwise_comparison_failed")

    def test_scalar_larger_does_not_imply_componentwise(self):
        p = synthetic()
        p["K_cert"][0][0] = "0"
        p["K_cert"][1][3] = "1000"
        self.assertGreater(sum(F(v)**2 for row in p["K_cert"] for v in row),
                           sum(F(v)**2 for row in p["path"]["K_path"] for v in row))
        self.reject(p, "componentwise_comparison_failed")

    def test_numeric_and_noncanonical_inputs(self):
        cases = [(0, "json_number_forbidden"), (0.5, "json_number_forbidden"),
                 (True, "rational_string_required"), (None, "rational_string_required")]
        cases += [(v, "rational_syntax") for v in
                  ["0.5", "1e-30", "NaN", "Infinity", "1/0", "1/-2", "01", "+1", " 1", "1 "]]
        cases += [(v, "rational_not_canonical") for v in ["2/4", "1/1", "0/2", "-0"]]
        cases += [("1" * 65, "rational_size")]
        for value, code in cases:
            with self.subTest(value=value):
                p = synthetic()
                p["K_cert"][0][0] = value
                self.reject(p, code)

    def test_unknown_fields_and_scope(self):
        for field in ["source_bound", "registry_eligible", "H_matrix_order", "tolerance", "ell2", "mu"]:
            p = synthetic()
            p[field] = True
            self.reject(p, "object_fields")
        p = synthetic()
        p["path"]["source_hash"] = "0" * 64
        self.reject(p, "object_fields")
        p = synthetic()
        p["scope"] = "source-bound"
        self.reject(p, "scope")
        p = synthetic()
        del p["path"]["Hjac"]
        self.reject(p, "object_fields")

    def test_coordinates_shapes_and_normalization(self):
        p = synthetic()
        p["coordinates"]["state"][1:3] = reversed(p["coordinates"]["state"][1:3])
        self.reject(p, "coordinate_order")
        p = synthetic()
        p["coordinates"]["force"].reverse()
        self.reject(p, "coordinate_order")
        for key in ["A", "Hjac", "Scoord", "K_path"]:
            p = synthetic()
            p["path"][key].pop()
            self.reject(p, "matrix_shape")
        p = synthetic()
        p["K_cert"][0].append("0")
        self.reject(p, "matrix_shape")
        p = synthetic()
        p["path"]["K_path"][0].reverse()
        self.reject(p, "pathK_identity_mismatch")
        p = synthetic()
        p["path"]["A"] = [[str(2 * F(v)) for v in row] for row in p["path"]["A"]]
        self.reject(p, "pathK_identity_mismatch")

    def test_negative_entries(self):
        for key in ["Hjac", "Scoord", "K_path", "K_cert"]:
            p = synthetic()
            target = p[key] if key == "K_cert" else p["path"][key]
            if key in {"Hjac", "Scoord"}:
                target = target[0]
            target[0][0] = "-1"
            self.reject(p, "negative_entry")

    def test_duplicate_keys_nonfinite_and_resource_limits(self):
        for data, code in [
            (b'{"a":{},"a":{}}', "duplicate_json_key"),
            (b'{"outer":{"a":"0","a":"1"}}', "duplicate_json_key"),
            (b'{"a":NaN}', "json_number_forbidden"),
            (b'{"a":Infinity}', "json_number_forbidden"),
            (b'{"a":1e-40}', "json_number_forbidden"),
            (b'[]', "object_fields"), (b'{} trailing', "invalid_json"),
            (b'\xff', "invalid_json"), (b' ' * (C.MAX_BYTES + 1), "input_size"),
            (b'[' * 2000, "invalid_json"),
        ]:
            with self.subTest(code=code, data=data[:30]):
                with self.assertRaises(C.Rejected) as caught:
                    C.check_bytes(data)
                self.assertEqual(caught.exception.code, code)
        p = synthetic()
        p["path"]["Hjac"] = []
        self.reject(p, "dimension_limit")
        with patch.object(C, "PATH_SOURCE_SHA256", "0" * 64):
            self.reject(synthetic(), "path_formula_version_changed")

    def test_cli_never_promotes(self):
        path = Path(C.__file__).resolve()
        for data, expected in [(raw(synthetic()), 0), (b'{"a":"0","a":"1"}', 1), (b'{}', 1)]:
            proc = subprocess.run([sys.executable, "-B", str(path), "--input", "-"],
                                  input=data, capture_output=True, timeout=15)
            self.assertEqual(proc.returncode, expected, proc.stderr)
            result = json.loads(proc.stdout)
            self.assertFalse(result["registry_eligible"])
            self.assertFalse(result["kernel_verified"])
            self.assertEqual(result["arithmetic_valid"], expected == 0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
