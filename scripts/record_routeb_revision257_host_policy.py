"""Persist host-cycle formalizable dispatch wiring and the retained fixture failure."""
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
    assert state.revision == 256 and not state.registry
    old = ROOT / "artifacts/routeb_6dof/block45-obligations-v210.json"
    new = ROOT / "artifacts/routeb_6dof/block45-obligations-v211.json"
    backup = ROOT / "artifacts/routeb_storage_checkpoint_20260907/state-before-revision257.json"
    gca = ROOT / "artifacts/task_GCA_existing_decomposition_fixture_failure_20260907"
    files = [gca / "REPORT.md", gca / "evidence.json",
             ROOT / "src/percolation_workflow/agent_bridge.py",
             ROOT / "src/percolation_workflow/host_cycle.py",
             ROOT / "src/percolation_workflow/cli.py",
             ROOT / "tests/test_agent_bridge.py",
             ROOT / "tests/test_host_cycle.py"]
    assert old.is_file() and not new.exists() and all(path.is_file() for path in files)
    evidence = json.loads((gca / "evidence.json").read_text(encoding="utf-8"))
    graph = json.loads(old.read_text(encoding="utf-8"))
    audits = [
        {
            "kind": "routeb_host_formalizable_lane_dispatch",
            "status": "FOCUSED_PATH_VERIFIED_FORMAL_GATE_UNCHANGED",
            "evidence_level": "host-cycle-and-cli-opt-in-policy",
            "semantic_boundary": (
                "prepare_requests, run_host_cycle and CLI prepare-agents/host-cycle "
                "now expose math_lane_policy=formalizable; default ordinary behavior "
                "is unchanged and numerical leaves are never promoted by this policy."
            ),
            "files": [ref(path) for path in files[2:]],
            "focused_tests": "1 host-cycle policy test + 3 bridge policy tests + 20 workflow tests passed",
            "registry_promoted": False,
            "formal_certificate_allowed": False,
        },
        {
            "kind": "routeb_existing_decomposition_fixture_obstruction",
            "status": evidence["status"],
            "evidence_level": "retained-focused-test-failure",
            "semantic_boundary": evidence["interpretation"],
            "sidecar": str(gca.resolve()),
            "files": [ref(path) for path in files[:2]],
            "failed_test": evidence["failed_test"],
            "error": evidence["error"],
            "registry_promoted": False,
            "formal_certificate_allowed": False,
        },
    ]
    graph.setdefault("bottleneck_audits", []).extend(audits)
    graph.setdefault("external_intakes", []).extend({
        "kind": audit["kind"], "source": "local-workflow-policy-and-fixture-audit",
        "sidecar": audit.get("sidecar"), "files": audit["files"],
        "registry_promoted": False, "formal_certificate_allowed": False,
    } for audit in audits)
    graph.setdefault("open_frontier_updates", []).extend({
        "node": audit["kind"], "status": "open_or_advisory_only",
        "reason": audit["semantic_boundary"],
    } for audit in audits)
    graph.update(schema="routeb-proposed-proof-dag-v211", supersedes=old.name)
    new.write_text(json.dumps(graph, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if not backup.exists():
        backup.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(store.path, backup)
    digest = sha(new)
    state.graph_artifacts.append({
        "schema_version": 1,
        "algorithm": "routeb_revision257_host_policy/v1",
        "graph_sha256": digest, "roots": [], "selected_nodes": [],
        "source": "local-formalizable-host-dispatch+GCA-fixture-audit",
        "evidence_sha256": sha(gca / "evidence.json"),
        "strict_compile": False, "registry_promoted": False,
        "formal_certificate_allowed": False,
    })
    state.event(
        "routeb_revision257_host_policy_recorded",
        proposed_dag=ref(new), proposed_dag_sha256=digest,
        audits=[{"kind": audit["kind"], "status": audit["status"]} for audit in audits],
        math_lane_policy="formalizable-opt-in", registry_promoted=False,
        formal_certificate_allowed=False, broad_regression_run=False,
    )
    store.save(state)
    print({"revision": state.revision, "graph": new.name, "registry": len(state.registry)})


if __name__ == "__main__":
    main()
