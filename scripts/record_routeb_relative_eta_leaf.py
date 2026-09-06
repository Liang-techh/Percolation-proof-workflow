"""Record the bounded relative-eta/direct-gate Lean leaf.

This importer intentionally promotes no theorem to the verified registry.  It
records a kernel-compiled candidate and keeps the physical two-regime assembly
open in the proposed DAG.
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
    assert state.revision == 57 and len(state.nodes) == 64 and not state.registry

    side = ROOT / "examples/routeb_positive_supply_relative_eta_lean"
    receipt = side / "FINAL_RECEIPT.md"
    source = side / "output/run-vLUcsyKh/RelativeEtaDenominator.lean"
    olean = side / "output/run-vLUcsyKh/RelativeEtaDenominator.olean"
    log = side / "output/run-vLUcsyKh/terminal.log"
    old_graph = ROOT / "artifacts/routeb_6dof/block45-obligations-v21.json"
    graph_path = ROOT / "artifacts/routeb_6dof/block45-obligations-v22.json"
    backup = ROOT / "artifacts/routeb_storage_checkpoint_20260905/state-before-revision57.json"

    for path in (receipt, source, olean, log, old_graph):
        assert path.is_file(), path
    assert not graph_path.exists()
    assert sha(source) == (
        "7205581770ed544f2d41608982600583a78b98e6606ae1ffde6d70639619bb73"
    )
    assert sha(olean) == (
        "ccce9f3aebca9225a5c9a42d1b06890a4036123aba3ad838225a5bb6ba1753c0"
    )
    receipt_text = receipt.read_text(encoding="utf-8")
    log_text = log.read_text(encoding="utf-8")
    for marker in (
        "Status: PASS",
        "RelativeEtaDenominator_COMPILE_EXIT_CODE=0",
        "VERIFY_EXIT_CODE=0",
        "standard axioms",
        "formal_certificate_allowed=false",
    ):
        assert marker in receipt_text + log_text
    source_text = source.read_text(encoding="utf-8").lower()
    assert "sorry" not in source_text and "admit" not in source_text

    state.event(
        "routeb_positive_supply_relative_eta_leaf",
        receipt=ref(receipt), source=ref(source), olean=ref(olean),
        terminal_log=ref(log), compile_exit=0, verify_exit=0,
        standard_axioms_only=True, no_sorry=True, no_admit=True,
        relative_eta_bound=True, direct_gate_without_division=True,
        source_unbound=True, physical_source_binding=False,
        uniform_feasibility=False, actual_J_proved=False,
        registry_promoted=False, formal_certificate_allowed=False,
    )

    graph = json.loads(old_graph.read_text(encoding="utf-8"))
    graph.update(
        schema="routeb-proposed-proof-dag-v22",
        supersedes="block45-obligations-v21.json",
        active_strategy="eta_relative_denominator_leaf_compiled_two_regime_assembly_open",
    )
    nodes = {node["id"]: node for node in graph["nodes"]}
    leaf_id = "positive_supply_relative_eta_kernel_leaf"
    nodes[leaf_id] = {
        "id": leaf_id,
        "status": "compiled_candidate_comparator_pending",
        "dependencies": ["positive_supply_gate"],
        "source": "../../examples/routeb_positive_supply_relative_eta_lean/RelativeEtaDenominator.lean",
        "statement": (
            "For exact A=2002229/24000000, D=29/20 and K=A+D, prove "
            "rho>0, 0<=tau<=1, |etaU|<=kappa*rho, kappa<K implies "
            "rho*(rho*(A+tau*D)-tau*etaU)>0; also expose the additive "
            "direct-gate form without division."),
        "verification": {
            "receipt": str(receipt.resolve()),
            "run": "output/run-vLUcsyKh",
            "compile_exit": 0,
            "verify_exit": 0,
            "standard_axioms_only": True,
            "no_sorry": True,
            "no_admit": True,
            "source_sha256": sha(source),
            "olean_sha256": sha(olean),
            "physical_source_binding": False,
            "uniform_feasibility": False,
            "J_proved": False,
        },
    }
    relative = nodes["positive_supply_relative_eta_lemma"]
    relative.update(
        status="compiled_candidate_comparator_pending",
        dependencies=[leaf_id, "source_semantics"],
        compiled_leaf=leaf_id,
        report=str((ROOT / "artifacts/routeb_6dof/positive-supply-frontier.md").resolve()),
    )
    direct = nodes["positive_supply_two_regime_direct_gate"]
    direct.update(
        status="open",
        dependencies=["positive_supply_gate", leaf_id],
        kernel_interface=leaf_id,
        statement=(
            "Assemble the division-free direct gate with a small-rho branch "
            "and the relative-eta division branch; physical eta projection, "
            "source coverage, and supply-floor feasibility remain open."),
    )
    if "positive_supply_relative_eta_lemma" in graph["next_frontier"]:
        graph["next_frontier"].remove("positive_supply_relative_eta_lemma")
    graph["next_frontier"] = [
        "positive_supply_eta_physical_projection_and_relative_bound",
        "positive_supply_two_regime_physical_assembly",
        *graph["next_frontier"],
    ]
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
        "routeb_positive_supply_relative_eta_checkpoint",
        proposed_dag=ref(graph_path), original_target_unchanged=True,
        actual_J_proved=False, formal_certificate_allowed=False,
        comparator_accepted=False, registry_promotions=0,
        broad_regression_run=False, two_regime_physical_assembly_open=True,
    )
    store.save(state)
    print(json.dumps({
        "revision": state.revision,
        "nodes": len(state.nodes),
        "graph_nodes": len(nodes),
        "registry": len(state.registry),
        "formal_certificate_allowed": False,
        "leaf": leaf_id,
        "physical_two_regime_assembly": "open",
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
