"""Persist the independently compiled conditional FD-8 tensor seam."""
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
    assert state.revision == 121 and not state.registry
    base = ROOT / "artifacts/routeb_fd8_tensor_christoffel_enclosure_20260906"
    source = base / "FD8TensorChristoffelEnclosure.lean"
    olean = base / "run-pinned/FD8TensorChristoffelEnclosure.olean"
    receipt = base / "FINAL_RECEIPT.md"
    receipt_json = base / "receipt.json"
    old_graph = ROOT / "artifacts/routeb_6dof/block45-obligations-v75.json"
    graph_path = ROOT / "artifacts/routeb_6dof/block45-obligations-v76.json"
    backup = ROOT / "artifacts/routeb_storage_checkpoint_20260905/state-before-revision122.json"
    for path in (source, olean, receipt, receipt_json, old_graph):
        assert path.is_file(), path
    assert not graph_path.exists() and not backup.exists()
    data = json.loads(receipt_json.read_text(encoding="utf-8"))
    source_text = source.read_text(encoding="utf-8")
    assert data["compile_exit_code"] == 0 and data["sorry_ax"] == 0
    assert data["state_mutation"] == 0 and data["registry_mutation"] == 0
    assert data["julia_float64_binding"] == "open"
    assert not any(token in source_text for token in ("sorry", "admit", "axiom "))

    graph = json.loads(old_graph.read_text(encoding="utf-8"))
    nodes = {node["id"]: node for node in graph["nodes"]}
    node_id = "B45-FD-8_tensor_christoffel_enclosure"
    assert node_id not in nodes
    nodes[node_id] = {
        "id": node_id,
        "status": "compiled_candidate_comparator_pending",
        "dependencies": ["B45-FD-6_7_float64_enclosure"],
        "source": "../../artifacts/routeb_fd8_tensor_christoffel_enclosure_20260906/FD8TensorChristoffelEnclosure.lean",
        "statement": (
            "Kernel-check the conditional FD-8 tensor/Christoffel seam: entrywise "
            "tensor error, three-term Christoffel budget, per-(j,k) product "
            "bound, and the complete finite six-dimensional contraction bound."
        ),
        "verification": {
            "source": ref(source), "olean": ref(olean),
            "receipt": ref(receipt), "receipt_json": ref(receipt_json),
            "source_sha256": sha(source), "olean_sha256": sha(olean),
            "receipt_sha256": sha(receipt), "receipt_json_sha256": sha(receipt_json),
            "compile_exit": 0, "verify_exit": 0, "sorry_ax": 0,
            "standard_axioms_only": True, "registry_promoted": False,
            "comparator_accepted": False,
        },
        "closed_subclaims": [
            "entrywise tensor enclosure over Fin 6",
            "three-term Christoffel error budget",
            "per-(j,k) contraction product enclosure",
            "complete finite double-sum contraction enclosure",
        ],
        "open_bridges": [
            "actual Julia Float64 tensor/Christoffel operation semantics",
            "deployed DH/COM/Jacobian source binding",
            "domain-wide finite/non-NaN and interval enclosure certificate",
            "source comparator acceptance and final C/G/FD aggregation",
        ],
        "semantic_boundary": "conditional tensor/contraction interface; no deployed Float64 equivalence",
    }
    subtree = nodes["B45-source_central_fd_binding_subtree"]
    subtree.setdefault("compiled_leaves", []).append(node_id)
    subtree.setdefault("float64_leaf_status", {})["FD-8"] = node_id
    graph["next_frontier"] = [
        "B45 bind actual Julia Float64 mass/tensor/Christoffel calls",
        "B45 FD-9/FD-10 potential and contraction enclosures",
    ] + [x for x in graph.get("next_frontier", []) if "FD-8" not in x]
    graph.update(schema="routeb-proposed-proof-dag-v76", supersedes="block45-obligations-v75.json")
    graph["nodes"] = list(nodes.values())

    ids = set(nodes)
    seen, visiting = set(), set()
    def visit(key):
        if key not in ids:
            raise ValueError("dangling dependency")
        if key in visiting:
            raise ValueError("cycle")
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
        "routeb_fd8_tensor_candidate_recorded",
        source=ref(source), olean=ref(olean), receipt=ref(receipt),
        receipt_json=ref(receipt_json), source_sha256=sha(source),
        olean_sha256=sha(olean), receipt_sha256=sha(receipt),
        receipt_json_sha256=sha(receipt_json), compile_exit=0, verify_exit=0,
        sorry_ax=0, standard_axioms_only=True, comparator_accepted=False,
        registry_promoted=False, conditional_contract_only=True,
        deployed_float64_binding_open=True, formal_certificate_allowed=False,
        proposed_dag=ref(graph_path), broad_regression_run=False,
    )
    store.save(state)
    print({"revision": state.revision, "graph_nodes": len(nodes),
           "registry": len(state.registry), "formal_certificate_allowed": False})


if __name__ == "__main__":
    main()
