"""Refresh the Schur full-q cell audit after the regularizer correction."""
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
    assert state.revision == 168 and not state.registry
    base = ROOT / "artifacts/routeb_agent_schur_fullq_next_20260906T091446Z"
    report, numbers, delta, ks, verify = (base / name for name in ("AUDIT.md", "NUMBERS.json", "DELTA_M_ENTRY_BOUNDS.csv", "K_S_DELTA_BOUNDS.csv", "verify_fullq_schur.py"))
    for path in (report, numbers, delta, ks, verify):
        assert path.is_file(), path
    old_graph = ROOT / "artifacts/routeb_6dof/block45-obligations-v122.json"
    graph_path = ROOT / "artifacts/routeb_6dof/block45-obligations-v123.json"
    backup = ROOT / "artifacts/routeb_storage_checkpoint_20260905/state-before-revision169.json"
    graph = json.loads(old_graph.read_text(encoding="utf-8"))
    graph["bottleneck_audits"] = graph.get("bottleneck_audits", [])
    graph["bottleneck_audits"].append({
        "kind": "B45_schur_fullq_one_cell_regularizer_refresh",
        "report": {"path": ref(report), "sha256": sha(report)},
        "numbers": {"path": ref(numbers), "sha256": sha(numbers)},
        "delta_M": {"path": ref(delta), "sha256": sha(delta)},
        "K_S_delta": {"path": ref(ks), "sha256": sha(ks)},
        "verifier": {"path": ref(verify), "sha256": sha(verify)},
        "evidence_level": "E1_conditional_exact_rational_one_cell",
        "status": "ONE_CELL_REGULARIZED_OPEN_GLOBAL",
        "regularizer": "10^-6 I",
        "rho": "0.03272250887647956",
        "K_mu_delta_inf": "0.004503254628774217",
        "S_mu_delta_inf": "0.0002409810928598445",
        "global_coverage": False,
        "float64_nonzero_bridge": False,
        "registry_promoted": False,
    })
    graph["open_frontier_updates"] = graph.get("open_frontier_updates", [])
    graph["open_frontier_updates"].append({"node": "B45-P4_regularized_schur_cell_to_partition", "status": "open", "reason": "regularized one-cell ledger must be connected to Float64 directed enclosure, correlated D-row port, and covered partition"})
    graph.update(schema="routeb-proposed-proof-dag-v123", supersedes="block45-obligations-v122.json")
    ids = {node["id"] for node in graph["nodes"]}
    for node in graph["nodes"]:
        for dependency in node.get("dependencies", []):
            if dependency not in ids:
                raise ValueError(f"dangling dependency: {dependency}")
    if not backup.exists():
        shutil.copy2(store.path, backup)
    graph_path.write_text(json.dumps(graph, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    digest = sha(graph_path)
    state.graph_artifacts.append({"schema_version": 1, "algorithm": "routeb_schur_fullq_refresh/v1", "graph_sha256": digest, "roots": [], "selected_nodes": [], "source": "regularized exact Fourier-rational one-cell Schur audit", "report_sha256": sha(report), "numbers_sha256": sha(numbers), "K_S_delta_sha256": sha(ks), "regularizer": "10^-6 I", "global_coverage": False, "formal_certificate_allowed": False})
    state.event("routeb_schur_fullq_regularizer_refresh_recorded", report=ref(report), report_sha256=sha(report), numbers=ref(numbers), numbers_sha256=sha(numbers), delta_M=ref(delta), delta_M_sha256=sha(delta), K_S_delta=ref(ks), K_S_delta_sha256=sha(ks), verifier=ref(verify), verifier_sha256=sha(verify), regularizer="10^-6 I", rho="0.03272250887647956", K_mu_delta_inf="0.004503254628774217", S_mu_delta_inf="0.0002409810928598445", status="ONE_CELL_REGULARIZED_OPEN_GLOBAL", global_coverage=False, float64_nonzero_bridge=False, registry_promoted=False, formal_certificate_allowed=False, proposed_dag=ref(graph_path), proposed_dag_sha256=digest, broad_regression_run=False)
    store.save(state)
    print({"revision": state.revision, "graph": graph_path.name, "registry": len(state.registry), "formal_certificate_allowed": False})


if __name__ == "__main__":
    main()
