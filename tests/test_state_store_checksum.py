import hashlib
import json
import tempfile
import unittest
from pathlib import Path

from percolation_workflow.model import WorkflowState
from percolation_workflow.store import (
    CheckpointIntegrityError,
    ConcurrentStateUpdate,
    StateStore,
)


class StateStoreChecksumTests(unittest.TestCase):
    def test_legacy_upgrade_checksum_corruption_and_cas(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'state.json'
            legacy = WorkflowState(revision=92, project='legacy-routeb')
            path.write_text(json.dumps(legacy.to_dict()), encoding='utf-8')

            store = StateStore(path)
            upgraded = store.load()
            self.assertEqual(upgraded.revision, 92)
            store.save(upgraded)

            payload = json.loads(path.read_text(encoding='utf-8'))
            checksum = payload.pop('state_checksum')
            canonical = json.dumps(
                payload,
                ensure_ascii=False,
                sort_keys=True,
                separators=(',', ':'),
                allow_nan=False,
            ).encode('utf-8')
            self.assertEqual(checksum, hashlib.sha256(canonical).hexdigest())
            self.assertEqual(upgraded.revision, 93)

            stale = store.load()
            current = store.load()
            store.save(current)
            with self.assertRaises(ConcurrentStateUpdate):
                store.save(stale)

            cached = store.load()
            damaged = json.loads(path.read_text(encoding='utf-8'))
            damaged['project'] = 'tampered'
            path.write_text(json.dumps(damaged), encoding='utf-8')
            with self.assertRaisesRegex(CheckpointIntegrityError, 'checksum mismatch'):
                store.load()
            with self.assertRaisesRegex(CheckpointIntegrityError, 'checksum mismatch'):
                store.save(cached)


if __name__ == '__main__':
    unittest.main()
