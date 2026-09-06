"""Attach the second single-block Gram remainder audit."""
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
    assert state.revision == 145 and not state.registry
    report = ROOT / "artifacts/routeb_agent_one_cell_inverse_20260906T080126Z/GRAM_BLOCK_COMPARATOR_REPORT.md"
    old_graph = ROOT / "artifacts/routeb_6dof/block45-obligations-v99.json"
    graph_path = ROOT / "artifacts/routeb_6dof/block45-obligations-v100.json"
    backup = ROOT / "artifacts/routeb_storage_checkpoint_20260905/state-before-revision146.json"
    for path in (report, old_graph):
        assert path.is_file(), path
    assert not graph_path.exists() and not backup.exists()
    text = report.read_text(encoding="utf-8")
    assert "NOT_YET_VALID_WITH_REMAINDER" in text
    assert "28" in text and ("epsilon" in text or "ε" in text)

    graph = json.loads(old_graph.read_text(encoding="utf-8"))
    nodes = {node["id"]: node for node in graph["nodes"]}
    node_id = "B45-P6_exact_gram_identity_obstruction"
    node = nodes[node_id]
    node.setdefault("verification", {}).setdefault("single_block_remainder_audits", []).append({
        "report": ref(report), "report_sha256": sha(report), "block": 3,
        "exact_ldl_positive": True, "identity_exact": False,
        "mismatch_terms": 28, "remainder_bound": "not constructed",
        "status": "NOT_YET_VALID_WITH_REMAINDER",
        "registry_eligible": False, "formal_certificate_allowed": False,
    })
    node.setdefault("open_bridges", []).append(
        "construct an exact domain-uniform epsilon_3 from the 28 mismatch coefficients"
    )
    graph.update(schema="routeb-proposed-proof-dag-v100", supersedes="block45-obligations-v99.json")
    graph["nodes"] = list(nodes.values())
    ids = set(nodes)
    for candidate in nodes.values():
        for dependency in candidate.get("dependencies", []):
            if dependency not in ids:
                raise ValueError(f"dangling dependency: {dependency}")
    shutil.copy2(store.path, backup)
    graph_path.write_text(json.dumps(graph, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    state.event(
        "routeb_gram_remainder_audit_recorded", node_id=node_id, report=ref(report),
        report_sha256=sha(report), block=3, exact_ldl_positive=True,
        identity_exact=False, mismatch_terms=28, remainder_bound="not constructed",
        status="NOT_YET_VALID_WITH_REMAINDER", registry_promoted=False,
        formal_certificate_allowed=False, proposed_dag=ref(graph_path),
        broad_regression_run=False,
    )
    store.save(state)
    print({"revision": state.revision, "graph_nodes": len(nodes),
           "registry": len(state.registry), "formal_certificate_allowed": False})


if __name__ == "__main__":
    main()
