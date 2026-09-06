"""Persist the body-trace exporter design as an audit-only frontier."""
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
    assert state.revision == 131 and not state.registry
    base = ROOT / "artifacts/routeb_agent_body_trace_design_20260906T071911Z"
    readme = base / "README.md"
    manifest_schema = base / "manifest.schema.json"
    row_schema = base / "trace_row.schema.json"
    exporter = base / "body_trace_sidecar.py"
    lean = base / "lean_body_trace_interface.lean"
    verification = base / "VERIFICATION.md"
    probe_manifest = base / "probe_output/routeB_fourier_mass_manifest.json"
    old_graph = ROOT / "artifacts/routeb_6dof/block45-obligations-v85.json"
    graph_path = ROOT / "artifacts/routeb_6dof/block45-obligations-v86.json"
    backup = ROOT / "artifacts/routeb_storage_checkpoint_20260905/state-before-revision132.json"
    for path in (readme, manifest_schema, row_schema, exporter, lean, verification, probe_manifest, old_graph):
        assert path.is_file(), path
    assert not graph_path.exists() and not backup.exists()
    verification_text = verification.read_text(encoding="utf-8")
    assert "TRACE_EQ_PASS" in verification_text
    assert "Lean 4.32.0" in verification_text
    data = json.loads(probe_manifest.read_text(encoding="utf-8"))
    assert data["body_count"] == 6
    assert data["source_binding"]["status"] == "OPEN_NOT_EVALUATED"
    assert data["generator"]["sha256"] == "0" * 64

    graph = json.loads(old_graph.read_text(encoding="utf-8"))
    nodes = {node["id"]: node for node in graph["nodes"]}
    node_id = "B45-1_body_trace_exporter_design"
    assert node_id not in nodes
    nodes[node_id] = {
        "id": node_id,
        "status": "source_audit_open",
        "dependencies": ["B45-1_610_body_trace_binding_obstruction"],
        "source": "../../artifacts/routeb_agent_body_trace_design_20260906T071911Z/README.md",
        "statement": (
            "Design and synthetic-probe the minimum pre-aggregation per-body Fourier "
            "trace and the aggregate=sum_body proof interface required to repair the "
            "610-row body attribution obstruction."
        ),
        "verification": {
            "readme": ref(readme), "manifest_schema": ref(manifest_schema),
            "trace_row_schema": ref(row_schema), "exporter": ref(exporter),
            "lean_interface": ref(lean), "verification": ref(verification),
            "probe_manifest": ref(probe_manifest), "readme_sha256": sha(readme),
            "manifest_schema_sha256": sha(manifest_schema), "trace_row_schema_sha256": sha(row_schema),
            "exporter_sha256": sha(exporter), "lean_interface_sha256": sha(lean),
            "verification_sha256": sha(verification), "probe_manifest_sha256": sha(probe_manifest),
            "python_probe": "TRACE_EQ_PASS", "trace_rows": 6, "aggregate_rows": 2,
            "lean_toolchain": "4.32.0 (not current pinned admission toolchain)",
            "source_binding": "OPEN_NOT_EVALUATED", "registry_eligible": False,
            "formal_certificate_allowed": False,
        },
        "closed_subclaims": [
            "minimum body/row/col/frequency/rational trace schema specified",
            "synthetic exact-Fraction aggregation probe passes",
            "aggregate=sum_body and DH body-evaluator theorem split specified",
            "omitted sparse keys are explicitly treated as exact zero",
        ],
        "open_bridges": [
            "run exporter on actual routeB generator before six-body accumulation",
            "replace synthetic generator hash with current source generator hook",
            "prove exact aggregate coverage for all 610 rows",
            "bind each body evaluator to deployed DH/Float64 semantics",
            "recompile interface under pinned Lean 4.33.1 and pass comparator",
        ],
        "semantic_boundary": "synthetic trace design/audit; no deployed source theorem",
    }
    graph["next_frontier"] = [
        "emit actual per-body Fourier trace from routeB generator",
        "prove aggregate=sum_body coverage over all 610 rows",
        "recompile body-trace interface under pinned Lean 4.33.1",
        "bind trace body evaluator to true DH source and Float64 comparator",
    ] + [x for x in graph.get("next_frontier", []) if "body trace" not in x.lower()]
    graph.update(schema="routeb-proposed-proof-dag-v86", supersedes="block45-obligations-v85.json")
    graph["nodes"] = list(nodes.values())
    ids = set(nodes)
    for node in nodes.values():
        for dep in node.get("dependencies", []):
            if dep not in ids:
                raise ValueError(f"dangling dependency: {dep}")

    shutil.copy2(store.path, backup)
    graph_path.write_text(json.dumps(graph, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    state.event(
        "routeb_body_trace_design_recorded",
        node_id=node_id, readme=ref(readme), exporter=ref(exporter),
        probe_manifest=ref(probe_manifest), python_probe="TRACE_EQ_PASS",
        lean_toolchain="4.32.0_not_admissible", source_binding_open=True,
        registry_eligible=False, formal_certificate_allowed=False,
        proposed_dag=ref(graph_path), broad_regression_run=False,
    )
    store.save(state)
    print({"revision": state.revision, "graph_nodes": len(nodes),
           "registry": len(state.registry), "formal_certificate_allowed": False})


if __name__ == "__main__":
    main()
