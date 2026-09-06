"""Persist the negative 610-row body-attribution audit."""
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
    assert state.revision == 124 and not state.registry
    base = ROOT / "artifacts/routeb_agent_610_body_binding_20260906T070705Z"
    report = base / "610_body_binding_audit.md"
    manifest = base / "audit_manifest.json"
    spec = base / "minimum_source_trace_spec.json"
    lean = base / "minimal_lean_interface.lean"
    attempt = base / "LEAN_COMPILE_ATTEMPT.md"
    old_graph = ROOT / "artifacts/routeb_6dof/block45-obligations-v78.json"
    graph_path = ROOT / "artifacts/routeb_6dof/block45-obligations-v79.json"
    backup = ROOT / "artifacts/routeb_storage_checkpoint_20260905/state-before-revision125.json"
    for path in (report, manifest, spec, lean, attempt, old_graph):
        assert path.is_file(), path
    assert not graph_path.exists() and not backup.exists()
    data = json.loads(manifest.read_text(encoding="utf-8"))
    assert data["verdict"] == "NO_BODY_BINDING_FROM_PAYLOAD_AND_GENERATOR_HASH"
    assert data["aggregate"]["data_rows"] == 610
    assert data["aggregate"]["body_identifier_column"] is False
    assert data["registry"]["registry_eligible"] is False
    assert data["registry"]["formal_certificate_allowed"] is False

    graph = json.loads(old_graph.read_text(encoding="utf-8"))
    nodes = {node["id"]: node for node in graph["nodes"]}
    node_id = "B45-1_610_body_trace_binding_obstruction"
    assert node_id not in nodes
    nodes[node_id] = {
        "id": node_id,
        "status": "source_audit_open",
        "dependencies": ["B45-1_deployed_source_comparator_contract_v62"],
        "source": "../../artifacts/routeb_agent_610_body_binding_20260906T070705Z/610_body_binding_audit.md",
        "statement": (
            "Audit whether the 610-row aggregate Fourier mass CSV plus generator "
            "hash can bind the six-body source decomposition required by the theorem."
        ),
        "verification": {
            "report": ref(report), "manifest": ref(manifest), "trace_spec": ref(spec),
            "lean_interface": ref(lean), "compile_attempt": ref(attempt),
            "report_sha256": sha(report), "manifest_sha256": sha(manifest),
            "trace_spec_sha256": sha(spec), "lean_interface_sha256": sha(lean),
            "body_identifier_column": False,
            "verdict": data["verdict"], "registry_eligible": False,
            "formal_certificate_allowed": False,
        },
        "closed_subclaims": [
            "aggregate CSV schema and 610-row count audited",
            "generator aggregation point loses body dimension",
            "hash provenance is not an inverse body trace",
            "minimum pre-aggregation trace schema specified",
        ],
        "open_bridges": list(data["missing_binding"]),
        "semantic_boundary": "negative source-binding audit; no theorem or registry evidence",
    }
    graph["next_frontier"] = [
        "emit per-body Fourier trace before six-body accumulation",
        "prove aggregate=sum over body trace with exact coverage",
        "bind each body trace to exact DH body contribution",
        "separately close Julia Float64 and solve/finite-difference comparator",
    ] + [x for x in graph.get("next_frontier", []) if "body identity" not in x and "610-row" not in x]
    graph.update(schema="routeb-proposed-proof-dag-v79", supersedes="block45-obligations-v78.json")
    graph["nodes"] = list(nodes.values())
    ids = set(nodes)
    for node in nodes.values():
        for dep in node.get("dependencies", []):
            if dep not in ids:
                raise ValueError(f"dangling dependency: {dep}")

    shutil.copy2(store.path, backup)
    graph_path.write_text(json.dumps(graph, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    state.event(
        "routeb_610_body_binding_obstruction_recorded",
        node_id=node_id, report=ref(report), manifest=ref(manifest), trace_spec=ref(spec),
        verdict=data["verdict"], data_rows=610, body_identifier_column=False,
        registry_eligible=False, formal_certificate_allowed=False,
        proposed_dag=ref(graph_path), broad_regression_run=False,
    )
    store.save(state)
    print({"revision": state.revision, "graph_nodes": len(nodes),
           "registry": len(state.registry), "formal_certificate_allowed": False})


if __name__ == "__main__":
    main()
