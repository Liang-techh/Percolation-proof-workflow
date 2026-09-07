import unittest

from percolation_workflow.math_frontier import (
    explain_math_bottleneck,
    explain_math_frontier,
    math_bottleneck,
    rank_formalizable_frontier,
)
from percolation_workflow.model import EvidenceStage, NodeStatus, WorkflowState
from percolation_workflow.scheduler import (
    FrontierResult,
    explain_frontier,
    rank_frontier,
    run_frontier_parallel,
)


class MathBottleneckDispatchTests(unittest.TestCase):
    def test_five_bottlenecks_have_canonical_labels_and_audit_reasons(self):
        rows = [
            ({"name": "deployed true-DH source comparator"}, "source_semantics"),
            ({"name": "physical Schur binding"}, "physical_schur_binding"),
            ({"name": "first-exit flowpipe coverage"}, "coverage"),
            ({"name": "h_src interval sign normalization"}, "interval_sign"),
            ({"name": "central finite difference bridge"}, "central_fd"),
        ]

        decisions = [explain_math_bottleneck(row) for row, _ in rows]
        self.assertEqual([decision.label for decision in decisions],
                         [expected for _, expected in rows])
        self.assertTrue(all(decision.source != "fallback" for decision in decisions))
        self.assertTrue(all(decision.reason.startswith("inferred ") for decision in decisions))

    def test_explicit_alias_is_canonical_and_invalid_value_fails_closed(self):
        alias = {"metadata": {"math_bottleneck": "schur-binding"}}
        invalid = {
            "name": "coverage",
            "metadata": {"math_bottleneck": "typo-category"},
        }

        decision = explain_math_bottleneck(alias)
        self.assertEqual(decision.label, "physical_schur_binding")
        self.assertEqual(decision.source, "metadata.math_bottleneck")
        self.assertEqual(math_bottleneck(invalid), "other")
        self.assertIn("unsupported explicit bottleneck", explain_math_bottleneck(invalid).reason)

    def test_evaluator_enclosure_is_a_distinct_source_bottleneck(self):
        decision = explain_math_bottleneck({
            "metadata": {
                "math_lane": "source_semantics",
                "math_bottleneck": "float64-enclosure",
            },
        })
        self.assertEqual(decision.label, "evaluator_enclosure")
        self.assertEqual(decision.priority, 1)

    def test_exact_coefficient_identity_is_a_first_class_math_bottleneck(self):
        decision = explain_math_bottleneck({
            "metadata": {
                "math_lane": "lean_adapter",
                "math_bottleneck": "exact-real-coefficient-identity",
            },
        })
        self.assertEqual(decision.label, "coefficient_identity")
        self.assertEqual(decision.priority, 1)

    def test_formalizable_dispatch_prefers_coefficient_identity_over_unrelated_leaves(self):
        state = WorkflowState()
        evaluator = state.add_node(
            "evaluator", "O2", metadata={
                "math_lane": "source_semantics", "math_bottleneck": "evaluator_enclosure",
            },
        )
        identity = state.add_node(
            "identity", "O1", metadata={
                "math_lane": "lean_adapter", "math_bottleneck": "coefficient_identity",
            },
        )
        unrelated = state.add_node("unrelated adapter", "other")

        self.assertEqual(rank_formalizable_frontier(state), [identity, evaluator, unrelated])

    def test_formalizable_dispatch_excludes_lean_typed_coverage_rows(self):
        state = WorkflowState()
        coverage = state.add_node(
            "legacy coverage row", "global flowpipe coverage",
            metadata={"verification_domain": "lean"},
        )
        identity = state.add_node(
            "identity", "O1", metadata={
                "math_lane": "lean_adapter", "math_bottleneck": "coefficient_identity",
            },
        )

        self.assertEqual(rank_formalizable_frontier(state), [identity])
        self.assertNotIn(coverage, rank_formalizable_frontier(state))

    def test_scheduler_uses_stable_math_order_but_never_relaxes_obstruction(self):
        state = WorkflowState()
        central = state.add_node("central_fd", "FD")
        sign = state.add_node("interval_sign", "SIGN")
        physical = state.add_node("physical_schur_binding", "SCHUR")
        source = state.add_node("source_semantics", "SOURCE")
        coverage = state.add_node("coverage", "COVER")
        blocked_coverage = state.add_node(
            "coverage_blocked", "BLOCKED",
            metadata={"math_bottleneck": "coverage", "status": "open_compile_blocked"},
        )
        jobs = {node_id: lambda _: FrontierResult("passed", []) for node_id in (
            central, sign, physical, source, coverage, blocked_coverage,
        )}
        before = state.to_dict()

        self.assertEqual(rank_frontier(state, jobs),
                         [coverage, source, physical, sign, central])
        rows = {row["node_id"]: row for row in explain_frontier(state, jobs)}
        self.assertFalse(rows[blocked_coverage]["eligible"])
        self.assertEqual(rows[blocked_coverage]["obstruction_reason"], "compile_obstruction")
        self.assertEqual(rows[physical]["math_bottleneck"], "physical_schur_binding")
        self.assertIn("physical_schur_binding", rows[physical]["math_bottleneck_reason"])
        self.assertEqual(state.to_dict(), before)

    def test_math_projection_and_scheduler_share_the_same_reason(self):
        state = WorkflowState()
        node_id = state.add_node("h_src interval sign", "SIGN")
        math_row = explain_math_frontier(state)[0]
        scheduler_row = explain_frontier(state)[0]

        self.assertEqual(math_row["math_bottleneck"], scheduler_row["math_bottleneck"])
        self.assertEqual(math_row["math_bottleneck_source"],
                         scheduler_row["math_bottleneck_source"])
        self.assertEqual(math_row["math_bottleneck_reason"],
                         scheduler_row["math_bottleneck_reason"])
        self.assertEqual(node_id, scheduler_row["node_id"])

    def test_passed_numerical_job_is_not_promoted_to_verified(self):
        state = WorkflowState()
        node_id = state.add_node(
            "coverage", "numerical coverage evidence",
            metadata={"math_bottleneck": "coverage", "math_lane": "numerical_blocker"},
        )

        outcomes = run_frontier_parallel(
            state, {node_id: lambda _: FrontierResult("passed", [])}, max_workers=1,
        )

        self.assertEqual(outcomes[node_id], "passed")
        self.assertEqual(state.nodes[node_id].status, NodeStatus.OPEN)
        self.assertEqual(state.nodes[node_id].metadata["evidence_stage"],
                         EvidenceStage.COMPILED_CANDIDATE)


if __name__ == "__main__":
    unittest.main()
