"""Persist the coordinator-owned post-compile cascade and resumable promotion."""
from __future__ import annotations

import hashlib
import json
import shutil
from pathlib import Path

from record_routeb_port_progress import ROOT, ref
from percolation_workflow.store import StateStore


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    store = StateStore(ROOT / "artifacts/routeb_6dof/state.json")
    state = store.load()
    assert state.revision == 276 and not state.registry
    old = ROOT / "artifacts/routeb_6dof/block45-obligations-v230.json"
    new = ROOT / "artifacts/routeb_6dof/block45-obligations-v231.json"
    backup = ROOT / "artifacts/routeb_storage_checkpoint_20260907/state-before-revision277.json"
    report = ROOT / "artifacts/task_GDB_repair_registry_gap_20260907/report.md"
    receipt = ROOT / "artifacts/task_GDB_repair_registry_gap_20260907/receipt.json"
    host = ROOT / "src/percolation_workflow/host_cycle.py"
    cli = ROOT / "src/percolation_workflow/cli.py"
    test = ROOT / "tests/test_host_cycle.py"
    assert old.is_file() and not new.exists() and all(path.is_file() for path in (report, receipt, host, cli, test))
    graph = json.loads(old.read_text(encoding="utf-8"))
    audit = {
        "kind": "host_cycle_coordinator_promotion_and_resume",
        "status": "IMPLEMENTED_FAIL_CLOSED",
        "evidence_level": "source-patch-plus-eight-focused-host-tests",
        "files": [ref(path) for path in (report, receipt, host, cli, test)],
        "source_sha256": {path.name: sha(path) for path in (host, cli, test)},
        "required_gates": [
            "explicit coordinator comparator command",
            "candidate.verification.requested=true",
            "verify_and_register",
            "repeat close_verified_reductions until fixed point",
        ],
        "untrusted_callback_command_rejected": True,
        "compile_success_alone_promotes": False,
        "checked_checkpoint_resumes": True,
        "registry_promoted": False,
        "formal_certificate_allowed": False,
        "semantic_boundary": "The bridge closes workflow control flow only; trusted verification, comparator acceptance, source freshness and physical Route-B premises remain mandatory.",
    }
    graph.setdefault("workflow_repairs", []).append(audit)
    graph.setdefault("open_frontier_updates", []).append({
        "node": audit["kind"], "status": "control_path_closed_trusted_gates_open",
        "reason": audit["semantic_boundary"],
    })
    graph.update(schema="routeb-proposed-proof-dag-v231", supersedes=old.name)
    new.write_text(json.dumps(graph, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if not backup.exists():
        backup.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(store.path, backup)
    digest = sha(new)
    state.graph_artifacts.append({
        "schema_version": 1, "algorithm": "routeb_revision277_host_cascade_resume/v1",
        "graph_sha256": digest, "roots": [], "selected_nodes": [],
        "source": "src/percolation_workflow/host_cycle.py",
        "evidence_sha256": sha(receipt), "strict_compile": True,
        "registry_promoted": False, "formal_certificate_allowed": False,
    })
    state.event("routeb_revision277_host_cascade_resume_recorded",
                proposed_dag=ref(new), proposed_dag_sha256=digest,
                host_promotion_bridge=True, checked_candidate_resume=True,
                comparator_command_is_coordinator_owned=True,
                parent_reduction_fixed_point=True, registry_promoted=False,
                formal_certificate_allowed=False, broad_regression_run=False)
    store.save(state)
    print(json.dumps({"revision": state.revision, "graph": new.name, "registry": len(state.registry)}))


if __name__ == "__main__":
    main()
