import copy
import hashlib
import json
import tempfile
import unittest
from pathlib import Path

from percolation_workflow.dry_run_migrator import dry_run_migrate
from percolation_workflow.model import WorkflowState


class DryRunMigratorTests(unittest.TestCase):
    def write_case(self, directory: str, *, proposal_nodes, revision=0):
        root = Path(directory)
        state_path = root / "state.json"
        state = WorkflowState(revision=revision)
        parent = state.add_node("parent", "P")
        state.add_node("other", "O")
        state_path.write_text(json.dumps(state.to_dict(), ensure_ascii=False), encoding="utf-8")
        raw = state_path.read_bytes()
        proposal = {"schema": "routeb-entry-dag-proposed-patch-v1", "mode": "proposal_only",
                    "state_mutation": False,
                    "snapshot": {"revision": revision, "root_id": parent,
                                  "state_sha256": hashlib.sha256(raw).hexdigest()},
                    "nodes": proposal_nodes(parent)}
        proposal_path = root / "proposal.json"
        proposal_path.write_text(json.dumps(proposal), encoding="utf-8")
        return state_path, proposal_path

    def test_valid_dry_run_has_no_state_or_registry_delta(self):
        def nodes(parent):
            return [{"id": f"L{i}", "name": f"Entry.L{i}", "parent_id": parent,
                     "dependencies": [], "statement": "S", "status": "open",
                     "metadata": {"entry_contract_layer": f"L{i}",
                                  "evidence_level": "audit_only", "conditional": True,
                                  "registry_eligible": False}}
                    for i in range(7)]
        with tempfile.TemporaryDirectory() as d:
            state_path, proposal_path = self.write_case(d, proposal_nodes=nodes)
            before = state_path.read_bytes()
            report = dry_run_migrate(state_path, proposal_path)
            self.assertTrue(report["safe_to_install"])
            self.assertEqual(state_path.read_bytes(), before)
            self.assertEqual(report["plan"]["registry_delta"], {"add": [], "remove": []})

    def test_snapshot_drift_and_verified_parent_fail_closed(self):
        def nodes(parent):
            rows = [{"id": f"L{i}", "name": f"Entry.L{i}", "parent_id": parent,
                     "dependencies": [], "status": "open",
                     "metadata": {"entry_contract_layer": f"L{i}",
                                  "evidence_level": "audit_only", "conditional": True,
                                  "registry_eligible": False}}
                    for i in range(7)]
            return rows
        with tempfile.TemporaryDirectory() as d:
            state_path, proposal_path = self.write_case(d, proposal_nodes=nodes)
            payload = json.loads(state_path.read_text(encoding="utf-8"))
            parent = payload["root_id"]
            payload["nodes"][parent]["status"] = "verified"
            state_path.write_text(json.dumps(payload), encoding="utf-8")
            report = dry_run_migrate(state_path, proposal_path)
            self.assertFalse(report["safe_to_install"])
            self.assertIn("snapshot_hash", report["failures"])
            self.assertIn(f"parent_open:{parent}", report["failures"])

    def test_shared_schema_allows_multiple_layers_and_cross_branch_dependencies(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            state = WorkflowState(revision=4)
            p3 = state.add_node("p3", "P3")
            p4 = state.add_node("p4", "P4")
            m4 = state.add_node("m4", "M4")
            state_path = root / "state.json"
            state_path.write_text(json.dumps(state.to_dict()), encoding="utf-8")
            raw = state_path.read_bytes()
            nodes = [
                {"id": "shared-manifest", "name": "S.source_manifest_contract",
                 "parent_id": None, "dependencies": [], "statement": "S1", "status": "open",
                 "metadata": {"logical_layer": "shared", "evidence_level": "audit_only",
                              "registry_eligible": False}},
                {"id": "shared-semantic", "name": "S.true_dh_semantic_binding",
                 "parent_id": None, "dependencies": ["shared-manifest"], "statement": "S2", "status": "open",
                 "metadata": {"logical_layer": "shared", "evidence_level": "conditional",
                              "registry_eligible": False}},
                {"id": "p3-child", "name": "P3.mass_box_soundness",
                 "parent_id": p3, "dependencies": ["shared-semantic"], "statement": "P3", "status": "open",
                 "metadata": {"logical_layer": "P3", "evidence_level": "conditional",
                              "registry_eligible": False}},
                {"id": "p4-child", "name": "P4.true_dh_residual_cell",
                 "parent_id": p4, "dependencies": ["shared-semantic"], "statement": "P4", "status": "open",
                 "metadata": {"logical_layer": "P4", "evidence_level": "conditional",
                              "registry_eligible": False}},
                {"id": "m4-join", "name": "M4.block45_assembly",
                 "parent_id": m4, "dependencies": ["p3-child", "p4-child"], "statement": "M4", "status": "open",
                 "metadata": {"logical_layer": "M4", "evidence_level": "conditional",
                              "registry_eligible": False}},
            ]
            proposal = {
                "schema": "routeb-shared-dag-proposed-patch-v2",
                "mode": "proposal_only", "state_mutation": False,
                "snapshot": {"revision": 4, "root_id": p3,
                              "state_sha256": hashlib.sha256(raw).hexdigest()},
                "layer_policy": {"mode": "allow_multiple",
                                  "allowed_layers": ["shared", "P3", "P4", "M4"]},
                "nodes": nodes,
            }
            proposal_path = root / "proposal.json"
            proposal_path.write_text(json.dumps(proposal), encoding="utf-8")
            before = state_path.read_bytes()
            report = dry_run_migrate(state_path, proposal_path)
            self.assertTrue(report["safe_to_install"])
            self.assertEqual(report["schema"], "theorem-dag-dry-run-migration-report-v2")
            self.assertEqual(len(report["plan"]["add_parent_edges"]), 3)
            self.assertEqual(state_path.read_bytes(), before)

    def test_shared_schema_rejects_cycle_and_unlisted_layer(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            state = WorkflowState(revision=1)
            parent = state.add_node("parent", "P")
            state_path = root / "state.json"
            state_path.write_text(json.dumps(state.to_dict()), encoding="utf-8")
            raw = state_path.read_bytes()
            def node(node_id, deps):
                return {"id": node_id, "name": node_id, "parent_id": None,
                        "dependencies": deps, "statement": node_id, "status": "open",
                        "metadata": {"logical_layer": "not-allowed", "evidence_level": "audit",
                                     "registry_eligible": False}}
            proposal = {"schema": "routeb-shared-dag-proposed-patch-v2",
                        "mode": "proposal_only", "state_mutation": False,
                        "snapshot": {"revision": 1, "root_id": parent,
                                      "state_sha256": hashlib.sha256(raw).hexdigest()},
                        "layer_policy": {"mode": "allow_multiple", "allowed_layers": ["shared"]},
                        "nodes": [node("a", ["b"]), node("b", ["a"])]}
            proposal_path = root / "proposal.json"
            proposal_path.write_text(json.dumps(proposal), encoding="utf-8")
            report = dry_run_migrate(state_path, proposal_path)
            self.assertFalse(report["safe_to_install"])
            self.assertIn("allowed_layers", report["failures"])
            self.assertIn("combined_acyclic", report["failures"])


if __name__ == "__main__":
    unittest.main()
