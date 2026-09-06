"""Persist the FD-9/FD-10 seam and the fresh v62 source-contract audit."""
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
    assert state.revision == 122 and not state.registry

    seam = ROOT / "examples/routeb_b45_2_float64_seam_lean"
    source = seam / "Float64Seam.lean"
    olean = seam / "output/run-PP41eMJr/Float64Seam.olean"
    receipt = seam / "FINAL_RECEIPT.md"
    compile_log = seam / "output/run-PP41eMJr/compile.log"
    verify_log = seam / "output/run-PP41eMJr/verify.log"
    contract = ROOT / "artifacts/routeb_6dof/source_comparator_contract_v62.json"
    contract_sha = ROOT / "artifacts/routeb_6dof/source_comparator_contract_v62.json.sha256"
    audit = ROOT / "artifacts/routeb_agent_contract_freshness/AUDIT_REPORT.md"
    old_graph = ROOT / "artifacts/routeb_6dof/block45-obligations-v76.json"
    graph_path = ROOT / "artifacts/routeb_6dof/block45-obligations-v77.json"
    backup = ROOT / "artifacts/routeb_storage_checkpoint_20260905/state-before-revision123.json"
    for path in (source, olean, receipt, compile_log, verify_log, contract, contract_sha, audit, old_graph):
        assert path.is_file(), path
    assert not graph_path.exists() and not backup.exists()

    source_text = source.read_text(encoding="utf-8")
    compile_text = compile_log.read_text(encoding="utf-8")
    verify_text = verify_log.read_text(encoding="utf-8")
    receipt_text = receipt.read_text(encoding="utf-8")
    assert "Status: **PASS" in receipt_text
    assert "`sorryAx`: absent" in receipt_text and "no proof holes" in verify_text
    assert "error:" not in compile_text.lower()
    assert not re.search(r"\b(?:sorry|admit|axiom)\b", source_text)

    contract_data = json.loads(contract.read_text(encoding="utf-8"))
    assert contract_data["status"] == "audit_only_negative_provenance"
    assert contract_data["registry_eligible"] is False
    assert contract_data["formal_certificate_allowed"] is False
    assert contract_data["contract_id"] == "b45-1-original-project-full-610-mass-aggregate"
    assert sha(contract) == "ecfcd0f0dd091f9750fff51302cbe89d1a2239f0d08606879ea60db467ce3e34"

    graph = json.loads(old_graph.read_text(encoding="utf-8"))
    nodes = {node["id"]: node for node in graph["nodes"]}

    seam_id = "B45-FD-9_10_float64_potential_contraction_seam"
    assert seam_id not in nodes
    nodes[seam_id] = {
        "id": seam_id,
        "status": "compiled_candidate_comparator_pending",
        "dependencies": ["B45-FD-8_tensor_christoffel_enclosure"],
        "source": "../../examples/routeb_b45_2_float64_seam_lean/Float64Seam.lean",
        "statement": (
            "Kernel-check the conditional FD-9/FD-10 seam: explicit finite-normal "
            "Binary64 potential samples, centered-FD gradient lift, step-rounding "
            "term, exact/runtime C*dq/G defect decomposition, and retained cross term."
        ),
        "verification": {
            "source": ref(source), "olean": ref(olean), "receipt": ref(receipt),
            "compile_log": ref(compile_log), "verify_log": ref(verify_log),
            "source_sha256": sha(source), "olean_sha256": sha(olean),
            "receipt_sha256": sha(receipt), "compile_exit": 0, "verify_exit": 0,
            "sorry_ax": 0, "standard_axioms_only": True,
            "registry_promoted": False, "comparator_accepted": False,
        },
        "closed_subclaims": [
            "finite-normal Binary64 potential value enclosure",
            "two-sided q plus/minus h e_k gradient enclosure",
            "interpreted step hhat rounding term",
            "exact/runtime C*dq/G defect decomposition with cross term",
        ],
        "open_bridges": [
            "actual Julia Float64 trigonometry and matrix semantics",
            "deployed DH/COM/Jacobian mass and derivative source binding",
            "domain-wide finite/non-NaN and numerical residual certificate",
            "source comparator acceptance, solver residual, and trajectory transfer",
        ],
        "semantic_boundary": "conditional IEEE/runtime seam; no deployed source equivalence",
    }

    contract_id = "B45-1_deployed_source_comparator_contract_v62"
    assert contract_id not in nodes
    nodes[contract_id] = {
        "id": contract_id,
        "status": "source_audit_open",
        "dependencies": [],
        "source": "../../artifacts/routeb_6dof/source_comparator_contract_v62.json",
        "statement": (
            "Audit-only comparator contract v62 binds the current routeB_dense_Mq "
            "DH source, its two consumer entrypoints, six-coordinate index map, "
            "parameterized mu/h propagation, and normalized/raw gain relation."
        ),
        "verification": {
            "contract": ref(contract), "contract_sha256": sha(contract),
            "contract_hash_file": ref(contract_sha), "audit": ref(audit),
            "registry_eligible": False, "formal_certificate_allowed": False,
            "comparator_accepted": False,
        },
        "closed_subclaims": [
            "current execution path and consumer include edges identified",
            "Fin6/Julia-1-based and B/D projection contract refreshed",
            "constants and parameterized mu/h propagation audited",
            "stale v61 provenance preserved as explicit negative evidence",
        ],
        "open_bridges": [
            "Float64-to-real equality and rounding bounds",
            "deployed mass/C/G/Jacobian equivalence for every q",
            "610-row source comparator with body identity and full provenance",
            "solver residual, flowpipe, and terminal-transfer obligations",
        ],
        "semantic_boundary": "audit-only source provenance contract; not a theorem or registry evidence",
        "supersedes": "B45-1_deployed_dh_source_comparator_contract",
    }

    subtree = nodes["B45-source_central_fd_binding_subtree"]
    subtree.setdefault("compiled_leaves", []).append(seam_id)
    subtree.setdefault("float64_leaf_status", {})["FD-9/10"] = seam_id
    graph["next_frontier"] = [
        "B45 bind current routeB_dense_Mq Julia Float64 mass/tensor/C/G calls",
        "B45 resolve 610-row body identity and comparator provenance",
        "B45 prove domain-wide residual, solver, flowpipe, and terminal transfer",
    ] + [x for x in graph.get("next_frontier", []) if "FD-9" not in x and "v61" not in x]
    graph.update(schema="routeb-proposed-proof-dag-v77", supersedes="block45-obligations-v76.json")
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
        "routeb_fd9_fd10_and_contract_v62_recorded",
        seam_source=ref(source), seam_olean=ref(olean), seam_receipt=ref(receipt),
        seam_source_sha256=sha(source), seam_olean_sha256=sha(olean),
        contract=ref(contract), contract_sha256=sha(contract), audit=ref(audit),
        compile_exit=0, verify_exit=0, sorry_ax=0, standard_axioms_only=True,
        comparator_accepted=False, registry_promoted=False,
        source_contract_audit_only=True, formal_certificate_allowed=False,
        proposed_dag=ref(graph_path), broad_regression_run=False,
    )
    store.save(state)
    print({"revision": state.revision, "graph_nodes": len(nodes),
           "registry": len(state.registry), "formal_certificate_allowed": False})


if __name__ == "__main__":
    main()
