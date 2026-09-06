"""Record the independent physical Q-norm projection leaf.

This importer records a pinned Lean compiled candidate and deliberately does
not promote it to the verified registry.  The result is an absolute
projection bound; the state-relative eta bridge remains an open frontier.
"""
from __future__ import annotations

import hashlib
import json
import shutil

from record_routeb_port_progress import ROOT, ref
from percolation_workflow.store import StateStore


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    store = StateStore(ROOT / "artifacts/routeb_6dof/state.json")
    state = store.load()
    assert state.revision == 60 and len(state.nodes) == 64 and not state.registry

    side = ROOT / "examples/routeb_positive_supply_q_projection_lean"
    receipt = side / "FINAL_RECEIPT.md"
    source = side / "output/run-TQRk7uuS/QProjection.lean"
    olean = side / "output/run-TQRk7uuS/QProjection.olean"
    log = side / "output/run-TQRk7uuS/terminal.log"
    report = ROOT / "artifacts/routeb_6dof/positive-supply-q-projection.md"
    old_graph = ROOT / "artifacts/routeb_6dof/block45-obligations-v24.json"
    graph_path = ROOT / "artifacts/routeb_6dof/block45-obligations-v25.json"
    backup = ROOT / "artifacts/routeb_storage_checkpoint_20260905/state-before-revision60.json"

    for path in (receipt, source, olean, log, report, old_graph):
        assert path.is_file(), path
    assert not graph_path.exists()
    assert sha(source) == (
        "3482783b07b44768c05f46df27788079dd57b918e93d48bba9e84ec966eed282"
    )
    assert sha(olean) == (
        "e3fadb3850a681f5e4d094bc380c0439d155233b49383427ef55b6f4e3522eba"
    )
    log_text = log.read_text(encoding="utf-8")
    receipt_text = receipt.read_text(encoding="utf-8")
    report_text = report.read_text(encoding="utf-8")
    for marker in (
        "QProjection_COMPILE_EXIT_CODE=0",
        "VERIFY_EXIT_CODE=0",
        "SNAPSHOT_HASHES_UNCHANGED=true",
        "propext",
        "Classical.choice",
        "Quot.sound",
    ):
        assert marker in log_text, marker
    for marker in (
        "sqrt(32/495)",
        "absolute Q-norm projection",
        "does **not** prove",
        "formal_certificate_allowed=false",
    ):
        assert marker in receipt_text + report_text, marker
    source_text = source.read_text(encoding="utf-8").lower()
    assert "sorry" not in source_text and "admit" not in source_text
    assert "sorryax" not in log_text.lower()

    state.event(
        "routeb_positive_supply_q_projection_leaf",
        receipt=ref(receipt), source=ref(source), olean=ref(olean),
        terminal_log=ref(log), report=ref(report), compile_exit=0,
        verify_exit=0, standard_axioms_only=True, no_sorry=True,
        no_admit=True, q_payload="diag(3,8,95/7,165/7,45,90), Q12=Q21=-5",
        direction="u=e4+e5", projection_constant_squared="32/495",
        projection_constant="sqrt(32/495)", sharp_witness=True,
        absolute_bound_only=True, relative_eta_bound=False,
        physical_source_binding=False, uniform_feasibility=False,
        registry_promoted=False, formal_certificate_allowed=False,
    )

    graph = json.loads(old_graph.read_text(encoding="utf-8"))
    graph.update(
        schema="routeb-proposed-proof-dag-v25",
        supersedes="block45-obligations-v24.json",
        active_strategy="physical_q_projection_compiled_relative_bridge_open",
    )
    nodes = {node["id"]: node for node in graph["nodes"]}
    leaf_id = "positive_supply_q_projection"
    bridge_id = "positive_supply_q_projection_relative_bridge"
    nodes[leaf_id] = {
        "id": leaf_id,
        "status": "compiled_candidate_comparator_pending",
        "dependencies": [],
        "source": str(source.resolve()),
        "statement": (
            "For the exact current Q with diag=(3,8,95/7,165/7,45,90) and "
            "Q[1,2]=Q[2,1]=-5, prove eta'Qeta<=epsilon_Q^2 and epsilon_Q>=0 "
            "imply |(e4+e5)'eta|<=sqrt(32/495)*epsilon_Q; record sharpness."),
        "proof_sketch": (
            "Complete the off-diagonal Q block into two nonnegative squares; "
            "apply the exact two-coordinate weighted Cauchy identity whose "
            "slack is (11*x-21*y)^2/231."),
        "verification": {
            "receipt": str(receipt.resolve()),
            "run": "output/run-TQRk7uuS",
            "compile_exit": 0,
            "verify_exit": 0,
            "standard_axioms_only": True,
            "no_sorry": True,
            "no_admit": True,
            "source_sha256": sha(source),
            "olean_sha256": sha(olean),
            "terminal_log_sha256": sha(log),
            "projection_constant_squared": "32/495",
            "absolute_bound_only": True,
            "relative_eta_bound": False,
            "registry_promoted": False,
        },
    }
    nodes[bridge_id] = {
        "id": bridge_id,
        "status": "open_physical_scaling_obligation",
        "dependencies": [leaf_id, "source_semantics"],
        "statement": (
            "Convert the absolute projection bound into |etaU|<=kappa*rho "
            "by proving equilibrium vanishing/state-relative scaling, or "
            "explicitly choose the direct-gate route with an absolute supply "
            "floor. The projection leaf alone is insufficient."),
        "report": str(report.resolve()),
        "required_extra_condition": "epsilon_Q <= c*rho or direct etaU relative bound",
        "status_boundary": "open",
    }
    rel = nodes["positive_supply_relative_eta_lemma"]
    rel.setdefault("physical_projection_inputs", []).append(leaf_id)
    rel["absolute_projection_status"] = "compiled_candidate_only"
    direct = nodes["positive_supply_two_regime_direct_gate"]
    if bridge_id not in direct["dependencies"]:
        direct["dependencies"].append(bridge_id)
    direct["physical_projection"] = leaf_id
    direct["relative_bridge"] = bridge_id
    direct["statement"] = (
        "Assemble the division-free direct gate with a small-rho branch and "
        "the relative-eta division branch; the Q projection is now exact, "
        "but state-relative scaling, source coverage, and supply-floor "
        "feasibility remain open.")
    if "positive_supply_eta_physical_projection_and_relative_bound" in graph["next_frontier"]:
        graph["next_frontier"].remove(
            "positive_supply_eta_physical_projection_and_relative_bound")
    graph["next_frontier"] = [
        "positive_supply_q_projection_relative_bridge",
        *graph["next_frontier"],
    ]
    graph["positive_supply_frontier"]["absolute_q_projection"] = {
        "status": "compiled_candidate_comparator_pending",
        "leaf": leaf_id,
        "constant_squared": "32/495",
        "constant": "sqrt(32/495)",
        "sharp": True,
        "relative_scaling": "open",
        "report": str(report.resolve()),
    }
    graph["positive_supply_frontier"]["relative_eta_boundary"] = (
        "absolute Q projection does not imply |etaU|<=kappa*rho without "
        "equilibrium vanishing or state-relative scaling")
    graph["nodes"] = list(nodes.values())

    def visit(key, stack):
        assert key not in stack
        for dep in nodes[key].get("dependencies", []):
            assert dep in nodes, (key, dep)
            visit(dep, stack | {key})

    for key in nodes:
        visit(key, set())

    if not backup.exists():
        shutil.copy2(store.path, backup)
    graph_path.write_text(
        json.dumps(graph, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    m4 = next(
        node for node in state.nodes.values()
        if node.name.startswith("M4.") and node.name != "M4.correlated_momentum_closure"
    )
    m4.metadata.setdefault("proposed_mathematical_dags", []).append(ref(graph_path))
    m4.metadata["next_mathematical_frontier"] = graph["next_frontier"]
    state.event(
        "routeb_positive_supply_q_projection_checkpoint",
        proposed_dag=ref(graph_path), original_target_unchanged=True,
        actual_J_proved=False, formal_certificate_allowed=False,
        comparator_accepted=False, registry_promotions=0,
        broad_regression_run=False, relative_scaling_open=True,
    )
    store.save(state)
    print(json.dumps({
        "revision": state.revision,
        "nodes": len(state.nodes),
        "graph_nodes": len(nodes),
        "registry": len(state.registry),
        "formal_certificate_allowed": False,
        "leaf": leaf_id,
        "projection_constant": "sqrt(32/495)",
        "relative_eta_bridge": "open",
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
