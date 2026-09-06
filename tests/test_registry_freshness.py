import unittest
from percolation_workflow.model import WorkflowState, NodeStatus
from percolation_workflow.registry import audit_registry, invalidate_dependents


class RegistryFreshnessTests(unittest.TestCase):
    def test_diamond_invalidation_preserves_unrelated_and_receipts(self):
        state = WorkflowState()
        leaf = state.add_node('leaf', 'L')
        a = state.add_node('a', 'A', dependencies=[leaf])
        b = state.add_node('b', 'B', dependencies=[leaf])
        parent = state.add_node('parent', 'P', dependencies=[a, b])
        unrelated = state.add_node('unrelated', 'U')
        for node in state.nodes.values():
            node.status = NodeStatus.VERIFIED
            state.registry[node.id] = {'statement': node.statement, 'artifact': 'fixture'}
        self.assertEqual(invalidate_dependents(state, [leaf], reason='source changed'), {leaf, a, b, parent})
        self.assertEqual(set(state.registry), {unrelated})
        self.assertTrue(state.nodes[parent].metadata['previous_verifications'])
        self.assertEqual({n.id for n in state.frontier()}, {leaf})

    def test_missing_evidence_is_not_claimed_stale(self):
        state = WorkflowState()
        node_id = state.add_node('leaf', 'L')
        state.nodes[node_id].status = NodeStatus.VERIFIED
        state.registry[node_id] = {'statement': 'L'}
        self.assertEqual(audit_registry(state)[node_id]['status'], 'unavailable')

    def test_running_ancestor_prevents_partial_invalidation(self):
        state = WorkflowState()
        leaf = state.add_node('leaf', 'L')
        parent = state.add_node('parent', 'P', dependencies=[leaf])
        state.begin_attempt(parent, 'worker')
        before = state.to_dict()
        with self.assertRaises(ValueError):
            invalidate_dependents(state, [leaf], reason='source changed')
        self.assertEqual(state.to_dict(), before)
