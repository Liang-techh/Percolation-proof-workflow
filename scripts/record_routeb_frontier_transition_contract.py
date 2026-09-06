"""Persist the explicit fail-closed frontier transition contract."""
import hashlib
import json
import shutil

from record_routeb_port_progress import ROOT, ref
from percolation_workflow.store import StateStore


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    store = StateStore(ROOT / "artifacts/routeb_6dof/state.json")
    state = store.load()
    assert state.revision == 148 and not state.registry
    report = ROOT / "artifacts/routeb_agent_frontier_transition_next_20260906T081225Z/REPORT.md"
    old_graph = ROOT / "artifacts/routeb_6dof/block45-obligations-v102.json"
    graph_path = ROOT / "artifacts/routeb_6dof/block45-obligations-v103.json"
    backup = ROOT / "artifacts/routeb_storage_checkpoint_20260905/state-before-revision149.json"
    for path in (report, old_graph):
        assert path.is_file(), path
    assert not graph_path.exists() and not backup.exists()
    text = report.read_text(encoding="utf-8")
    assert "scheduler" in text.lower() and "candidate" in text.lower()
    assert "fail-closed" in text.lower()

    graph = json.loads(old_graph.read_text(encoding="utf-8"))
    graph.setdefault("workflow_guards", {})["frontier_transition_contract"] = {
        "artifact_auto_discovery": False,
        "candidate_intake": "explicit_callback_only",
        "compiled_candidate_transition": "coordinator_compile_success_only",
        "registry_transition": "comparator_and_lean_admission_only",
        "audit": ref(report),
        "audit_sha256": sha(report),
    }
    graph.update(schema="routeb-proposed-proof-dag-v103", supersedes="block45-obligations-v102.json")
    graph_path.write_text(json.dumps(graph, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    shutil.copy2(store.path, backup)
    state.event(
        "routeb_frontier_transition_contract_recorded",
        audit=ref(report), audit_sha256=sha(report), artifact_auto_discovery=False,
        candidate_intake="explicit_callback_only",
        compiled_candidate_transition="coordinator_compile_success_only",
        registry_promoted=False, formal_certificate_allowed=False,
        proposed_dag=ref(graph_path), broad_regression_run=False,
    )
    store.save(state)
    print({"revision": state.revision, "graph_nodes": len(graph["nodes"]),
           "registry": len(state.registry), "formal_certificate_allowed": False})


if __name__ == "__main__":
    main()
