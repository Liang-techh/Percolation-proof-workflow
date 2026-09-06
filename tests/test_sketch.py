import tempfile
import unittest
import hashlib
from pathlib import Path
from percolation_workflow.model import WorkflowState
from percolation_workflow.store import StateStore
from percolation_workflow.decomposition import ChildGoal, propose_decomposition
from percolation_workflow.sketch import check_sketch
from percolation_workflow.lean import run_lean
from percolation_workflow.agent_bridge import prepare_requests
from percolation_workflow.reduction import close_verified_reductions
from percolation_workflow.registry import audit_registry
from percolation_workflow.model import NodeStatus


class SketchTests(unittest.TestCase):
    @staticmethod
    def _comparator_gate(name, statement):
        normalized = ' '.join(statement.split())
        return {name: {
            'source_identity': {
                'source': f'{name}.lean', 'module': name, 'name': f'{name}.{name}',
                'statement_sha256': hashlib.sha256(normalized.encode()).hexdigest()},
            'source_statement': statement,
            'covered_source': [f'{name}.lean'],
            'target_theorem_identity': {'module': name, 'name': f'{name}.{name}'}}}

    def test_accepted_reduction_auto_closes_parent_after_children_are_verified(self):
        with tempfile.TemporaryDirectory() as directory:
            project = Path(directory)
            (project / 'lean-toolchain').write_bytes(
                (Path(__file__).parents[1] / 'examples/minimal_lean/lean-toolchain').read_bytes())
            (project / 'lakefile.toml').write_text(
                'name = "reductionCascade"\n[[lean_lib]]\nname = "Challenge"\n'
                '[[lean_lib]]\nname = "Reduction"\n')
            (project / 'Challenge.lean').write_text(
                'theorem target : True ∧ True := by sorry\n'
                'theorem left : True := by sorry\n'
                'theorem right : True := by sorry\n', encoding='utf-8')
            (project / 'Reduction.lean').write_text(
                'import Challenge\n'
                'theorem reduction : True → True → True ∧ True := by\n'
                '  intro a b\n  exact And.intro a b\n', encoding='utf-8')
            self.assertTrue(run_lean(project, ['lake', 'update']).ok)
            state = WorkflowState()
            parent = state.add_node('target', 'theorem target : True ∧ True')
            children = propose_decomposition(state, parent, 'pair the two propositions',
                [ChildGoal('left', 'theorem left : True'), ChildGoal('right', 'theorem right : True')],
                agent_id='cascade-planner',
                comparator_gate=self._comparator_gate('left', 'theorem left : True') |
                                self._comparator_gate('right', 'theorem right : True'))
            store = StateStore(project / 'state.json')
            store.save(state)
            self.assertTrue(check_sketch(store, parent, project, challenge_module='Challenge',
                                         reduction_module='Reduction', reduction_name='reduction'))
            state = store.load()
            for child in children:
                state.nodes[child].status = NodeStatus.VERIFIED
                state.registry[child] = {
                    'node_id': child, 'name': state.nodes[child].name,
                    'statement': state.nodes[child].statement, 'artifact': str(project),
                    'verification_receipt': {'source_digest': 'verified-child'},
                }
            store.save(state)
            self.assertEqual(close_verified_reductions(store), [parent])
            saved = store.load()
            self.assertEqual(saved.nodes[parent].status, NodeStatus.VERIFIED)
            self.assertEqual(saved.registry[parent]['verification_receipt']['verification_kind'], 'reduction')
            self.assertEqual(audit_registry(saved)[parent]['status'], 'current')
            self.assertTrue(any(event['kind'] == 'reduction_cascade_verified'
                                for event in saved.events))

    def test_real_lean_checks_implication_and_rejects_sorry_dependency(self):
        implication = 'True → True → True ∧ True'
        for proof, statement, expected in [('by intro a b; exact And.intro a b', implication, True),
                                ('by intro a b; exact target', implication, False),
                                ('by sorry', implication, False), ('by trivial', 'True', False)]:
            with self.subTest(proof=proof), tempfile.TemporaryDirectory() as directory:
                project = Path(directory)
                (project / 'lean-toolchain').write_bytes(
                    (Path(__file__).parents[1] / 'examples/minimal_lean/lean-toolchain').read_bytes())
                (project / 'lakefile.toml').write_text(
                    'name = "sketchTest"\n[[lean_lib]]\nname = "Challenge"\n'
                    '[[lean_lib]]\nname = "Reduction"\n')
                (project / 'Challenge.lean').write_text(
                    'theorem target : True ∧ True := by sorry\n'
                    'theorem left : True := by sorry\n'
                    'theorem right : True := by sorry\n', encoding='utf-8')
                (project / 'Reduction.lean').write_text(
                    'import Challenge\ntheorem reduction : ' + statement + ' := ' + proof + '\n',
                    encoding='utf-8')
                self.assertTrue(run_lean(project, ['lake', 'update']).ok)
                state = WorkflowState()
                parent = state.add_node('target', 'theorem target : True ∧ True')
                children = propose_decomposition(state, parent, 'pair the two propositions',
                    [ChildGoal('left', 'theorem left : True'), ChildGoal('right', 'theorem right : True')],
                    agent_id='fixture-planner',
                    comparator_gate=self._comparator_gate('left', 'theorem left : True') |
                                    self._comparator_gate('right', 'theorem right : True'))
                store = StateStore(project / 'state.json')
                store.save(state)
                self.assertEqual(prepare_requests(store), [])
                accepted = check_sketch(store, parent, project, challenge_module='Challenge',
                                        reduction_module='Reduction', reduction_name='reduction')
                self.assertEqual(accepted, expected, str(store.load().events[-1]))
                saved = store.load()
                self.assertEqual(saved.registry, {})
                self.assertEqual(saved.nodes[parent].status, 'open')
                if expected:
                    proposal = saved.nodes[parent].metadata['reduction_proposals'][-1]
                    self.assertEqual(proposal['reduction_status'], 'accepted')
                    self.assertEqual(proposal['status'], 'sketch_checked')
                self.assertEqual(len(prepare_requests(store)), len(children) if expected else 0)
