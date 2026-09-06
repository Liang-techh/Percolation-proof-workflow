"""Persist the independently compiled exact-real B45-5 Schur repair leaf."""
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
    assert state.revision == 113 and not state.registry
    base = ROOT / "artifacts/routeb_b45_5_minimal_interface_20260906/output/audit-repair-20260906"
    source = base / "B45SchurResidualRepair.lean"
    olean = base / "B45SchurResidualRepair.olean"
    receipt = base / "compile-receipt.md"
    log = base / "compile.log"
    old_graph = ROOT / "artifacts/routeb_6dof/block45-obligations-v69.json"
    graph_path = ROOT / "artifacts/routeb_6dof/block45-obligations-v70.json"
    backup = ROOT / "artifacts/routeb_storage_checkpoint_20260905/state-before-revision114.json"
    for path in (source, olean, receipt, log, old_graph):
        assert path.is_file(), path
    assert not graph_path.exists() and not backup.exists()
    receipt_text = receipt.read_text(encoding="utf-8")
    log_text = log.read_text(encoding="utf-8")
    assert "Status: PASS" in receipt_text
    assert "All four Lean invocations exited with code `0`" in receipt_text
    assert "SOURCE_RESTRICTION_CHECK=PASSED" in receipt_text
    assert "MAIN_STATE_MODIFIED=NO" in receipt_text
    assert "sorryAx" not in log_text
    source_text = source.read_text(encoding="utf-8")
    for marker in ("exact_descriptor_residual", "schur_remainder_bound", "remote_term_transport"):
        assert marker in source_text
    assert not any(token in source_text for token in ("sorry", "admit", "axiom "))

    graph = json.loads(old_graph.read_text(encoding="utf-8"))
    nodes = {node["id"]: node for node in graph["nodes"]}
    node_id = "B45-5_descriptor_schur_residual_repair"
    assert node_id not in nodes
    nodes[node_id] = {
        "id": node_id,
        "status": "compiled_candidate_comparator_pending",
        "dependencies": [
            "B45-5_minimal_fullstate_descriptor_interface",
            "B45-5_descriptor_terms_adapter",
            "B45-5_residual_decomposition_exact_lean",
        ],
        "source": "../../artifacts/routeb_b45_5_minimal_interface_20260906/output/audit-repair-20260906/B45SchurResidualRepair.lean",
        "statement": (
            "Kernel-check the exact-real descriptor/Schur residual repair: a "
            "binding structure, exact descriptor residual decomposition, a "
            "conditional Schur remainder bound, and transport of a bounded "
            "remote term."
        ),
        "verification": {
            "source": ref(source), "olean": ref(olean),
            "receipt": ref(receipt), "log": ref(log),
            "source_sha256": sha(source), "olean_sha256": sha(olean),
            "receipt_sha256": sha(receipt), "log_sha256": sha(log),
            "compile_exit": 0, "verify_exit": 0,
            "standard_axioms_only": True,
            "source_restriction": "passed",
            "registry_promoted": False,
            "comparator_accepted": False,
        },
        "closed_subclaims": [
            "descriptor residual binding structure",
            "exact six-term residual decomposition transport",
            "conditional Schur remainder inequality",
            "bounded remote-term transport",
        ],
        "open_bridges": [
            "bind actual deployed Float64 C/G/FD outputs",
            "prove cellwise PMI/Schur bound over the covered first-exit domain",
            "prove source comparator and reachability/terminal-transfer obligations",
        ],
        "semantic_boundary": "exact-real conditional repair only; no physical or Float64 binding",
    }
    gate = nodes["B45-5_model_replacement_gate"]
    gate.setdefault("compiled_precursors", []).append(node_id)
    gate.setdefault("open_precursors", []).append(node_id)
    gate["descriptor_schur_repair_candidate"] = node_id
    graph["next_frontier"] = [
        "B45-5 bind actual source C/G/FD outputs into DescriptorSchurInterface",
        "B45-5 prove strict Schur remote bound over covered domain",
    ] + [x for x in graph["next_frontier"] if "instantiate DescriptorSchurInterface" not in x]
    graph.update(schema="routeb-proposed-proof-dag-v70", supersedes="block45-obligations-v69.json")
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
        "routeb_b45_schur_repair_compiled_candidate_recorded",
        source=ref(source), olean=ref(olean), receipt=ref(receipt), log=ref(log),
        source_sha256=sha(source), olean_sha256=sha(olean),
        receipt_sha256=sha(receipt), log_sha256=sha(log),
        compile_exit=0, verify_exit=0, standard_axioms_only=True,
        comparator_accepted=False, registry_promoted=False,
        exact_real_conditional_only=True, physical_float64_binding_open=True,
        cellwise_pmi_bound_open=True, formal_certificate_allowed=False,
        proposed_dag=ref(graph_path), broad_regression_run=False,
    )
    store.save(state)
    print({"revision": state.revision, "graph_nodes": len(nodes),
           "registry": len(state.registry), "formal_certificate_allowed": False})


if __name__ == "__main__":
    main()
