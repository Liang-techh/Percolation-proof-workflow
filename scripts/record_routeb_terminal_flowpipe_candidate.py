"""Persist the conditional terminal/flowpipe/first-exit interface candidate."""
import hashlib
import json
import re
import shutil

from record_routeb_port_progress import ROOT, ref
from percolation_workflow.store import StateStore


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    store = StateStore(ROOT / "artifacts/routeb_6dof/state.json")
    state = store.load()
    assert state.revision == 127 and not state.registry
    base = ROOT / "artifacts/routeb_agent_terminal_flowpipe_20260906T070808Z"
    source = base / "RouteBTerminalFlowpipe.lean"
    olean = base / "run-pinned-bBk77iRR/RouteBTerminalFlowpipe.olean"
    receipt = base / "FINAL_RECEIPT.md"
    boundary = base / "DAG_BOUNDARY.md"
    log = base / "run-pinned-bBk77iRR/compile.log"
    old_graph = ROOT / "artifacts/routeb_6dof/block45-obligations-v81.json"
    graph_path = ROOT / "artifacts/routeb_6dof/block45-obligations-v82.json"
    backup = ROOT / "artifacts/routeb_storage_checkpoint_20260905/state-before-revision128.json"
    for path in (source, olean, receipt, boundary, log, old_graph):
        assert path.is_file(), path
    assert not graph_path.exists() and not backup.exists()
    receipt_text = receipt.read_text(encoding="utf-8")
    source_text = source.read_text(encoding="utf-8")
    log_text = log.read_text(encoding="utf-8")
    assert "COMPILE_EXIT_CODE=0" in receipt_text
    assert "SOURCE_RESTRICTION_CHECK=PASSED" in receipt_text
    assert "not closed" in receipt_text
    assert "COMPILE_EXIT_CODE=0" in log_text
    assert not re.search(r"\b(?:sorry|admit|axiom)\b", source_text)

    graph = json.loads(old_graph.read_text(encoding="utf-8"))
    nodes = {node["id"]: node for node in graph["nodes"]}
    node_id = "B45-8_terminal_flowpipe_first_exit_interface"
    assert node_id not in nodes
    nodes[node_id] = {
        "id": node_id,
        "status": "compiled_candidate_comparator_pending",
        "dependencies": ["B45-5_fullstate_descriptor_terminal_interface"],
        "source": "../../artifacts/routeb_agent_terminal_flowpipe_20260906T070808Z/RouteBTerminalFlowpipe.lean",
        "statement": (
            "Kernel-check the conditional first-exit barrier and terminal-transfer "
            "interface: continuity/IVT flowpipe exclusion plus energy-to-terminal "
            "comparison under explicit premises."
        ),
        "verification": {
            "source": ref(source), "olean": ref(olean), "receipt": ref(receipt),
            "boundary": ref(boundary), "compile_log": ref(log),
            "source_sha256": sha(source), "olean_sha256": sha(olean),
            "receipt_sha256": sha(receipt), "boundary_sha256": sha(boundary),
            "compile_log_sha256": sha(log), "compile_exit": 0, "verify_exit": 0,
            "sorry_ax": 0, "standard_axioms_only": True,
            "registry_promoted": False, "comparator_accepted": False,
        },
        "closed_subclaims": [
            "continuity/IVT boundary-barrier implication",
            "conditional first-exit flowpipe exclusion",
            "conditional energy-to-terminal metric comparison",
            "explicit separation of numeric gate from deployed source theorem",
        ],
        "open_bridges": [
            "actual rounded RHS existence and continuation through the horizon",
            "uniform prefix residual/energy budget over every initial state and ramp",
            "full domain coverage and strict boundary exclusion for true DH",
            "direct terminal qpoly comparison with the original target",
            "source comparator and kernel registry admission",
        ],
        "semantic_boundary": "conditional first-exit/terminal interface; original M4 remains open",
    }
    graph["next_frontier"] = [
        "prove true-DH rounded RHS regularity and continuation",
        "absorb all residuals uniformly on the full prefix domain",
        "establish direct terminal qpoly bound at T=1",
        "run source comparator and final strict admission",
    ] + [x for x in graph.get("next_frontier", []) if "first-exit" not in x and "terminal" not in x]
    graph.update(schema="routeb-proposed-proof-dag-v82", supersedes="block45-obligations-v81.json")
    graph["nodes"] = list(nodes.values())
    ids = set(nodes)
    for node in nodes.values():
        for dep in node.get("dependencies", []):
            if dep not in ids:
                raise ValueError(f"dangling dependency: {dep}")

    shutil.copy2(store.path, backup)
    graph_path.write_text(json.dumps(graph, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    state.event(
        "routeb_terminal_flowpipe_candidate_recorded",
        node_id=node_id, source=ref(source), olean=ref(olean), receipt=ref(receipt),
        source_sha256=sha(source), olean_sha256=sha(olean), receipt_sha256=sha(receipt),
        compile_exit=0, verify_exit=0, sorry_ax=0, standard_axioms_only=True,
        comparator_accepted=False, registry_promoted=False,
        actual_flowpipe_open=True, terminal_comparison_open=True,
        formal_certificate_allowed=False, proposed_dag=ref(graph_path),
        broad_regression_run=False,
    )
    store.save(state)
    print({"revision": state.revision, "graph_nodes": len(nodes),
           "registry": len(state.registry), "formal_certificate_allowed": False})


if __name__ == "__main__":
    main()
