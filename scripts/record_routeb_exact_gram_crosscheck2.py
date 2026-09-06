"""Attach a second independent exact-Gram audit to the P6 obstruction node."""
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
    assert state.revision == 132 and not state.registry
    base = ROOT / "artifacts/routeb_agent_exact_gram_20260906_012551"
    report = base / "AUDIT_REPORT.md"
    metrics = base / "block_metrics.csv"
    format_doc = base / "MINIMAL_EXACT_CERTIFICATE_FORMAT.md"
    sums = base / "SHA256SUMS.txt"
    summary = base / "SUMMARY.json"
    old_graph = ROOT / "artifacts/routeb_6dof/block45-obligations-v86.json"
    graph_path = ROOT / "artifacts/routeb_6dof/block45-obligations-v87.json"
    backup = ROOT / "artifacts/routeb_storage_checkpoint_20260905/state-before-revision133.json"
    for path in (report, metrics, format_doc, sums, summary, old_graph):
        assert path.is_file(), path
    assert not graph_path.exists() and not backup.exists()
    data = json.loads(summary.read_text(encoding="utf-8"))
    assert data["blocks"] == 20
    assert data["exact_binary_rational_ldl_all_positive"] is True
    assert data["exact_target_identity"] is False
    assert data["identity_mismatch_blocks"] == 20
    assert data["identity_mismatch_terms_total"] == 1752
    report_text = report.read_text(encoding="utf-8")
    assert "EXPORTED_RATIONAL_GRAM_SPD = true" in report_text

    graph = json.loads(old_graph.read_text(encoding="utf-8"))
    nodes = {node["id"]: node for node in graph["nodes"]}
    node_id = "B45-P6_exact_gram_identity_obstruction"
    assert node_id in nodes
    node = nodes[node_id]
    node.setdefault("verification", {}).setdefault("independent_crosschecks", []).append({
        "report": ref(report), "block_metrics": ref(metrics),
        "certificate_format": ref(format_doc), "sha256s": ref(sums), "summary": ref(summary),
        "report_sha256": sha(report), "block_metrics_sha256": sha(metrics),
        "certificate_format_sha256": sha(format_doc), "sha256s_sha256": sha(sums),
        "summary_sha256": sha(summary), "blocks": 20,
        "exact_binary_rational_ldl_all_positive": True,
        "exact_target_identity": False, "identity_mismatch_terms_total": 1752,
        "max_abs_identity_residual": "4.6971686824165398e-08",
        "fragile_block": 8, "uniform_loaded_matrix_margin": "1/1000000000000",
        "status": "EXPORTED_RATIONAL_GRAM_SPD_ONLY",
        "registry_eligible": False, "formal_certificate_allowed": False,
    })
    node.setdefault("open_bridges", []).append(
        "reconcile all independent Gram audits before selecting an identity-valid witness"
    )
    graph.update(schema="routeb-proposed-proof-dag-v87", supersedes="block45-obligations-v86.json")
    graph["nodes"] = list(nodes.values())
    ids = set(nodes)
    for candidate in nodes.values():
        for dep in candidate.get("dependencies", []):
            if dep not in ids:
                raise ValueError(f"dangling dependency: {dep}")

    shutil.copy2(store.path, backup)
    graph_path.write_text(json.dumps(graph, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    state.event(
        "routeb_exact_gram_crosscheck2_recorded",
        node_id=node_id, report=ref(report), summary=ref(summary), blocks=20,
        exact_binary_rational_ldl_all_positive=True, exact_target_identity=False,
        identity_mismatch_terms_total=1752, registry_eligible=False,
        formal_certificate_allowed=False, proposed_dag=ref(graph_path),
        broad_regression_run=False,
    )
    store.save(state)
    print({"revision": state.revision, "graph_nodes": len(nodes),
           "registry": len(state.registry), "formal_certificate_allowed": False})


if __name__ == "__main__":
    main()
