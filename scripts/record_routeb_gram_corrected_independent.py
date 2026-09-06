"""Attach the independent exact corrected-Gram audit as an audit-only surrogate."""
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
    assert state.revision == 157 and not state.registry
    base = ROOT / "artifacts/routeb_agent_gram_corrected_independent_20260906T083222Z"
    report = base / "REPORT.md"
    summary = base / "summary.json"
    gram3 = base / "block3_corrected_gram.csv"
    gram4 = base / "block4_corrected_gram.csv"
    old_graph = ROOT / "artifacts/routeb_6dof/block45-obligations-v111.json"
    graph_path = ROOT / "artifacts/routeb_6dof/block45-obligations-v112.json"
    backup = ROOT / "artifacts/routeb_storage_checkpoint_20260905/state-before-revision158.json"
    for path in (report, summary, gram3, gram4, old_graph):
        assert path.is_file(), path
    assert not graph_path.exists() and not backup.exists()
    data = json.loads(summary.read_text(encoding="utf-8"))
    for block in ("3", "4"):
        assert data["blocks"][block]["corrected_identity_exact"] is True
        assert data["blocks"][block]["global_exact_spd"] is True
    graph = json.loads(old_graph.read_text(encoding="utf-8"))
    nodes = {node["id"]: node for node in graph["nodes"]}
    node_id = "B45-P6_exact_gram_identity_obstruction"
    node = nodes[node_id]
    node.setdefault("verification", {}).setdefault("corrected_gram_audits", []).append({
        "report": ref(report), "summary": ref(summary), "block3": ref(gram3), "block4": ref(gram4),
        "report_sha256": sha(report), "summary_sha256": sha(summary),
        "block3_sha256": sha(gram3), "block4_sha256": sha(gram4),
        "blocks": [3, 4], "mismatch_terms": {"3": 28, "4": 28},
        "corrected_identity_exact": True, "global_exact_spd": True,
        "exact_spd_margin": {"3": "45881327/31250000000", "4": "38915015523/1000000000000"},
        "status": "EXPORTED_TARGET_CORRECTED_GRAM_AUDIT_ONLY",
        "source_level_exact_rational_export": False,
        "registry_eligible": False, "formal_certificate_allowed": False,
    })
    node.setdefault("closed_subclaims", []).extend([
        "blocks 3/4 have no pairwise-basis support obstruction",
        "an explicit rational post-export correction reconciles all 28 mismatch terms per block",
        "the corrected block 3/4 matrices have exact shifted-LDL SPD witnesses",
    ])
    node.setdefault("open_bridges", []).extend([
        "bind corrected Gram to source-faithful rational SOS or retain explicit surrogate status",
        "bind target coefficients to authoritative DH/FD/domain semantics before comparator admission",
    ])
    graph.update(schema="routeb-proposed-proof-dag-v112", supersedes="block45-obligations-v111.json")
    graph["nodes"] = list(nodes.values())
    ids = set(nodes)
    for candidate in nodes.values():
        for dependency in candidate.get("dependencies", []):
            if dependency not in ids:
                raise ValueError(f"dangling dependency: {dependency}")
    shutil.copy2(store.path, backup)
    graph_path.write_text(json.dumps(graph, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    state.event(
        "routeb_gram_corrected_independent_recorded", node_id=node_id,
        report=ref(report), summary=ref(summary), block3=ref(gram3), block4=ref(gram4),
        report_sha256=sha(report), summary_sha256=sha(summary),
        block3_sha256=sha(gram3), block4_sha256=sha(gram4), blocks=[3, 4],
        mismatch_terms={"3": 28, "4": 28}, corrected_identity_exact=True, global_exact_spd=True,
        exact_spd_margin={"3": "45881327/31250000000", "4": "38915015523/1000000000000"},
        status="EXPORTED_TARGET_CORRECTED_GRAM_AUDIT_ONLY", source_level_exact_rational_export=False,
        registry_promoted=False, formal_certificate_allowed=False,
        proposed_dag=ref(graph_path), broad_regression_run=False,
    )
    store.save(state)
    print({"revision": state.revision, "graph_nodes": len(nodes),
           "registry": len(state.registry), "formal_certificate_allowed": False})


if __name__ == "__main__":
    main()
