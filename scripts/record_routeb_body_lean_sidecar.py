"""Attach the pinned Lean exact body/aggregate sidecar without promoting it."""
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
    assert state.revision == 152 and not state.registry
    base = ROOT / "artifacts/routeb_agent_body_trace_lean_20260906T081507Z"
    report = base / "README.md"
    source = base / "RouteBExactAggregationB45.lean"
    receipt = base / "receipt.json"
    metadata = base / "generation_metadata.json"
    old_graph = ROOT / "artifacts/routeb_6dof/block45-obligations-v106.json"
    graph_path = ROOT / "artifacts/routeb_6dof/block45-obligations-v107.json"
    backup = ROOT / "artifacts/routeb_storage_checkpoint_20260905/state-before-revision153.json"
    for path in (report, source, receipt, metadata, old_graph):
        assert path.is_file(), path
    assert not graph_path.exists() and not backup.exists()
    data = json.loads(receipt.read_text(encoding="utf-8"))
    lean = data["lean"]
    audit = lean["axiom_audit"]
    assert data["status"] == "PASS"
    assert lean["exit_code"] == 0
    assert lean["toolchain"] == "leanprover/lean4:v4.33.1"
    assert lean["mathlib_git_head"] == "0df444a360eaa60ab8c11dca51a86af692955474"
    assert audit["sorryAx"] is False
    assert audit["admit"] is False
    assert audit["user_declared_axiom"] is False
    assert data["mutation_scope"]["original_project_modified"] is False

    graph = json.loads(old_graph.read_text(encoding="utf-8"))
    nodes = {node["id"]: node for node in graph["nodes"]}
    node_id = "B45-1_610_body_trace_binding_obstruction"
    node = nodes[node_id]
    node.setdefault("verification", {}).setdefault("lean_sidecars", []).append({
        "source": ref(source),
        "receipt": ref(receipt),
        "metadata": ref(metadata),
        "source_sha256": sha(source),
        "receipt_sha256": sha(receipt),
        "metadata_sha256": sha(metadata),
        "status": "PINNED_LEAN_SIDECAR_COMPILED_RUNTIME_BINDING_PENDING",
        "theorems": data["theorems"],
        "body_rows_encoded": data["source_checks"]["body_rows_encoded"],
        "unique_b45_keys_encoded": data["source_checks"]["unique_b45_keys_encoded"],
        "lean_exit_code": lean["exit_code"],
        "sorryAx": False,
        "admit": False,
        "user_declared_axiom": False,
        "registry_eligible": False,
        "formal_certificate_allowed": False,
    })
    node.setdefault("open_bridges", []).extend([
        "bind encoded body/aggregate theorem to authoritative deployed Julia body sink",
        "recompile the theorem from a source snapshot whose runtime hashes are part of the receipt",
    ])
    graph.update(schema="routeb-proposed-proof-dag-v107", supersedes="block45-obligations-v106.json")
    graph["nodes"] = list(nodes.values())
    ids = set(nodes)
    for candidate in nodes.values():
        for dependency in candidate.get("dependencies", []):
            if dependency not in ids:
                raise ValueError(f"dangling dependency: {dependency}")
    shutil.copy2(store.path, backup)
    graph_path.write_text(json.dumps(graph, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    state.event(
        "routeb_body_lean_sidecar_recorded", node_id=node_id,
        source=ref(source), receipt=ref(receipt), metadata=ref(metadata),
        source_sha256=sha(source), receipt_sha256=sha(receipt), metadata_sha256=sha(metadata),
        status="PINNED_LEAN_SIDECAR_COMPILED_RUNTIME_BINDING_PENDING",
        theorems=data["theorems"], body_rows_encoded=data["source_checks"]["body_rows_encoded"],
        unique_b45_keys_encoded=data["source_checks"]["unique_b45_keys_encoded"],
        lean_exit_code=lean["exit_code"], sorryAx=False, admit=False,
        user_declared_axiom=False, registry_promoted=False,
        formal_certificate_allowed=False, proposed_dag=ref(graph_path),
        broad_regression_run=False,
    )
    store.save(state)
    print({"revision": state.revision, "graph_nodes": len(nodes),
           "registry": len(state.registry), "formal_certificate_allowed": False})


if __name__ == "__main__":
    main()
