"""Append this mathematical checkpoint and every retained compiler attempt.

This is an evidence importer, not a verifier/registry bypass. New nodes remain
OPEN until independent statement comparison and the normal admission gates.
Run only after taking a recoverable state backup and completing the Lean runs.
"""
import json
from pathlib import Path
import re
import sys

from record_routeb_math_progress import ROOT, ref
from percolation_workflow.statements import index_statements
from percolation_workflow.store import StateStore

LEAN = "/home/z5242/.elan/toolchains/leanprover--lean4---v4.33.1/bin/lean"


def clean_axioms(theorem, output):
    match = re.search(re.escape(f"'{theorem}' depends on axioms:") + r"\s*\[([^\]]*)\]", output)
    return match is not None and {a.strip() for a in match[1].split(",") if a.strip()} <= {
        "propext", "Classical.choice", "Quot.sound"}


def wsl(path):
    p = Path(path).resolve()
    if p.drive.lower() != "c:":
        raise ValueError("this checkpoint records C-drive WSL runs only")
    return "/mnt/c/" + p.as_posix()[3:]


def main():
    specs = [
        ("routeb_port_absorption", "PortAbsorption", "RouteBPortAbsorption.conditional_absorption", "01a072be-a5ff-7cb2-abec-218b0130749b"),
        ("routeb_block_potential", "BlockPotential", "RouteBBlockPotential.potential_factor", "01a07293-ab66-7160-8adc-1e554c8d3db3"),
        ("routeb_local_energy_budget", "LocalEnergyBudget", "RouteBLocalEnergyBudget.outputs_of_cap", "01a072be-a5ff-7cb2-abec-218b0130749b"),
        ("routeb_implicit_port", "ImplicitPort", "RouteBImplicitPort.absorption_of_reduced_bound", "coordinator"),
        ("routeb_implicit_port", "BlockTargets", "RouteBBlockTargets.tube_does_not_imply_terminal", "coordinator"),
        ("routeb_implicit_port", "GateBounds", "RouteBPortGates.actual_gate_iff", "coordinator"),
        ("routeb_implicit_port", "PhysicalPortAssembly", "RouteBPhysicalPortAssembly.physical_port_absorption", "coordinator"),
        ("routeb_implicit_port", "VariableErrorTube", "RouteBVariableErrorTube.capped_cumulative_ramp_budget", "coordinator"),
        ("routeb_implicit_port", "LocalTubeAssembly", "RouteBLocalTubeAssembly.conditional_original_block_outputs", "coordinator"),
    ]
    store = StateStore(ROOT / "artifacts/routeb_6dof/state.json")
    if not store.path.is_file():
        raise ValueError("existing state required")
    state = store.load()
    if state.project != "routeb-6dof-external" or any(n.status == "in_progress" for n in state.nodes.values()):
        raise ValueError("wrong project or active attempts")
    new_nodes = new_attempts = 0
    for directory, module, theorem, agent in specs:
        side = ROOT / "examples" / directory
        source = side / f"{module}.lean"
        source_ref = ref(source)
        records = []
        for log in sorted((side / "output").glob("*/verify.log"), key=lambda p: p.stat().st_mtime_ns):
            snapshot = log.parent / source.name
            if not snapshot.is_file():
                continue
            output = log.read_text(encoding="utf-8")
            success = "LEAN_COMPILE_EXIT_CODE=0" in output and "VERIFY_EXIT_CODE=1" not in output
            terminal = success or bool(re.search(r"(?:LEAN_COMPILE|VERIFY)_EXIT_CODE=[1-9]", output))
            if not terminal:
                raise ValueError(f"no terminal compiler evidence: {log}")
            records.append((log, snapshot, output, success))
        accepted = [(log, snapshot) for log, snapshot, output, success in records
                    if success and source_ref["sha256"] == ref(snapshot)["sha256"]
                    and source_ref["sha256"] in output
                    and clean_axioms(theorem, output) and "sorryAx" not in output]
        if not accepted:
            raise ValueError(f"no source-bound successful compile: {theorem}")
        success_log, _ = accepted[-1]
        matches = [n for n in state.nodes.values() if n.name == theorem]
        if matches:
            node = matches[0]
            if node.metadata.get("source") != source_ref:
                raise ValueError("refuse silently replacing an existing candidate version")
        else:
            declarations = [d for d in index_statements(source) if d.qualified_name == theorem]
            if len(declarations) != 1:
                raise ValueError(f"exact declaration not uniquely indexed: {theorem}")
            node_id = state.add_node(theorem, declarations[0].source,
                proof_sketch="Exact local energy or port reduction with explicit physical, residual, regularity and domain premises.",
                metadata={"verification_domain": "lean", "research_stage": "P5",
                          "statement_status": "compiled_source_unbound", "registry_eligible": False,
                          "source": source_ref, "compile_log": ref(success_log),
                          "comparator_accepted": False, "physical_parent_reduction_checked": False,
                          "evidence_level": "lean_compiled_candidate"})
            node = state.nodes[node_id]
            new_nodes += 1
        old_logs = {e.get("log", {}).get("sha256") for e in state.events
                    if e.get("kind") == "routeb_port_attempt_imported" and e.get("node_id") == node.id}
        for log, snapshot, output, success in records:
            log_ref = ref(log)
            if log_ref["sha256"] in old_logs:
                continue
            # BlockPotential compiles its live source with --root=SIDE. All
            # other selected recipes compile the preserved RUN snapshot.
            compile_root = side if module == "BlockPotential" else log.parent
            compile_source = source if module == "BlockPotential" else snapshot
            command = [LEAN, "-DwarningAsError=true", "--root=" + wsl(compile_root),
                       "-o", wsl(log.parent / f"{module}.olean"), wsl(compile_source)]
            attempt = state.begin_attempt(node.id, agent, source_path=str(snapshot.resolve()))
            state.finish_attempt(attempt, status="compiled" if success else "compile_error",
                                 command=command, stdout=output, stderr="", exit_code=0 if success else 1)
            state.event("routeb_port_attempt_imported", node_id=node.id, log=log_ref,
                        snapshot=ref(snapshot), current_source_matches=ref(snapshot)["sha256"] == source_ref["sha256"],
                        registry_promoted=False)
            new_attempts += 1
    graph_ref = ref(ROOT / "artifacts/routeb_6dof/block45-obligations-v3.json")
    docs = [ref(ROOT / p) for p in (
        "docs/routeb-block-targets-v2.md", "examples/routeb_block_potential/DERIVATION.md",
        "examples/routeb_block_potential/audit_results.json",
        "examples/routeb_implicit_port/README.md",
        "artifacts/routeb_port_checkpoint_20260905/REPORT.md")]
    if not any(e.get("kind") == "routeb_port_math_checkpoint" and e.get("proposed_dag") == graph_ref for e in state.events):
        m4 = next(n for n in state.nodes.values() if n.name.startswith("M4."))
        m4.metadata.setdefault("proposed_mathematical_dags", []).append(graph_ref)
        m4.metadata["domain_target"] = "p=3/2*(q4^2+q5^2)+4/5*(v4^2+v5^2) <= 28/5 for t in [0,1]"
        m4.metadata["terminal_target"] = "qpoly=3*(q4^2+q5^2)+2*(v4^2+v5^2) <=12 at T=1"
        m4.metadata["next_mathematical_frontier"] = [
            "total_reference_block_force_error_cumulative_cost_le_1_over_10",
            "actual_DH_Float64_curve_and_energy_regularities",
            "full12_initial_and_all_coordinate_first_exit_continuation",
            "strict_port_and_residual_bracket_or_tighter_local_error_allocation"]
        state.event("routeb_port_math_checkpoint", proposed_dag=graph_ref, artifacts=docs,
                    local_error_budget_proved=False, flowpipe_proved=False,
                    comparator_accepted=False, mathematical_edges_checked=False,
                    target_correction="5.6 is the p-domain bound; terminal qpoly uses different weights and alpha=12",
                    formal_certificate_allowed=False, registry_promotions=0)
    store.save(state)
    print(json.dumps({"revision": state.revision, "new_nodes": new_nodes,
                      "new_attempts": new_attempts, "total_nodes": len(state.nodes),
                      "registry": len(state.registry), "all_new_nodes_remain_open": True}))


if __name__ == "__main__":
    main()
