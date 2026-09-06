"""Attach an independent exact-Gram audit without overwriting prior evidence."""
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
    assert state.revision == 130 and not state.registry
    base = ROOT / "artifacts/routeb_agent_exact_gram_20260906T072054Z"
    report = base / "EXACT_GRAM_AUDIT.md"
    split = base / "THEOREM_SPLIT.md"
    schema = base / "CERTIFICATE_SCHEMA.json"
    stats = base / "block_stats.csv"
    sums = base / "SHA256SUMS.csv"
    summary = base / "summary.json"
    old_graph = ROOT / "artifacts/routeb_6dof/block45-obligations-v84.json"
    graph_path = ROOT / "artifacts/routeb_6dof/block45-obligations-v85.json"
    backup = ROOT / "artifacts/routeb_storage_checkpoint_20260905/state-before-revision131.json"
    for path in (report, split, schema, stats, sums, summary, old_graph):
        assert path.is_file(), path
    assert not graph_path.exists() and not backup.exists()
    data = json.loads(summary.read_text(encoding="utf-8"))
    assert data["blocks"] == 20
    assert data["all_exact_decimal_grams_pd"] is True
    assert data["all_exact_identity"] is False
    assert data["all_exact_shift_witnesses_found"] is True
    report_text = report.read_text(encoding="utf-8")
    assert "1,752" in report_text and "4.697168745162832e-8" in report_text

    graph = json.loads(old_graph.read_text(encoding="utf-8"))
    nodes = {node["id"]: node for node in graph["nodes"]}
    node_id = "B45-P6_exact_gram_identity_obstruction"
    assert node_id in nodes
    node = nodes[node_id]
    node.setdefault("verification", {}).setdefault("independent_crosschecks", []).append({
        "report": ref(report), "theorem_split": ref(split), "certificate_schema": ref(schema),
        "block_stats": ref(stats), "sha256s": ref(sums), "summary": ref(summary),
        "report_sha256": sha(report), "theorem_split_sha256": sha(split),
        "certificate_schema_sha256": sha(schema), "block_stats_sha256": sha(stats),
        "sha256s_sha256": sha(sums), "summary_sha256": sha(summary),
        "blocks": 20, "exact_ldl_pivots_positive": True,
        "exact_coefficient_identities": False, "identity_mismatch_count": 1752,
        "max_identity_error": "4.697168745162832e-8",
        "min_exact_verified_margin": "1.808867948386037e-11",
        "registry_eligible": False, "formal_certificate_allowed": False,
    })
    node.setdefault("open_bridges", []).append(
        "reconcile independent exact-Gram rationalization margins and identity witnesses"
    )
    graph["next_frontier"] = [
        "reconcile exact-Gram crosscheck metrics",
        "construct identity-valid rational Gram/LDL witnesses for all required blocks",
        "record exact coefficient equality and strict PSD margin in a pinned checker",
    ] + [x for x in graph.get("next_frontier", []) if "Gram" not in x and "SOS" not in x]
    graph.update(schema="routeb-proposed-proof-dag-v85", supersedes="block45-obligations-v84.json")
    graph["nodes"] = list(nodes.values())
    ids = set(nodes)
    for candidate in nodes.values():
        for dep in candidate.get("dependencies", []):
            if dep not in ids:
                raise ValueError(f"dangling dependency: {dep}")

    shutil.copy2(store.path, backup)
    graph_path.write_text(json.dumps(graph, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    state.event(
        "routeb_exact_gram_crosscheck_recorded",
        node_id=node_id, report=ref(report), summary=ref(summary), blocks=20,
        exact_ldl_pivots_positive=True, exact_coefficient_identities=False,
        identity_mismatch_count=1752, registry_eligible=False,
        formal_certificate_allowed=False, proposed_dag=ref(graph_path),
        broad_regression_run=False,
    )
    store.save(state)
    print({"revision": state.revision, "graph_nodes": len(nodes),
           "registry": len(state.registry), "formal_certificate_allowed": False})


if __name__ == "__main__":
    main()
