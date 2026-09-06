import tempfile
import unittest
from pathlib import Path

from percolation_workflow.model import WorkflowState
from percolation_workflow.store import ConcurrentStateUpdate, StateStore


class StateStoreConcurrencyTests(unittest.TestCase):
    def test_unknown_state_schema_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'state.json'
            path.write_text('{"schema_version": 99}', encoding='utf-8')
            with self.assertRaisesRegex(ValueError, 'unsupported workflow state schema'):
                StateStore(path).load()

    def test_stale_writer_cannot_overwrite_newer_revision(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'state.json'
            first_store = StateStore(path)
            state = WorkflowState()
            state.add_node('goal', 'True')
            first_store.save(state)
            stale = StateStore(path).load()
            current = StateStore(path).load()
            current.event('newer-coordinator')
            StateStore(path).save(current)
            stale.event('stale-coordinator')
            with self.assertRaises(ConcurrentStateUpdate):
                StateStore(path).save(stale)
            saved = StateStore(path).load()
            self.assertTrue(any(event['kind'] == 'newer-coordinator' for event in saved.events))
            self.assertFalse(any(event['kind'] == 'stale-coordinator' for event in saved.events))
