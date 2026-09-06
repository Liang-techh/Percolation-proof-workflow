import copy
import unittest

from percolation_workflow.math_frontier import project_frontier_receipt
from percolation_workflow.model import WorkflowState


class FrontierReceiptProjectionTests(unittest.TestCase):
    def test_projection_records_lane_blocker_hash_and_priority_without_mutation(self):
        state = WorkflowState()
        node_id = state.add_node("coverage", "coverage", metadata={
            "math_lane": "numerical_blocker", "status": "open_compile_blocked"})
        before = copy.deepcopy(state.to_dict())

        receipt = project_frontier_receipt(state)
        row = receipt["frontier"][0]
        self.assertEqual(receipt["formal_admission"], "unchanged")
        self.assertEqual(row["node_id"], node_id)
        self.assertEqual(row["lane"], "numerical_blocker")
        self.assertEqual(row["blocker"], "compile_obstruction")
        self.assertEqual(row["priority"], 2)
        self.assertEqual(len(row["evidence_hash"]), 64)
        self.assertEqual(state.to_dict(), before)

    def test_hash_changes_when_advisory_evidence_changes(self):
        state = WorkflowState()
        node_id = state.add_node("adapter", "adapter", metadata={"math_lane": "lean_adapter"})
        first = project_frontier_receipt(state)["frontier"][0]["evidence_hash"]
        state.nodes[node_id].metadata["evidence_note"] = "updated"
        second = project_frontier_receipt(state)["frontier"][0]["evidence_hash"]
        self.assertNotEqual(first, second)


if __name__ == "__main__":
    unittest.main()
