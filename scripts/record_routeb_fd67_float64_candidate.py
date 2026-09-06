"""Persist the independently verified conditional FD-6/FD-7 seam."""
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
    assert state.revision == 119 and not state.registry
    base = ROOT / "artifacts/routeb_fd6_fd7_float64_enclosure_20260906"
    source = base / "FD67Float64Enclosure.lean"
    olean = base / "run-pinned/FD67Float64Enclosure.olean"
    receipt = base / "FINAL_RECEIPT.md"
    receipt_json = base / "receipt.json"
    log = base / "run-pinned/compile.log"
    old_graph = ROOT / "artifacts/routeb_6dof/block45-obligations-v74.json"
    graph_path = ROOT / "artifacts/routeb_6dof/block45-obligations-v75.json"
    backup = ROOT / "artifacts/routeb_storage_checkpoint_20260905/state-before-revision120.json"
    for path in (source, olean, receipt, receipt_json, log, old_graph):
        assert path.is_file(), path
    assert not graph_path.exists() and not backup.exists()
    data = json.loads(receipt_json.read_text(encoding="utf-8"))
    source_text = source.read_text(encoding="utf-8")
    assert data["compile_exit_code"] == 0
    assert data["verify_exit_code"] == 0
    assert data["source_restriction_check"] == "passed"
    assert data["registry_mutation"] == 0
    assert data["float64_source_binding"] == "open"
    assert not any(token in source_text for token in ("sorry", "admit", "axiom "))
    log_text = log.read_text(encoding="utf-8")
    assert "RouteBFD67Float64Enclosure.central_fd_entry_enclosure" in log_text

    graph = json.loads(old_graph.read_text(encoding="utf-8"))
    nodes = {node["id"]: node for node in graph["nodes"]}
    node_id = "B45-FD-6_7_float64_enclosure"
    assert node_id not in nodes
    nodes[node_id] = {
        "id": node_id,
        "status": "compiled_candidate_comparator_pending",
        "dependencies": [
            "B45-FD-2_tensor_extensionality",
            "B45-FD-5_analytic_central_fd_remainder",
        ],
        "source": "../../artifacts/routeb_fd6_fd7_float64_enclosure_20260906/FD67Float64Enclosure.lean",
        "statement": (
            "Kernel-check the conditional FD-6/FD-7 seam: explicit Binary64 "
            "finite/non-NaN and per-operation enclosure contracts, twelve "
            "q±h e_k mass calls with shared mu, and the central-FD entry error lift."
        ),
        "verification": {
            "source": ref(source), "olean": ref(olean),
            "receipt": ref(receipt), "receipt_json": ref(receipt_json),
            "log": ref(log), "source_sha256": sha(source),
            "olean_sha256": sha(olean), "receipt_sha256": sha(receipt),
            "receipt_json_sha256": sha(receipt_json),
            "compile_exit": 0, "verify_exit": 0,
            "standard_axioms_only": True, "source_restriction": "passed",
            "registry_promoted": False, "comparator_accepted": False,
        },
        "closed_subclaims": [
            "six-coordinate Fin-6 contract",
            "entrywise Float64-to-exact conditional mass enclosure",
            "raw central-FD mass error lift over 12 calls",
            "quotient rounding and analytic remainder budget separation",
        ],
        "open_bridges": [
            "actual Julia Float64 sin/cos and matrix operation semantics",
            "deployed DH/COM/Jacobian mass-call binding",
            "domain-wide finite/non-NaN and interval enclosure certificate",
            "source comparator acceptance and C/G/FD contraction",
        ],
        "semantic_boundary": "conditional enclosure interface; no deployed Float64 equivalence",
    }
    subtree = nodes["B45-source_central_fd_binding_subtree"]
    subtree.setdefault("compiled_leaves", []).append(node_id)
    subtree.setdefault("float64_leaf_status", {})["FD-6/7"] = node_id
    graph["next_frontier"] = [
        "B45 FD-0, FD-3, FD-4 exact-real source loop adapters",
        "B45 bind actual Julia Float64 mass calls to FD-6/FD-7 contract",
        "B45 FD-8 tensor enclosure and FD-9/FD-10 potential/contraction enclosures",
    ] + [x for x in graph["next_frontier"] if "FD-6..FD-10" not in x and "FD-0, FD-3, FD-4" not in x]
    graph.update(schema="routeb-proposed-proof-dag-v75", supersedes="block45-obligations-v74.json")
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
        "routeb_fd67_float64_enclosure_compiled_candidate_recorded",
        source=ref(source), olean=ref(olean), receipt=ref(receipt),
        receipt_json=ref(receipt_json), log=ref(log),
        source_sha256=sha(source), olean_sha256=sha(olean),
        receipt_sha256=sha(receipt), receipt_json_sha256=sha(receipt_json),
        compile_exit=0, verify_exit=0, standard_axioms_only=True,
        comparator_accepted=False, registry_promoted=False,
        conditional_contract_only=True, deployed_float64_binding_open=True,
        analytic_remainder_binding_open=True, formal_certificate_allowed=False,
        proposed_dag=ref(graph_path), broad_regression_run=False,
    )
    store.save(state)
    print({"revision": state.revision, "graph_nodes": len(nodes),
           "registry": len(state.registry), "formal_certificate_allowed": False})


if __name__ == "__main__":
    main()
