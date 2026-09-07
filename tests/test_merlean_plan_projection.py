import json
import tempfile
import unittest
from pathlib import Path

from percolation_workflow.merlean_plan_projection import (
    cycles, export_views, forward_cone, levels, project, topo_order,
)
from percolation_workflow.model import EvidenceStage, NodeStatus, ProofNode, WorkflowState


class MerLeanProjectionTests(unittest.TestCase):
    def make_state(self):
        state = WorkflowState(project="demo", revision=7)
        state.nodes = {
            "a": ProofNode("a", "leaf", "P", proof_sketch="prove P",
                           metadata={"provenance": {"source": "fixture"}}),
            "b": ProofNode("b", "middle", "P -> Q", dependencies=["a"],
                           metadata={"evidence_stage": EvidenceStage.COMPILED_CANDIDATE.value}),
            "c": ProofNode("c", "root", "Q -> R", dependencies=["b"]),
        }
        state.root_id = "c"
        return state

    def test_graph_queries_are_deterministic(self):
        state = self.make_state()
        self.assertEqual(topo_order(state), ["a", "b", "c"])
        self.assertEqual(levels(state), {"a": 0, "b": 1, "c": 2})
        self.assertEqual(forward_cone(state, "a"), ["b", "c"])
        self.assertEqual(cycles(state), [])

    def test_notes_are_excluded_and_candidate_cannot_be_verified(self):
        state = self.make_state()
        before = json.dumps(state.to_dict(), sort_keys=True)
        view = project(state)
        after = json.dumps(state.to_dict(), sort_keys=True)
        self.assertEqual(before, after)
        middle = next(row for row in view["statements"] if row["statement_id"] == "b")
        self.assertEqual(middle["evidence_stage"], "compiled_candidate")
        self.assertEqual(middle["status"], "pending")
        self.assertEqual(middle["admission_status"], "compiled_candidate")
        self.assertTrue(all(note["excluded_from_graph"] for note in view["notes"]))
        self.assertNotIn("completed_axiom", json.dumps(view))

    def test_verified_requires_registry_and_lean_stage(self):
        state = self.make_state()
        node = state.nodes["a"]
        node.status = NodeStatus.VERIFIED
        self.assertEqual(next(row for row in project(state)["statements"] if row["statement_id"] == "a")["status"], "pending")
        node.metadata["evidence_stage"] = EvidenceStage.LEAN_VERIFIED.value
        state.registry["a"] = {"node_id": "a"}
        self.assertEqual(next(row for row in project(state)["statements"] if row["statement_id"] == "a")["status"], "completed")

    def test_export_writes_disjoint_views(self):
        with tempfile.TemporaryDirectory() as directory:
            paths = export_views(self.make_state(), directory)
            self.assertEqual(set(paths), {"statements.json", "progress.json", "analytics.json"})
            statements = json.loads(Path(paths["statements.json"]).read_text(encoding="utf-8"))
            progress = json.loads(Path(paths["progress.json"]).read_text(encoding="utf-8"))
            self.assertNotIn("notes", statements)
            self.assertNotIn("content", progress["statements"][0])

    def test_cycle_is_reported(self):
        state = self.make_state()
        state.nodes["a"].dependencies = ["c"]
        self.assertEqual(cycles(state), [["a", "b", "c"]])
        with self.assertRaises(ValueError):
            project(state)


if __name__ == "__main__":
    unittest.main()
