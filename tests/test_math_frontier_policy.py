import unittest

from percolation_workflow.math_frontier import (
    MathLane,
    build_frontier_cut,
    explain_math_frontier,
    math_lane,
    math_bottleneck,
    rank_math_obstruction_frontier,
    rank_formalizable_frontier,
    rank_math_frontier,
)
from percolation_workflow.model import WorkflowState


class MathFrontierPolicyTests(unittest.TestCase):
    def test_explicit_lanes_are_authoritative_and_ordered(self):
        state = WorkflowState()
        numeric = state.add_node("coverage", "N", metadata={"math_lane": "numerical_blocker"})
        source = state.add_node("bridge", "S", metadata={"math_lane": "source_semantics"})
        adapter = state.add_node("adapter", "L", metadata={"math_lane": "lean_adapter"})
        jobs = {node_id: object() for node_id in (numeric, source, adapter)}

        self.assertEqual(rank_math_frontier(state, jobs), [adapter, source, numeric])
        self.assertEqual(math_lane(state.nodes[adapter]), MathLane.LEAN_ADAPTER)

    def test_v125_style_rows_are_classified_without_workflow_metadata(self):
        self.assertEqual(math_lane({
            "id": "B45-1_fourier_phase_bridge",
            "status": "compiled_candidate_comparator_pending",
            "source": "../../examples/adapter.lean",
        }), MathLane.LEAN_ADAPTER)
        self.assertEqual(math_lane({
            "id": "B45-source_central_fd_binding_subtree",
            "status": "decomposed_open",
            "dependencies": ["source_semantics"],
        }), MathLane.SOURCE_SEMANTICS)
        self.assertEqual(math_lane({
            "id": "B45-P3_global_coverage_interval_interface",
            "status": "open",
            "statement": "global flowpipe interval coverage",
        }), MathLane.NUMERICAL_BLOCKER)

    def test_explicit_verification_domain_fills_legacy_lane_gap(self):
        self.assertEqual(math_lane({
            "id": "lean_leaf",
            "verification_domain": "lean",
            "status": "open",
        }), MathLane.LEAN_ADAPTER)
        self.assertEqual(math_lane({
            "id": "source_leaf",
            "metadata": {"verification_domain": "external-research"},
            "status": "open",
        }), MathLane.SOURCE_SEMANTICS)

    def test_formalizable_adapter_excludes_numeric_dead_ends_opt_in(self):
        state = WorkflowState()
        numeric = state.add_node("coverage", "N",
                                metadata={"math_lane": "numerical_blocker"})
        adapter = state.add_node("adapter", "L",
                                 metadata={"math_lane": "lean_adapter"})
        jobs = {node_id: object() for node_id in (numeric, adapter)}
        self.assertEqual(rank_math_frontier(state, jobs), [adapter, numeric])
        self.assertEqual(rank_formalizable_frontier(state, jobs), [adapter])

        numeric_only = WorkflowState()
        only = numeric_only.add_node("coverage", "N",
                                    metadata={"math_lane": "numerical_blocker"})
        self.assertEqual(rank_formalizable_frontier(numeric_only, {only: object()}), [])

    def test_explanation_is_read_only_and_keeps_obstruction_gate(self):
        state = WorkflowState()
        blocked = state.add_node("adapter", "L", metadata={
            "math_lane": "lean_adapter", "status": "open_compile_blocked"})
        before = len(state.attempts)
        rows = explain_math_frontier(state)
        self.assertEqual(rows[0]["math_lane"], "lean_adapter")
        self.assertFalse(rows[0]["eligible"])
        self.assertEqual(len(state.attempts), before)
        self.assertEqual(blocked, rows[0]["node_id"])

    def test_obstruction_order_exposes_math_bottleneck_without_dispatch(self):
        state = WorkflowState()
        fd = state.add_node("central_fd", "FD", metadata={
            "math_lane": "source_semantics", "math_bottleneck": "central_fd",
            "status": "open_compile_blocked"})
        sign = state.add_node("interval_sign", "SIGN", metadata={
            "math_lane": "source_semantics", "math_bottleneck": "interval_sign",
            "status": "source_comparator_blocked"})
        schur = state.add_node("physical_schur_binding", "SCHUR", metadata={
            "math_lane": "numerical_blocker", "math_bottleneck": "physical_schur_binding",
            "status": "open"})
        coverage = state.add_node("coverage", "COVER", metadata={
            "math_lane": "numerical_blocker", "math_bottleneck": "coverage",
            "status": "open"})
        before = state.to_dict()
        self.assertEqual(rank_math_obstruction_frontier(state), [coverage, schur, sign, fd])
        self.assertEqual(math_bottleneck(state.nodes[fd]), "central_fd")
        self.assertEqual(state.to_dict(), before)
        # The audit order does not relax the ordinary obstruction gate.
        rows = {row["node_id"]: row for row in explain_math_frontier(state)}
        self.assertFalse(rows[fd]["eligible"])
        self.assertFalse(rows[sign]["eligible"])

    def test_frontier_cut_is_grouped_stable_and_read_only(self):
        state = WorkflowState()
        lean = state.add_node("lean", "L", metadata={"math_lane": "lean_adapter"})
        source = state.add_node("source", "S", metadata={"math_lane": "source_semantics"})
        state.add_node("numeric", "N", metadata={"math_lane": "numerical_blocker"})
        before = state.to_dict()
        cut = build_frontier_cut(state, {lean: object(), source: object()})
        again = build_frontier_cut(state, {source: object(), lean: object()})
        self.assertEqual(cut["cut_sha256"], again["cut_sha256"])
        self.assertEqual(cut["lanes"]["lean_adapter"], [lean])
        self.assertEqual(cut["lanes"]["source_semantics"], [source])
        self.assertFalse(cut["frontier"][2]["eligible"])
        self.assertEqual(state.to_dict(), before)


if __name__ == "__main__":
    unittest.main()
