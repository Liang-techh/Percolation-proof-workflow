"""Record P3 coverage obstruction and P4 interface PMI prototype."""
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
    assert state.revision == 165 and not state.registry
    coverage = ROOT / "artifacts/routeb_agent_p3_coverage_next_20260906T091543Z"
    cov_script, cov_json = coverage / "audit_p3_coverage_bridge.py", coverage / "p3_coverage_bridge_audit.json"
    p4 = ROOT / "artifacts/routeb_agent_p4_interface_next_20260906T091429Z"
    p4_report, p4_receipt, p4_lean, p4_verify = (p4 / name for name in ("REPORT.md", "FINAL_RECEIPT.md", "P4InterfacePMI.lean", "verify.ps1"))
    for path in (cov_script, cov_json, p4_report, p4_receipt, p4_lean, p4_verify):
        assert path.is_file(), path
    old_graph = ROOT / "artifacts/routeb_6dof/block45-obligations-v119.json"
    graph_path = ROOT / "artifacts/routeb_6dof/block45-obligations-v120.json"
    backup = ROOT / "artifacts/routeb_storage_checkpoint_20260905/state-before-revision166.json"
    graph = json.loads(old_graph.read_text(encoding="utf-8"))
    graph["bottleneck_audits"] = graph.get("bottleneck_audits", [])
    graph["bottleneck_audits"].extend([
        {"kind": "P3_coverage_bridge_obstruction", "script": {"path": ref(cov_script), "sha256": sha(cov_script)}, "audit": {"path": ref(cov_json), "sha256": sha(cov_json)}, "status": "MEMBERSHIP_NOT_PROVED", "evidence_level": "E1_recorded_interval_replay", "registry_promoted": False},
        {"kind": "P4_interface_schur_weighted_pmi_lean", "report": {"path": ref(p4_report), "sha256": sha(p4_report)}, "receipt": {"path": ref(p4_receipt), "sha256": sha(p4_receipt)}, "source": {"path": ref(p4_lean), "sha256": sha(p4_lean)}, "verifier": {"path": ref(p4_verify), "sha256": sha(p4_verify)}, "status": "LEAN_COMPILED_CONDITIONAL", "evidence_level": "exact_real_finite_dimensional_prototype", "registry_promoted": False},
    ])
    graph["open_frontier_updates"] = graph.get("open_frontier_updates", [])
    graph["open_frontier_updates"].extend([
        {"node": "B45-P3_local_cell_entry_or_cover", "status": "open", "reason": "local_positive_box is disjoint from initial/P8 narrow hull; need entry or sibling cover"},
        {"node": "B45-P4_fullstate_PSD_from_source_SOS", "status": "open", "reason": "Lean interface only assumes FullStatePSD/WeightedFullStatePSD"},
    ])
    graph.update(schema="routeb-proposed-proof-dag-v120", supersedes="block45-obligations-v119.json")
    ids = {node["id"] for node in graph["nodes"]}
    for node in graph["nodes"]:
        for dependency in node.get("dependencies", []):
            if dependency not in ids:
                raise ValueError(f"dangling dependency: {dependency}")
    if not backup.exists():
        shutil.copy2(store.path, backup)
    graph_path.write_text(json.dumps(graph, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    digest = sha(graph_path)
    state.graph_artifacts.append({"schema_version": 1, "algorithm": "routeb_coverage_and_p4_interface/v1", "graph_sha256": digest, "roots": [], "selected_nodes": [], "source": "P3 coverage bridge replay plus P4 Lean interface prototype", "coverage_proved": False, "formal_certificate_allowed": False})
    state.event("routeb_coverage_obstruction_and_p4_interface_recorded", coverage_audit=ref(cov_json), coverage_audit_sha256=sha(cov_json), coverage_status="MEMBERSHIP_NOT_PROVED", p4_report=ref(p4_report), p4_report_sha256=sha(p4_report), p4_receipt=ref(p4_receipt), p4_receipt_sha256=sha(p4_receipt), p4_source=ref(p4_lean), p4_source_sha256=sha(p4_lean), p4_status="LEAN_COMPILED_CONDITIONAL", registry_promoted=False, formal_certificate_allowed=False, proposed_dag=ref(graph_path), proposed_dag_sha256=digest, broad_regression_run=False)
    store.save(state)
    print({"revision": state.revision, "graph": graph_path.name, "registry": len(state.registry), "formal_certificate_allowed": False})


if __name__ == "__main__":
    main()
