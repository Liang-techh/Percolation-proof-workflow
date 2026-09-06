"""Attach the isolated authoritative body-trace instrumentation candidate."""
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
    assert state.revision == 150 and not state.registry
    base = ROOT / "artifacts/routeb_agent_authoritative_body_instrument_20260906T021137"
    report = base / "REPORT.md"
    runner = base / "body_trace_runner.py"
    patched = base / "routeB_fourier_rational_probe_instrumented.py"
    patch = base / "dhport_lib_body_trace.patch"
    manifest = base / "run_output/manifest.json"
    trace = base / "run_output/routeB_fourier_mass_body_trace.csv"
    aggregate = base / "run_output/routeB_fourier_mass_aggregate_from_trace.csv"
    old_graph = ROOT / "artifacts/routeb_6dof/block45-obligations-v104.json"
    graph_path = ROOT / "artifacts/routeb_6dof/block45-obligations-v105.json"
    backup = ROOT / "artifacts/routeb_storage_checkpoint_20260905/state-before-revision151.json"
    for path in (report, runner, patched, patch, manifest, trace, aggregate, old_graph):
        assert path.is_file(), path
    assert not graph_path.exists() and not backup.exists()
    text = report.read_text(encoding="utf-8")
    assert "aggregate_equals_sum_body_exact = true" in text
    assert "Julia was not available" in text
    data = json.loads(manifest.read_text(encoding="utf-8"))
    checks = data["checks"]
    assert checks.get("aggregate_equals_sum_body_exact") is True
    assert checks.get("aggregate_vs_frozen_csv_exact") is True
    assert checks.get("body_trace_data_rows") == 727

    graph = json.loads(old_graph.read_text(encoding="utf-8"))
    nodes = {node["id"]: node for node in graph["nodes"]}
    node_id = "B45-1_610_body_trace_binding_obstruction"
    node = nodes[node_id]
    node.setdefault("verification", {}).setdefault("authoritative_instrumentation", []).append({
        "report": ref(report), "runner": ref(runner), "patched_generator": ref(patched),
        "runtime_patch": ref(patch), "manifest": ref(manifest), "trace": ref(trace),
        "aggregate": ref(aggregate), "report_sha256": sha(report),
        "runner_sha256": sha(runner), "patched_generator_sha256": sha(patched),
        "runtime_patch_sha256": sha(patch), "manifest_sha256": sha(manifest),
        "trace_sha256": sha(trace), "aggregate_sha256": sha(aggregate),
        "status": "EXACT_BODY_TRACE_SIDECAR_PASS_RUNTIME_PATCH_PENDING",
        "aggregate_equals_sum_body_exact": True, "aggregate_vs_frozen_csv_exact": True,
        "body_trace_rows": 727, "julia_runtime_executed": False,
        "deployed_source_bound": False, "registry_eligible": False,
        "formal_certificate_allowed": False,
    })
    node.setdefault("open_bridges", []).extend([
        "apply the optional trace hook only in a recoverable project copy and execute Julia runtime replay",
        "bind emitted runtime body trace to deployed Float64 mass_matrix and its source manifest",
    ])
    graph.update(schema="routeb-proposed-proof-dag-v105", supersedes="block45-obligations-v104.json")
    graph["nodes"] = list(nodes.values())
    ids = set(nodes)
    for candidate in nodes.values():
        for dependency in candidate.get("dependencies", []):
            if dependency not in ids:
                raise ValueError(f"dangling dependency: {dependency}")
    shutil.copy2(store.path, backup)
    graph_path.write_text(json.dumps(graph, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    state.event(
        "routeb_authoritative_body_instrumentation_recorded", node_id=node_id,
        report=ref(report), manifest=ref(manifest), trace=ref(trace),
        report_sha256=sha(report), manifest_sha256=sha(manifest), trace_sha256=sha(trace),
        status="EXACT_BODY_TRACE_SIDECAR_PASS_RUNTIME_PATCH_PENDING",
        aggregate_equals_sum_body_exact=True, aggregate_vs_frozen_csv_exact=True,
        body_trace_rows=727, julia_runtime_executed=False, deployed_source_bound=False,
        registry_promoted=False, formal_certificate_allowed=False,
        proposed_dag=ref(graph_path), broad_regression_run=False,
    )
    store.save(state)
    print({"revision": state.revision, "graph_nodes": len(nodes),
           "registry": len(state.registry), "formal_certificate_allowed": False})


if __name__ == "__main__":
    main()
