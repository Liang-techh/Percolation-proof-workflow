"""Record real Lean sidecar attempts as OPEN candidates, never as VERIFIED."""
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from percolation_workflow.statements import index_statements
from percolation_workflow.store import StateStore


def ref(path):
    return {"path": str(path.resolve()), "sha256": hashlib.sha256(path.read_bytes()).hexdigest()}


def main():
    store = StateStore(ROOT / "artifacts/routeb_6dof/state.json")
    if not store.path.is_file():
        raise ValueError("existing research state required")
    state = store.load()
    if state.project != "routeb-6dof-external" or any(n.status == "in_progress" for n in state.nodes.values()):
        raise ValueError("wrong project or active attempts")
    core = ROOT / "examples/routeb_supply_core"
    residual = ROOT / "examples/routeb_residual_power"
    binding = ROOT / "examples/routeb_dh_power_binding"
    christoffel = ROOT / "examples/routeb_christoffel_power"
    potential = ROOT / "examples/routeb_potential_slice"
    shifted = ROOT / "examples/routeb_shifted_storage"
    entries = [
        ("RouteBSupplyCore.pointwise_supply_bound", core / "RouteBSupplyCore.lean",
         core / "output/run-T5uqSOxk/verify.log", None,
         "01a07275-46c3-7b32-a1e7-f8e395a3eb44"),
        ("RouteBResidualPower.zero_input_obstruction", residual / "ResidualPower.lean",
         residual / "output/run-LstptWRG/verify.log", residual / "output/run-cwI9TzoS/verify.log", "coordinator"),
        ("RouteBResidualPower.supply_with_squared_force_error", residual / "ResidualPower.lean",
         residual / "output/run-LstptWRG/verify.log", residual / "output/run-cwI9TzoS/verify.log", "coordinator"),
        ("RouteBDHPowerBinding.implemented_energy_bound_of_component_enclosures", binding / "DHPowerBinding.lean",
         binding / "output/run-5RHBCcg9/verify.log", binding / "output/run-uaJqj9FL/verify.log", "coordinator"),
        ("RouteBChristoffelPower.mechanical_energy_hC", christoffel / "ChristoffelPower.lean",
         christoffel / "output/run-YC2fOLUR/verify.log", None, "01a07298-98de-7663-8661-4b84b821a9e2"),
        ("RouteBFDForceBudget.implemented_energy_fd_plus_runtime", binding / "FDForceBudget.lean",
         binding / "output/tube-NXa8rD7u/verify.log", None, "coordinator"),
        ("RouteBMechanicalAssembly.full_power_bound_from_mechanical_derivatives", binding / "MechanicalAssembly.lean",
         binding / "output/tube-NXa8rD7u/verify.log", None, "coordinator"),
        ("RouteBEnergyTube.ramp_terminal_budget", binding / "EnergyTube.lean",
         binding / "output/tube-NXa8rD7u/verify.log", binding / "output/tube-yIpLef7b/verify.log", "coordinator"),
        ("RouteBStorageObstruction.no_nonnegative_storage_of_slice", binding / "StorageObstruction.lean",
         binding / "output/tube-RWfVZNvn/verify.log", None, "coordinator"),
        ("RouteBPotentialSlice.no_global_nonnegative_W", potential / "PotentialSlice.lean",
         potential / "output/run-SuGxG04V/verify.log", None, "01a07293-ab66-7160-8adc-1e554c8d3db3"),
        ("RouteBShiftedStorage.fourier_p45_bound", shifted / "ShiftedStorage.lean",
         shifted / "output/run-pKu0JIpS/verify.log", None, "01a07298-98de-7663-8661-4b84b821a9e2"),
        ("RouteBActualShift.actual_W_shifted_coercivity", shifted / "ActualShift.lean",
         shifted / "output/actual-GqBg6J4g/verify.log", shifted / "output/actual-fYGBJat5/verify.log", "01a07298-98de-7663-8661-4b84b821a9e2"),
        ("RouteBShiftBudgetObstruction.no_coarse_terminal_budget", binding / "ShiftBudgetObstruction.lean",
         binding / "output/tube-DRiLEgLi/verify.log", None, "coordinator"),
    ]
    for name, source, success, failure, agent in entries:
        if any(n.name == name for n in state.nodes.values()):
            continue
        src_ref, log_ref = ref(source), ref(success)
        log = success.read_text(encoding="utf-8")
        if src_ref["sha256"] not in log or f"'{name}' depends on axioms:" not in log or "sorryAx" in log:
            raise ValueError("source/log binding or axiom evidence missing")
        if not ("LEAN_COMPILE_EXIT_CODE=0" in log or "Lean exit code: 0" in log):
            raise ValueError("no completed compilation evidence")
        matches = [r for r in index_statements(source) if r.qualified_name == name]
        if len(matches) != 1:
            raise ValueError(f"cannot index exact candidate: {name}")
        node_id = state.add_node(name, matches[0].source,
            proof_sketch="Finite-sum identities, exact quadratic bounds and differential comparison; explicit source, storage and physical assumptions remain separate.",
            metadata={"verification_domain": "lean", "statement_status": "compiled_source_unbound",
                      "research_stage": "P5", "physical_parent_reduction_checked": False,
                      "source": src_ref, "compile_log": log_ref, "comparator_accepted": False,
                      "evidence_level": "lean_compiled_candidate", "registry_eligible": False})
        if failure:
            failure_log = failure.read_text(encoding="utf-8")
            attempt = state.begin_attempt(node_id, agent)
            run_script = "verify_tube.sh" if source.name == "EnergyTube.lean" else "verify.sh"
            if source.name == "ActualShift.lean":
                run_script = "verify_actual.sh"
            state.finish_attempt(attempt, status="compile_error", command=["bash", str(source.parent / run_script)],
                                 stdout=failure_log, stderr="", exit_code=1)
            state.event("sidecar_failed_compile_imported", node_id=node_id, log=ref(failure))
        attempt = state.begin_attempt(node_id, agent)
        run_script = "verify_tube.sh" if source.name in {"EnergyTube.lean", "FDForceBudget.lean", "MechanicalAssembly.lean", "StorageObstruction.lean", "ShiftBudgetObstruction.lean"} else "verify.sh"
        if source.name == "ActualShift.lean":
            run_script = "verify_actual.sh"
        command = ["bash", str(source.parent / run_script)]
        if source.name in {"StorageObstruction.lean", "ShiftBudgetObstruction.lean"}:
            command.append(source.stem)
        state.finish_attempt(attempt, status="compiled", command=command,
                             stdout=log, stderr="", exit_code=0)
        state.event("sidecar_compile_imported", node_id=node_id, source=src_ref,
                    log=log_ref, physical_parent_reduction_checked=False, registry_promoted=False)
    comparator = core / "output/comparator-cached-exporter-ec0FOjSk/comparator.log"
    if not any(e.get("kind") == "routeb_supply_comparator_incompatible" for e in state.events):
        state.event("routeb_supply_comparator_incompatible", log=ref(comparator),
                    reason="Lean 4.33.1 objects; cached lean4export 4.32.0 incompatible header",
                    statement_comparison_reached=False, nanoda_reached=False, registry_promoted=False)
    research = [ref(ROOT / p) for p in (
        "examples/routeb_fd_force_budget/results.json",
        "examples/routeb_fd_force_budget/storage_results.json",
        "examples/routeb_fd_force_budget/REPORT.md",
        "examples/routeb_fd_force_budget/storage_report.md",
        "examples/routeb_potential_slice/output/run-SuGxG04V/source_evidence.json",
        "examples/routeb_shifted_storage/ACTUAL_SHIFT.md",
        "examples/routeb_dh_power_binding/ShiftBudgetObstruction.lean",
        "examples/routeb_dh_power_binding/output/tube-DRiLEgLi/verify.log",
        "docs/routeb-target-contract-extraction.md",
        "artifacts/routeb_6dof/block45-obligations-v2.json",
    )]
    if not any(e.get("kind") == "routeb_storage_obstruction_frontier" and
               e.get("artifacts") == research for e in state.events):
        m4 = next(n for n in state.nodes.values() if n.name.startswith("M4."))
        m4.metadata.setdefault("proposed_mathematical_dags", []).append(research[-1])
        m4.metadata["unshifted_storage_kinetic_shortcut"] = "refuted_for_exact_fourier_model"
        m4.metadata["constant_shift_only_coarse_comparison"] = "cannot_meet_eta56_with_factor_1600000_over_9401_and_nonnegative_Ecap"
        m4.metadata["next_mathematical_frontier"] = [
            "source_to_DH_and_derivative_binding", "shifted_or_direct_block_comparison",
            "original_initial_and_disturbance_budget", "all_coordinate_domain_bootstrap",
            "Float64_and_solve_force_enclosures"]
        state.event("routeb_storage_obstruction_frontier", artifacts=research,
                    invalid_shortcut="E >= 9401/2000000 * sum(v_i^2) for unshifted E",
                    scope="exact rational Fourier model; physical/source binding remains open",
                    conditional_fd_budget_preserved=True,
                    coefficient_to_slice_compiled=True,
                    exact_shift_coercivity_compiled=True,
                    coarse_comparison_shift_optimization_insufficient=True,
                    original_target_refuted=False, controller_changed=False,
                    mathematical_edges_checked=False, registry_promotions=0,
                    formal_certificate_allowed=False)
    store.save(state)
    print(json.dumps({"revision": state.revision, "nodes": len(state.nodes),
                      "registry": len(state.registry), "candidate_nodes_remain_open": True}))


if __name__ == "__main__":
    main()
