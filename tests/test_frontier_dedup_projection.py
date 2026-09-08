import copy
import unittest

from percolation_workflow.frontier_dedup_projection import project_frontier_dedup
from percolation_workflow.model import EvidenceStage, WorkflowState, node_is_closed
from percolation_workflow.scheduler import rank_frontier, select_frontier_jobs


def never_run(_):
    raise AssertionError("read-only projection must not execute a job")


class FrontierDedupProjectionTests(unittest.TestCase):
    def test_duplicate_maps_to_policy_winner_without_erasing_either_node(self):
        state = WorkflowState()
        first = state.add_node("agent-one", "same candidate", metadata={
            "candidate_key": "fixture-candidate", "scheduler_priority": 1})
        preferred = state.add_node("agent-two", "same candidate", metadata={
            "candidate_key": "fixture-candidate", "scheduler_priority": 3})
        jobs = {first: never_run, preferred: never_run}
        projection = project_frontier_dedup(state, jobs)
        rows = {r["node_id"]: r for r in projection["frontier"]}
        self.assertEqual(projection["ranked_node_ids"], rank_frontier(state, jobs))
        self.assertEqual(projection["ranked_node_ids"], [preferred])
        self.assertEqual(set(rows), {first, preferred})
        self.assertTrue(rows[first]["eligible"])
        self.assertEqual(rows[first]["dedup_status"], "duplicate")
        self.assertEqual(rows[first]["deduplicated_into"], preferred)
        self.assertIsNone(rows[first]["rank_after_dedup"])
        self.assertEqual(rows[preferred]["dedup_status"], "retained")
        self.assertEqual(rows[preferred]["rank_after_dedup"], 0)

    def test_obstruction_and_registration_precede_dedup(self):
        state = WorkflowState()
        blocked = state.add_node("blocked", "C", metadata={
            "candidate_key": "shared", "status": "open_compile_blocked",
            "scheduler_priority": 100})
        pending = state.add_node("pending", "C", metadata={"candidate_key": "shared"})
        state.set_evidence_stage(pending, EvidenceStage.COMPILED_CANDIDATE)
        unregistered = state.add_node("unregistered", "C", metadata={
            "candidate_key": "shared", "scheduler_priority": 200})
        runnable = state.add_node("runnable", "C", metadata={"candidate_key": "shared"})
        jobs = {n: never_run for n in (blocked, pending, runnable)}
        projection = project_frontier_dedup(state, jobs)
        self.assertEqual(projection["ranked_node_ids"], [runnable])
        rows = {r["node_id"]: r for r in projection["frontier"]}
        for n, reason in ((blocked, "compile_obstruction"),
                          (pending, "comparator_or_candidate_obstruction"),
                          (unregistered, "no_registered_job")):
            self.assertEqual(rows[n]["dedup_status"], "ineligible")
            self.assertEqual(rows[n]["obstruction_reason"], reason)
            self.assertIsNone(rows[n]["deduplicated_into"])
        self.assertFalse(node_is_closed(state.nodes[pending]))

    def test_names_and_conditional_pass_are_not_candidate_identity(self):
        state = WorkflowState()
        ids = [state.add_node("same task", "same statement", metadata={
            "review_status": "CONDITIONAL_PASS", "registry_status": "pending",
            "source_agent": agent}) for agent in ("one", "two")]
        jobs = {n: never_run for n in ids}
        before = copy.deepcopy(state.to_dict())
        projection = project_frontier_dedup(state, jobs)
        self.assertEqual(set(projection["ranked_node_ids"]), set(ids))
        self.assertTrue(all(r["dedup_status"] == "retained" for r in projection["frontier"]))
        self.assertEqual(state.to_dict(), before)
        self.assertTrue(all(not node_is_closed(state.nodes[n]) for n in ids))

    def test_pure_detached_projection_is_stable_under_map_order(self):
        state = WorkflowState()
        ids = [state.add_node(str(i), "C", metadata={
            "candidate_key": "shared", "required_node_ids": [],
            "registry_status": "pending"}) for i in range(2)]
        state.event("fixture_history", payload={"append_only": [1, 2]})
        before = copy.deepcopy(state.to_dict())
        jobs = {n: never_run for n in ids}
        projection = project_frontier_dedup(state, jobs)
        self.assertEqual(projection, project_frontier_dedup(state, dict(reversed(list(jobs.items())))))
        state.nodes = dict(reversed(list(state.nodes.items())))
        self.assertEqual(projection, project_frontier_dedup(state, jobs))
        self.assertEqual(projection["formal_admission"], "unchanged")
        projection["frontier"][0]["required_node_ids"].append("not-a-state-write")
        projection["ranked_node_ids"].clear()
        self.assertEqual(state.to_dict(), before)

    def test_empty_registration_and_budget_scope_are_explicit(self):
        state = WorkflowState()
        ids = [state.add_node(str(i), "C", metadata={"candidate_key": str(i)})
               for i in range(2)]
        self.assertEqual(project_frontier_dedup(state, {})["ranked_node_ids"], [])
        jobs = {n: never_run for n in ids}
        projection = project_frontier_dedup(state, jobs)
        self.assertEqual(len(projection["ranked_node_ids"]), 2)
        self.assertEqual(len(select_frontier_jobs(state, jobs, max_workers=1)), 1)
        self.assertEqual(projection["selection_scope"], "rank_frontier_before_worker_and_cost_limits")
        self.assertEqual(project_frontier_dedup(WorkflowState(), {})["frontier"], [])


if __name__ == "__main__":
    unittest.main()
