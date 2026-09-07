import tempfile
import json
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch
from percolation_workflow.controller import verify_frontier, final_project_check, verify_manifest_frontier
from percolation_workflow.model import WorkflowState, NodeStatus
from percolation_workflow.store import StateStore


class ControllerTests(unittest.TestCase):
    def test_manifest_wrapper_stages_every_dag_node_and_binds_identity(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / 'target'
            source.mkdir()
            state_path = root / 'state.json'
            state = WorkflowState()
            parent = state.add_node('parent', 'P', metadata={'statement_status': 'indexed'})
            state.add_node('child', 'C', parent_id=parent,
                           metadata={'statement_status': 'indexed'})
            StateStore(state_path).save(state)
            manifest_path = source / 'verification-manifest.json'
            manifest_path.write_text(json.dumps({
                'schema_version': 1, 'workspace_root': '..', 'state_path': '../state.json',
                'target': {'root': 'parent'}, 'dependency': {'name': 'Pinned'},
                'nodes': {
                    'parent': {'challenge_module': 'ParentChallenge', 'solution_module': 'ParentSolution',
                               'source_files': ['ParentChallenge.lean', 'ParentSolution.lean']},
                    'child': {'challenge_module': 'ChildChallenge', 'solution_module': 'ChildSolution',
                              'source_files': ['ChildChallenge.lean', 'ChildSolution.lean']}}}),
                encoding='utf-8')
            staged = {}
            def stage(*args, **kwargs):
                staged[kwargs['node_name']] = kwargs
                return root / (kwargs['node_name'] + '-bundle')
            with patch('percolation_workflow.controller.stage_bundle', side_effect=stage), \
                 patch('percolation_workflow.controller.verify_frontier', return_value='verified') as verify:
                outcome = verify_manifest_frontier(StateStore(state_path), manifest_path,
                                                   root / 'dependency', root / 'bundles', ['comparator'])
            self.assertEqual(outcome, 'verified')
            self.assertEqual(set(staged), {'parent', 'child'})
            verify.assert_called_once()
            self.assertEqual(verify.call_args.kwargs['manifest_identity']['sha256'],
                             staged['parent'] and StateStore(state_path).load().manifest['sha256'])
    def test_final_build_success_does_not_replace_comparator(self):
        with tempfile.TemporaryDirectory() as directory:
            store = StateStore(Path(directory) / 'state.json')
            state = WorkflowState()
            state.add_node('root', 'theorem root : True')
            with patch('percolation_workflow.controller.load_config', return_value=SimpleNamespace(
                    theorem_names=['root'], challenge_module='Challenge', solution_module='Solution',
                    enable_nanoda=True, permitted_axioms=[])), \
                 patch('percolation_workflow.controller.index_statements', return_value=[SimpleNamespace(
                    qualified_name='root', source='theorem root : True')]), \
                 patch('percolation_workflow.controller.source_snapshot', return_value={'fixture': 'same'}), \
                 patch('percolation_workflow.controller.run_lean', return_value=SimpleNamespace(
                    ok=True, exit_code=0, stdout='', stderr='', command=['lake', 'build'])), \
                 patch('percolation_workflow.controller.run_comparator', return_value=(False, '', 'wrong statement')):
                self.assertEqual(final_project_check(store, state, directory, ['comparator']), 'needs_repair')
            self.assertFalse(store.load().events[-1]['accepted'])

    def test_dynamic_parent_selection_and_restart_preserves_in_progress(self):
        with tempfile.TemporaryDirectory() as directory:
            store = StateStore(Path(directory) / 'state.json')
            state = WorkflowState()
            parent = state.add_node('arbitrary-parent', 'P', metadata={'statement_status': 'indexed'})
            child = state.add_node('arbitrary-child', 'C', parent_id=parent,
                                   metadata={'statement_status': 'indexed'})
            store.save(state)
            order = []
            projects = {child: str(Path(directory) / 'child-bundle'),
                        parent: str(Path(directory) / 'parent-bundle')}
            with self.assertRaises(ValueError):
                verify_frontier(store, directory, ['comparator'], node_projects={child: projects[child]})
            def simulated_gate(state, node_id, *args, store):
                order.append(node_id)
                self.assertEqual(str(args[0]), projects[node_id])
                state.nodes[node_id].status = NodeStatus.VERIFIED
                state.set_evidence_stage(node_id, 'lean_verified')
                state.registry[node_id] = {'test_fixture': True}
                if node_id == parent:
                    state.global_closure['formal_certificate_allowed'] = True
                store.save(state)
                return True
            with patch('percolation_workflow.controller.verify_and_register', side_effect=simulated_gate), \
                 patch('percolation_workflow.controller.load_config', return_value=SimpleNamespace(
                     theorem_names=['arbitrary-parent'], challenge_module='Challenge', solution_module='Solution',
                     enable_nanoda=True, permitted_axioms=[])), \
                 patch('percolation_workflow.controller.index_statements', return_value=[SimpleNamespace(
                     qualified_name='arbitrary-parent', source='P')]), \
                 patch('percolation_workflow.controller.source_snapshot', return_value={'fixture': 'same'}), \
                 patch('percolation_workflow.controller.run_comparator',
                       return_value=(True, 'Your solution is okay!', '')) as comparator, \
                 patch('percolation_workflow.controller.run_lean', return_value=SimpleNamespace(
                     ok=True, exit_code=0, stdout='', stderr='', command=['lake', 'build'])) as build:
                self.assertEqual(verify_frontier(store, directory, ['comparator'], node_projects=projects), 'verified')
                build.assert_called_once_with(Path(directory).resolve(), ['lake', 'build', 'Challenge', 'Solution'])
                comparator.assert_called_once_with(Path(directory).resolve(), ['comparator'])
            self.assertEqual(order, [child, parent])
            working_store = StateStore(Path(directory) / 'working-state.json')
            state = WorkflowState()
            node = state.add_node('working', 'W', metadata={'statement_status': 'indexed'})
            attempt = state.begin_attempt(node, 'agent')
            working_store.save(state)
            self.assertEqual(verify_frontier(working_store, directory, ['comparator']), 'awaiting_work')
            self.assertIsNone(working_store.load().attempts[attempt].finished_at)
