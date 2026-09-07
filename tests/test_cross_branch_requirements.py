import unittest

from percolation_workflow.model import NodeStatus, WorkflowState


class CrossBranchRequirementTests(unittest.TestCase):
    def close(self, state, node_id):
        state.nodes[node_id].status = NodeStatus.VERIFIED

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


if __name__ == "__main__":
    unittest.main()
