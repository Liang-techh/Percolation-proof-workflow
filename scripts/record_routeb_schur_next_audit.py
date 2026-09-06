"""Attach the exact Schur-residual audit and its scaling obstruction."""
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
    assert state.revision == 138 and not state.registry
    report = ROOT / "artifacts/routeb_agent_schur_next_20260906T015153/AUDIT.md"
    old_graph = ROOT / "artifacts/routeb_6dof/block45-obligations-v92.json"
    graph_path = ROOT / "artifacts/routeb_6dof/block45-obligations-v93.json"
    backup = ROOT / "artifacts/routeb_storage_checkpoint_20260905/state-before-revision139.json"
    for path in (report, old_graph):
        assert path.is_file(), path
    assert not graph_path.exists() and not backup.exists()
    text = report.read_text(encoding="utf-8")
    assert "7/18750" in text
    assert "7/60" in text and "不存在只依赖当前 PMI projection 坐标的有限" in text

    graph = json.loads(old_graph.read_text(encoding="utf-8"))
    nodes = {node["id"]: node for node in graph["nodes"]}
    node_id = "B45-5_kc_mismatch_and_mbd_obstruction"
    node = nodes[node_id]
    node.setdefault("verification", {}).setdefault("independent_audits", []).append({
        "report": ref(report), "report_sha256": sha(report),
        "status": "EXACT_RESIDUAL_ALGEBRA_WITH_MBD_SCALING_OBSTRUCTION",
        "rho_kc_squared_bound": "7/18750",
        "mbd_zero_e1": ["7/60", "-21/80000"],
        "remote_residual_scaling": "unbounded_under_lambda_e1_projection",
        "registry_eligible": False, "formal_certificate_allowed": False,
    })
    node.setdefault("open_bridges", []).append(
        "bind a_D to a bounded descriptor/flowpipe set before attempting Schur residual absorption"
    )
    graph.update(schema="routeb-proposed-proof-dag-v93", supersedes="block45-obligations-v92.json")
    graph["nodes"] = list(nodes.values())
    ids = set(nodes)
    for candidate in nodes.values():
        for dependency in candidate.get("dependencies", []):
            if dependency not in ids:
                raise ValueError(f"dangling dependency: {dependency}")
    shutil.copy2(store.path, backup)
    graph_path.write_text(json.dumps(graph, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    state.event(
        "routeb_schur_next_audit_recorded", node_id=node_id, report=ref(report),
        report_sha256=sha(report), rho_kc_squared_bound="7/18750",
        mbd_zero_e1=["7/60", "-21/80000"],
        remote_residual_scaling="unbounded_under_lambda_e1_projection",
        registry_promoted=False, formal_certificate_allowed=False,
        proposed_dag=ref(graph_path), broad_regression_run=False,
    )
    store.save(state)
    print({"revision": state.revision, "graph_nodes": len(nodes),
           "registry": len(state.registry), "formal_certificate_allowed": False})


if __name__ == "__main__":
    main()
