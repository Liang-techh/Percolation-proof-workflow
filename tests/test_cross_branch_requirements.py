import unittest
import hashlib

from percolation_workflow.model import NodeStatus, WorkflowState


class CrossBranchRequirementTests(unittest.TestCase):
    def close(self, state, node_id):
        state.nodes[node_id].status = NodeStatus.VERIFIED
        state.registry[node_id] = {"node_id": node_id, "artifact": f"{node_id}.lean"}

    def test_required_cross_branch_input_gates_frontier_and_cascade(self):
        state = WorkflowState()
        root = state.add_node("root", "R")
        input_root = state.add_node("input-root", "I")
        bridge = state.add_node(
            "bridge", "B", parent_id=root,
            metadata={"required_node_ids": [input_root]})

        self.assertEqual({node.id for node in state.frontier()}, {input_root})
        self.assertEqual(state.frontier_closability(bridge), 0)
        self.close(state, input_root)
        self.assertEqual([node.id for node in state.frontier()], [bridge])
        self.close(state, bridge)
        self.assertEqual([node.id for node in state.frontier()], [root])

    def test_unknown_or_self_required_input_is_rejected(self):
        state = WorkflowState()
        node_id = state.add_node("node", "N", metadata={"required_node_ids": ["missing"]})
        with self.assertRaisesRegex(ValueError, "required_node_ids"):
            state.validate()
        state.nodes[node_id].metadata["required_node_ids"] = [node_id]
        with self.assertRaisesRegex(ValueError, "required_node_ids"):
            state.validate()

    def test_verified_flag_without_registry_receipt_does_not_open_consumer(self):
        state = WorkflowState()
        input_id = state.add_node("input", "I")
        state.nodes[input_id].status = NodeStatus.VERIFIED
        consumer_id = state.add_node(
            "consumer", "C", metadata={"required_node_ids": [input_id]})

        self.assertNotIn(consumer_id, {node.id for node in state.frontier()})

    def test_global_closure_reaches_cross_branch_inputs(self):
        state = WorkflowState()
        root = state.add_node("root", "R")
        input_node = state.add_node("input", "I")
        state.nodes[root].metadata["required_node_ids"] = [input_node]
        report = state.global_closure_report()
        self.assertIn(input_node, report["reachable_nodes"])

    def test_registry_requires_explicit_cross_branch_input_evidence(self):
        state = WorkflowState()
        input_id = state.add_node("input", "theorem input : True")
        target_id = state.add_node(
            "target", "theorem target : True",
            metadata={"required_node_ids": [input_id],
                      "evidence_stage": "lean_verified"})
        self.close(state, input_id)
        state.nodes[input_id].metadata["evidence_stage"] = "lean_verified"
        state.registry[input_id] = {"node_id": input_id, "artifact": "input.lean"}
        attempt_id = state.begin_attempt(target_id, "agent")
        state.finish_attempt(attempt_id, status="passed", command=["lean"],
                             stdout="", stderr="", exit_code=0)
        receipt = {
            "attempt_id": attempt_id,
            "source_hashes": {"target.lean": "digest"},
            "source_digest": "digest",
            "statement_identity": {
                "name": "target",
                "statement_sha256": hashlib.sha256(
                    state.nodes[target_id].statement.encode()).hexdigest()},
            "comparator_command": ["comparator"],
            "comparator_stdout": "Your solution is okay!\n",
            "comparator_stderr": "",
        }
        with self.assertRaisesRegex(ValueError, "cross-branch input evidence"):
            state._register_verified(target_id, "target.lean", receipt=receipt)
        receipt["required_input_registries"] = {input_id: "input.lean"}
        state._register_verified(target_id, "target.lean", receipt=receipt)
        self.assertEqual(state.nodes[target_id].status, NodeStatus.VERIFIED)


if __name__ == "__main__":
    unittest.main()
