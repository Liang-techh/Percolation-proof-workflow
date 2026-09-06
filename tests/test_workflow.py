import tempfile
import unittest
from pathlib import Path
import shutil

from percolation_workflow.model import NodeStatus, WorkflowState
from percolation_workflow.store import StateStore
from percolation_workflow.comparator import load_config, normalized_statement
from percolation_workflow.lean import run_lean
from percolation_workflow.repair import repair_until_verified
from percolation_workflow.graph import attach_statement_index, import_decl_graph
from percolation_workflow.scheduler import FrontierResult, run_frontier_parallel
from percolation_workflow.statements import index_statements


class WorkflowTests(unittest.TestCase):
    def simulated_verified(self, state, node_id, artifact):
        # A pre-existing verified-state fixture for graph/serialization tests, not proof evidence.
        node = state.nodes[node_id]
        node.status = NodeStatus.VERIFIED
        node.verified_artifact = artifact
        state.registry[node_id] = {'node_id': node_id, 'artifact': artifact}

    def test_frontier_and_parent_close(self):
        state = WorkflowState()
        root = state.add_node("critical_continuity", "theta(p_c) = 0")
        a = state.add_node("gluing", "P(o↔b) ≥ P(o↔A)-t", parent_id=root)
        b = state.add_node("harris", "positive association", parent_id=root)
        self.assertEqual({n.id for n in state.frontier()}, {a, b})
        self.simulated_verified(state, a, "Solutions/gluing.lean")
        self.assertEqual([n.id for n in state.frontier()], [b])
        self.assertEqual(state.nodes[root].status, NodeStatus.OPEN)
        self.simulated_verified(state, b, "Solutions/harris.lean")
        self.assertEqual([n.id for n in state.frontier()], [root])

    def test_frontier_prioritizes_the_leaf_with_highest_closability(self):
        state = WorkflowState()
        root = state.add_node("root", "R")
        cascade = state.add_node("cascade", "C", parent_id=root)
        leaf = state.add_node("leaf", "L", parent_id=cascade)
        side = state.add_node("side", "S", parent_id=root)
        self.simulated_verified(state, side, "side.lean")
        self.assertEqual(state.frontier_closability(leaf), 2)
        self.assertEqual([node.id for node in state.frontier()], [leaf])
        self.simulated_verified(state, leaf, "leaf.lean")
        self.assertEqual(state.nodes[cascade].status, NodeStatus.OPEN)
        self.assertEqual(state.frontier_closability(cascade), 1)

        sibling_root = state.add_node("sibling-root", "SR")
        first = state.add_node("first", "F", parent_id=sibling_root)
        state.add_node("second", "S", parent_id=sibling_root)
        self.assertEqual(state.frontier_closability(first), 0)

    def test_round_trip_is_atomic_and_preserves_registry(self):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "state.json"
            state = WorkflowState(project="test")
            node = state.add_node("leaf", "True")
            self.simulated_verified(state, node, "leaf.lean")
            store = StateStore(path)
            store.save(state)
            loaded = store.load()
            self.assertEqual(loaded.project, "test")
            self.assertEqual(loaded.nodes[node].status, NodeStatus.VERIFIED)
            self.assertIn(node, loaded.registry)

    def test_uncompared_artifact_cannot_enter_registry(self):
        state = WorkflowState()
        node = state.add_node("leaf", "True")
        with self.assertRaises(ValueError):
            state._register_verified(node, "leaf.lean", receipt={})

    def test_failed_attempt_is_retained_for_repair(self):
        state = WorkflowState()
        node = state.add_node("leaf", "True")
        attempt = state.begin_attempt(node, "agent-1", "Solutions/leaf.lean")
        state.finish_attempt(attempt, status="compile_error", command=["lake", "build"],
                             stdout="", stderr="unknown identifier", exit_code=1)
        self.assertEqual(state.nodes[node].status, NodeStatus.OPEN)
        self.assertEqual(state.attempts[attempt].stderr, "unknown identifier")
        self.assertEqual(normalized_statement("a\n  b"), "a b")

    def test_cycle_is_rejected(self):
        state = WorkflowState()
        a = state.add_node("a", "A")
        b = state.add_node("b", "B", parent_id=a)
        state.nodes[a].dependencies.append(a)
        with self.assertRaises(ValueError):
            state.validate()

    def test_parent_link_must_agree_with_dependency_edge(self):
        state = WorkflowState()
        parent = state.add_node("parent", "P")
        child = state.add_node("child", "C", parent_id=parent)
        state.nodes[parent].dependencies.remove(child)
        with self.assertRaisesRegex(ValueError, "parent/dependency mismatch"):
            state.validate()

    def test_dangling_root_is_rejected(self):
        state = WorkflowState()
        state.root_id = "missing"
        with self.assertRaisesRegex(ValueError, "root_id"):
            state.validate()

    def test_real_lean_fixture_builds(self):
        project = Path(__file__).parents[1] / "examples" / "minimal_lean"
        result = run_lean(project)
        self.assertTrue(result.ok, result.stderr or result.stdout)

    def test_repair_loop_uses_compiler_feedback_and_then_passes(self):
        with tempfile.TemporaryDirectory() as d:
            project = Path(d) / "minimal_lean"
            shutil.copytree(Path(__file__).parents[1] / "examples" / "minimal_lean", project)
            solution = project / "Solution.lean"
            original = solution.read_text(encoding="utf-8")
            solution.write_text(original.replace("by omega", "by definitely_not_a_tactic"), encoding="utf-8")
            state = WorkflowState()
            node = state.add_node("repairable_leaf", "n + 1 ≤ n + 2")
            diagnostics = []
            def repair(path, stdout, stderr, round_no):
                diagnostics.append(stderr or stdout)
                solution.write_text(original, encoding="utf-8")
                return path
            ok = repair_until_verified(state, node, "agent-repair", project, str(solution), repair)
            self.assertTrue(ok)
            self.assertTrue(diagnostics)
            self.assertEqual(state.attempts[next(iter(state.attempts))].status, "compile_error")
            requested = [event for event in state.events if event["kind"] == "repair_requested"]
            self.assertEqual(len(requested), 1)
            self.assertTrue(requested[0]["disjoint_do"]["ok"])

    def test_comparator_config_is_loaded_from_upstream_shape(self):
        config = load_config(Path(__file__).parents[1] / "examples" / "minimal_lean" / "comparator.json")
        self.assertEqual(config.challenge_module, "Challenge")
        self.assertEqual(config.theorem_names, ("Minimal.main",))

    def test_decl_graph_import_and_parallel_frontier(self):
        with tempfile.TemporaryDirectory() as d:
            graph = Path(d) / "decl_graph.jsonl"
            graph.write_text('\n'.join([
                '{"name":"P.a","kind":"theorem","valueDeps":[]}',
                '{"name":"P.b","kind":"theorem","valueDeps":[]}',
                '{"name":"P.main","kind":"theorem","valueDeps":["P.a","P.b"]}',
            ]), encoding="utf-8")
            state = WorkflowState()
            ids = import_decl_graph(state, graph, project_prefix="P.")
            outcomes = run_frontier_parallel(state, {
                ids["P.a"]: lambda _: FrontierResult("passed", ["lake", "build"]),
                ids["P.b"]: lambda _: FrontierResult("passed", ["lake", "build"]),
            }, max_workers=2)
            self.assertEqual(set(outcomes.values()), {"passed"})
            self.assertEqual(len(state.attempts), 2)
            self.simulated_verified(state, ids["P.a"], "a.lean")
            self.simulated_verified(state, ids["P.b"], "b.lean")
            self.assertIn(ids["P.main"], {n.id for n in state.frontier()})

    def test_percolation_challenge_statement_index_stops_before_proofs(self):
        path = Path(__file__).parents[1] / "upstream" / "formal-math" / "percolation" / "Challenge.lean"
        records = index_statements(path)
        names = {r.qualified_name for r in records}
        self.assertIn("BondPercolation.percolation_continuity", names)
        self.assertIn("BondPercolation.percolation_continuity_Z3", names)
        self.assertIn("BondPercolation.criticalProb_mem_Icc", names)
        self.assertTrue(all(":=" not in r.source for r in records))
        critical = next(r for r in records if r.name == "criticalProb_mem_Icc")
        self.assertEqual(critical.end_line, 117)

    def test_statement_index_attaches_to_imported_dag(self):
        state = WorkflowState()
        node = state.add_node("BondPercolation.percolation_continuity", "pending",
                              metadata={"statement_status": "unresolved"})
        records = index_statements(Path(__file__).parents[1] / "upstream" / "formal-math" /
                                   "percolation" / "Challenge.lean")
        self.assertEqual(attach_statement_index(state, records), 1)
        self.assertIn("PercolationContinuity d", state.nodes[node].statement)
        self.assertEqual(state.nodes[node].metadata["statement_status"], "indexed")


if __name__ == "__main__":
    unittest.main()
