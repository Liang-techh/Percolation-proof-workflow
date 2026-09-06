import json
import tempfile
import unittest
from pathlib import Path
from percolation_workflow.bundles import stage_bundle


class BundleTests(unittest.TestCase):
    def test_digest_is_independent_of_dependency_checkout_path(self):
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            source, dependency_a, dependency_b = (base / name for name in
                                                   ('source', 'dependency-a', 'dependency-b'))
            for project in (source, dependency_a, dependency_b):
                project.mkdir()
                (project / 'lean-toolchain').write_text('leanprover/lean4:v4.32.0\n')
                (project / 'lake-manifest.json').write_text(json.dumps({'packages': [
                    {'name': 'mathlib', 'type': 'git', 'url': 'fixture-url', 'rev': 'fixture-rev'}]}))
            (source / 'lake-manifest.json').write_text(json.dumps({'packages': [
                {'name': 'mathlib', 'type': 'git', 'url': 'fixture-url', 'rev': 'fixture-rev'},
                {'name': 'Foundation', 'type': 'path', 'dir': '../dependency-a'}]}))
            (source / 'Goal.lean').write_text('theorem leaf : True := by sorry\n')
            (source / 'Candidate.lean').write_text('theorem leaf : True := by trivial\n')
            kwargs = dict(node_name='leaf', challenge_module='Goal', solution_module='Candidate',
                          source_files=['Goal.lean', 'Candidate.lean'], dependency_name='Foundation',
                          link_cache=False)
            first = stage_bundle(source, base / 'bundles', dependency_project=dependency_a, **kwargs)
            second = stage_bundle(source, base / 'bundles', dependency_project=dependency_b, **kwargs)
            self.assertEqual(first, second)
            self.assertIn('.lake/pinned-dependency',
                          (first / 'lake-manifest.json').read_text(encoding='utf-8'))
            self.assertNotIn(str(dependency_a), (first / 'lakefile.toml').read_text(encoding='utf-8'))

    def test_manifest_identity_is_part_of_bundle_digest(self):
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            source, dependency = base / 'source', base / 'dependency'
            source.mkdir(); dependency.mkdir()
            for project in (source, dependency):
                (project / 'lean-toolchain').write_text('leanprover/lean4:v4.32.0\n')
                (project / 'lake-manifest.json').write_text(json.dumps({'packages': [
                    {'name': 'mathlib', 'type': 'git', 'url': 'fixture-url', 'rev': 'fixture-rev'}]}))
            (source / 'lake-manifest.json').write_text(json.dumps({'packages': [
                {'name': 'mathlib', 'type': 'git', 'url': 'fixture-url', 'rev': 'fixture-rev'},
                {'name': 'Foundation', 'type': 'path', 'dir': '../dependency'}]}))
            (source / 'Goal.lean').write_text('theorem leaf : True := by sorry\n')
            (source / 'Candidate.lean').write_text('theorem leaf : True := by trivial\n')
            kwargs = dict(node_name='leaf', challenge_module='Goal', solution_module='Candidate',
                          source_files=['Goal.lean', 'Candidate.lean'], dependency_project=dependency,
                          dependency_name='Foundation', link_cache=False)
            first = stage_bundle(source, base / 'bundles', manifest_identity={'sha256': 'a'}, **kwargs)
            second = stage_bundle(source, base / 'bundles', manifest_identity={'sha256': 'b'}, **kwargs)
            self.assertNotEqual(first, second)
            self.assertEqual(json.loads((first / 'manifest.identity.json').read_text())['sha256'], 'a')

    def test_freezes_only_selected_lemma_and_keeps_old_version(self):
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            source, dependency = base / 'source', base / 'dependency'
            source.mkdir()
            dependency.mkdir()
            for project in (source, dependency):
                (project / 'lean-toolchain').write_text('leanprover/lean4:v4.32.0\n')
            pin = {'name': 'mathlib', 'type': 'git', 'url': 'fixture-url', 'rev': 'fixture-rev'}
            (source / 'lake-manifest.json').write_text(json.dumps({'packages': [pin,
                {'name': 'Foundation', 'type': 'path', 'dir': '../dependency'}]}))
            (dependency / 'lake-manifest.json').write_text(json.dumps({'packages': [pin]}))
            (source / 'Goal.lean').write_text('theorem leaf : True := by sorry\n')
            (source / 'Candidate.lean').write_text('theorem leaf : True := by trivial\n')
            (source / 'UnfinishedSibling.lean').write_text('this does not compile')
            kwargs = dict(node_name='leaf', challenge_module='Goal', solution_module='Candidate',
                          source_files=['Goal.lean', 'Candidate.lean'], dependency_project=dependency,
                          dependency_name='Foundation', link_cache=False)
            first = stage_bundle(source, base / 'bundles', **kwargs)
            self.assertFalse((first / 'UnfinishedSibling.lean').exists())
            self.assertEqual(json.loads((first / 'comparator.json').read_text())['theorem_names'], ['leaf'])
            self.assertEqual(first, stage_bundle(source, base / 'bundles', **kwargs))
            original = (first / 'Candidate.lean').read_bytes()
            (source / 'Candidate.lean').write_text('theorem leaf : True := True.intro\n')
            second = stage_bundle(source, base / 'bundles', **kwargs)
            self.assertNotEqual(first, second)
            self.assertEqual((first / 'Candidate.lean').read_bytes(), original)
            (second / 'Candidate.lean').write_text('modified')
            with self.assertRaisesRegex(ValueError, 'modified'):
                stage_bundle(source, base / 'bundles', **kwargs)
            with self.assertRaisesRegex(ValueError, 'safe relative'):
                stage_bundle(source, base / 'bundles', **{**kwargs, 'source_files': ['../outside.lean']})
            (dependency / 'lean-toolchain').write_text('different-version')
            with self.assertRaisesRegex(ValueError, 'toolchain mismatch'):
                stage_bundle(source, base / 'bundles', **kwargs)
