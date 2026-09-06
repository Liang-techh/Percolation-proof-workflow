"""Record the bounded P3 subdivision negative result."""
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
    assert state.revision == 155 and not state.registry
    base = ROOT / "artifacts/routeb_agent_p3_child_cell_20260906T022240"
    report = base / "REPORT.md"
    manifest = base / "manifest.json"
    payload = base / "child_payload_id16.json"
    frontier = base / "child_frontier_depth4.csv"
    old_graph = ROOT / "artifacts/routeb_6dof/block45-obligations-v109.json"
    graph_path = ROOT / "artifacts/routeb_6dof/block45-obligations-v110.json"
    backup = ROOT / "artifacts/routeb_storage_checkpoint_20260905/state-before-revision156.json"
    for path in (report, manifest, payload, frontier, old_graph):
        assert path.is_file(), path
    assert not graph_path.exists() and not backup.exists()
    data = json.loads(manifest.read_text(encoding="utf-8"))
    final = data["final_candidate"]
    assert data["verification"]["checker_result"] == "P3_CHILD_PAYLOAD_REPLAY_OK"
    assert data["verification"]["coverage_complete"] is False
    assert final["cell_id"] == 16 and final["kappa"].startswith("30.236595751457")
    graph = json.loads(old_graph.read_text(encoding="utf-8"))
    nodes = {node["id"]: node for node in graph["nodes"]}
    node_id = "B45-P3_global_coverage_interval_interface"
    node = nodes[node_id]
    node.setdefault("verification", {}).setdefault("subdivision_audits", []).append({
        "report": ref(report), "manifest": ref(manifest), "payload": ref(payload),
        "frontier": ref(frontier), "report_sha256": sha(report),
        "manifest_sha256": sha(manifest), "payload_sha256": sha(payload),
        "frontier_sha256": sha(frontier), "root_cell_id": 1, "final_cell_id": 16,
        "depth": 4, "max_nodes": 31,
        "min_kappa": "30.236595751457012087343219612768937246684897651...",
        "status": "BOUNDED_SUBDIVISION_GUARD_FAIL",
        "inverse_guard": "UNKNOWN_DOMAIN_BOUNDARY", "coverage_complete": False,
        "registry_eligible": False, "formal_certificate_allowed": False,
    })
    node.setdefault("open_bridges", []).extend([
        "continue subdivision only with explicit sibling coverage accounting",
        "close exact-rational and independent interval/DH semantic binding before treating child kappa as a theorem witness",
    ])
    graph.update(schema="routeb-proposed-proof-dag-v110", supersedes="block45-obligations-v109.json")
    graph["nodes"] = list(nodes.values())
    ids = set(nodes)
    for candidate in nodes.values():
        for dependency in candidate.get("dependencies", []):
            if dependency not in ids:
                raise ValueError(f"dangling dependency: {dependency}")
    shutil.copy2(store.path, backup)
    graph_path.write_text(json.dumps(graph, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    state.event(
        "routeb_p3_child_subdivision_recorded", node_id=node_id,
        report=ref(report), manifest=ref(manifest), payload=ref(payload), frontier=ref(frontier),
        report_sha256=sha(report), manifest_sha256=sha(manifest), payload_sha256=sha(payload),
        frontier_sha256=sha(frontier), root_cell_id=1, final_cell_id=16, depth=4, max_nodes=31,
        min_kappa="30.236595751457012087343219612768937246684897651...",
        status="BOUNDED_SUBDIVISION_GUARD_FAIL", inverse_guard="UNKNOWN_DOMAIN_BOUNDARY",
        coverage_complete=False, registry_promoted=False, formal_certificate_allowed=False,
        proposed_dag=ref(graph_path), broad_regression_run=False,
    )
    store.save(state)
    print({"revision": state.revision, "graph_nodes": len(nodes),
           "registry": len(state.registry), "formal_certificate_allowed": False})


if __name__ == "__main__":
    main()
