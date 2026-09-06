import tempfile
import unittest
from pathlib import Path
from percolation_workflow.provenance import lean_checks, write_audit
from percolation_workflow.lean import run_lean


class ProvenanceTests(unittest.TestCase):
    def test_repeated_audit_preserves_snapshot_and_rejects_tampering(self):
        with tempfile.TemporaryDirectory() as directory:
            project = Path(directory)
            contract = {'forbidden_modules': ['Original']}
            first = write_audit(project, 'Candidate', 'candidate', contract)
            before = {p.name: p.read_bytes() for p in project.iterdir()}
            self.assertEqual(first, write_audit(project, 'Candidate', 'candidate', contract))
            self.assertEqual(before, {p.name: p.read_bytes() for p in project.iterdir()})
            first[0].write_text('modified audit')
            with self.assertRaisesRegex(ValueError, 'modified'):
                write_audit(project, 'Candidate', 'candidate', contract)

    def test_real_lean_rejects_transitive_import_and_definition_wrapper(self):
        with tempfile.TemporaryDirectory() as directory:
            project = Path(directory)
            (project / 'lean-toolchain').write_bytes(
                (Path(__file__).parents[1] / 'examples/minimal_lean/lean-toolchain').read_bytes())
            (project / 'lakefile.toml').write_text(
                'name = "provenanceTest"\n[[lean_lib]]\nname = "Wrapper"\n'
                '[[lean_lib]]\nname = "Original"\n')
            (project / 'Original.lean').write_text('theorem original : True := by trivial\n')
            (project / 'Wrapper.lean').write_text(
                'import Original\ndef hidden : True := original\ntheorem candidate : True := hidden\n')
            build = run_lean(project, ['lake', 'build', 'Wrapper'])
            self.assertTrue(build.ok, build.stdout + build.stderr)
            cases = [({}, True, ''),
                     ({'forbidden_modules': ['Original']}, False, 'forbidden transitive import'),
                     ({'forbidden_existing_proofs': ['original']}, False, 'forbidden proof dependency')]
            for i, (contract, accepted, diagnostic) in enumerate(cases):
                source = project / f'Audit{i}.lean'
                source.write_text('import Wrapper\nimport Lean\nopen Lean in\nrun_meta do\n'
                                  '  let env ← getEnv\n' + lean_checks(contract, 'candidate') +
                                  '  logInfo "audit completed"\n', encoding='utf-8')
                result = run_lean(project, ['lake', 'env', 'lean', str(source)])
                self.assertEqual(result.ok, accepted, result.stdout + result.stderr)
                self.assertIn(diagnostic, result.stdout)
