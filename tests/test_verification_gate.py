import json
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch
from percolation_workflow.model import WorkflowState
from percolation_workflow.store import StateStore
from percolation_workflow.verification import verify_and_register


class VerificationGateTests(unittest.TestCase):
    def _admission_fixture(self, root: Path, *, strict_admission: bool):
        for name, contents in {
            'lean-toolchain': 'leanprover/lean4:v4.33.1\n',
            'lake-manifest.json': json.dumps({'packages': []}),
            'lakefile.toml': '',
            'Challenge.lean': 'theorem target : True := by trivial\n',
            'Solution.lean': 'theorem target : True := by trivial\n',
        }.items():
            (root / name).write_text(contents, encoding='utf-8')
        (root / 'comparator.json').write_text(json.dumps(dict(
            challenge_module='Challenge', solution_module='Solution', theorem_names=['target'],
            permitted_axioms=['propext'], enable_nanoda=True,
            strict_admission=strict_admission)), encoding='utf-8')

    def test_strict_admission_rejection_is_before_comparator_and_registry_promotion(self):
        with tempfile.TemporaryDirectory() as directory:
            project = Path(directory)
            self._admission_fixture(project, strict_admission=True)
            state = WorkflowState()
            node_id = state.add_node('target', 'theorem target : True',
                                     metadata={'statement_status': 'indexed'})
            store = StateStore(project / 'state.json')
            lean_result = SimpleNamespace(ok=True, command=['lake', 'build', 'Solution'],
                                          stdout='', stderr='', exit_code=0)
            rejected = SimpleNamespace(accepted=False, theorem_names=('target',), axioms={},
                                       toolchain='', toolchain_sha256='', lake_manifest_sha256='',
                                       reasons=('missing strict evidence',), command=(), stdout='', stderr='')
            with patch('percolation_workflow.verification.load_config') as load_config, \
                 patch('percolation_workflow.verification.index_statements', return_value=[
                     SimpleNamespace(qualified_name='target', source='theorem target : True')]), \
                 patch('percolation_workflow.verification.run_lean', return_value=lean_result), \
                 patch('percolation_workflow.verification.audit_strict_admission', return_value=rejected) as audit, \
                 patch('percolation_workflow.verification.run_comparator') as comparator:
                load_config.return_value = SimpleNamespace(
                    theorem_names=['target'], challenge_module='Challenge', solution_module='Solution',
                    enable_nanoda=True, permitted_axioms=[], strict_admission=True, source_files=())
                self.assertFalse(verify_and_register(state, node_id, project, ['trusted-comparator'], store=store))
            audit.assert_called_once()
            comparator.assert_not_called()
            self.assertEqual(store.load().registry, {})
            self.assertEqual(store.load().attempts[next(iter(store.load().attempts))].status,
                             'strict_admission_rejected')

    def test_strict_admission_defaults_false_and_preserves_comparator_promotion(self):
        with tempfile.TemporaryDirectory() as directory:
            project = Path(directory)
            self._admission_fixture(project, strict_admission=False)
            state = WorkflowState()
            node_id = state.add_node('target', 'theorem target : True',
                                     metadata={'statement_status': 'indexed'})
            store = StateStore(project / 'state.json')
            lean_result = SimpleNamespace(ok=True, command=['lake', 'build', 'Solution'],
                                          stdout='', stderr='', exit_code=0)
            with patch('percolation_workflow.verification.load_config') as load_config, \
                 patch('percolation_workflow.verification.index_statements', return_value=[
                     SimpleNamespace(qualified_name='target', source='theorem target : True')]), \
                 patch('percolation_workflow.verification.run_lean', return_value=lean_result), \
                 patch('percolation_workflow.verification.audit_strict_admission') as audit, \
                 patch('percolation_workflow.verification.run_comparator',
                       return_value=(True, 'Your solution is okay!', '')) as comparator:
                load_config.return_value = SimpleNamespace(
                    theorem_names=['target'], challenge_module='Challenge', solution_module='Solution',
                    enable_nanoda=True, permitted_axioms=[], source_files=())
                self.assertTrue(verify_and_register(state, node_id, project, ['trusted-comparator'], store=store))
            audit.assert_not_called()
            comparator.assert_called_once_with(project.resolve(), ['trusted-comparator'])
            self.assertIn(node_id, store.load().registry)

    def test_comparator_success_cannot_promote_changed_source(self):
        with tempfile.TemporaryDirectory() as directory:
            project = Path(directory)
            for name in ('lean-toolchain', 'lake-manifest.json', 'lakefile.toml', 'Solution.lean'):
                (project / name).write_text('initial', encoding='utf-8')
            (project / 'comparator.json').write_text(json.dumps(dict(
                challenge_module='Challenge', solution_module='Solution', theorem_names=['target'],
                permitted_axioms=['propext'], enable_nanoda=True)))
            state = WorkflowState()
            (project / 'Challenge.lean').write_text('theorem target : True := by sorry\n')
            node_id = state.add_node('target', 'theorem target : True', metadata={'statement_status': 'indexed'})
            store = StateStore(project / 'state.json')
            result = SimpleNamespace(ok=True, command=['lake', 'build', 'Solution'], stdout='',
                                     stderr='', exit_code=0)
            original = state.nodes[node_id].statement
            state.nodes[node_id].statement = 'False'
            with self.assertRaisesRegex(ValueError, 'trusted Challenge'):
                verify_and_register(state, node_id, project, ['trusted-comparator'], store=store)
            self.assertEqual(state.attempts, {})
            state.nodes[node_id].statement = original

            def changed_source(*args):
                self.assertEqual(store.load().nodes[node_id].status, 'in_progress')
                self.assertEqual(state.frontier(), [])
                with self.assertRaises(ValueError):
                    state.begin_attempt(node_id, 'duplicate-worker')
                (project / 'Solution.lean').write_text('changed', encoding='utf-8')
                return True, 'Your solution is okay!', ''

            with patch('percolation_workflow.verification.run_lean', return_value=result), \
                 patch('percolation_workflow.verification.run_comparator', side_effect=changed_source):
                self.assertFalse(verify_and_register(state, node_id, project, ['trusted-comparator'], store=store))
            saved = store.load()
            self.assertEqual(saved.registry, {})
            self.assertTrue(saved.events[-1]['source_changed'])
            self.assertEqual(len(saved.attempts), 1)

    def test_verified_retry_and_late_completion_rejected(self):
        state = WorkflowState()
        node_id = state.add_node('target', 'True')
        attempt = state.begin_attempt(node_id, 'worker')
        state.finish_attempt(attempt, status='compile_error', command=[], stdout='', stderr='', exit_code=1)
        state.begin_attempt(node_id, 'new-worker')
        with self.assertRaises(ValueError):
            state.finish_attempt(attempt, status='passed', command=[], stdout='', stderr='', exit_code=0)
        self.assertEqual(state.nodes[node_id].status, 'in_progress')
        state.nodes[node_id].status = 'verified'
        with self.assertRaises(ValueError):
            state.begin_attempt(node_id, 'retry')
