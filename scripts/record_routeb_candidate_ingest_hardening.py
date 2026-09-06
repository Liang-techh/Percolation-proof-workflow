"""Persist the candidate-claim ingest and compiled-candidate stage boundary."""
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
    assert state.revision == 140 and not state.registry
    design = ROOT / "artifacts/routeb_agent_candidate_ingest_design_20260906T074923Z/DESIGN.md"
    old_graph = ROOT / "artifacts/routeb_6dof/block45-obligations-v94.json"
    graph_path = ROOT / "artifacts/routeb_6dof/block45-obligations-v95.json"
    backup = ROOT / "artifacts/routeb_storage_checkpoint_20260905/state-before-revision141.json"
    for path in (design, old_graph):
        assert path.is_file(), path
    assert not graph_path.exists() and not backup.exists()
    text = design.read_text(encoding="utf-8")
    assert "candidate_ingest" in text and "registry_status=pending" in text
    assert "collect_candidate(ok=true" in text and "coordinator" in text

    graph = json.loads(old_graph.read_text(encoding="utf-8"))
    graph.setdefault("workflow_guards", {})["candidate_receipt_ingest"] = {
        "design": ref(design),
        "design_sha256": sha(design),
        "callback_receipt": "untrusted_claim_preserved_with_canonical_digest",
        "compile_success_transition": "evidence_stage=compiled_candidate",
        "comparator_status": "pending",
        "registry_status": "pending",
        "registry_direct_from_callback": False,
        "registry_direct_from_compiled_candidate": False,
    }
    graph.update(schema="routeb-proposed-proof-dag-v95", supersedes="block45-obligations-v94.json")
    shutil.copy2(store.path, backup)
    graph_path.write_text(json.dumps(graph, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    state.event(
        "routeb_candidate_ingest_hardening_recorded",
        design=ref(design), design_sha256=sha(design),
        callback_receipt="untrusted_claim_preserved_with_canonical_digest",
        compile_success_transition="evidence_stage=compiled_candidate",
        comparator_status="pending", registry_status="pending",
        registry_promoted=False, formal_certificate_allowed=False,
        proposed_dag=ref(graph_path), broad_regression_run=False,
    )
    store.save(state)
    print({"revision": state.revision, "graph_nodes": len(graph["nodes"]),
           "registry": len(state.registry), "formal_certificate_allowed": False})


if __name__ == "__main__":
    main()
