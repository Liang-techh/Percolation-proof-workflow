"""Persist the independently verified exact-real FD-2 tensor leaf."""
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
    assert state.revision == 116 and not state.registry
    base = ROOT / "artifacts/routeb_fd2_tensor_extensionality_20260906"
    source = base / "FD2TensorExtensionality.lean"
    olean = base / "run-pinned/FD2TensorExtensionality.olean"
    receipt = base / "receipt.json"
    log = base / "run-pinned/compile.log"
    history = base / "ATTEMPT_HISTORY.md"
    old_graph = ROOT / "artifacts/routeb_6dof/block45-obligations-v71.json"
    graph_path = ROOT / "artifacts/routeb_6dof/block45-obligations-v72.json"
    backup = ROOT / "artifacts/routeb_storage_checkpoint_20260905/state-before-revision117.json"
    for path in (source, olean, receipt, log, history, old_graph):
        assert path.is_file(), path
    assert not graph_path.exists() and not backup.exists()
    receipt_data = json.loads(receipt.read_text(encoding="utf-8"))
    source_text = source.read_text(encoding="utf-8")
    assert receipt_data["compile_exit_code"] == 0
    assert receipt_data["verify_exit_code"] == 0
    assert receipt_data["source_restriction_check"] == "PASSED"
    assert receipt_data["claims"]["registry_promoted"] is False
    assert receipt_data["claims"]["main_state_mutated"] is False
    assert not any(token in source_text for token in ("sorry", "admit", "axiom "))
    log_text = log.read_text(encoding="utf-8")
    assert "RouteBFD2TensorExtensionality.tensor_extensionality" in log_text

    graph = json.loads(old_graph.read_text(encoding="utf-8"))
    nodes = {node["id"]: node for node in graph["nodes"]}
    node_id = "B45-FD-2_tensor_extensionality"
    assert node_id not in nodes
    nodes[node_id] = {
        "id": node_id,
        "status": "compiled_candidate_comparator_pending",
        "dependencies": ["B45-FD-1_regularizer_cancellation"],
        "source": "../../artifacts/routeb_fd2_tensor_extensionality_20260906/FD2TensorExtensionality.lean",
        "statement": (
            "Kernel-check the exact-real FD-2 tensor seam over full six-dimensional "
            "q/dq: Fin-6 index transport, matrix and third-order tensor "
            "extensionality, central-FD entry equality, and Christoffel contraction."
        ),
        "verification": {
            "source": ref(source), "olean": ref(olean),
            "receipt": ref(receipt), "log": ref(log),
            "attempt_history": ref(history),
            "source_sha256": sha(source), "olean_sha256": sha(olean),
            "receipt_sha256": sha(receipt),
            "compile_exit": 0, "verify_exit": 0,
            "standard_axioms_only": True, "source_restriction": "passed",
            "registry_promoted": False, "comparator_accepted": False,
        },
        "closed_subclaims": [
            "Fin-6 Julia/Lean index transport",
            "matrix extensionality",
            "third-order tensor extensionality",
            "central-FD entry and tensor equality",
            "full-state dq contraction and Christoffel congruence",
        ],
        "open_bridges": [
            "deployed Julia Float64 tensor and central-FD operation binding",
            "analytic remainder and IEEE-754 enclosure",
            "physical DH C/G source comparator",
        ],
        "semantic_boundary": "exact-real tensor algebra only; no deployed Float64 binding",
    }
    subtree = nodes["B45-source_central_fd_binding_subtree"]
    subtree.setdefault("compiled_leaves", []).append(node_id)
    subtree.setdefault("exact_real_leaf_status", {})["FD-2"] = node_id
    graph["next_frontier"] = [
        "B45 FD-0, FD-3, FD-4 exact-real source loop adapters",
        "B45 FD-5 analytic central-difference remainder bounds",
    ] + [x for x in graph["next_frontier"] if "FD-0, FD-2, FD-3" not in x]
    graph.update(schema="routeb-proposed-proof-dag-v72", supersedes="block45-obligations-v71.json")
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
        "routeb_fd2_tensor_extensionality_compiled_candidate_recorded",
        source=ref(source), olean=ref(olean), receipt=ref(receipt), log=ref(log),
        source_sha256=sha(source), olean_sha256=sha(olean), receipt_sha256=sha(receipt),
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
