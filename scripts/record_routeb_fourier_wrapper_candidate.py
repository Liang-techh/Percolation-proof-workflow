"""Persist the successful pinned Lake wrapper for the Fourier aggregation seam."""
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
    assert state.revision == 112 and not state.registry
    base = ROOT / "examples/routeb_b45_source_mass_fourier_bridge_lean"
    source = base / "SourceMassFourierBridge.lean"
    olean = base / ".lake/build/lib/lean/SourceMassFourierBridge.olean"
    receipt = base / "compile_receipt.md"
    log = base / "output/run-pinned-20260906/terminal.log"
    lakefile = base / "lakefile.lean"
    old_graph = ROOT / "artifacts/routeb_6dof/block45-obligations-v68.json"
    graph_path = ROOT / "artifacts/routeb_6dof/block45-obligations-v69.json"
    backup = ROOT / "artifacts/routeb_storage_checkpoint_20260905/state-before-revision113.json"
    for path in (source, olean, receipt, log, lakefile, old_graph):
        assert path.is_file(), path
    assert not graph_path.exists() and not backup.exists()
    log_text = log.read_text(encoding="utf-8")
    receipt_text = receipt.read_text(encoding="utf-8")
    assert "EXIT_CODE=0" in log_text
    assert "compiled candidate" in receipt_text
    assert "Real output" in receipt_text
    assert "#print axioms" in log_text or "depends on axioms" in log_text

    graph = json.loads(old_graph.read_text(encoding="utf-8"))
    nodes = {node["id"]: node for node in graph["nodes"]}
    node_id = "B45-1_source_mass_fourier_aggregation_seam"
    node = nodes[node_id]
    assert node["status"] == "open_compile_blocked"
    evidence = node.setdefault("candidate_evidence", {})
    evidence.update({
        "compiled_receipt": True,
        "compile_receipt": {"path": str(receipt), "sha256": sha(receipt)},
        "compile_receipt_sha256": sha(receipt),
        "compile_log": {"path": str(log), "sha256": sha(log)},
        "olean_snapshot": True,
        "olean": {"path": str(olean), "sha256": sha(olean)},
        "olean_sha256": sha(olean),
        "compile_exit": 0,
        "standard_axioms_only": True,
    })
    node["status"] = "compiled_candidate_comparator_pending"
    node["failure_boundary"] = "compiled under pinned Lake wrapper; source and physical binding remain conditional"
    node["open_bridges"] = [
        bridge for bridge in node.get("open_bridges", [])
        if "Lake wrapper" not in bridge and "missing pinned compile" not in bridge
    ]
    node["open_bridges"].insert(0, "per-body DH/Jacobian/Fourier comparator premise")
    node["open_bridges"].insert(1, "full 610-row aggregate CSV binding")
    node["verification"] = {
        "source": ref(source), "olean": ref(olean), "receipt": ref(receipt),
        "log": ref(log), "lakefile": ref(lakefile),
        "source_sha256": sha(source), "olean_sha256": sha(olean),
        "receipt_sha256": sha(receipt), "log_sha256": sha(log),
        "compile_exit": 0, "verify_exit": 0,
        "standard_axioms_only": True, "registry_promoted": False,
        "comparator_accepted": False,
    }
    graph["next_frontier"] = [
        "B45-1 prove per-body or aggregate 610-row mass comparator",
        "B45-1 prove Fourier evaluator equals six-body contract sum",
    ] + [x for x in graph["next_frontier"] if "minimal Lake wrapper" not in x]
    graph.update(schema="routeb-proposed-proof-dag-v69", supersedes="block45-obligations-v68.json")
    graph["nodes"] = list(nodes.values())

    ids = set(nodes)
    seen = set()
    visiting = set()
    def visit(key):
        if key not in ids or key in visiting:
            raise ValueError("dangling dependency or cycle")
        if key in seen:
            return
        visiting.add(key)
        for dep in nodes[key].get("dependencies", []):
            visit(dep)
        visiting.remove(key)
        seen.add(key)
    for key in ids:
        visit(key)

    shutil.copy2(store.path, backup)
    graph_path.write_text(json.dumps(graph, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    state.event(
        "routeb_fourier_aggregation_compiled_candidate_recorded",
        source=ref(source), olean=ref(olean), receipt=ref(receipt), log=ref(log),
        source_sha256=sha(source), olean_sha256=sha(olean),
        receipt_sha256=sha(receipt), log_sha256=sha(log),
        compile_exit=0, verify_exit=0, standard_axioms_only=True,
        comparator_accepted=False, registry_promoted=False,
        conditional_h_body_preserved=True, csv_610_row_binding_open=True,
        float64_dh_binding_open=True, formal_certificate_allowed=False,
        proposed_dag=ref(graph_path), broad_regression_run=False,
    )
    store.save(state)
    print({"revision": state.revision, "graph_nodes": len(nodes),
           "registry": len(state.registry), "formal_certificate_allowed": False})


if __name__ == "__main__":
    main()
