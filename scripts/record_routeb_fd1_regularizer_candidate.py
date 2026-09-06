"""Persist the independently verified exact-real FD-1 leaf."""
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
    assert state.revision == 114 and not state.registry
    base = ROOT / "artifacts/routeb_fd1_regularizer_cancellation_20260906"
    source = base / "FD1RegularizerCancellation.lean"
    olean = base / "run-uovRuZwV/FD1RegularizerCancellation.olean"
    receipt = base / "FINAL_RECEIPT.md"
    receipt_json = base / "receipt.json"
    history = base / "ATTEMPT_HISTORY.md"
    old_graph = ROOT / "artifacts/routeb_6dof/block45-obligations-v70.json"
    graph_path = ROOT / "artifacts/routeb_6dof/block45-obligations-v71.json"
    backup = ROOT / "artifacts/routeb_storage_checkpoint_20260905/state-before-revision115.json"
    for path in (source, olean, receipt, receipt_json, history, old_graph):
        assert path.is_file(), path
    assert not graph_path.exists() and not backup.exists()
    receipt_text = receipt.read_text(encoding="utf-8")
    receipt_data = json.loads(receipt_json.read_text(encoding="utf-8"))
    source_text = source.read_text(encoding="utf-8")
    for marker in ("FD1RegularizerCancellation", "COMPILE_EXIT_CODE=0",
                   "VERIFY_EXIT_CODE=0", "SOURCE_RESTRICTION_CHECK=PASSED",
                   "FLOAT64_BINDING=OPEN", "REGISTRY_MUTATION=0"):
        assert marker in receipt_text or marker in source_text
    assert receipt_data["compile_exit_code"] == 0
    assert receipt_data["verify_exit_code"] == 0
    assert receipt_data["registry_mutation"] == 0
    assert not any(token in source_text for token in ("sorry", "admit", "axiom "))

    graph = json.loads(old_graph.read_text(encoding="utf-8"))
    nodes = {node["id"]: node for node in graph["nodes"]}
    node_id = "B45-FD-1_regularizer_cancellation"
    assert node_id not in nodes
    nodes[node_id] = {
        "id": node_id,
        "status": "compiled_candidate_comparator_pending",
        "dependencies": [],
        "source": "../../artifacts/routeb_fd1_regularizer_cancellation_20260906/FD1RegularizerCancellation.lean",
        "statement": (
            "Kernel-check exact-real cancellation of the same regularizer "
            "mu I_6 in the positive and negative central finite-difference "
            "mass calls, preserving full six-dimensional q/dq interfaces."
        ),
        "verification": {
            "source": ref(source), "olean": ref(olean),
            "receipt": ref(receipt), "receipt_json": ref(receipt_json),
            "attempt_history": ref(history),
            "source_sha256": sha(source), "olean_sha256": sha(olean),
            "receipt_sha256": sha(receipt), "receipt_json_sha256": sha(receipt_json),
            "compile_exit": 0, "verify_exit": 0,
            "standard_axioms_only": True, "source_restriction": "passed",
            "registry_promoted": False, "comparator_accepted": False,
        },
        "closed_subclaims": [
            "positive/negative mass-call regularizer cancellation",
            "central-FD quotient identity for arbitrary exact-real Mstruct",
            "full six-dimensional q and dq interfaces",
            "mu=1/1000000 and h=1/100000 retained",
        ],
        "open_bridges": [
            "deployed Float64 mass-call equivalence and rounding enclosure",
            "source finite-difference analytic remainder and operation bounds",
            "binding into the full C/G/FD contraction and physical comparator",
        ],
        "semantic_boundary": "exact-real algebra leaf only; no deployed Float64 binding",
    }
    subtree = nodes["B45-source_central_fd_binding_subtree"]
    subtree.setdefault("compiled_leaves", []).append(node_id)
    subtree.setdefault("exact_real_leaf_status", {})["FD-1"] = node_id
    subtree.setdefault("open_bridges", []).append("FD-1 deployed Float64 binding")
    graph["next_frontier"] = [
        "B45 FD-0, FD-2, FD-3, FD-4 exact-real source loop adapters",
        "B45 FD-5 analytic central-difference remainder bounds",
    ] + [x for x in graph["next_frontier"] if "FD-0..FD-4" not in x]
    graph.update(schema="routeb-proposed-proof-dag-v71", supersedes="block45-obligations-v70.json")
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
        "routeb_fd1_regularizer_compiled_candidate_recorded",
        source=ref(source), olean=ref(olean), receipt=ref(receipt),
        receipt_json=ref(receipt_json), history=ref(history),
        source_sha256=sha(source), olean_sha256=sha(olean),
        receipt_sha256=sha(receipt), receipt_json_sha256=sha(receipt_json),
        compile_exit=0, verify_exit=0, standard_axioms_only=True,
        comparator_accepted=False, registry_promoted=False,
        exact_real_only=True, float64_binding_open=True,
        formal_certificate_allowed=False, proposed_dag=ref(graph_path),
        broad_regression_run=False,
    )
    store.save(state)
    print({"revision": state.revision, "graph_nodes": len(nodes),
           "registry": len(state.registry), "formal_certificate_allowed": False})


if __name__ == "__main__":
    main()
