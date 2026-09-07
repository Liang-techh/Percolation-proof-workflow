import unittest

from percolation_workflow.model import EvidenceStage, NodeStatus, WorkflowState, status_is_closed


class EvidenceStageTests(unittest.TestCase):
    def test_generic_closed_predicate_is_theorem_only(self):
        self.assertTrue(status_is_closed(NodeStatus.VERIFIED))
        self.assertFalse(status_is_closed(NodeStatus.EVIDENCE_COMPLETE))

    def test_compiled_candidate_is_not_a_closed_dag_edge(self):
        state = WorkflowState()
        parent = state.add_node("parent", "P")
        child = state.add_node("child", "C", parent_id=parent)
        state.set_evidence_stage(child, EvidenceStage.COMPILED_CANDIDATE)
        self.assertEqual([node.id for node in state.frontier()], [child])
        self.assertEqual(state.nodes[child].status, NodeStatus.OPEN)
        self.assertEqual(state.global_closure_report()["status"], "open")

    def test_global_closure_requires_explicit_ci_receipt(self):
        state = WorkflowState()
        root = state.add_node("root", "R")
        state.nodes[root].status = NodeStatus.VERIFIED
        state.set_evidence_stage(root, EvidenceStage.LEAN_VERIFIED)
        self.assertEqual(state.global_closure_report()["status"],
                         "verified_root_pending_global_gate")
        with self.assertRaises(ValueError):
            state.close_global_theorem({"ci_passed": False})
        state.close_global_theorem({"ci_passed": True,
                                    "formal_certificate_allowed": True,
                                    "project_sha256": "abc"})
        self.assertEqual(state.global_closure_report()["status"], "global_closed")
        state.validate()

    def test_invalid_global_stage_cannot_be_serialized_as_verified(self):
        state = WorkflowState()
        node = state.add_node("root", "R")
        state.nodes[node].metadata["evidence_stage"] = EvidenceStage.GLOBAL_CLOSED.value
        with self.assertRaises(ValueError):
            state.validate()


if __name__ == "__main__":
    unittest.main()
