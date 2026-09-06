import copy
import json
import tempfile
import unittest
from pathlib import Path

from percolation_workflow.model import (
    ATTEMPT_OUTPUT_SUMMARY_LIMIT,
    WorkflowState,
)
from percolation_workflow.store import StateStore


class AttemptHistoryReplayTests(unittest.TestCase):
    @staticmethod
    def finished_state() -> tuple[WorkflowState, str, str]:
        state = WorkflowState(project="attempt-history-test")
        node_id = state.add_node("leaf", "True")
        attempt_id = state.begin_attempt(node_id, "lean-agent", "Solution.lean")
        long_stdout = "header\n" + "x" * (ATTEMPT_OUTPUT_SUMMARY_LIMIT * 2) + "\nstdout-tail"
        long_stderr = "diagnostic\n" + "y" * (ATTEMPT_OUTPUT_SUMMARY_LIMIT * 2) + "\nstderr-tail"
        state.finish_attempt(
            attempt_id,
            status="compile_error",
            command=["lean", "Solution.lean"],
            stdout=long_stdout,
            stderr=long_stderr,
            exit_code=1,
        )
        return state, node_id, attempt_id

    def test_append_replay_bounded_summaries_and_checksum_round_trip(self):
        state, node_id, attempt_id = self.finished_state()
        self.assertEqual([entry["event"] for entry in state.attempt_history],
                         ["started", "finished"])
        finished = state.attempt_history[-1]
        self.assertEqual(finished["node_id"], node_id)
        self.assertEqual(finished["agent_id"], "lean-agent")
        self.assertEqual(finished["source_path"], "Solution.lean")
        self.assertEqual(finished["status"], "compile_error")
        self.assertEqual(finished["exit_code"], 1)
        self.assertLessEqual(len(finished["stdout_summary"]), ATTEMPT_OUTPUT_SUMMARY_LIMIT)
        self.assertLessEqual(len(finished["stderr_summary"]), ATTEMPT_OUTPUT_SUMMARY_LIMIT)
        self.assertTrue(finished["stdout_summary"].endswith("stdout-tail"))
        self.assertTrue(finished["stderr_summary"].endswith("stderr-tail"))

        replayed = state.replay_attempt_history()[attempt_id]
        self.assertEqual(replayed["status"], "compile_error")
        self.assertEqual(replayed["created_at"], state.attempts[attempt_id].created_at)
        self.assertEqual(replayed["finished_at"], state.attempts[attempt_id].finished_at)

        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "state.json"
            store = StateStore(path)
            store.save(state)
            payload = json.loads(path.read_text(encoding="utf-8"))
            self.assertIn("state_checksum", payload)
            self.assertEqual(payload["attempt_history"], state.attempt_history)
            loaded = store.load()
            self.assertEqual(loaded.attempt_history, state.attempt_history)
            self.assertEqual(loaded.replay_attempt_history(), state.replay_attempt_history())

    def test_active_and_legacy_attempts_reconstruct_a_replayable_history(self):
        active = WorkflowState(project="legacy-active")
        node_id = active.add_node("leaf", "True")
        attempt_id = active.begin_attempt(node_id, "agent", None)
        legacy_payload = active.to_dict()
        legacy_payload.pop("attempt_history")

        restored = WorkflowState.from_dict(legacy_payload)
        self.assertEqual(len(restored.attempt_history), 1)
        self.assertEqual(restored.attempt_history[0]["event"], "started")
        self.assertEqual(restored.replay_attempt_history()[attempt_id]["status"], "created")

        finished, _, finished_id = self.finished_state()
        legacy_payload = finished.to_dict()
        legacy_payload.pop("attempt_history")
        restored = WorkflowState.from_dict(legacy_payload)
        self.assertEqual([entry["event"] for entry in restored.attempt_history],
                         ["started", "finished"])
        self.assertEqual(restored.replay_attempt_history()[finished_id]["exit_code"], 1)

    def test_malformed_or_inconsistent_history_fails_closed(self):
        state, _, _ = self.finished_state()
        payload = state.to_dict()

        corruptions = {
            "sequence": lambda history: history[-1].__setitem__("sequence", 8),
            "node": lambda history: history[-1].__setitem__("node_id", "other"),
            "agent": lambda history: history[-1].__setitem__("agent_id", "other"),
            "source": lambda history: history[-1].__setitem__("source_path", "Other.lean"),
            "status": lambda history: history[-1].__setitem__("status", "passed"),
            "exit": lambda history: history[-1].__setitem__("exit_code", 0),
            "created_time": lambda history: history[-1].__setitem__(
                "created_at", "2026-09-05T00:00:00+00:00"),
            "finished_time": lambda history: history[-1].__setitem__(
                "finished_at", "not-a-time"),
            "stdout_summary": lambda history: history[-1].__setitem__(
                "stdout_summary", "tampered"),
        }
        for name, corrupt in corruptions.items():
            with self.subTest(name=name):
                damaged = copy.deepcopy(payload)
                corrupt(damaged["attempt_history"])
                with self.assertRaises(ValueError):
                    WorkflowState.from_dict(damaged)

        for name, history in {
            "missing_finish": copy.deepcopy(payload["attempt_history"][:-1]),
            "finish_before_start": list(reversed(copy.deepcopy(payload["attempt_history"]))),
            "unknown_field": copy.deepcopy(payload["attempt_history"]),
        }.items():
            with self.subTest(name=name):
                damaged = copy.deepcopy(payload)
                damaged["attempt_history"] = history
                if name == "unknown_field":
                    damaged["attempt_history"][0]["unexpected"] = True
                with self.assertRaises(ValueError):
                    WorkflowState.from_dict(damaged)


    def test_rebind_preserves_immutable_started_owner(self):
        state = WorkflowState(project="rebind-history-test")
        node_id = state.add_node("leaf", "True")
        attempt_id = state.begin_attempt(node_id, "dispatch-pending:req")
        started_before = copy.deepcopy(state.attempt_history[0])

        state.rebind_attempt(attempt_id, "real-host-agent")

        self.assertEqual(state.attempt_history[0], started_before)
        self.assertEqual(state.attempts[attempt_id].created_agent_id, "dispatch-pending:req")
        self.assertEqual(state.attempts[attempt_id].agent_id, "real-host-agent")
        state.finish_attempt(attempt_id, status="compile_error", command=[],
                             stdout="", stderr="failed", exit_code=1)
        self.assertEqual(state.attempt_history[0]["agent_id"], "dispatch-pending:req")
        self.assertEqual(state.attempt_history[1]["agent_id"], "real-host-agent")
        state.validate()


if __name__ == "__main__":
    unittest.main()
