"""Attach the negative authoritative-cell witness audit to the P3 node."""
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
    assert state.revision == 137 and not state.registry
    report = ROOT / "artifacts/routeb_agent_coverage_witness_20260906T074821Z/AUDIT.md"
    old_graph = ROOT / "artifacts/routeb_6dof/block45-obligations-v91.json"
    graph_path = ROOT / "artifacts/routeb_6dof/block45-obligations-v92.json"
    backup = ROOT / "artifacts/routeb_storage_checkpoint_20260905/state-before-revision138.json"
    for path in (report, old_graph):
        assert path.is_file(), path
    assert not graph_path.exists() and not backup.exists()
    text = report.read_text(encoding="utf-8")
    assert "IMPORTABLE_CURRENT_CELL_WITNESS              = NOT FOUND" in text
    assert "FORMAL_CERTIFICATE_ALLOWED                   = false" in text
    assert "UNKNOWN_INVERSE" in text and "UNKNOWN_DOMAIN_BOUNDARY" in text

    graph = json.loads(old_graph.read_text(encoding="utf-8"))
    nodes = {node["id"]: node for node in graph["nodes"]}
    node_id = "B45-P3_global_coverage_interval_interface"
    node = nodes[node_id]
    node.setdefault("verification", {}).setdefault("authoritative_witness_audits", []).append({
        "report": ref(report), "report_sha256": sha(report),
        "status": "CURRENT_AUTHORITATIVE_WITNESS_NOT_FOUND",
        "unknown_inverse": 8191, "unknown_domain_boundary": 512,
        "unknown_bracket": 511, "accepted_global_cells": 0,
        "registry_eligible": False, "formal_certificate_allowed": False,
    })
    node.setdefault("open_bridges", []).append(
        "export one current-authority cell with exact box/source/partition provenance and replayable witness payload"
    )
    graph.update(schema="routeb-proposed-proof-dag-v92", supersedes="block45-obligations-v91.json")
    graph["nodes"] = list(nodes.values())
    ids = set(nodes)
    for candidate in nodes.values():
        for dependency in candidate.get("dependencies", []):
            if dependency not in ids:
                raise ValueError(f"dangling dependency: {dependency}")
    shutil.copy2(store.path, backup)
    graph_path.write_text(json.dumps(graph, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    state.event(
        "routeb_authoritative_coverage_witness_audit_recorded",
        node_id=node_id, report=ref(report), report_sha256=sha(report),
        status="CURRENT_AUTHORITATIVE_WITNESS_NOT_FOUND", unknown_inverse=8191,
        unknown_domain_boundary=512, unknown_bracket=511, accepted_global_cells=0,
        registry_promoted=False, formal_certificate_allowed=False,
        proposed_dag=ref(graph_path), broad_regression_run=False,
    )
    store.save(state)
    print({"revision": state.revision, "graph_nodes": len(nodes),
           "registry": len(state.registry), "formal_certificate_allowed": False})


if __name__ == "__main__":
    main()
