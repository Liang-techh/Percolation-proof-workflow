import time
import unittest

from percolation_workflow.model import EvidenceStage, NodeStatus, WorkflowState, node_is_closed
from percolation_workflow.scheduler import (
    FrontierResult,
    candidate_identity,
    explain_frontier,
    obstruction_rank,
    rank_frontier,
    run_frontier_parallel,
    select_frontier_jobs,
)


class SchedulerPolicyTests(unittest.TestCase):
    def test_rank_prefers_unlocking_node_then_cost(self):
        state = WorkflowState()
        root = state.add_node("root", "True")
        parent = state.add_node("parent", "True", parent_id=root)
        sibling = state.add_node("sibling", "True", parent_id=parent)
        state.nodes[sibling].status = NodeStatus.VERIFIED
        first = state.add_node("first", "True", parent_id=parent,
                               metadata={"resource_cost": 10})
        second = state.add_node("second", "True",
                                metadata={"resource_cost": 1})
        # First closes parent and then root; second is intentionally unconnected.
        jobs = {first: lambda _: FrontierResult("passed", []),
                second: lambda _: FrontierResult("passed", [])}
        self.assertEqual(rank_frontier(state, jobs)[0], first)

    def test_obstructions_are_explicitly_excluded_from_dispatch(self):
        state = WorkflowState()
        blocked = state.add_node("blocked", "B",
                                 metadata={"status": "open_compile_blocked"})
        pending = state.add_node("pending", "P",
                                 metadata={"source_comparator": "open"})
        runnable = state.add_node("runnable", "R")
        jobs = {node_id: lambda _: FrontierResult("passed", [])
                for node_id in (blocked, pending, runnable)}

        self.assertEqual(obstruction_rank(state.nodes[blocked]), 2)
        self.assertEqual(obstruction_rank(state.nodes[pending]), 1)
        self.assertEqual(rank_frontier(state, jobs), [runnable])
        self.assertEqual(list(select_frontier_jobs(state, jobs, max_workers=3)), [runnable])

    def test_compiled_candidate_never_closes_a_dependency_edge(self):
        state = WorkflowState()
        parent = state.add_node("parent", "P")
        child = state.add_node("child", "C", parent_id=parent)
        state.set_evidence_stage(child, EvidenceStage.COMPILED_CANDIDATE)

        self.assertFalse(node_is_closed(state.nodes[child]))
        self.assertEqual([node.id for node in state.frontier()], [child])
        self.assertEqual(obstruction_rank(state.nodes[child]), 1)

    def test_explain_frontier_preserves_obstruction_reasons_without_mutation(self):
        state = WorkflowState()
        blocked = state.add_node("blocked", "B",
                                 metadata={"status": "open_compile_blocked"})
        pending = state.add_node("pending", "P",
                                 metadata={"source_comparator": "open"})
        runnable = state.add_node("runnable", "R", metadata={"resource_cost": 3})
        before = (len(state.attempts), state.nodes[runnable].status)

        rows = explain_frontier(state, {blocked: lambda _: FrontierResult("passed", []),
                                        pending: lambda _: FrontierResult("passed", []),
                                        runnable: lambda _: FrontierResult("passed", [])})
        by_name = {row["name"]: row for row in rows}
        self.assertEqual(by_name["blocked"]["obstruction_reason"], "compile_obstruction")
        self.assertEqual(by_name["pending"]["obstruction_reason"],
                         "comparator_or_candidate_obstruction")
        self.assertTrue(by_name["runnable"]["eligible"])
        self.assertEqual(by_name["runnable"]["resource_cost"], 3.0)
        self.assertEqual(before, (len(state.attempts), state.nodes[runnable].status))

    def test_explicit_candidate_identity_is_deduplicated_after_policy_sort(self):
        state = WorkflowState()
        root = state.add_node("root", "R")
        parent = state.add_node("parent", "P", parent_id=root)
        sibling = state.add_node("sibling", "S", parent_id=parent)
        state.nodes[sibling].status = NodeStatus.VERIFIED
        preferred = state.add_node("preferred", "C", parent_id=parent,
                                   metadata={"candidate_digest": "same-candidate"})
        duplicate = state.add_node("duplicate", "C",
                                   metadata={"candidate_digest": "same-candidate"})
        jobs = {node_id: lambda _: FrontierResult("passed", [])
                for node_id in (preferred, duplicate)}

        self.assertEqual(candidate_identity(state.nodes[preferred]), "same-candidate")
        self.assertEqual(rank_frontier(state, jobs), [preferred])

    def test_budget_defers_expensive_jobs_without_deadlocking(self):
        state = WorkflowState()
        cheap = state.add_node("cheap", "True", metadata={"resource_cost": 1})
        expensive = state.add_node("expensive", "True", metadata={"resource_cost": 50})
        jobs = {cheap: lambda _: FrontierResult("passed", []),
                expensive: lambda _: FrontierResult("passed", [])}
        chosen = select_frontier_jobs(state, jobs, max_workers=2, max_cost=2)
        self.assertEqual(list(chosen), [cheap])

    def test_timeout_releases_frontier_and_records_timeout(self):
        state = WorkflowState()
        node_id = state.add_node("slow", "True")

        def slow(_):
            time.sleep(0.15)
            return FrontierResult("passed", [])

        started = time.monotonic()
        outcomes = run_frontier_parallel(state, {node_id: slow}, timeout_s=0.01)
        elapsed = time.monotonic() - started
        self.assertEqual(outcomes[node_id], "timeout")
        self.assertEqual(state.nodes[node_id].status, "open")
        self.assertLess(elapsed, 0.12)
        self.assertTrue(any(e["kind"] == "frontier_job_timed_out" for e in state.events))


if __name__ == "__main__":
    unittest.main()
