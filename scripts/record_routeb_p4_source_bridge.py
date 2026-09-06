"""Record the compiled source-to-P4-interface bridge as conditional evidence."""
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
    assert state.revision == 170 and not state.registry
    base = ROOT / "artifacts/routeb_agent_p4_source_bridge_next_20260906T092639Z"
    report, receipt, source, verifier, compile_log, verify_log, olean = (base / name for name in ("REPORT.md", "RECEIPT.md", "SourceToP4Bridge.lean", "verify.ps1", "run-pinned/compile.log", "run-pinned/verify.log", "run-pinned/SourceToP4Bridge.olean"))
    for path in (report, receipt, source, verifier, compile_log, verify_log, olean):
        assert path.is_file(), path
    old_graph = ROOT / "artifacts/routeb_6dof/block45-obligations-v124.json"
    graph_path = ROOT / "artifacts/routeb_6dof/block45-obligations-v125.json"
    backup = ROOT / "artifacts/routeb_storage_checkpoint_20260905/state-before-revision171.json"
    graph = json.loads(old_graph.read_text(encoding="utf-8"))
    graph["bottleneck_audits"] = graph.get("bottleneck_audits", [])
    graph["bottleneck_audits"].append({
        "kind": "P4_source_to_interface_bridge",
        "report": {"path": ref(report), "sha256": sha(report)},
        "receipt": {"path": ref(receipt), "sha256": sha(receipt)},
        "source": {"path": ref(source), "sha256": sha(source)},
        "verifier": {"path": ref(verifier), "sha256": sha(verifier)},
        "compile_log": {"path": ref(compile_log), "sha256": sha(compile_log)},
        "verify_log": {"path": ref(verify_log), "sha256": sha(verify_log)},
        "olean": {"path": ref(olean), "sha256": sha(olean)},
        "status": "LEAN_COMPILED_CONDITIONAL",
        "evidence_level": "exact_real_source_derived_adapter",
        "physical_source_bridge": False,
        "registry_promoted": False,
    })
    graph["open_frontier_updates"] = graph.get("open_frontier_updates", [])
    graph["open_frontier_updates"].append({"node": "B45-P4_source_derived_constants_to_deployed_semantics", "status": "open", "reason": "exact-real transcription still needs Julia/Float64, regularizer, FD and source-function equivalence bridge"})
    graph.update(schema="routeb-proposed-proof-dag-v125", supersedes="block45-obligations-v124.json")
    ids = {node["id"] for node in graph["nodes"]}
    for node in graph["nodes"]:
        for dependency in node.get("dependencies", []):
            if dependency not in ids:
                raise ValueError(f"dangling dependency: {dependency}")
    if not backup.exists():
        shutil.copy2(store.path, backup)
    graph_path.write_text(json.dumps(graph, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    digest = sha(graph_path)
    state.graph_artifacts.append({"schema_version": 1, "algorithm": "routeb_p4_source_bridge/v1", "graph_sha256": digest, "roots": [], "selected_nodes": [], "source": "isolated exact-real source-to-P4 bridge", "report_sha256": sha(report), "receipt_sha256": sha(receipt), "source_sha256": sha(source), "olean_sha256": sha(olean), "physical_source_bridge": False, "formal_certificate_allowed": False})
    state.event("routeb_p4_source_bridge_recorded", report=ref(report), report_sha256=sha(report), receipt=ref(receipt), receipt_sha256=sha(receipt), source=ref(source), source_sha256=sha(source), verifier=ref(verifier), verifier_sha256=sha(verifier), compile_log=ref(compile_log), compile_log_sha256=sha(compile_log), verify_log=ref(verify_log), verify_log_sha256=sha(verify_log), olean=ref(olean), olean_sha256=sha(olean), status="LEAN_COMPILED_CONDITIONAL", physical_source_bridge=False, registry_promoted=False, formal_certificate_allowed=False, proposed_dag=ref(graph_path), proposed_dag_sha256=digest, broad_regression_run=False)
    store.save(state)
    print({"revision": state.revision, "graph": graph_path.name, "registry": len(state.registry), "formal_certificate_allowed": False})


if __name__ == "__main__":
    main()
