import json
import tempfile
import unittest
from pathlib import Path
import sys
import copy
import hashlib
import subprocess
from types import SimpleNamespace
from unittest.mock import patch

from percolation_workflow.external import (
    ROUTEB_STAGES, initialize_routeb_intake, run_external_gate, refresh_routeb_tracking,
    external_evidence_staleness,
)
from percolation_workflow.model import NodeStatus
from percolation_workflow.research import next_actions
from percolation_workflow.store import StateStore


class ExternalResearchTests(unittest.TestCase):
    def make_target(self, root: Path) -> None:
        (root / "robot_formal_v1").mkdir(parents=True)
        (root / "robot_final").mkdir()
        (root / "routeB_dense_Mq").mkdir()
        (root / "PROJECT_REFORM_TARGET.md").write_text("target brief\n", encoding="utf-8")
        (root / "PROJECT_REFORM_AUDIT.md").write_text("audit\n", encoding="utf-8")
        (root / "robot_formal_v1" / "manifest.json").write_text(
            json.dumps({"schema_version": "robot-formal-v1-index",
                        "current_gate": {"formal_certificate_allowed": False}}),
            encoding="utf-8")
        (root / "robot_formal_v1" / "README.md").write_text("readme\n", encoding="utf-8")
        (root / "robot_final" / "verify_all.py").write_text("# checker\n", encoding="utf-8")
        (root / "robot_final" / "routeB_certificate_manifest.toml").write_text("coverage_completed = true\n", encoding="utf-8")
        for stage in ROUTEB_STAGES:
            for rel in [*stage["artifacts"], stage["command"][1]]:
                path = root / rel
                if not path.exists():
                    path.parent.mkdir(parents=True, exist_ok=True)
                    path.write_text("print('UNKNOWN')\n" if path.suffix == ".py" else "fixture\n", encoding="utf-8")

    def setup_target(self, directory):
        target = Path(directory) / "target"
        self.make_target(target)
        store = StateStore(Path(directory) / "state.json")
        initialize_routeb_intake(target, store)
        return target, store

    def node(self, state, prefix):
        return next(n for n in state.nodes.values() if n.name.startswith(prefix + "."))

    def isolate(self, store, prefix):
        state = store.load()
        node = self.node(state, prefix)
        node.dependencies = []  # Test this checker without fabricating closed mathematical premises.
        store.save(state)
        return node

    def run_baseline(self, store):
        return run_external_gate(store, "P0.reproducibility_baseline",
                                 command=[sys.executable, "robot_final/verify_all.py"])

    def test_intake_exposes_only_first_external_frontier(self):
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "target"
            self.make_target(target)
            store = StateStore(Path(directory) / "state.json")
            state = initialize_routeb_intake(target, store)
            self.assertEqual(state.root_id, next(n.id for n in state.nodes.values()
                                                 if n.name == "P9.full_6dof_extension"))
            self.assertEqual([n.name for n in state.frontier()],
                             ["P0.reproducibility_baseline"])
            self.assertEqual(state.registry, {})
            self.assertEqual(next_actions(store)[0]["kind"], "run_external_gate")

    def test_external_evidence_closes_dependency_but_not_registry(self):
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "target"
            self.make_target(target)
            store = StateStore(Path(directory) / "state.json")
            initialize_routeb_intake(target, store)
            result = run_external_gate(
                store, "P0.reproducibility_baseline",
                command=[sys.executable, "robot_final/verify_all.py"],
                cwd=target)
            self.assertEqual(result["status"], "evidence_complete")
            state = store.load()
            node = next(n for n in state.nodes.values() if n.name == "P0.reproducibility_baseline")
            self.assertEqual(node.status, NodeStatus.EVIDENCE_COMPLETE)
            self.assertNotIn(node.id, state.registry)
            self.assertEqual([n.name for n in state.frontier()], ["P1.bracket_decision"])
            self.assertEqual(next_actions(store)[0]["kind"], "run_external_gate")

    def test_source_drift_rejects_external_gate(self):
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "target"
            self.make_target(target)
            store = StateStore(Path(directory) / "state.json")
            initialize_routeb_intake(target, store)
            # The checker changes a tracked intake artifact, so a zero exit code
            # must still be rejected and remain outside the registry.
            command = [sys.executable, "-c",
                       "from pathlib import Path; Path('PROJECT_REFORM_AUDIT.md').write_text('drift')"]
            result = run_external_gate(store, "P0.reproducibility_baseline",
                                       command=command, cwd=target)
            self.assertEqual(result["status"], "open")
            state = store.load()
            node = next(n for n in state.nodes.values() if n.name == "P0.reproducibility_baseline")
            self.assertEqual(node.status, NodeStatus.OPEN)
            self.assertEqual(node.metadata["execution_status"], "source_drift_rejected")
            self.assertEqual(state.attempts[result["attempt_id"]].status, "source_drift_rejected")
            receipt = node.metadata["last_external_receipt"]
            self.assertNotEqual(receipt["source_hashes_before"], receipt["source_hashes"])

    def test_external_gate_keeps_utf8_diagnostics(self):
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "target"
            self.make_target(target)
            store = StateStore(Path(directory) / "state.json")
            initialize_routeb_intake(target, store)
            result = run_external_gate(
                store, "P0.reproducibility_baseline",
                command=[sys.executable, "-c", "import sys; sys.stderr.write('诊断\\n'); sys.exit(1)"],
                cwd=target)
            self.assertEqual(result["status"], "open")
            state = store.load()
            attempt = state.attempts[result["attempt_id"]]
            self.assertEqual(attempt.stderr, "诊断\n")
            self.assertEqual(attempt.exit_code, 1)
            self.assertNotIn("SyntaxError", attempt.stderr)

    def test_arbitrary_exit_zero_cannot_accept_baseline(self):
        with tempfile.TemporaryDirectory() as directory:
            target, store = self.setup_target(directory)
            result = run_external_gate(store, "P0.reproducibility_baseline",
                                       command=[sys.executable, "-c", "print('ok')"])
            state = store.load()
            self.assertEqual(result["exit_code"], 0)
            self.assertEqual(result["status"], "open")
            self.assertEqual(state.attempts[result["attempt_id"]].status, "command_not_approved")
            self.assertEqual(state.registry, {})

    def test_zero_unknown_mathematics_stays_open_even_with_acceptance_flags(self):
        for prefix in ("P1", "P2", "P3", "P4", "P5", "P6", "P8", "M4", "P9"):
            with self.subTest(stage=prefix), tempfile.TemporaryDirectory() as directory:
                target = Path(directory) / "target"
                self.make_target(target)
                (target / "robot_formal_v1/manifest.json").write_text(json.dumps({"current_gate": {
                    "formal_certificate_allowed": True, "coverage_complete": True,
                    "remainder_absorbed": True}}), encoding="utf-8")
                store = StateStore(Path(directory) / "state.json")
                initialize_routeb_intake(target, store)
                node = self.isolate(store, prefix)
                # Julia need not be installed to test its process-result boundary.
                with patch("percolation_workflow.external.subprocess.run", return_value=SimpleNamespace(
                        stdout="UNKNOWN: mathematical claim remains open\n", stderr="", returncode=0)):
                    result = run_external_gate(store, node.name)
                state = store.load()
                current = state.nodes[node.id]
                self.assertEqual(result["status"], "open")
                self.assertEqual(current.metadata["claim_status"], node.metadata["claim_status"])
                self.assertEqual(current.metadata["execution_status"], "checker_passed")
                self.assertEqual(state.attempts[result["attempt_id"]].status, "passed")
                self.assertIn("UNKNOWN", state.attempts[result["attempt_id"]].stdout)
                self.assertFalse(current.metadata["last_external_receipt"]["dependency_closing"])
                action = next(a for a in next_actions(store) if a.get("node_id") == node.id)
                self.assertEqual(action["kind"], "decompose_external_obligation")
                self.assertEqual(state.registry, {})
                self.assertNotIn("final_project_check", [a["kind"] for a in next_actions(store)])

    def test_real_unknown_checker_does_not_unlock_successor(self):
        with tempfile.TemporaryDirectory() as directory:
            target, store = self.setup_target(directory)
            self.run_baseline(store)
            result = run_external_gate(store, "P1.bracket_decision",
                                       command=[sys.executable, "robot_final/verify_solver_metadata.py"])
            self.assertEqual(result["stdout"], "UNKNOWN\n")
            self.assertEqual(result["status"], "open")
            self.assertEqual([n.name for n in store.load().frontier()], ["P1.bracket_decision"])
            self.assertEqual(next_actions(store)[0]["kind"], "decompose_external_obligation")

    def test_stale_ancestor_rejected_before_execution_and_scheduling(self):
        with tempfile.TemporaryDirectory() as directory:
            target, store = self.setup_target(directory)
            self.run_baseline(store)
            (target / "robot_final/verify_all.py").write_text("# changed\n", encoding="utf-8")
            before = store.path.read_bytes()
            with patch("percolation_workflow.external.subprocess.run") as run:
                with self.assertRaisesRegex(ValueError, "stale"):
                    run_external_gate(store, "P1.bracket_decision")
                run.assert_not_called()
            self.assertEqual(store.path.read_bytes(), before)
            self.assertEqual([a["kind"] for a in next_actions(store)], ["revalidate_external_evidence"])
            self.assertEqual(store.load().frontier(), [])

    def test_explicit_audit_scope_and_transitive_stale_ancestor(self):
        with tempfile.TemporaryDirectory() as directory:
            target, store = self.setup_target(directory)
            self.run_baseline(store)
            state = store.load()
            metadata = copy.deepcopy(self.node(state, "P1").metadata)
            metadata["closure_scope"] = "audit"
            audit_id = state.add_node("audit.fixture", "The metadata checker completes",
                                      metadata=metadata, dependencies=[self.node(state, "P0").id])
            self.node(state, "P3").dependencies = [audit_id]
            store.save(state)
            result = run_external_gate(store, "audit.fixture",
                                       command=[sys.executable, "robot_final/verify_solver_metadata.py"])
            self.assertEqual(result["status"], "evidence_complete")
            (target / "robot_final/verify_all.py").write_text("# changed ancestor\n", encoding="utf-8")
            self.assertEqual(external_evidence_staleness(store.load().nodes[audit_id]), [])
            with patch("percolation_workflow.external.subprocess.run") as run:
                with self.assertRaisesRegex(ValueError, "P0"):
                    run_external_gate(store, "P3.strict_true_dh_bounds")
                run.assert_not_called()

    def test_ancestor_drift_during_execution_is_recorded_as_rejection(self):
        with tempfile.TemporaryDirectory() as directory:
            target, store = self.setup_target(directory)
            self.run_baseline(store)
            def drift(*args, **kwargs):
                (target / "robot_final/verify_all.py").write_text("# changed\n", encoding="utf-8")
                return SimpleNamespace(stdout="UNKNOWN\n", stderr="", returncode=0)
            with patch("percolation_workflow.external.subprocess.run", side_effect=drift):
                result = run_external_gate(store, "P1.bracket_decision")
            state = store.load()
            self.assertEqual(state.attempts[result["attempt_id"]].status, "stale_dependency_rejected")
            self.assertEqual(result["status"], "open")

    def test_unsatisfied_manifest_flags_do_not_repeat_successful_math_checker(self):
        with tempfile.TemporaryDirectory() as directory:
            target, store = self.setup_target(directory)
            node = self.isolate(store, "M4")
            result = run_external_gate(store, node.name,
                                       command=[sys.executable, "robot_final/verify_solver_metadata.py"])
            self.assertEqual(result["status"], "open")
            self.assertEqual(store.load().attempts[result["attempt_id"]].status, "target_gate_not_satisfied")
            action = next(a for a in next_actions(store) if a.get("node_id") == node.id)
            self.assertEqual(action["kind"], "decompose_external_obligation")

    def test_external_verified_flags_never_signal_final_completion(self):
        with tempfile.TemporaryDirectory() as directory:
            target, store = self.setup_target(directory)
            state = store.load()
            for node in state.nodes.values():
                node.status = NodeStatus.VERIFIED
                state.registry[node.id] = {"statement": node.statement}
            store.save(state)
            self.assertTrue(all(a["kind"] == "revalidate_external_evidence" for a in next_actions(store)))
            refresh_routeb_tracking(store)
            state = store.load()
            self.assertEqual(state.registry, {})
            self.assertTrue(all(n.status == NodeStatus.OPEN for n in state.nodes.values()))

    def test_refresh_same_path_hash_drift_invalidates_descendants_preserves_history(self):
        with tempfile.TemporaryDirectory() as directory:
            target, store = self.setup_target(directory)
            self.run_baseline(store)
            state = store.load()
            p0 = self.node(state, "P0")
            receipt = copy.deepcopy(p0.metadata["evidence_receipt"])
            p3 = self.node(state, "P3")
            p3.status = NodeStatus.EVIDENCE_COMPLETE
            p3.metadata["evidence_receipt"] = copy.deepcopy(receipt)
            store.save(state)
            attempts = copy.deepcopy(store.load().attempts)
            checker = target / "robot_final/verify_all.py"
            checker.write_text("# new checker\n", encoding="utf-8")
            result = refresh_routeb_tracking(store)
            state = store.load()
            self.assertIn(p0.name, result["reopened"])
            self.assertIn(p3.name, result["reopened"])
            self.assertEqual(state.attempts, attempts)
            self.assertIn(receipt, state.nodes[p0.id].metadata["previous_external_receipts"])
            self.assertEqual(state.nodes[p0.id].metadata["source_hashes"]["robot_final/verify_all.py"],
                             hashlib.sha256(checker.read_bytes()).hexdigest())
            self.assertTrue(all(n.status == NodeStatus.OPEN for n in state.nodes.values()))

    def test_baseline_inventory_tracks_child_checker_and_data_drift(self):
        for rel in ("robot_final/verify_interval_artifacts.py", "robot_final/routeB_interval_bounds.csv",
                    "robot_final/P3_INTERVAL_BOUNDS.md", "robot_final/cross_validation/routeB_reachability_full_dh_probe.csv"):
            with self.subTest(path=rel), tempfile.TemporaryDirectory() as directory:
                target, store = self.setup_target(directory)
                self.run_baseline(store)
                (target / rel).write_text("changed child input\n", encoding="utf-8")
                p0 = self.node(store.load(), "P0")
                self.assertIn(f"changed:{rel}", external_evidence_staleness(p0))
                self.assertEqual(next_actions(store)[0]["kind"], "revalidate_external_evidence")
                refresh_routeb_tracking(store)
                self.assertEqual(self.node(store.load(), "P0").status, NodeStatus.OPEN)

    def test_baseline_inventory_detects_new_inputs_in_both_directories(self):
        for folder in ("robot_final", "robot_final/cross_validation"):
            for suffix in (".py", ".jl", ".csv", ".md", ".toml", ".json", ".ps1", ".bat"):
                with self.subTest(folder=folder, suffix=suffix), tempfile.TemporaryDirectory() as directory:
                    target, store = self.setup_target(directory)
                    self.run_baseline(store)
                    rel = f"{folder}/new_input{suffix}"
                    (target / rel).write_text("new input\n", encoding="utf-8")
                    self.assertIn(f"changed:{rel}", external_evidence_staleness(self.node(store.load(), "P0")))
                    refresh_routeb_tracking(store)
                    p0 = self.node(store.load(), "P0")
                    self.assertEqual(p0.status, NodeStatus.OPEN)
                    self.assertIn(rel, p0.metadata["source_hashes"])

    def test_new_input_during_checker_is_a_rejected_scope_change(self):
        with tempfile.TemporaryDirectory() as directory:
            target, store = self.setup_target(directory)
            def create_input(*args, **kwargs):
                (target / "robot_final/new_input.csv").write_text("data\n", encoding="utf-8")
                return SimpleNamespace(stdout="ok\n", stderr="", returncode=0)
            with patch("percolation_workflow.external.subprocess.run", side_effect=create_input):
                result = self.run_baseline(store)
            state = store.load()
            receipt = self.node(state, "P0").metadata["last_external_receipt"]
            self.assertEqual(state.attempts[result["attempt_id"]].status, "source_drift_rejected")
            self.assertNotIn("robot_final/new_input.csv", receipt["source_hashes_before"])
            self.assertIn("robot_final/new_input.csv", receipt["source_hashes"])

    def test_baseline_inventory_includes_safe_exact_manifest_inputs_and_excludes_caches(self):
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "target"
            self.make_target(target)
            manifest = target / "robot_formal_v1/manifest.json"
            payload = json.loads(manifest.read_text(encoding="utf-8"))
            exact = "routeB_dense_Mq/nested/exact_input.bin"
            excluded = [".lake/cache.csv", "depot/input.csv", "robot_final/backups/old.csv",
                        "robot_final/cross_validation/archive/old.py", "robot_final/old_backup.csv",
                        "robot_final/old_archive.json"]
            for rel in [exact, *excluded]:
                path = target / rel
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text("fixture\n", encoding="utf-8")
            payload["artifacts"] = [{"path": rel} for rel in [exact, *excluded, "../escape.csv",
                                   "C:/outside.csv", "robot_final\\unsafe.csv", "robot_final/*.csv"]]
            manifest.write_text(json.dumps(payload), encoding="utf-8")
            store = StateStore(Path(directory) / "state.json")
            initialize_routeb_intake(target, store)
            self.assertEqual(self.run_baseline(store)["status"], "evidence_complete")
            p0 = self.node(store.load(), "P0")
            self.assertIn(exact, p0.metadata["source_hashes"])
            for rel in excluded:
                self.assertNotIn(rel, p0.metadata["artifact_paths"])
                (target / rel).write_text("ignored update\n", encoding="utf-8")
            self.assertEqual(external_evidence_staleness(p0), [])
            (target / exact).write_text("changed exact input\n", encoding="utf-8")
            self.assertIn(f"changed:{exact}", external_evidence_staleness(p0))

    def test_safe_missing_manifest_input_blocks_baseline(self):
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "target"
            self.make_target(target)
            manifest = target / "robot_formal_v1/manifest.json"
            payload = json.loads(manifest.read_text(encoding="utf-8"))
            payload["artifacts"] = [{"path": "routeB_dense_Mq/missing.csv"}]
            manifest.write_text(json.dumps(payload), encoding="utf-8")
            store = StateStore(Path(directory) / "state.json")
            initialize_routeb_intake(target, store)
            with patch("percolation_workflow.external.subprocess.run") as run:
                result = self.run_baseline(store)
                run.assert_not_called()
            self.assertEqual(result["status"], "open")
            self.assertEqual(store.load().attempts[result["attempt_id"]].status, "intake_drift_rejected")

    def test_refresh_migrates_mathematical_closure_without_rerunning_diagnostic(self):
        with tempfile.TemporaryDirectory() as directory:
            target, store = self.setup_target(directory)
            self.run_baseline(store)
            result = run_external_gate(store, "P1.bracket_decision",
                                       command=[sys.executable, "robot_final/verify_solver_metadata.py"])
            state = store.load()
            p1 = self.node(state, "P1")
            p1.status = NodeStatus.EVIDENCE_COMPLETE  # Legacy adapter's inappropriate closure.
            p1.metadata["claim_status"] = "checker_passed"
            p1.metadata["evidence_receipt"] = copy.deepcopy(p1.metadata["last_external_receipt"])
            p1.metadata.pop("closure_scope")
            store.save(state)
            attempts = copy.deepcopy(state.attempts)
            refresh_routeb_tracking(store)
            state = store.load()
            self.assertEqual(state.nodes[p1.id].status, NodeStatus.OPEN)
            self.assertEqual(state.nodes[p1.id].metadata["claim_status"], "unknown_needs_coverage")
            self.assertEqual(state.attempts, attempts)
            self.assertEqual(state.attempts[result["attempt_id"]].stdout, "UNKNOWN\n")
            self.assertEqual(next_actions(store)[0]["kind"], "decompose_external_obligation")
            self.assertEqual(refresh_routeb_tracking(store)["reopened"], [])

    def test_refresh_scope_expansion_reopens_and_reads_fresh_manifest(self):
        with tempfile.TemporaryDirectory() as directory:
            target, store = self.setup_target(directory)
            self.run_baseline(store)
            (target / "extra.txt").write_text("scope\n", encoding="utf-8")
            stages = copy.deepcopy(ROUTEB_STAGES)
            stages[0]["artifacts"].append("extra.txt")
            with patch("percolation_workflow.external.ROUTEB_STAGES", stages):
                refresh_routeb_tracking(store)
            state = store.load()
            self.assertEqual(self.node(state, "P0").status, NodeStatus.OPEN)
            self.assertIn("extra.txt", self.node(state, "P0").metadata["source_hashes"])
            (target / "robot_formal_v1/manifest.json").write_text(
                json.dumps({"current_gate": {"formal_certificate_allowed": True}}), encoding="utf-8")
            refresh_routeb_tracking(store)
            self.assertTrue(all(n.metadata["target_gate_snapshot"]["formal_certificate_allowed"]
                                for n in store.load().nodes.values()))

    def test_refresh_refuses_active_attempt_without_partial_save(self):
        with tempfile.TemporaryDirectory() as directory:
            target, store = self.setup_target(directory)
            state = store.load()
            state.begin_attempt(self.node(state, "P8").id, "running-descendant")
            store.save(state)
            before = store.path.read_bytes()
            (target / "PROJECT_REFORM_AUDIT.md").write_text("changed\n", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "in progress"):
                refresh_routeb_tracking(store)
            self.assertEqual(store.path.read_bytes(), before)

    def test_intake_drift_rejected_with_actual_before_snapshot(self):
        with tempfile.TemporaryDirectory() as directory:
            target, store = self.setup_target(directory)
            (target / "PROJECT_REFORM_AUDIT.md").write_text("changed before execution\n", encoding="utf-8")
            with patch("percolation_workflow.external.subprocess.run") as run:
                result = self.run_baseline(store)
                run.assert_not_called()
            state = store.load()
            receipt = self.node(state, "P0").metadata["last_external_receipt"]
            self.assertEqual(state.attempts[result["attempt_id"]].status, "intake_drift_rejected")
            self.assertEqual(receipt["source_hashes_before"], receipt["source_hashes"])
            self.assertNotEqual(receipt["source_hashes_before"], receipt["source_hashes_at_intake"])
            self.assertFalse(receipt["source_unchanged"])

    def test_timeout_bytes_are_decoded_and_attempt_finished(self):
        with tempfile.TemporaryDirectory() as directory:
            target, store = self.setup_target(directory)
            error = subprocess.TimeoutExpired("checker", 1, output="输出\n".encode(), stderr="诊断\n".encode() + b"\xff")
            with patch("percolation_workflow.external.subprocess.run", side_effect=error):
                result = self.run_baseline(store)
            state = store.load()
            attempt = state.attempts[result["attempt_id"]]
            self.assertEqual(attempt.status, "external_timeout")
            self.assertEqual(attempt.stdout, "输出\n")
            self.assertIn("诊断\n\ufffd", attempt.stderr)
            self.assertEqual(attempt.exit_code, 124)
            self.assertIsNotNone(attempt.finished_at)
            self.assertEqual(result["status"], "open")

    def test_manifest_errors_finish_attempt_fail_closed(self):
        for payload in (None, b"{bad json", b"\xff", b"[]", b'{"current_gate": true}'):
            with self.subTest(payload=payload), tempfile.TemporaryDirectory() as directory:
                target, store = self.setup_target(directory)
                def break_manifest(*args, **kwargs):
                    manifest = target / "robot_formal_v1/manifest.json"
                    if payload is None:
                        manifest.unlink()
                    else:
                        manifest.write_bytes(payload)
                    return SimpleNamespace(stdout="diagnostic passed\n", stderr="", returncode=0)
                with patch("percolation_workflow.external.subprocess.run", side_effect=break_manifest):
                    result = self.run_baseline(store)
                state = store.load()
                attempt = state.attempts[result["attempt_id"]]
                self.assertEqual(result["status"], "open")
                self.assertEqual(attempt.status, "target_manifest_error")
                self.assertIsNotNone(attempt.finished_at)
                self.assertEqual(attempt.stdout, "diagnostic passed\n")
                self.assertEqual(state.registry, {})

    def test_external_cannot_register_even_with_valid_looking_lean_receipt(self):
        with tempfile.TemporaryDirectory() as directory:
            target, store = self.setup_target(directory)
            state = store.load()
            node = self.node(state, "P0")
            attempt = state.begin_attempt(node.id, "checker")
            state.finish_attempt(attempt, status="passed", command=["lake", "build"], stdout="", stderr="", exit_code=0)
            receipt = {"attempt_id": attempt, "source_hashes": {"proof.lean": "hash"},
                       "source_digest": "digest", "statement_identity": {"name": node.name,
                       "statement_sha256": hashlib.sha256(node.statement.encode()).hexdigest()},
                       "comparator_command": ["comparator"], "comparator_stdout": "Your solution is okay!",
                       "manifest": state.manifest}
            node.metadata["registry_eligible"] = True
            with self.assertRaisesRegex(ValueError, "external research"):
                state._register_verified(node.id, "proof.lean", receipt=receipt)
            self.assertEqual(state.registry, {})


if __name__ == "__main__":
    unittest.main()
