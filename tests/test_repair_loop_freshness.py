import hashlib
import json
import tempfile
import unittest
from pathlib import Path

from percolation_workflow.freshness import audit_freshness, bind_freshness


class RepairLoopFreshnessTests(unittest.TestCase):
    def test_each_expired_input_fails_closed(self):
        with tempfile.TemporaryDirectory() as directory:
            project = Path(directory)
            for name, text in {
                'lean-toolchain': 'leanprover/lean4:v4.32.0\n',
                'comparator.json': json.dumps({'target': 'parent'}),
                'Parent.lean': 'theorem parent : True := by trivial\n',
                'Parent.olean': 'compiled-parent\n',
            }.items():
                (project / name).write_text(text, encoding='utf-8')
            source = {'Parent.lean': hashlib.sha256((project / 'Parent.lean').read_bytes()).hexdigest()}
            binding = bind_freshness(project, source, olean_paths=['Parent.olean'])
            self.assertTrue(audit_freshness(project, binding)[0])
            for field, path in [('source', 'Parent.lean'), ('lean', 'lean-toolchain'),
                                ('comparator', 'comparator.json'), ('olean', 'Parent.olean')]:
                with self.subTest(field=field):
                    (project / path).write_text((project / path).read_text(encoding='utf-8') + 'drift', encoding='utf-8')
                    accepted, reasons = audit_freshness(project, binding)
                    self.assertFalse(accepted)
                    self.assertTrue(reasons)
                    (project / path).write_text((project / path).read_text(encoding='utf-8')[:-5], encoding='utf-8')

    def test_missing_binding_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            self.assertEqual(audit_freshness(Path(directory), {}),
                             (False, ('source hashes missing', 'Lean pin binding missing',
                                      '.olean bindings missing')))


if __name__ == '__main__':
    unittest.main()
