import hashlib
import shutil
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from percolation_workflow.strict_admission import audit_strict_admission


class RealStrictAdmissionFixtureTests(unittest.TestCase):
    """Small integration checks against the project's actual Lake/Lean toolchain."""

    @unittest.skipUnless(shutil.which("lake"), "Lake is not installed")
    def test_imports_solution_excludes_challenge_and_records_hashes(self):
        with TemporaryDirectory() as directory:
            root = Path(directory)
            toolchain = "leanprover/lean4:v4.33.1\n"
            manifest = (
                '{"version": "1.2.0",\n'
                ' "packagesDir": ".lake/packages",\n'
                ' "packages": [],\n'
                ' "name": "StrictAdmissionFixture",\n'
                ' "lakeDir": ".lake",\n'
                ' "fixedToolchain": false}\n'
            )
            (root / "lean-toolchain").write_text(toolchain, encoding="utf-8")
            (root / "lake-manifest.json").write_text(manifest, encoding="utf-8")
            (root / "lakefile.toml").write_text(
                'name = "StrictAdmissionFixture"\n'
                'version = "0.1.0"\n'
                'defaultTargets = ["Challenge", "Solution"]\n\n'
                '[[lean_lib]]\nname = "Challenge"\nroots = ["Challenge"]\n\n'
                '[[lean_lib]]\nname = "Solution"\nroots = ["Solution"]\n',
                encoding="utf-8",
            )
            (root / "Challenge.lean").write_text(
                "namespace Fixture\n"
                "def Goal : Prop := True\n"
                "theorem forbidden : True := by sorry\n"
                "end Fixture\n",
                encoding="utf-8",
            )
            (root / "Solution.lean").write_text(
                "import Challenge\n"
                "namespace Fixture\n"
                "theorem verified : Goal := by trivial\n"
                "end Fixture\n",
                encoding="utf-8",
            )

            audit = audit_strict_admission(
                root,
                ["Fixture.verified"],
                solution_module="Solution",
                challenge_module="Challenge",
                expected_toolchain=toolchain.strip(),
            )

            self.assertTrue(audit.accepted, audit.reasons + (audit.stderr, audit.stdout))
            self.assertEqual(audit.axioms["Fixture.verified"], ())
            self.assertEqual(list(root.glob("strict_admission_*.lean")), [])
            self.assertEqual(audit.toolchain_sha256, hashlib.sha256(toolchain.strip().encode()).hexdigest())
            self.assertEqual(
                audit.lake_manifest_sha256,
                hashlib.sha256((root / "lake-manifest.json").read_bytes()).hexdigest(),
            )


if __name__ == "__main__":
    unittest.main()
