"""Persist the independently verified exact-real FD-5 remainder leaf."""
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
    assert state.revision == 118 and not state.registry
    base = ROOT / "artifacts/routeb_fd5_analytic_remainder_20260906"
    source = base / "FD5AnalyticRemainder.lean"
    olean = base / "output/run-4mRwiktj/FD5AnalyticRemainder.olean"
    receipt = base / "FINAL_RECEIPT.md"
    receipt_json = base / "receipt.json"
    history = base / "ATTEMPT_HISTORY.md"
    log = base / "output/run-4mRwiktj/verify.log"
    old_graph = ROOT / "artifacts/routeb_6dof/block45-obligations-v73.json"
    graph_path = ROOT / "artifacts/routeb_6dof/block45-obligations-v74.json"
    backup = ROOT / "artifacts/routeb_storage_checkpoint_20260905/state-before-revision119.json"
    for path in (source, olean, receipt, receipt_json, history, log, old_graph):
        assert path.is_file(), path
    assert not graph_path.exists() and not backup.exists()
    data = json.loads(receipt_json.read_text(encoding="utf-8"))
    source_text = source.read_text(encoding="utf-8")
    assert data["compile_exit_code"] == 0
    assert data["verify_exit_code"] == 0
    assert data["source_restriction"] == "passed"
    assert data["registry_mutation"] == 0
    assert data["formal_certificate_allowed"] is False
    assert not any(token in source_text for token in ("sorry", "admit", "axiom "))
    log_text = log.read_text(encoding="utf-8")
    assert "FD5AnalyticRemainder_COMPILE_EXIT_CODE=0" in log_text
    assert "VERIFY_EXIT_CODE=0" in log_text

    graph = json.loads(old_graph.read_text(encoding="utf-8"))
    nodes = {node["id"]: node for node in graph["nodes"]}
    node_id = "B45-FD-5_analytic_central_fd_remainder"
    assert node_id not in nodes
    nodes[node_id] = {
        "id": node_id,
        "status": "compiled_candidate_comparator_pending",
        "dependencies": ["B45-FD-2_tensor_extensionality"],
        "source": "../../artifacts/routeb_fd5_analytic_remainder_20260906/FD5AnalyticRemainder.lean",
        "statement": (
            "Kernel-check the exact-real central finite-difference remainder "
            "bound |(f(x+h)-f(x-h))/(2h)-f1| <= h^2 B/6 from explicit third-order "
            "Taylor remainder premises, while retaining full q/dq and mass/potential interfaces."
        ),
        "verification": {
            "source": ref(source), "olean": ref(olean),
            "receipt": ref(receipt), "receipt_json": ref(receipt_json),
            "attempt_history": ref(history), "log": ref(log),
            "source_sha256": sha(source), "olean_sha256": sha(olean),
            "receipt_sha256": sha(receipt), "receipt_json_sha256": sha(receipt_json),
            "compile_exit": 0, "verify_exit": 0,
            "standard_axioms_only": True, "source_restriction": "passed",
            "registry_promoted": False, "comparator_accepted": False,
        },
        "closed_subclaims": [
            "central-FD h^2 B/6 bound from two Taylor remainder premises",
            "exact-real mass-entry and potential-coordinate interfaces",
            "h=1/100000 and mu=1/1000000 retained",
            "full six-dimensional q/dq interface retained",
        ],
        "open_bridges": [
            "derive C^3 and third-derivative bounds for concrete DH source",
            "IEEE-754/Float64 and trigonometric enclosure",
            "bind analytic remainder to deployed C/G/FD source calls",
        ],
        "semantic_boundary": "exact-real analytic interface only; source regularity and Float64 binding remain open",
    }
    subtree = nodes["B45-source_central_fd_binding_subtree"]
    subtree.setdefault("compiled_leaves", []).append(node_id)
    subtree.setdefault("exact_real_leaf_status", {})["FD-5"] = node_id
    graph["next_frontier"] = [
        "B45 FD-0, FD-3, FD-4 exact-real source loop adapters",
        "B45 FD-6..FD-10 Float64 operation/FD/contraction enclosures",
        "B45 derive concrete DH C^3 and third-derivative bounds",
    ] + [x for x in graph["next_frontier"] if "FD-5 analytic" not in x and "FD-0, FD-3, FD-4" not in x]
    graph.update(schema="routeb-proposed-proof-dag-v74", supersedes="block45-obligations-v73.json")
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
        "routeb_fd5_analytic_remainder_compiled_candidate_recorded",
        source=ref(source), olean=ref(olean), receipt=ref(receipt),
        receipt_json=ref(receipt_json), history=ref(history), log=ref(log),
        source_sha256=sha(source), olean_sha256=sha(olean),
        receipt_sha256=sha(receipt), receipt_json_sha256=sha(receipt_json),
        compile_exit=0, verify_exit=0, standard_axioms_only=True,
        comparator_accepted=False, registry_promoted=False,
        exact_real_only=True, concrete_c3_binding_open=True,
        float64_binding_open=True, formal_certificate_allowed=False,
        proposed_dag=ref(graph_path), broad_regression_run=False,
    )
    store.save(state)
    print({"revision": state.revision, "graph_nodes": len(nodes),
           "registry": len(state.registry), "formal_certificate_allowed": False})


if __name__ == "__main__":
    main()
