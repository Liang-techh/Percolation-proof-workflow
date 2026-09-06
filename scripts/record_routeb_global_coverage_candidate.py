"""Persist the global-coverage interface and its fail-closed checker result."""
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
    assert state.revision == 128 and not state.registry
    base = ROOT / "artifacts/routeb_agent_global_coverage_20260906T011623Z"
    source = base / "RouteBGlobalCoverageInterface.lean"
    olean = base / "RouteBGlobalCoverageInterface.olean"
    report = base / "REPORT.md"
    receipt = base / "receipt.json"
    log = base / "compile.log"
    sums = base / "SHA256SUMS.csv"
    old_graph = ROOT / "artifacts/routeb_6dof/block45-obligations-v82.json"
    graph_path = ROOT / "artifacts/routeb_6dof/block45-obligations-v83.json"
    backup = ROOT / "artifacts/routeb_storage_checkpoint_20260905/state-before-revision129.json"
    for path in (source, olean, report, receipt, log, sums, old_graph):
        assert path.is_file(), path
    assert not graph_path.exists() and not backup.exists()
    data = json.loads(receipt.read_text(encoding="utf-8"))
    assert data["status"] == "blocked_global_true_dh_coverage"
    assert data["lean"]["compile_exit_code"] == 0
    assert data["lean"]["sorry_admit_user_axiom"] is False
    assert data["coverage"]["geometry_cells"] == 8192
    assert data["coverage"]["accepted_global_cells"] == 0
    assert data["coverage"]["coverage_complete"] is False
    assert data["formal_certificate_allowed"] is False

    graph = json.loads(old_graph.read_text(encoding="utf-8"))
    nodes = {node["id"]: node for node in graph["nodes"]}
    node_id = "B45-P3_global_coverage_interval_interface"
    assert node_id not in nodes
    nodes[node_id] = {
        "id": node_id,
        "status": "compiled_candidate_comparator_pending",
        "dependencies": [
            "B45-5_fullstate_descriptor_terminal_interface",
            "B45-8_terminal_flowpipe_first_exit_interface",
        ],
        "source": "../../artifacts/routeb_agent_global_coverage_20260906T011623Z/RouteBGlobalCoverageInterface.lean",
        "statement": (
            "Kernel-check the conditional interval/Taylor and robust-Schur coverage "
            "interface, together with the global coverage receipt and mass coercivity "
            "screen for Route-B block-(4,5)."
        ),
        "verification": {
            "source": ref(source), "olean": ref(olean), "report": ref(report),
            "receipt": ref(receipt), "compile_log": ref(log), "sha256s": ref(sums),
            "source_sha256": sha(source), "olean_sha256": sha(olean),
            "report_sha256": sha(report), "receipt_sha256": sha(receipt),
            "compile_log_sha256": sha(log), "compile_exit": 0, "verify_exit": 0,
            "sorry_ax": 0, "standard_axioms_only": True,
            "registry_promoted": False, "comparator_accepted": False,
            "geometry_cells": 8192, "accepted_global_cells": 0,
            "unknown_inverse": 8191, "unknown_domain_boundary": 512,
            "unknown_bracket": 511, "coverage_complete": False,
        },
        "closed_subclaims": [
            "conditional Taylor-cell interval transport",
            "global regularized mass lower bound 1/1000000",
            "conditional scalar robust-Schur absorption",
            "geometry partition count and checker receipt are frozen",
        ],
        "open_bridges": [
            "cellwise inverse guards and full-state domain coverage",
            "true-DH C/G/FD/solve source binding",
            "descriptor a_D and M_BD a_D enclosure",
            "uniform residual absorption and strict PSD/Gram proof",
            "first-exit continuation and direct terminal target",
        ],
        "semantic_boundary": "conditional coverage/Schur interface; global true-DH coverage blocked",
    }
    graph["next_frontier"] = [
        "resolve 8191 UNKNOWN_INVERSE cells with rational inverse witnesses",
        "resolve 512 UNKNOWN_DOMAIN_BOUNDARY cells and full-state domain",
        "resolve 511 UNKNOWN_BRACKET cells and true-DH source binding",
        "connect cellwise residual/descriptor bounds to flowpipe and terminal target",
    ] + [x for x in graph.get("next_frontier", []) if "coverage" not in x.lower() and "inverse" not in x.lower()]
    graph.update(schema="routeb-proposed-proof-dag-v83", supersedes="block45-obligations-v82.json")
    graph["nodes"] = list(nodes.values())
    ids = set(nodes)
    for node in nodes.values():
        for dep in node.get("dependencies", []):
            if dep not in ids:
                raise ValueError(f"dangling dependency: {dep}")

    shutil.copy2(store.path, backup)
    graph_path.write_text(json.dumps(graph, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    state.event(
        "routeb_global_coverage_interface_recorded",
        node_id=node_id, source=ref(source), olean=ref(olean), receipt=ref(receipt),
        source_sha256=sha(source), olean_sha256=sha(olean), receipt_sha256=sha(receipt),
        compile_exit=0, verify_exit=0, sorry_ax=0, standard_axioms_only=True,
        geometry_cells=8192, accepted_global_cells=0, coverage_complete=False,
        unknown_inverse=8191, unknown_domain_boundary=512, unknown_bracket=511,
        comparator_accepted=False, registry_promoted=False,
        formal_certificate_allowed=False, proposed_dag=ref(graph_path),
        broad_regression_run=False,
    )
    store.save(state)
    print({"revision": state.revision, "graph_nodes": len(nodes),
           "registry": len(state.registry), "formal_certificate_allowed": False})


if __name__ == "__main__":
    main()
