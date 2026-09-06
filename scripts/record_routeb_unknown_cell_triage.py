"""Attach the pinned UNKNOWN-cell triage interface to the P3 coverage node."""
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
    assert state.revision == 134 and not state.registry
    base = ROOT / "artifacts/routeb_agent_unknown_cell_triage_20260906T073550Z"
    source = base / "RouteBUnknownCellTriage.lean"
    olean = base / "RouteBUnknownCellTriage.olean"
    receipt = base / "receipt.json"
    report = base / "TRIAGE_REPORT.md"
    interface = base / "MINIMAL_CELL_WITNESS_FORMAT.md"
    compile_log = base / "compile.log"
    old_graph = ROOT / "artifacts/routeb_6dof/block45-obligations-v88.json"
    graph_path = ROOT / "artifacts/routeb_6dof/block45-obligations-v89.json"
    backup = ROOT / "artifacts/routeb_storage_checkpoint_20260905/state-before-revision135.json"
    for path in (source, olean, receipt, report, interface, compile_log, old_graph):
        assert path.is_file(), path
    assert not graph_path.exists() and not backup.exists()

    data = json.loads(receipt.read_text(encoding="utf-8"))
    assert data["status"] == "COMPILED_INTERFACE_ONLY"
    assert data["pinned_compile"]["compile_exit_code"] == 0
    assert data["pinned_compile"]["sorry_admit_user_axiom"] is False
    assert data["global_coverage_closed"] is False
    assert data["formal_certificate_allowed"] is False

    graph = json.loads(old_graph.read_text(encoding="utf-8"))
    nodes = {node["id"]: node for node in graph["nodes"]}
    node_id = "B45-P3_global_coverage_interval_interface"
    assert node_id in nodes
    node = nodes[node_id]
    verification = node.setdefault("verification", {})
    verification.setdefault("unknown_cell_triage", []).append({
        "source": ref(source), "olean": ref(olean), "receipt": ref(receipt),
        "report": ref(report), "interface": ref(interface), "compile_log": ref(compile_log),
        "source_sha256": sha(source), "olean_sha256": sha(olean),
        "receipt_sha256": sha(receipt), "report_sha256": sha(report),
        "interface_sha256": sha(interface), "compile_log_sha256": sha(compile_log),
        "compile_exit": 0, "sorry_admit_user_axiom": False,
        "lean_commit": data["pinned_compile"]["lean_commit"],
        "mathlib_commit": data["pinned_compile"]["mathlib_commit"],
        "unknown_inverse": data["triage"]["unknown_inverse"],
        "unknown_domain_boundary": data["triage"]["unknown_domain_boundary"],
        "unknown_bracket": data["triage"]["unknown_bracket"],
        "accepted_global_cells": data["triage"]["accepted_global_cells"],
        "status": "COMPILED_INTERFACE_ONLY",
        "registry_eligible": False, "formal_certificate_allowed": False,
    })
    node.setdefault("open_bridges", []).extend([
        "instantiate an exact current-source witness for at least one UNKNOWN_INVERSE cell",
        "bind triage payload to deployed DH/FD/Float64 semantics before any global-cell closure",
    ])
    graph.update(schema="routeb-proposed-proof-dag-v89", supersedes="block45-obligations-v88.json")
    graph["nodes"] = list(nodes.values())
    ids = set(nodes)
    for candidate in nodes.values():
        for dependency in candidate.get("dependencies", []):
            if dependency not in ids:
                raise ValueError(f"dangling dependency: {dependency}")

    shutil.copy2(store.path, backup)
    graph_path.write_text(json.dumps(graph, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    state.event(
        "routeb_unknown_cell_triage_recorded",
        node_id=node_id, source=ref(source), olean=ref(olean), receipt=ref(receipt),
        compile_exit=0, sorry_admit_user_axiom=False,
        unknown_inverse=data["triage"]["unknown_inverse"],
        unknown_domain_boundary=data["triage"]["unknown_domain_boundary"],
        unknown_bracket=data["triage"]["unknown_bracket"],
        accepted_global_cells=0, registry_promoted=False,
        formal_certificate_allowed=False, proposed_dag=ref(graph_path),
        broad_regression_run=False,
    )
    store.save(state)
    print({"revision": state.revision, "graph_nodes": len(nodes),
           "registry": len(state.registry), "formal_certificate_allowed": False})


if __name__ == "__main__":
    main()
