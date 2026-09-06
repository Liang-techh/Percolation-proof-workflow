"""Persist the compiled conditional full-state descriptor interface."""
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
    assert state.revision == 125 and not state.registry
    base = ROOT / "artifacts/routeb_agent_b45_fullstate_20260906_010406"
    source = base / "B45FullStateDescriptorInterface.lean"
    olean = base / "compile/B45FullStateDescriptorInterface.olean"
    receipt = base / "receipt.md"
    report = base / "obstruction_lemma_report.md"
    log = base / "compile/terminal.log"
    old_graph = ROOT / "artifacts/routeb_6dof/block45-obligations-v79.json"
    graph_path = ROOT / "artifacts/routeb_6dof/block45-obligations-v80.json"
    backup = ROOT / "artifacts/routeb_storage_checkpoint_20260905/state-before-revision126.json"
    for path in (source, olean, receipt, report, log, old_graph):
        assert path.is_file(), path
    assert not graph_path.exists() and not backup.exists()
    source_text = source.read_text(encoding="utf-8")
    receipt_text = receipt.read_text(encoding="utf-8")
    log_text = log.read_text(encoding="utf-8")
    assert "Compile exit code: `0`" in receipt_text
    assert "No `sorryAx`" in receipt_text
    assert "depends on axioms" in log_text
    assert not any(token in source_text for token in ("sorry", "admit", "axiom "))

    graph = json.loads(old_graph.read_text(encoding="utf-8"))
    nodes = {node["id"]: node for node in graph["nodes"]}
    node_id = "B45-5_fullstate_descriptor_terminal_interface"
    assert node_id not in nodes
    nodes[node_id] = {
        "id": node_id,
        "status": "compiled_candidate_comparator_pending",
        "dependencies": [
            "B45-5_descriptor_schur_residual_repair",
            "B45-FD-9_10_float64_potential_contraction_seam",
        ],
        "source": "../../artifacts/routeb_agent_b45_fullstate_20260906_010406/B45FullStateDescriptorInterface.lean",
        "statement": (
            "Kernel-check the conditional full-state descriptor interface: exact "
            "block residual transport, six-term residual budget, and explicit "
            "terminal comparator interface."
        ),
        "verification": {
            "source": ref(source), "olean": ref(olean), "receipt": ref(receipt),
            "report": ref(report), "compile_log": ref(log),
            "source_sha256": sha(source), "olean_sha256": sha(olean),
            "receipt_sha256": sha(receipt), "report_sha256": sha(report),
            "compile_log_sha256": sha(log), "compile_exit": 0, "verify_exit": 0,
            "sorry_ax": 0, "standard_axioms_only": True,
            "registry_promoted": False, "comparator_accepted": False,
        },
        "closed_subclaims": [
            "exact two-row descriptor block residual identity",
            "conditional six-term residual budget",
            "common-domain transport between descriptor interfaces",
            "explicit terminal storage-to-metric comparator interface",
        ],
        "open_bridges": [
            "complete bounded q/dq domain and first-exit continuation",
            "real external descriptor acceleration a_D and M_BD a_D bound",
            "deployed DH/Float64 C/G/FD/solve single-budget binding",
            "cellwise Schur remainder absorption",
            "actual terminal transfer and Route-B target inequality",
            "kc mismatch resolution between PMI model and deployed torque law",
        ],
        "semantic_boundary": "conditional exact-real descriptor/terminal interface; no M4 theorem",
    }
    graph["next_frontier"] = [
        "bind complete q/dq domain and external descriptor acceleration",
        "resolve deployed torque kc mismatch and source semantics",
        "absorb cellwise Schur remainder with one FD/solve budget",
        "prove first-exit continuation and actual terminal transfer",
    ] + [x for x in graph.get("next_frontier", []) if "full-state" not in x and "terminal" not in x]
    graph.update(schema="routeb-proposed-proof-dag-v80", supersedes="block45-obligations-v79.json")
    graph["nodes"] = list(nodes.values())
    ids = set(nodes)
    for node in nodes.values():
        for dep in node.get("dependencies", []):
            if dep not in ids:
                raise ValueError(f"dangling dependency: {dep}")

    shutil.copy2(store.path, backup)
    graph_path.write_text(json.dumps(graph, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    state.event(
        "routeb_b45_fullstate_interface_candidate_recorded",
        node_id=node_id, source=ref(source), olean=ref(olean), receipt=ref(receipt),
        source_sha256=sha(source), olean_sha256=sha(olean), receipt_sha256=sha(receipt),
        compile_exit=0, verify_exit=0, sorry_ax=0, standard_axioms_only=True,
        comparator_accepted=False, registry_promoted=False,
        complete_domain_open=True, terminal_transfer_open=True,
        formal_certificate_allowed=False, proposed_dag=ref(graph_path),
        broad_regression_run=False,
    )
    store.save(state)
    print({"revision": state.revision, "graph_nodes": len(nodes),
           "registry": len(state.registry), "formal_certificate_allowed": False})


if __name__ == "__main__":
    main()
