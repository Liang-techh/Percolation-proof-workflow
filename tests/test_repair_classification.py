import copy
import unittest

from percolation_workflow.model import WorkflowState
from percolation_workflow.repair_classification import dry_run_repair_integration


class RepairClassificationTests(unittest.TestCase):
    def test_all_five_classes_project_to_disjoint_requests_without_mutation(self):
        state = WorkflowState(project="classification")
        root = state.add_node("Root", "True")
        child = state.add_node("Child", "True", parent_id=root)
        for diagnostic in ("unexpected token", "unknown tactic", "type mismatch"):
            attempt = state.begin_attempt(child, "agent")
            state.finish_attempt(attempt, status="compile_error", command=[], stdout="",
                                 stderr=diagnostic, exit_code=1)
        state.event("controller_final_comparator", accepted=False, stdout="wrong statement",
                    stderr="")
        state.event("coverage_checker_finished", node_id=child,
                    coverage_complete=False, reason="flowpipe gap")
        before = copy.deepcopy(state.to_dict())

        report = dry_run_repair_integration(state)

        self.assertFalse(report["persisted"])
        self.assertEqual({r["class"] for r in report["error_records"]},
                         {"syntax", "api", "semantic", "comparator", "coverage"})
        self.assertEqual(len(report["repair_requests"]), 5)
        self.assertTrue(any(r["node_id"] == root and r["repair_of_attempt_id"] is None
                            for r in report["repair_requests"]))
        self.assertEqual(state.to_dict(), before)
        self.assertEqual(state.registry, {})

    def test_unknown_compile_diagnostic_is_manual_review(self):
        state = WorkflowState(project="classification")
        node = state.add_node("Root", "True")
        attempt = state.begin_attempt(node, "agent")
        state.finish_attempt(attempt, status="compile_error", command=[], stdout="",
                             stderr="opaque failure", exit_code=1)
        report = dry_run_repair_integration(state)
        self.assertEqual(report["error_records"][0]["class"], "manual_review")
        self.assertEqual(report["repair_requests"][0]["repair_context"]["next_action"],
                         "manual_review")


if __name__ == "__main__":
    unittest.main()
