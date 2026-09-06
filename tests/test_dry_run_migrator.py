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


if __name__ == "__main__":
    unittest.main()
