import tempfile
import unittest
from pathlib import Path
from percolation_workflow.model import WorkflowState
from percolation_workflow.store import StateStore
from percolation_workflow.scheduler import run_frontier_parallel, FrontierResult


class PersistentAttemptsTests(unittest.TestCase):
    def test_agent_sees_started_attempt_on_disk_and_crash_is_retained(self):
        with tempfile.TemporaryDirectory() as directory:
            store = StateStore(Path(directory) / 'state.json')
            state = WorkflowState()
            node_id = state.add_node('leaf', 'True')

            def crashing_agent(_):
                checkpoint = store.load()
                self.assertEqual(checkpoint.nodes[node_id].status, 'in_progress')
                self.assertEqual(len(checkpoint.attempts), 1)
                raise RuntimeError('agent process lost')

            result = run_frontier_parallel(state, {node_id: crashing_agent}, store=store)
            self.assertEqual(result[node_id], 'agent_error')
            checkpoint = store.load()
            attempt = next(iter(checkpoint.attempts.values()))
            self.assertIn('agent process lost', attempt.stderr)
            self.assertEqual(checkpoint.nodes[node_id].status, 'open')
            self.assertEqual(checkpoint.registry, {})
