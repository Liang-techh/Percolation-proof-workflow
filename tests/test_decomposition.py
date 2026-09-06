import unittest
import tempfile
import hashlib
from pathlib import Path
from percolation_workflow.store import StateStore
from percolation_workflow.agent_bridge import prepare_requests, bind_agent, record_result
from percolation_workflow.research import next_actions
from percolation_workflow.model import WorkflowState
from percolation_workflow.decomposition import ChildGoal, propose_decomposition


class DecompositionTests(unittest.TestCase):
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

    def test_agent_decomposition_is_not_mistaken_for_a_parent_proof(self):
        with tempfile.TemporaryDirectory() as directory:
            store = StateStore(Path(directory) / 'state.json')
            state = WorkflowState()
            parent = state.add_node('parent', 'P', metadata={'statement_status': 'indexed'})
            store.save(state)
            request_id = prepare_requests(store)[0]['request_id']
            bind_agent(store, request_id, 'fixture-planner')
            result = {'status': {'fixture-planner': {'completed': 'decomposition candidate'}}}
            record_result(store, request_id, 'fixture-planner', result)
            state = store.load()
            propose_decomposition(state, parent, 'reduce to child', [ChildGoal('child', 'C')],
                                  agent_id='fixture-planner', store=store,
                                  comparator_gate=self._comparator_gate('child', 'C'))
            record_result(store, request_id, 'fixture-planner', result)
            self.assertEqual(store.load().agent_requests[request_id]['status'], 'decomposed')
            self.assertEqual([a['kind'] for a in next_actions(store)], ['check_sketch'])
            self.assertEqual(prepare_requests(store), [])
            proposal = store.load().nodes[parent].metadata['reduction_proposals'][-1]
            self.assertEqual(proposal['child_order'], proposal['children'])
            self.assertEqual(proposal['imports'][0]['kind'], 'theorem')
            self.assertTrue(proposal['proposal_id'])

    def test_failed_parent_can_split_and_shared_child_is_reused(self):
        state = WorkflowState()
        a = state.add_node('parentA', 'A')
        b = state.add_node('parentB', 'B')
        attempt = state.begin_attempt(a, 'solver')
        state.finish_attempt(attempt, status='compile_error', command=['lean'],
                             stdout='', stderr='unsolved goals', exit_code=1)
        first = propose_decomposition(state, a, 'combine the two bounds',
            [ChildGoal('lower', 'L'), ChildGoal('upper', 'U')], agent_id='planner',
            comparator_gate=self._comparator_gate('lower', 'L') |
                            self._comparator_gate('upper', 'U'))
        second = propose_decomposition(state, b, 'reuse the lower bound',
            [ChildGoal('lower', 'L')], agent_id='planner',
            comparator_gate=self._comparator_gate('lower', 'L'))
        self.assertEqual(second, first[:1])
        self.assertEqual({n.id for n in state.frontier()}, set(first))
        self.assertEqual(state.nodes[a].attempts, [attempt])
        self.assertEqual(state.registry, {})

    def test_cyclic_proposal_is_atomic(self):
        state = WorkflowState()
        parent = state.add_node('parent', 'P')
        before = state.to_dict()
        with self.assertRaises(ValueError):
            propose_decomposition(state, parent, 'invalid self reduction',
                [ChildGoal('new', 'N'), ChildGoal('parent', 'P')], agent_id='planner',
                comparator_gate=self._comparator_gate('new', 'N') |
                                self._comparator_gate('parent', 'P'))
        self.assertEqual(state.to_dict(), before)
