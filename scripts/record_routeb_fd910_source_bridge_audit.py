"""Attach the negative FD-9/10 source-bridge audit."""
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
    assert state.revision == 139 and not state.registry
    report = ROOT / "artifacts/routeb_agent_fd910_source_bridge_20260906T015120Z/AUDIT.md"
    old_graph = ROOT / "artifacts/routeb_6dof/block45-obligations-v93.json"
    graph_path = ROOT / "artifacts/routeb_6dof/block45-obligations-v94.json"
    backup = ROOT / "artifacts/routeb_storage_checkpoint_20260905/state-before-revision140.json"
    for path in (report, old_graph):
        assert path.is_file(), path
    assert not graph_path.exists() and not backup.exists()
    text = report.read_text(encoding="utf-8")
    assert "Do not promote" in text
    assert "No existing artifact proves" in text
    assert "Float64" in text

    graph = json.loads(old_graph.read_text(encoding="utf-8"))
    nodes = {node["id"]: node for node in graph["nodes"]}
    node_id = "B45-FD-9_10_float64_potential_contraction_seam"
    node = nodes[node_id]
    node.setdefault("verification", {}).setdefault("source_bridge_audits", []).append({
        "report": ref(report), "report_sha256": sha(report),
        "status": "SOURCE_EQUALITY_NOT_FOUND",
        "comparator_pending": True, "qpoly_terminal_comparator": False,
        "registry_eligible": False, "formal_certificate_allowed": False,
    })
    node.setdefault("open_bridges", []).extend([
        "provide pinned Float64 potential samples and FD gradient enclosures for all declared q,k",
        "bind full six-dimensional C*dq contraction and rounding semantics to the exact-real seam",
    ])
    graph.update(schema="routeb-proposed-proof-dag-v94", supersedes="block45-obligations-v93.json")
    graph["nodes"] = list(nodes.values())
    ids = set(nodes)
    for candidate in nodes.values():
        for dependency in candidate.get("dependencies", []):
            if dependency not in ids:
                raise ValueError(f"dangling dependency: {dependency}")
    shutil.copy2(store.path, backup)
    graph_path.write_text(json.dumps(graph, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    state.event(
        "routeb_fd910_source_bridge_audit_recorded", node_id=node_id, report=ref(report),
        report_sha256=sha(report), status="SOURCE_EQUALITY_NOT_FOUND",
        comparator_pending=True, qpoly_terminal_comparator=False,
        registry_promoted=False, formal_certificate_allowed=False,
        proposed_dag=ref(graph_path), broad_regression_run=False,
    )
    store.save(state)
    print({"revision": state.revision, "graph_nodes": len(nodes),
           "registry": len(state.registry), "formal_certificate_allowed": False})


if __name__ == "__main__":
    main()
