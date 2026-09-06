"""Refresh hashes for the completed P4 interface sidecar."""
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
    assert state.revision == 167 and not state.registry
    base = ROOT / "artifacts/routeb_agent_p4_interface_next_20260906T091429Z"
    report, final_receipt, receipt, source, verifier = (base / name for name in ("REPORT.md", "FINAL_RECEIPT.md", "receipt.json", "P4InterfacePMI.lean", "verify.ps1"))
    for path in (report, final_receipt, receipt, source, verifier):
        assert path.is_file(), path
    old_graph = ROOT / "artifacts/routeb_6dof/block45-obligations-v121.json"
    graph_path = ROOT / "artifacts/routeb_6dof/block45-obligations-v122.json"
    backup = ROOT / "artifacts/routeb_storage_checkpoint_20260905/state-before-revision168.json"
    graph = json.loads(old_graph.read_text(encoding="utf-8"))
    graph["bottleneck_audits"] = graph.get("bottleneck_audits", [])
    graph["bottleneck_audits"].append({
        "kind": "P4_interface_pmi_receipt_refresh",
        "report": {"path": ref(report), "sha256": sha(report)},
        "final_receipt": {"path": ref(final_receipt), "sha256": sha(final_receipt)},
        "receipt_json": {"path": ref(receipt), "sha256": sha(receipt)},
        "source": {"path": ref(source), "sha256": sha(source)},
        "verifier": {"path": ref(verifier), "sha256": sha(verifier)},
        "status": "LEAN_COMPILED_CONDITIONAL",
        "evidence_level": "exact_real_finite_dimensional_prototype",
        "registry_promoted": False,
    })
    graph.update(schema="routeb-proposed-proof-dag-v122", supersedes="block45-obligations-v121.json")
    ids = {node["id"] for node in graph["nodes"]}
    for node in graph["nodes"]:
        for dependency in node.get("dependencies", []):
            if dependency not in ids:
                raise ValueError(f"dangling dependency: {dependency}")
    if not backup.exists():
        shutil.copy2(store.path, backup)
    graph_path.write_text(json.dumps(graph, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    digest = sha(graph_path)
    state.graph_artifacts.append({"schema_version": 1, "algorithm": "routeb_p4_interface_refresh/v1", "graph_sha256": digest, "roots": [], "selected_nodes": [], "source": "refreshed P4 interface PMI receipt", "report_sha256": sha(report), "receipt_sha256": sha(receipt), "source_sha256": sha(source), "formal_certificate_allowed": False})
    state.event("routeb_p4_interface_receipt_refreshed", report=ref(report), report_sha256=sha(report), final_receipt=ref(final_receipt), final_receipt_sha256=sha(final_receipt), receipt=ref(receipt), receipt_sha256=sha(receipt), source=ref(source), source_sha256=sha(source), verifier=ref(verifier), verifier_sha256=sha(verifier), status="LEAN_COMPILED_CONDITIONAL", registry_promoted=False, formal_certificate_allowed=False, proposed_dag=ref(graph_path), proposed_dag_sha256=digest, broad_regression_run=False)
    store.save(state)
    print({"revision": state.revision, "graph": graph_path.name, "registry": len(state.registry), "formal_certificate_allowed": False})


if __name__ == "__main__":
    main()
