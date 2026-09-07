import copy
import random
import unittest
from unittest.mock import patch

from percolation_workflow.model import NodeStatus, WorkflowState
from percolation_workflow.reduction_batch import reduction_closure_batch


class ReductionBatchTests(unittest.TestCase):
    def make_state(self):
        state = WorkflowState()
        parent = state.add_node("parent", "P")
        children = [state.add_node(name, statement, parent_id=parent)
                    for name, statement in (("a", "A"), ("b", "B"), ("c", "C"))]
        state.nodes[parent].metadata["reduction_proposals"] = [{
            "proposal_id": "proposal-1", "status": "sketch_checked",
            "reduction_status": "accepted", "children": children,
            "child_order": children,
        }]
        return state, parent, children

    def test_projection_is_read_only_and_key_is_stable(self):
        state, parent, children = self.make_state()
        before = copy.deepcopy(state.to_dict())
        first = reduction_closure_batch(state, parent)
        completion_order = list(children)
        random.Random(7).shuffle(completion_order)
        shuffled = copy.deepcopy(state)
        for child_id in completion_order:
            shuffled.registry[child_id] = {"statement": shuffled.nodes[child_id].statement}
        second = reduction_closure_batch(shuffled, parent)
        self.assertEqual(first["closure_key"], second["closure_key"])
        self.assertEqual(first["ordered_child_ids"], children)
        self.assertEqual(state.to_dict(), before)
        self.assertEqual(len(first["closure_key"]), 64)

    def test_statuses_and_registry_are_projected(self):
        state, parent, children = self.make_state()
        for child_id in children:
            state.nodes[child_id].status = NodeStatus.VERIFIED
            state.registry[child_id] = {"statement": state.nodes[child_id].statement}
        with patch("percolation_workflow.reduction_batch.audit_registry",
                   return_value={child_id: {"status": "current"} for child_id in children}):
            batch = reduction_closure_batch(state, parent)
        self.assertEqual(set(batch["child_status"].values()), {"verified"})
        self.assertEqual(set(batch["registry_status"].values()), {"verified"})

    def test_statement_only_registry_entry_is_not_current(self):
        state, parent, children = self.make_state()
        state.nodes[children[0]].status = NodeStatus.VERIFIED
        state.registry[children[0]] = {"statement": state.nodes[children[0]].statement}
        batch = reduction_closure_batch(state, parent)
        self.assertNotEqual(batch["registry_status"][children[0]], "verified")

    def test_missing_child_data_fails_closed_and_legacy_falls_back(self):
        state, parent, children = self.make_state()
        del state.nodes[children[1]]
        with self.assertRaises(ValueError):
            reduction_closure_batch(state, parent)
        state, parent, children = self.make_state()
        state.nodes[parent].metadata["reduction_proposals"][0]["children"] = [children[0], children[0]]
        with self.assertRaises(ValueError):
            reduction_closure_batch(state, parent)
        state.nodes[parent].metadata["reduction_proposals"] = []
        self.assertIsNone(reduction_closure_batch(state, parent))

    def test_machine_closure_gate_requires_parent_receipt_after_children(self):
        state, parent, children = self.make_state()
        obligations = ["typed_adapter", "same_semantics"]
        state.nodes[parent].metadata["decomposition_contract"] = {
            "closure_gate": {
                "required_child_ids": children,
                "required_parent_receipt": "typed_source_binding",
                "required_obligations": obligations,
            },
        }
        for child_id in children:
            state.nodes[child_id].status = NodeStatus.VERIFIED
            state.registry[child_id] = {
                "statement": state.nodes[child_id].statement,
            }
        blocked = state.decomposition_closure_gate(parent)
        self.assertFalse(blocked["satisfied"])
        self.assertIn("missing parent receipt", " ".join(blocked["reasons"]))

        state.nodes[parent].metadata["parent_receipts"] = {
            "typed_source_binding": {
                "status": "accepted",
                "closed_obligations": obligations,
                "registry_eligible": True,
            },
        }
        self.assertTrue(state.decomposition_closure_gate(parent)["satisfied"])


if __name__ == "__main__":
    unittest.main()
