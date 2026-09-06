"""Record the one-cell exact-rational Schur resolvent extension."""
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
    assert state.revision == 166 and not state.registry
    base = ROOT / "artifacts/routeb_agent_schur_fullq_next_20260906T091446Z"
    report, numbers, delta, ks, verify = (base / name for name in ("AUDIT.md", "NUMBERS.json", "DELTA_M_ENTRY_BOUNDS.csv", "K_S_DELTA_BOUNDS.csv", "verify_fullq_schur.py"))
    for path in (report, numbers, delta, ks, verify):
        assert path.is_file(), path
    old_graph = ROOT / "artifacts/routeb_6dof/block45-obligations-v120.json"
    graph_path = ROOT / "artifacts/routeb_6dof/block45-obligations-v121.json"
    backup = ROOT / "artifacts/routeb_storage_checkpoint_20260905/state-before-revision167.json"
    graph = json.loads(old_graph.read_text(encoding="utf-8"))
    graph["bottleneck_audits"] = graph.get("bottleneck_audits", [])
    graph["bottleneck_audits"].append({
        "kind": "B45_schur_fullq_one_cell_resolvent",
        "report": {"path": ref(report), "sha256": sha(report)},
        "numbers": {"path": ref(numbers), "sha256": sha(numbers)},
        "delta_M": {"path": ref(delta), "sha256": sha(delta)},
        "K_S_delta": {"path": ref(ks), "sha256": sha(ks)},
        "verifier": {"path": ref(verify), "sha256": sha(verify)},
        "evidence_level": "E1_conditional_exact_rational_one_cell",
        "status": "ONE_CELL_OPEN_GLOBAL",
        "cell": "|q_i| <= 1/1000",
        "rho": "0.0327225088764795621695964618332",
        "K_delta_inf": "0.30019606039984190719217879127188",
        "S_delta_inf": "0.03562779565311785401845538235699",
        "global_coverage": False,
        "float64_nonzero_bridge": False,
        "registry_promoted": False,
    })
    graph["open_frontier_updates"] = graph.get("open_frontier_updates", [])
    graph["open_frontier_updates"].append({"node": "B45-P4_Schur_fullq_cell_to_partition", "status": "open", "reason": "extend one-cell exact resolvent to covered cells and bind deployed Float64 semantics"})
    graph.update(schema="routeb-proposed-proof-dag-v121", supersedes="block45-obligations-v120.json")
    ids = {node["id"] for node in graph["nodes"]}
    for node in graph["nodes"]:
        for dependency in node.get("dependencies", []):
            if dependency not in ids:
                raise ValueError(f"dangling dependency: {dependency}")
    if not backup.exists():
        shutil.copy2(store.path, backup)
    graph_path.write_text(json.dumps(graph, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    digest = sha(graph_path)
    state.graph_artifacts.append({"schema_version": 1, "algorithm": "routeb_schur_fullq_cell/v1", "graph_sha256": digest, "roots": [], "selected_nodes": [], "source": "exact Fourier-rational one-cell Schur resolvent audit", "cell": "|q_i|<=1/1000", "global_coverage": False, "formal_certificate_allowed": False})
    state.event("routeb_schur_fullq_one_cell_recorded", report=ref(report), report_sha256=sha(report), numbers=ref(numbers), numbers_sha256=sha(numbers), delta_M=ref(delta), delta_M_sha256=sha(delta), K_S_delta=ref(ks), K_S_delta_sha256=sha(ks), verifier=ref(verify), verifier_sha256=sha(verify), status="ONE_CELL_OPEN_GLOBAL", rho="0.0327225088764795621695964618332", K_delta_inf="0.30019606039984190719217879127188", S_delta_inf="0.03562779565311785401845538235699", global_coverage=False, float64_nonzero_bridge=False, registry_promoted=False, formal_certificate_allowed=False, proposed_dag=ref(graph_path), proposed_dag_sha256=digest, broad_regression_run=False)
    store.save(state)
    print({"revision": state.revision, "graph": graph_path.name, "registry": len(state.registry), "formal_certificate_allowed": False})


if __name__ == "__main__":
    main()
