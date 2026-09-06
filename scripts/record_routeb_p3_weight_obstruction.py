"""Record the exact positive-weight obstruction for the current P3 cell."""
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
    assert state.revision == 153 and not state.registry
    base = ROOT / "artifacts/routeb_agent_p3_weight_opt_20260906T022409"
    report = base / "REPORT.md"
    payload = ROOT / "artifacts/routeb_agent_p3_payload_export_20260906T021457/payload_cell_1.json"
    old_graph = ROOT / "artifacts/routeb_6dof/block45-obligations-v107.json"
    graph_path = ROOT / "artifacts/routeb_6dof/block45-obligations-v108.json"
    backup = ROOT / "artifacts/routeb_storage_checkpoint_20260905/state-before-revision154.json"
    for path in (report, payload, old_graph):
        assert path.is_file(), path
    assert not graph_path.exists() and not backup.exists()
    text = report.read_text(encoding="utf-8")
    assert "5030.700033473802428" in text
    assert "rho(C)" in text
    assert "UNKNOWN_INVERSE" in text
    data = json.loads(payload.read_text(encoding="utf-8"))
    assert data["cell_id"] == 1
    graph = json.loads(old_graph.read_text(encoding="utf-8"))
    nodes = {node["id"]: node for node in graph["nodes"]}
    node_id = "B45-P3_global_coverage_interval_interface"
    node = nodes[node_id]
    node.setdefault("verification", {}).setdefault("weight_optimizations", []).append({
        "report": ref(report), "payload": ref(payload),
        "report_sha256": sha(report), "payload_sha256": sha(payload),
        "cell_id": 1,
        "current_kappa": "5030.700033473802584308492823253492590316756326455871492021679959...",
        "rho_lower_bound": "5030.700033473802428168252520321128391430042402637811382084946186...",
        "max_absolute_improvement": "1.56140240302932364198886713924e-13",
        "required_R_shrink_factor": "5030.700033473802428...",
        "status": "EXACT_POSITIVE_WEIGHT_OBSTRUCTION",
        "inverse_guard": "UNKNOWN_INVERSE",
        "registry_eligible": False, "formal_certificate_allowed": False,
    })
    node.setdefault("open_bridges", []).extend([
        "do not spend further effort on positive diagonal weights for cell 1",
        "tighten R through dependency-aware enclosure, Taylor/mean-value bounds, or cell subdivision",
    ])
    graph.update(schema="routeb-proposed-proof-dag-v108", supersedes="block45-obligations-v107.json")
    graph["nodes"] = list(nodes.values())
    ids = set(nodes)
    for candidate in nodes.values():
        for dependency in candidate.get("dependencies", []):
            if dependency not in ids:
                raise ValueError(f"dangling dependency: {dependency}")
    shutil.copy2(store.path, backup)
    graph_path.write_text(json.dumps(graph, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    state.event(
        "routeb_p3_weight_obstruction_recorded", node_id=node_id,
        report=ref(report), payload=ref(payload), report_sha256=sha(report),
        payload_sha256=sha(payload), cell_id=1,
        current_kappa="5030.700033473802584...",
        rho_lower_bound="5030.700033473802428...",
        max_absolute_improvement="1.56140240302932364198886713924e-13",
        required_R_shrink_factor="5030.700033473802428...",
        status="EXACT_POSITIVE_WEIGHT_OBSTRUCTION", inverse_guard="UNKNOWN_INVERSE",
        registry_promoted=False, formal_certificate_allowed=False,
        proposed_dag=ref(graph_path), broad_regression_run=False,
    )
    store.save(state)
    print({"revision": state.revision, "graph_nodes": len(nodes),
           "registry": len(state.registry), "formal_certificate_allowed": False})


if __name__ == "__main__":
    main()
