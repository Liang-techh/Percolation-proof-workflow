"""Attach the exact terminal-metric audit and retain its conditional boundary."""
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
    assert state.revision == 136 and not state.registry
    base = ROOT / "artifacts/routeb_agent_terminal_metric_20260906T073733Z"
    report = base / "AUDIT_REPORT.md"
    manifest = base / "evidence_manifest.json"
    recompute = base / "recompute_exact.py"
    sums = base / "SHA256SUMS.txt"
    old_graph = ROOT / "artifacts/routeb_6dof/block45-obligations-v90.json"
    graph_path = ROOT / "artifacts/routeb_6dof/block45-obligations-v91.json"
    backup = ROOT / "artifacts/routeb_storage_checkpoint_20260905/state-before-revision137.json"
    for path in (report, manifest, recompute, sums, old_graph):
        assert path.is_file(), path
    assert not graph_path.exists() and not backup.exists()

    report_text = report.read_text(encoding="utf-8")
    assert "qpoly" in report_text
    evidence = json.loads(manifest.read_text(encoding="utf-8"))
    if isinstance(evidence, dict):
        assert evidence
        assert evidence.get("schema") == "routeb-terminal-metric-audit-v1"

    graph = json.loads(old_graph.read_text(encoding="utf-8"))
    nodes = {node["id"]: node for node in graph["nodes"]}
    node_id = "B45-8_terminal_flowpipe_first_exit_interface"
    assert node_id in nodes
    node = nodes[node_id]
    node.setdefault("verification", {}).setdefault("terminal_metric_audits", []).append({
        "report": ref(report), "evidence_manifest": ref(manifest),
        "recompute_script": ref(recompute), "sha256s": ref(sums),
        "report_sha256": sha(report), "evidence_manifest_sha256": sha(manifest),
        "recompute_script_sha256": sha(recompute), "sha256s_sha256": sha(sums),
        "status": "EXACT_TERMINAL_METRIC_AUDIT_OK",
        "direct_qpoly_12_comparator": False,
        "conditional_qpoly_12_bound": True,
        "flowpipe_remainder_gate": "open",
        "registry_eligible": False, "formal_certificate_allowed": False,
    })
    node.setdefault("open_bridges", []).extend([
        "prove the stronger remainder/flowpipe gate required by the exact qpoly<=12 comparator",
        "do not infer qpoly<=12 from p<=5.6; that implication only yields qpoly<=14",
    ])
    graph.update(schema="routeb-proposed-proof-dag-v91", supersedes="block45-obligations-v90.json")
    graph["nodes"] = list(nodes.values())
    ids = set(nodes)
    for candidate in nodes.values():
        for dependency in candidate.get("dependencies", []):
            if dependency not in ids:
                raise ValueError(f"dangling dependency: {dependency}")

    shutil.copy2(store.path, backup)
    graph_path.write_text(json.dumps(graph, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    state.event(
        "routeb_terminal_metric_audit_recorded",
        node_id=node_id, report=ref(report), evidence_manifest=ref(manifest),
        report_sha256=sha(report), direct_qpoly_12_comparator=False,
        conditional_qpoly_12_bound=True, flowpipe_remainder_gate="open",
        registry_promoted=False, formal_certificate_allowed=False,
        proposed_dag=ref(graph_path), broad_regression_run=False,
    )
    store.save(state)
    print({"revision": state.revision, "graph_nodes": len(nodes),
           "registry": len(state.registry), "formal_certificate_allowed": False})


if __name__ == "__main__":
    main()
