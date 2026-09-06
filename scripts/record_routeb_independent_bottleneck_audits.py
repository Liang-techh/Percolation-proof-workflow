"""Attach independent body-trace and Gram-repair audits without promoting evidence."""
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
    assert state.revision == 135 and not state.registry
    body = ROOT / "artifacts/routeb_agent_body_trace_next_20260906_014555/AUDIT.md"
    gram = ROOT / "artifacts/routeb_agent_exact_gram_repair_20260906T074718Z/AUDIT.md"
    old_graph = ROOT / "artifacts/routeb_6dof/block45-obligations-v89.json"
    graph_path = ROOT / "artifacts/routeb_6dof/block45-obligations-v90.json"
    backup = ROOT / "artifacts/routeb_storage_checkpoint_20260905/state-before-revision136.json"
    for path in (body, gram, old_graph):
        assert path.is_file(), path
    assert not graph_path.exists() and not backup.exists()

    graph = json.loads(old_graph.read_text(encoding="utf-8"))
    nodes = {node["id"]: node for node in graph["nodes"]}
    body_node = nodes["B45-1_610_body_trace_binding_obstruction"]
    body_node.setdefault("verification", {}).setdefault("independent_audits", []).append({
        "report": ref(body), "report_sha256": sha(body),
        "status": "audit_only_negative_provenance",
        "aggregate_sum_body": False, "registry_eligible": False,
        "formal_certificate_allowed": False,
    })
    body_node.setdefault("open_bridges", []).append(
        "instrument routeB_fourier_rational_probe.py body-level mass traces before aggregation"
    )
    gram_node = nodes["B45-P6_exact_gram_identity_obstruction"]
    gram_node.setdefault("verification", {}).setdefault("independent_audits", []).append({
        "report": ref(gram), "report_sha256": sha(gram),
        "status": "audit_only_exported_gram_surrogate",
        "identity_valid_for_original_pmi": False,
        "registry_eligible": False, "formal_certificate_allowed": False,
    })
    gram_node.setdefault("open_bridges", []).append(
        "replace exported-Gram surrogate or prove a domain remainder budget before comparator admission"
    )
    graph.update(schema="routeb-proposed-proof-dag-v90", supersedes="block45-obligations-v89.json")
    graph["nodes"] = list(nodes.values())
    ids = set(nodes)
    for candidate in nodes.values():
        for dependency in candidate.get("dependencies", []):
            if dependency not in ids:
                raise ValueError(f"dangling dependency: {dependency}")

    shutil.copy2(store.path, backup)
    graph_path.write_text(json.dumps(graph, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    state.event(
        "routeb_independent_bottleneck_audits_recorded",
        body_trace_report=ref(body), body_trace_report_sha256=sha(body),
        body_trace_status="audit_only_negative_provenance",
        gram_repair_report=ref(gram), gram_repair_report_sha256=sha(gram),
        gram_status="audit_only_exported_gram_surrogate",
        registry_promoted=False, formal_certificate_allowed=False,
        proposed_dag=ref(graph_path), broad_regression_run=False,
    )
    store.save(state)
    print({"revision": state.revision, "graph_nodes": len(nodes),
           "registry": len(state.registry), "formal_certificate_allowed": False})


if __name__ == "__main__":
    main()
