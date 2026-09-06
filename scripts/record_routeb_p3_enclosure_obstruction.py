"""Record the current P3 enclosure-tightening negative audit."""
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
    assert state.revision == 156 and not state.registry
    base = ROOT / "artifacts/routeb_agent_p3_enclosure_tighten_20260906T082609Z"
    report = base / "REPORT.md"
    hashes = base / "SOURCE_HASHES.txt"
    old_graph = ROOT / "artifacts/routeb_6dof/block45-obligations-v110.json"
    graph_path = ROOT / "artifacts/routeb_6dof/block45-obligations-v111.json"
    backup = ROOT / "artifacts/routeb_storage_checkpoint_20260905/state-before-revision157.json"
    for path in (report, hashes, old_graph):
        assert path.is_file(), path
    assert not graph_path.exists() and not backup.exists()
    text = report.read_text(encoding="utf-8")
    assert "5030.70" in text and "meanvalue" in text and "UNKNOWN_INVERSE" in text
    graph = json.loads(old_graph.read_text(encoding="utf-8"))
    nodes = {node["id"]: node for node in graph["nodes"]}
    node_id = "B45-P3_global_coverage_interval_interface"
    node = nodes[node_id]
    node.setdefault("verification", {}).setdefault("enclosure_audits", []).append({
        "report": ref(report), "source_hashes": ref(hashes),
        "report_sha256": sha(report), "source_hashes_sha256": sha(hashes),
        "root_cell_id": 1,
        "variants": {
            "natural_natural_fd": "5030.7000334738",
            "meanvalue_natural_fd": "169944.9080913834",
            "taylor2_natural_fd": "2241881.7700890",
            "natural_meanvalue_fd": "5030.7000334738",
        },
        "status": "ENCLOSURE_TIGHTENING_GUARD_FAIL",
        "best_direction": "meanvalue_fd_CG_dependency_reduction",
        "inverse_guard": "UNKNOWN_INVERSE",
        "registry_eligible": False, "formal_certificate_allowed": False,
    })
    node.setdefault("open_bridges", []).extend([
        "prove a dependency-aware M(q) enclosure with positive weighted inverse contraction",
        "retain meanvalue_fd as a candidate only after the mass inverse guard closes",
    ])
    graph.update(schema="routeb-proposed-proof-dag-v111", supersedes="block45-obligations-v110.json")
    graph["nodes"] = list(nodes.values())
    ids = set(nodes)
    for candidate in nodes.values():
        for dependency in candidate.get("dependencies", []):
            if dependency not in ids:
                raise ValueError(f"dangling dependency: {dependency}")
    shutil.copy2(store.path, backup)
    graph_path.write_text(json.dumps(graph, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    state.event(
        "routeb_p3_enclosure_obstruction_recorded", node_id=node_id,
        report=ref(report), source_hashes=ref(hashes), report_sha256=sha(report),
        source_hashes_sha256=sha(hashes), root_cell_id=1,
        variants={"natural_natural_fd":"5030.7000334738",
                  "meanvalue_natural_fd":"169944.9080913834",
                  "taylor2_natural_fd":"2241881.7700890",
                  "natural_meanvalue_fd":"5030.7000334738"},
        status="ENCLOSURE_TIGHTENING_GUARD_FAIL",
        best_direction="meanvalue_fd_CG_dependency_reduction", inverse_guard="UNKNOWN_INVERSE",
        registry_promoted=False, formal_certificate_allowed=False,
        proposed_dag=ref(graph_path), broad_regression_run=False,
    )
    store.save(state)
    print({"revision": state.revision, "graph_nodes": len(nodes),
           "registry": len(state.registry), "formal_certificate_allowed": False})


if __name__ == "__main__":
    main()
