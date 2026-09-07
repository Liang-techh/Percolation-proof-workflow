from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import tempfile
import unittest


HERE = Path(__file__).resolve().parent


def load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


generator = load("p8_generator", HERE / "generate_payload.py")
checker = load("p8_checker", HERE / "check_receipt.py")


class P8PayloadTests(unittest.TestCase):
    def test_generator_reads_contract_and_emits_fourteen_coordinates(self):
        root = Path(r"C:\Users\z5242\Desktop\重构版\6dof_sos_optimized\6dof_sos_optimized")
        metadata, receipt = generator.build_documents(root)
        self.assertEqual(metadata["coordinate_order"], generator.COORDINATE_ORDER)
        self.assertEqual(len(metadata["coordinate_mapping"]), 14)
        self.assertEqual(len(receipt["rhs_endpoint_intervals"]), 14)
        self.assertEqual(metadata["source_contract"]["julia_state_dimension"], 13)
        self.assertEqual(metadata["source_contract"]["ramp_binding"], "OPEN")

    def test_template_is_structurally_checked_but_not_concrete(self):
        root = Path(r"C:\Users\z5242\Desktop\重构版\6dof_sos_optimized\6dof_sos_optimized")
        _, receipt = generator.build_documents(root)
        report = checker.validate(receipt, source_root=root, allow_pending=True)
        self.assertEqual(report["status"], "pending_endpoint_payload")
        with self.assertRaises(checker.ReceiptError):
            checker.validate(receipt, source_root=root)

    def test_metadata_mutation_fails_closed(self):
        root = Path(r"C:\Users\z5242\Desktop\重构版\6dof_sos_optimized\6dof_sos_optimized")
        _, receipt = generator.build_documents(root)
        mutated = json.loads(json.dumps(receipt))
        mutated["coordinate_order"][13] = "w"
        with self.assertRaises(checker.ReceiptError):
            checker.validate(mutated, source_root=root, allow_pending=True)

    def test_complete_shape_is_still_only_a_candidate_payload(self):
        root = Path(r"C:\Users\z5242\Desktop\重构版\6dof_sos_optimized\6dof_sos_optimized")
        _, receipt = generator.build_documents(root)
        concrete = json.loads(json.dumps(receipt))
        for row in concrete["rhs_endpoint_intervals"]:
            row["lower"] = "0"
            row["upper"] = "0"
        concrete["receipt_status"] = "concrete_endpoint_payload"
        concrete["rounding"]["endpoint_rounding"] = "outward"
        concrete["rounding"]["direction"] = "outward"
        report = checker.validate(concrete, source_root=root)
        self.assertEqual(report["status"], "candidate_payload_only")
        self.assertIsNone(report["formal_admission"])


if __name__ == "__main__":
    unittest.main()
