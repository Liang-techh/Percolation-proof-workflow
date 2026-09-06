import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "build_platform_tree", ROOT / "scripts" / "build_platform_tree.py")
BUILD = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(BUILD)


class PlatformCompileOrderTests(unittest.TestCase):
    def test_imports_override_alphabetical_order(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            definition = root / "Definitions" / "Def_Base.lean"
            child = root / "Theorems" / "Thm_Z_child.lean"
            parent = root / "Theorems" / "Thm_A_parent.lean"
            for path in (definition, child, parent):
                path.parent.mkdir(parents=True, exist_ok=True)
            definition.write_text("def base : Nat := 0\n", encoding="utf-8")
            child.write_text("import Definitions.Def_Base\ntheorem child : True := by trivial\n",
                              encoding="utf-8")
            parent.write_text("import Theorems.Thm_Z_child\ntheorem parent : True := by trivial\n",
                              encoding="utf-8")
            ordered = BUILD._ordered_paths([
                ("Theorems/Thm_A_parent.lean", parent),
                ("Definitions/Def_Base.lean", definition),
                ("Theorems/Thm_Z_child.lean", child),
            ])
            self.assertEqual([relative for relative, _ in ordered], [
                "Definitions/Def_Base.lean",
                "Theorems/Thm_Z_child.lean",
                "Theorems/Thm_A_parent.lean",
            ])

    def test_import_cycle_fails_closed(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            left = root / "Theorems" / "Thm_Left.lean"
            right = root / "Theorems" / "Thm_Right.lean"
            left.parent.mkdir(parents=True, exist_ok=True)
            left.write_text("import Theorems.Thm_Right\n", encoding="utf-8")
            right.write_text("import Theorems.Thm_Left\n", encoding="utf-8")
            with self.assertRaises(ValueError):
                BUILD._ordered_paths([
                    ("Theorems/Thm_Left.lean", left),
                    ("Theorems/Thm_Right.lean", right),
                ])

    def test_missing_platform_import_fails_closed_even_if_olean_might_exist(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "Solutions" / "Sol_Main.lean"
            source.parent.mkdir(parents=True, exist_ok=True)
            source.write_text("import Theorems.Thm_Stale\ntheorem solution : True := by trivial\n",
                              encoding="utf-8")
            with self.assertRaises(ValueError):
                BUILD._ordered_paths([("Solutions/Sol_Main.lean", source)])

    def test_receipt_rejects_source_drift_during_compile(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            tree = root / "tree"
            source = tree / "Definitions" / "Def_Main.lean"
            source.parent.mkdir(parents=True, exist_ok=True)
            source.write_text("def main : Nat := 0\n", encoding="utf-8")
            (tree / "tree-manifest.json").write_text(json.dumps({
                "schema_version": 1,
                "files": ["Definitions/Def_Main.lean"],
            }), encoding="utf-8")
            lake_project = root / "lake"
            lake_project.mkdir()

            def fake_compile(command, **kwargs):
                source.write_text(source.read_text(encoding="utf-8") + "-- drift\n",
                                   encoding="utf-8")
                return BUILD.subprocess.CompletedProcess(command, 0, "", "")

            argv = ["build_platform_tree.py", str(tree), "--lake-project", str(lake_project)]
            with patch.object(BUILD.sys, "argv", argv), patch.object(
                    BUILD.subprocess, "run", side_effect=fake_compile):
                self.assertEqual(BUILD.main(), 1)
            receipt = json.loads((tree / "compile-receipt.json").read_text(encoding="utf-8"))
            self.assertEqual(receipt["status"], "failed")
            self.assertTrue(receipt["modules"][0]["source_changed_during_compile"])
            self.assertEqual(receipt["modules"][0]["error"], "source changed during compilation")


if __name__ == "__main__":
    unittest.main()
