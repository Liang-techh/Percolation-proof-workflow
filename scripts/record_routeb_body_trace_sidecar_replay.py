"""Attach the exact sidecar body-trace replay with its deployed-source boundary."""
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
    assert state.revision == 143 and not state.registry
    base = ROOT / "artifacts/routeb_agent_body_trace_replay_20260906_015834"
    result = base / "result.json"
    schema = base / "artifact.schema.json"
    body_csv = base / "body_fourier_mass.csv"
    aggregate_csv = base / "aggregate_fourier_mass.csv"
    replay = base / "replay_body_fourier_mass.py"
    wrapper = base / "routeb_body_mass_julia_wrapper.jl"
    old_graph = ROOT / "artifacts/routeb_6dof/block45-obligations-v97.json"
    graph_path = ROOT / "artifacts/routeb_6dof/block45-obligations-v98.json"
    backup = ROOT / "artifacts/routeb_storage_checkpoint_20260905/state-before-revision144.json"
    for path in (result, schema, body_csv, aggregate_csv, replay, wrapper, old_graph):
        assert path.is_file(), path
    assert not graph_path.exists() and not backup.exists()
    data = json.loads(result.read_text(encoding="utf-8"))
    assert data["status"] == "PASS"
    assert data["exact_checks"]["aggregate_equals_sum_body"] is True
    assert data["exact_checks"]["aggregate_vs_direct_mismatch_count"] == 0
    assert data["source"]["read_only"] is True

    graph = json.loads(old_graph.read_text(encoding="utf-8"))
    nodes = {node["id"]: node for node in graph["nodes"]}
    node_id = "B45-1_610_body_trace_binding_obstruction"
    node = nodes[node_id]
    node.setdefault("verification", {}).setdefault("sidecar_replays", []).append({
        "result": ref(result), "schema": ref(schema), "body_csv": ref(body_csv),
        "aggregate_csv": ref(aggregate_csv), "replay": ref(replay), "wrapper": ref(wrapper),
        "result_sha256": sha(result), "schema_sha256": sha(schema),
        "body_csv_sha256": sha(body_csv), "aggregate_csv_sha256": sha(aggregate_csv),
        "replay_sha256": sha(replay), "wrapper_sha256": sha(wrapper),
        "status": "EXACT_FOURIER_SIDECAR_REPLAY_ONLY",
        "aggregate_equals_sum_body": True, "aggregate_vs_direct_mismatch_count": 0,
        "deployed_mass_matrix_body_trace": False,
        "registry_eligible": False, "formal_certificate_allowed": False,
    })
    node.setdefault("open_bridges", []).extend([
        "treat sidecar replay as semantic evidence only; bind deployed mass_matrix body sink separately",
        "compare sidecar body terms against the exact authoritative generator and deployed Float64 path",
    ])
    graph.update(schema="routeb-proposed-proof-dag-v98", supersedes="block45-obligations-v97.json")
    graph["nodes"] = list(nodes.values())
    ids = set(nodes)
    for candidate in nodes.values():
        for dependency in candidate.get("dependencies", []):
            if dependency not in ids:
                raise ValueError(f"dangling dependency: {dependency}")
    shutil.copy2(store.path, backup)
    graph_path.write_text(json.dumps(graph, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    state.event(
        "routeb_body_trace_sidecar_replay_recorded", node_id=node_id, result=ref(result),
        result_sha256=sha(result), status="EXACT_FOURIER_SIDECAR_REPLAY_ONLY",
        aggregate_equals_sum_body=True, deployed_mass_matrix_body_trace=False,
        registry_promoted=False, formal_certificate_allowed=False,
        proposed_dag=ref(graph_path), broad_regression_run=False,
    )
    store.save(state)
    print({"revision": state.revision, "graph_nodes": len(nodes),
           "registry": len(state.registry), "formal_certificate_allowed": False})


if __name__ == "__main__":
    main()
