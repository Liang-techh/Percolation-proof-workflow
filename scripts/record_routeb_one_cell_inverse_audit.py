"""Attach the negative one-cell inverse witness attempt to P3."""
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
    assert state.revision == 142 and not state.registry
    base = ROOT / "artifacts/routeb_agent_one_cell_inverse_20260906T015908Z"
    report, attempt, inputs = (base / name for name in ("REPORT.md", "attempt.json", "INPUTS.md"))
    old_graph = ROOT / "artifacts/routeb_6dof/block45-obligations-v96.json"
    graph_path = ROOT / "artifacts/routeb_6dof/block45-obligations-v97.json"
    backup = ROOT / "artifacts/routeb_storage_checkpoint_20260905/state-before-revision143.json"
    for path in (report, attempt, inputs, old_graph):
        assert path.is_file(), path
    assert not graph_path.exists() and not backup.exists()
    text = report.read_text(encoding="utf-8")
    assert "未能构造" in text and "cell_id=1" in text
    data = json.loads(attempt.read_text(encoding="utf-8"))
    assert data

    graph = json.loads(old_graph.read_text(encoding="utf-8"))
    nodes = {node["id"]: node for node in graph["nodes"]}
    node_id = "B45-P3_global_coverage_interval_interface"
    node = nodes[node_id]
    node.setdefault("verification", {}).setdefault("single_cell_attempts", []).append({
        "report": ref(report), "attempt": ref(attempt), "inputs": ref(inputs),
        "report_sha256": sha(report), "attempt_sha256": sha(attempt),
        "inputs_sha256": sha(inputs), "cell_id": 1,
        "status": "CURRENT_AUTHORITATIVE_EXACT_WITNESS_NOT_CONSTRUCTED",
        "missing_payload": ["box_lo", "box_hi", "A0", "R", "X", "C", "weights",
                            "exact_kappa", "rhs_center", "rhs_radius"],
        "registry_eligible": False, "formal_certificate_allowed": False,
    })
    node.setdefault("open_bridges", []).append(
        "extend authoritative branch exporter with cell-indexed exact inverse payload before replay"
    )
    graph.update(schema="routeb-proposed-proof-dag-v97", supersedes="block45-obligations-v96.json")
    graph["nodes"] = list(nodes.values())
    ids = set(nodes)
    for candidate in nodes.values():
        for dependency in candidate.get("dependencies", []):
            if dependency not in ids:
                raise ValueError(f"dangling dependency: {dependency}")
    shutil.copy2(store.path, backup)
    graph_path.write_text(json.dumps(graph, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    state.event(
        "routeb_one_cell_inverse_audit_recorded", node_id=node_id, report=ref(report),
        attempt=ref(attempt), cell_id=1,
        status="CURRENT_AUTHORITATIVE_EXACT_WITNESS_NOT_CONSTRUCTED",
        registry_promoted=False, formal_certificate_allowed=False,
        proposed_dag=ref(graph_path), broad_regression_run=False,
    )
    store.save(state)
    print({"revision": state.revision, "graph_nodes": len(nodes),
           "registry": len(state.registry), "formal_certificate_allowed": False})


if __name__ == "__main__":
    main()
