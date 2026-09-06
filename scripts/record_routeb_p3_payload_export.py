"""Attach the current-source single-cell P3 payload export."""
import hashlib
import json
import shutil
from decimal import Decimal

from record_routeb_port_progress import ROOT, ref
from percolation_workflow.store import StateStore


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    store = StateStore(ROOT / "artifacts/routeb_6dof/state.json")
    state = store.load()
    assert state.revision == 151 and not state.registry
    base = ROOT / "artifacts/routeb_agent_p3_payload_export_20260906T021457"
    report = base / "REPORT.md"
    payload = base / "payload_cell_1.json"
    branch = base / "branch_cell_1.csv"
    checker = base / "check_payload.py"
    run_report = base / "branch_run_report.md"
    old_graph = ROOT / "artifacts/routeb_6dof/block45-obligations-v105.json"
    graph_path = ROOT / "artifacts/routeb_6dof/block45-obligations-v106.json"
    backup = ROOT / "artifacts/routeb_storage_checkpoint_20260905/state-before-revision152.json"
    for path in (report, payload, branch, checker, run_report, old_graph):
        assert path.is_file(), path
    assert not graph_path.exists() and not backup.exists()
    text = report.read_text(encoding="utf-8")
    assert "payload_status=OK" in text
    assert "kappa = 5030" in text
    assert "P3_CELL_PAYLOAD_STRUCTURE_OK" in text
    data = json.loads(payload.read_text(encoding="utf-8"))
    assert data
    assert data.get("cell_id") == 1
    assert Decimal(str(data.get("kappa"))) > 1

    graph = json.loads(old_graph.read_text(encoding="utf-8"))
    nodes = {node["id"]: node for node in graph["nodes"]}
    node_id = "B45-P3_global_coverage_interval_interface"
    node = nodes[node_id]
    node.setdefault("verification", {}).setdefault("current_source_payloads", []).append({
        "report": ref(report), "payload": ref(payload), "branch": ref(branch),
        "checker": ref(checker), "run_report": ref(run_report),
        "report_sha256": sha(report), "payload_sha256": sha(payload),
        "branch_sha256": sha(branch), "checker_sha256": sha(checker),
        "run_report_sha256": sha(run_report), "cell_id": 1,
        "payload_structure_replay": True, "kappa": str(data.get("kappa")),
        "inverse_guard": "UNKNOWN_INVERSE", "status": "PAYLOAD_COMPLETE_GUARD_FAIL",
        "registry_eligible": False, "formal_certificate_allowed": False,
    })
    node.setdefault("open_bridges", []).extend([
        "tighten current-source cell 1 enclosure or subdivide until kappa < 1",
        "repeat payload capture for all remaining cells before global inverse coverage"
    ])
    graph.update(schema="routeb-proposed-proof-dag-v106", supersedes="block45-obligations-v105.json")
    graph["nodes"] = list(nodes.values())
    ids = set(nodes)
    for candidate in nodes.values():
        for dependency in candidate.get("dependencies", []):
            if dependency not in ids:
                raise ValueError(f"dangling dependency: {dependency}")
    shutil.copy2(store.path, backup)
    graph_path.write_text(json.dumps(graph, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    state.event(
        "routeb_p3_current_source_payload_recorded", node_id=node_id,
        report=ref(report), payload=ref(payload), branch=ref(branch),
        report_sha256=sha(report), payload_sha256=sha(payload), cell_id=1,
        payload_structure_replay=True, kappa=str(data.get("kappa")),
        inverse_guard="UNKNOWN_INVERSE", status="PAYLOAD_COMPLETE_GUARD_FAIL",
        registry_promoted=False, formal_certificate_allowed=False,
        proposed_dag=ref(graph_path), broad_regression_run=False,
    )
    store.save(state)
    print({"revision": state.revision, "graph_nodes": len(nodes),
           "registry": len(state.registry), "formal_certificate_allowed": False})


if __name__ == "__main__":
    main()
