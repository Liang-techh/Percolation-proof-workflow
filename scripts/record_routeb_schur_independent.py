"""Record the independent conditional B45 Schur remote-term audit."""
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
    assert state.revision == 158 and not state.registry
    base = ROOT / "artifacts/routeb_agent_schur_independent_20260906T083822Z"
    report = base / "AUDIT.md"
    numbers = base / "NUMBERS.json"
    old_graph = ROOT / "artifacts/routeb_6dof/block45-obligations-v112.json"
    graph_path = ROOT / "artifacts/routeb_6dof/block45-obligations-v113.json"
    backup = ROOT / "artifacts/routeb_storage_checkpoint_20260905/state-before-revision159.json"
    for path in (report, numbers, old_graph):
        assert path.is_file(), path
    assert not graph_path.exists() and not backup.exists()
    data = json.loads(numbers.read_text(encoding="utf-8"))
    assert data["formal_certificate_allowed"] is False
    assert data["registry_promoted"] is False
    graph = json.loads(old_graph.read_text(encoding="utf-8"))
    nodes = {node["id"]: node for node in graph["nodes"]}
    node_id = "B45-5_kc_mismatch_and_mbd_obstruction"
    node = nodes[node_id]
    node.setdefault("verification", {}).setdefault("independent_schur_audits", []).append({
        "report": ref(report), "numbers": ref(numbers), "report_sha256": sha(report),
        "numbers_sha256": sha(numbers), "partition": {"B": [4, 5], "D": [1, 2, 3, 6]},
        "status": "CONDITIONAL_EXACT_FULLSTATE_REMOTE_BOUND",
        "aD_infinity_bound": data["aD_infinity_bound"],
        "gammaRemote": data["gammaRemote"], "gammaSchur32": data["gammaSchur32"],
        "projection_obstruction": True, "deployed_float64_bound": False,
        "target_budget_absorbed": False, "registry_eligible": False,
        "formal_certificate_allowed": False,
    })
    node.setdefault("closed_subclaims", []).extend([
        "the block remote term is M_BD a_D and cannot be replaced by (M-M0)_BD a_D",
        "q=0 exact projection witnesses nonzero constant remote coupling",
        "conditional full-state exact-rational a_D and remote Schur bounds are finite",
    ])
    node.setdefault("open_bridges", []).extend([
        "bind ideal Fourier/central-FD mirror to deployed Julia Float64 with one explicit remainder",
        "prove full-state cover and first-exit continuation supplying dq/a_D premises",
        "replace the conservative gammaSchur32 bound or show sharp per-cell residual absorption",
    ])
    graph.update(schema="routeb-proposed-proof-dag-v113", supersedes="block45-obligations-v112.json")
    graph["nodes"] = list(nodes.values())
    ids = set(nodes)
    for candidate in nodes.values():
        for dependency in candidate.get("dependencies", []):
            if dependency not in ids:
                raise ValueError(f"dangling dependency: {dependency}")
    shutil.copy2(store.path, backup)
    graph_path.write_text(json.dumps(graph, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    state.event(
        "routeb_schur_independent_recorded", node_id=node_id, report=ref(report), numbers=ref(numbers),
        report_sha256=sha(report), numbers_sha256=sha(numbers), partition={"B":[4,5],"D":[1,2,3,6]},
        status="CONDITIONAL_EXACT_FULLSTATE_REMOTE_BOUND", aD_infinity_bound=data["aD_infinity_bound"],
        gammaRemote=data["gammaRemote"], gammaSchur32=data["gammaSchur32"],
        projection_obstruction=True, deployed_float64_bound=False, target_budget_absorbed=False,
        registry_promoted=False, formal_certificate_allowed=False, proposed_dag=ref(graph_path),
        broad_regression_run=False,
    )
    store.save(state)
    print({"revision": state.revision, "graph_nodes": len(nodes),
           "registry": len(state.registry), "formal_certificate_allowed": False})


if __name__ == "__main__":
    main()
