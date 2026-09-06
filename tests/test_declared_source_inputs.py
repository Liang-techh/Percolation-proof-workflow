import json
import tempfile
import unittest
from pathlib import Path

from percolation_workflow.comparator import load_config
from percolation_workflow.verification import source_snapshot


class DeclaredSourceInputTests(unittest.TestCase):
    def project(self, directory: str) -> Path:
        project = Path(directory)
        for name in ('lean-toolchain', 'lake-manifest.json', 'comparator.json'):
            (project / name).write_text(name, encoding='utf-8')
        (project / 'comparator.json').write_text(json.dumps({
            'challenge_module': 'Challenge',
            'solution_module': 'Solution',
            'theorem_names': ['target'],
            'source_files': ['.routeB/dhport_lib.jl', 'coefficients.csv'],
        }), encoding='utf-8')
        (project / 'Challenge.lean').write_text('theorem target : True := by trivial\n', encoding='utf-8')
        (project / 'Solution.lean').write_text('theorem target : True := by trivial\n', encoding='utf-8')
        (project / '.routeB').mkdir()
        (project / '.routeB/dhport_lib.jl').write_text('m = [1.0]\n', encoding='utf-8')
        (project / 'coefficients.csv').write_text('1/3\n', encoding='utf-8')
        return project

    def test_declared_non_lean_inputs_are_hashed_and_detect_drift(self):
        with tempfile.TemporaryDirectory() as directory:
            project = self.project(directory)
            config = load_config(project / 'comparator.json')
            before = source_snapshot(project, declared_source_files=config.source_files)
            self.assertIn('.routeB/dhport_lib.jl', before)
            self.assertIn('coefficients.csv', before)
            (project / 'coefficients.csv').write_text('2/3\n', encoding='utf-8')
            after = source_snapshot(project, declared_source_files=config.source_files)
            self.assertNotEqual(before, after)

    def test_unsafe_or_missing_declared_input_fails_closed(self):
        with tempfile.TemporaryDirectory() as directory:
            project = self.project(directory)
            payload = json.loads((project / 'comparator.json').read_text(encoding='utf-8'))
            payload['source_files'] = ['../outside.csv']
            (project / 'comparator.json').write_text(json.dumps(payload), encoding='utf-8')
            with self.assertRaises(ValueError):
                load_config(project / 'comparator.json')
            payload['source_files'] = ['missing.jl']
            (project / 'comparator.json').write_text(json.dumps(payload), encoding='utf-8')
            config = load_config(project / 'comparator.json')
            with self.assertRaises(ValueError):
                source_snapshot(project, declared_source_files=config.source_files)


if __name__ == '__main__':
    unittest.main()
