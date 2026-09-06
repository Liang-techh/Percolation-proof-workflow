import json
from pathlib import Path
import tempfile
import unittest

from percolation_workflow.agent_bridge import bind_agent, prepare_requests
from percolation_workflow.host_adapter import FilesystemHostAdapter, HostAdapter
from percolation_workflow.model import WorkflowState
from percolation_workflow.store import StateStore


class HostAdapterTests(unittest.TestCase):
    def _store_with_request(self, root: Path, *, manifest: dict | None = None):
        store = StateStore(root / "state.json")
        state = WorkflowState()
        state.add_node("goal", "theorem goal : True", metadata={"statement_status": "indexed"})
        if manifest is not None:
            state.manifest = manifest
        store.save(state)
        request = prepare_requests(store)[0]
        bind_agent(store, request["request_id"], "agent-1")
        return store, request

    def test_dispatch_envelope_comes_from_next_actions_and_request(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            store = StateStore(root / "state.json")
            state = WorkflowState()
            state.add_node("goal", "theorem goal : True", metadata={"statement_status": "indexed"})
            store.save(state)
            adapter = FilesystemHostAdapter(root, store=store)
            self.assertIsInstance(adapter, HostAdapter)

            envelopes = adapter.dispatch()

            self.assertEqual(len(envelopes), 1)
            envelope = envelopes[0]
            self.assertEqual(envelope["kind"], "agent_dispatch")
            self.assertEqual(envelope["action"]["kind"], "dispatch_agent")
            self.assertEqual(envelope["request_id"], envelope["request"]["request_id"])
            self.assertEqual(envelope["attempt_id"], envelope["request"]["attempt_id"])
            self.assertEqual(envelope["protocol_version"], 1)
            self.assertIsNone(envelope["manifest_sha256"])
            saved = next((root / "dispatch").glob("*.json"))
            self.assertEqual(json.loads(saved.read_text(encoding="utf-8")), envelope)
            # Replaying the same next_actions result is safe and never replaces bytes.
            before = saved.read_bytes()
            self.assertEqual(adapter.dispatch(), [envelope])
            self.assertEqual(saved.read_bytes(), before)

    def test_callback_inbox_is_atomic_and_rejects_duplicate_event(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            store, request = self._store_with_request(root)
            adapter = FilesystemHostAdapter(root, store=store)
            envelope = {
                "protocol_version": 1,
                "kind": "agent_result",
                "request_id": request["request_id"],
                "attempt_id": request["attempt_id"],
                "event_id": "event-1",
                "agent_id": "agent-1",
                "manifest_sha256": None,
                "payload": {"status": {"agent-1": {"completed": "host payload"}}},
                "host_metadata": {"raw": True},
            }

            path = adapter.write_callback(envelope)

            self.assertEqual(json.loads(path.read_text(encoding="utf-8")), envelope)
            self.assertFalse(list((root / "callback-inbox").glob("*.tmp")))
            with self.assertRaisesRegex(FileExistsError, "already exists"):
                adapter.write_callback(envelope)
            changed = dict(envelope, payload={"status": {"agent-1": {"errored": "changed"}}})
            with self.assertRaises(FileExistsError):
                adapter.write_callback(changed)
            self.assertEqual(path.read_text(encoding="utf-8"), json.dumps(envelope, ensure_ascii=False,
                                                                            indent=2, sort_keys=True) + "\n")

    def test_mismatched_correlation_fields_are_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            manifest = {"path": "verification-manifest.json", "sha256": "a" * 64, "target": None}
            store, request = self._store_with_request(root, manifest=manifest)
            adapter = FilesystemHostAdapter(root, store=store)
            base = {
                "protocol_version": 1,
                "kind": "agent_result",
                "request_id": request["request_id"],
                "attempt_id": request["attempt_id"],
                "event_id": "event-2",
                "agent_id": "agent-1",
                "manifest_sha256": request["manifest_sha256"],
                "payload": {"status": {"agent-1": {"completed": "host payload"}}},
            }
            for field, value, message in (
                ("request_id", "other-request", "unknown request"),
                ("attempt_id", "other-attempt", "different attempt"),
                ("protocol_version", 2, "protocol"),
                ("manifest_sha256", "b" * 64, "different verification manifest"),
            ):
                with self.subTest(field=field):
                    with self.assertRaisesRegex(ValueError, message):
                        adapter.write_callback(dict(base, **{field: value}))
            self.assertFalse(list((root / "callback-inbox").glob("*.json")))


if __name__ == "__main__":
    unittest.main()
