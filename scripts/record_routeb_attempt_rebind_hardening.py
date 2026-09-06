"""Persist immutable attempt-owner provenance hardening."""
import json
import shutil

from record_routeb_port_progress import ROOT, ref
from percolation_workflow.store import StateStore


def main():
    store = StateStore(ROOT / "artifacts/routeb_6dof/state.json")
    state = store.load()
    assert state.revision == 146 and not state.registry
    old_graph = ROOT / "artifacts/routeb_6dof/block45-obligations-v100.json"
    graph_path = ROOT / "artifacts/routeb_6dof/block45-obligations-v101.json"
    backup = ROOT / "artifacts/routeb_storage_checkpoint_20260905/state-before-revision147.json"
    assert old_graph.is_file()
    assert not graph_path.exists() and not backup.exists()
    graph = json.loads(old_graph.read_text(encoding="utf-8"))
    graph.setdefault("workflow_guards", {})["attempt_owner_provenance"] = {
        "started_record": "immutable_created_agent_id",
        "rebind": "append_only_state_event",
        "finished_record": "current_agent_id",
        "schema_compatible": True,
    }
    graph.update(schema="routeb-proposed-proof-dag-v101", supersedes="block45-obligations-v100.json")
    graph_path.write_text(json.dumps(graph, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    shutil.copy2(store.path, backup)
    state.event(
        "routeb_attempt_rebind_hardening_recorded",
        proposed_dag=ref(graph_path),
        started_record="immutable_created_agent_id",
        rebind="append_only_state_event", finished_record="current_agent_id",
        registry_promoted=False, formal_certificate_allowed=False,
        broad_regression_run=False,
    )
    store.save(state)
    print({"revision": state.revision, "graph_nodes": len(graph["nodes"]),
           "registry": len(state.registry), "formal_certificate_allowed": False})


if __name__ == "__main__":
    main()
