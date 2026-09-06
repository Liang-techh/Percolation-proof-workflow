"""Persist idempotent candidate-claim ingest hardening."""
import json
import shutil

from record_routeb_port_progress import ROOT, ref
from percolation_workflow.store import StateStore


def main():
    store = StateStore(ROOT / "artifacts/routeb_6dof/state.json")
    state = store.load()
    assert state.revision == 147 and not state.registry
    old_graph = ROOT / "artifacts/routeb_6dof/block45-obligations-v101.json"
    graph_path = ROOT / "artifacts/routeb_6dof/block45-obligations-v102.json"
    backup = ROOT / "artifacts/routeb_storage_checkpoint_20260905/state-before-revision148.json"
    assert old_graph.is_file()
    assert not graph_path.exists() and not backup.exists()
    graph = json.loads(old_graph.read_text(encoding="utf-8"))
    graph.setdefault("workflow_guards", {})["candidate_claim_idempotence"] = {
        "identity": ["event_id", "canonical_receipt_sha256"],
        "duplicate_claim_event": False,
        "raw_receipt_preserved": True,
        "registry_promotion": False,
    }
    graph.update(schema="routeb-proposed-proof-dag-v102", supersedes="block45-obligations-v101.json")
    graph_path.write_text(json.dumps(graph, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    shutil.copy2(store.path, backup)
    state.event(
        "routeb_candidate_claim_idempotence_recorded",
        proposed_dag=ref(graph_path),
        identity=["event_id", "canonical_receipt_sha256"],
        duplicate_claim_event=False, registry_promoted=False,
        formal_certificate_allowed=False, broad_regression_run=False,
    )
    store.save(state)
    print({"revision": state.revision, "graph_nodes": len(graph["nodes"]),
           "registry": len(state.registry), "formal_certificate_allowed": False})


if __name__ == "__main__":
    main()
