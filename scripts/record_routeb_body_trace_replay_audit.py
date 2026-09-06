"""Attach the precise body-trace provenance obstruction audit."""
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
    assert state.revision == 141 and not state.registry
    base = ROOT / "artifacts/routeb_agent_body_trace_replay_20260906T075831Z"
    report = base / "AUDIT.md"
    manifest = base / "audit_manifest.json"
    patch = base / "minimal_patch_entry.diff"
    old_graph = ROOT / "artifacts/routeb_6dof/block45-obligations-v95.json"
    graph_path = ROOT / "artifacts/routeb_6dof/block45-obligations-v96.json"
    backup = ROOT / "artifacts/routeb_storage_checkpoint_20260905/state-before-revision142.json"
    for path in (report, manifest, patch, old_graph):
        assert path.is_file(), path
    assert not graph_path.exists() and not backup.exists()
    text = report.read_text(encoding="utf-8")
    assert "cannot strictly verify" in text.lower() or "cannot" in text.lower()
    assert "body" in text.lower() and "aggregate" in text.lower()
    data = json.loads(manifest.read_text(encoding="utf-8"))
    assert data

    graph = json.loads(old_graph.read_text(encoding="utf-8"))
    nodes = {node["id"]: node for node in graph["nodes"]}
    node_id = "B45-1_610_body_trace_binding_obstruction"
    node = nodes[node_id]
    node.setdefault("verification", {}).setdefault("replay_audits", []).append({
        "report": ref(report), "manifest": ref(manifest), "minimal_patch": ref(patch),
        "report_sha256": sha(report), "manifest_sha256": sha(manifest),
        "minimal_patch_sha256": sha(patch),
        "status": "AGGREGATE_BODY_ATTRIBUTION_LOST",
        "aggregate_sum_body": False, "registry_eligible": False,
        "formal_certificate_allowed": False,
    })
    node.setdefault("open_bridges", []).append(
        "instrument the exact Fourier generator before aggregation and export body-labelled terms with an exact gate"
    )
    graph.update(schema="routeb-proposed-proof-dag-v96", supersedes="block45-obligations-v95.json")
    graph["nodes"] = list(nodes.values())
    ids = set(nodes)
    for candidate in nodes.values():
        for dependency in candidate.get("dependencies", []):
            if dependency not in ids:
                raise ValueError(f"dangling dependency: {dependency}")
    shutil.copy2(store.path, backup)
    graph_path.write_text(json.dumps(graph, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    state.event(
        "routeb_body_trace_replay_audit_recorded", node_id=node_id, report=ref(report),
        manifest=ref(manifest), minimal_patch=ref(patch), report_sha256=sha(report),
        status="AGGREGATE_BODY_ATTRIBUTION_LOST", aggregate_sum_body=False,
        registry_promoted=False, formal_certificate_allowed=False,
        proposed_dag=ref(graph_path), broad_regression_run=False,
    )
    store.save(state)
    print({"revision": state.revision, "graph_nodes": len(nodes),
           "registry": len(state.registry), "formal_certificate_allowed": False})


if __name__ == "__main__":
    main()
