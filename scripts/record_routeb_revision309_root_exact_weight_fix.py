"""Record the proof-domain root-box repair with fail-closed evidence."""
from __future__ import annotations

import hashlib
import json
import shutil
from pathlib import Path

from record_routeb_port_progress import ROOT, ref
from percolation_workflow.coverage_receipt import validate_coverage_receipt
from percolation_workflow.store import StateStore


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    store = StateStore(ROOT / "artifacts/routeb_6dof/state.json")
    state = store.load()
    if state.revision != 308 or state.registry:
        raise ValueError("revision-309 recorder requires revision 308 and empty registry")
    side = ROOT / "artifacts/task_routeb_root_exact_weight_fix_current"
    report = ROOT / "artifacts/task_routeb_revision309_root_exact_weight_fix/REPORT.md"
    checker = side / "check_root_exact_weight.py"
    result = side / "ROOT_EXACT_RUNTIME.json"
    check_result = side / "CHECK_RESULT.json"
    stdout = side / "JULIA_PROBE.stdout.txt"
    receipt = side / "routeB_interval_coverage_receipt_root_exact_weight_probe.json"
    branch = Path(r"C:\Users\z5242\Desktop\重构版\6dof_sos_optimized\6dof_sos_optimized\robot_final\routeB_interval_branch_bound.jl")
    bounds = branch.with_name("routeB_interval_bounds.jl")
    backup = ROOT / "artifacts/routeb_canonical_backup_20260908/routeB_interval_branch_bound.jl.before_exact_weight_root_fix"
    if not all(p.is_file() for p in (report, checker, result, check_result, stdout, receipt, branch, bounds, backup)):
        raise ValueError("missing revision-309 evidence")
    check = json.loads(check_result.read_text(encoding="utf-8"))
    if (check.get("status") != "PASS" or check.get("fraction_containment_axes") != 6
            or check.get("lower_boundary_direction_checks") != 6
            or check.get("upper_boundary_direction_checks") != 6
            or not check.get("julia_runtime_rounding_restored")):
        raise ValueError("root exact checker did not pass")
    runtime = json.loads(result.read_text(encoding="utf-8"))
    if (runtime.get("proof_dq_weight_exact") != "4/5"
            or not runtime.get("ambient_rounding_restored")
            or len(runtime.get("axes", [])) != 6
            or not all(axis.get("lower_direction_outward") and axis.get("upper_direction_outward")
                       for axis in runtime["axes"])):
        raise ValueError("root exact runtime evidence is incomplete")
    summary = validate_coverage_receipt(json.loads(receipt.read_text(encoding="utf-8")))
    if summary["complete_claim"] or summary["node_count"] != 1:
        raise ValueError("root probe was unexpectedly promoted")
    graph_old = ROOT / "artifacts/routeb_6dof/block45-obligations-v262.json"
    graph_new = ROOT / "artifacts/routeb_6dof/block45-obligations-v263.json"
    graph = json.loads(graph_old.read_text(encoding="utf-8"))
    record = {
        "kind": "routeb_exact_proof_domain_root_weight_repair",
        "status": "PASS_EXACT_ROOT_CONTAINMENT_FOCUSED_PROBE_GLOBAL_COVERAGE_OPEN",
        "evidence_level": "source-hashed-julia-plus-fraction-focused-check",
        "files": [ref(report), ref(checker), ref(check_result), ref(result), ref(stdout), ref(receipt)],
        "branch_source_sha256": sha(branch),
        "interval_source_sha256": sha(bounds),
        "backup": ref(backup),
        "proof_weight_exact": ["3/2", "4/5"],
        "velocity_axis_checks": 6,
        "rounding_restored": True,
        "global_tree_executed": False,
        "receipt_summary": summary,
        "registry_promoted": False,
        "formal_certificate_allowed": False,
    }
    graph.setdefault("bottleneck_audits", []).append(record)
    graph.setdefault("workflow_hardening", []).append(record)
    graph.setdefault("open_frontier_updates", []).append({
        "node": "B45-1_exact_root_domain_coverage",
        "status": "proof_weight_root_containment_repaired",
        "reason": "exact 4/5 proof weight and outward radius remove the six-axis thin-shell mismatch; global partition and dynamics remain open.",
    })
    graph.update(schema="routeb-proposed-proof-dag-v263", supersedes=graph_old.name)
    graph_new.write_text(json.dumps(graph, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    checkpoint = ROOT / "artifacts/routeb_storage_checkpoint_20260908/state-before-revision309.json"
    if not checkpoint.exists():
        checkpoint.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(store.path, checkpoint)
    graph_sha = sha(graph_new)
    state.graph_artifacts.append({
        "schema_version": 1,
        "algorithm": "routeb_revision309_root_exact_weight_fix/v1",
        "graph_sha256": graph_sha,
        "roots": [],
        "selected_nodes": [],
        "evidence_sha256": sha(report),
        "branch_source_sha256": sha(branch),
        "interval_source_sha256": sha(bounds),
        "root_fraction_check": True,
        "rounding_restored": True,
        "global_tree_executed": False,
        "dynamics_coverage_complete": False,
        "registry_promoted": False,
        "formal_certificate_allowed": False,
    })
    state.event(
        "routeb_revision309_root_exact_weight_fix_recorded",
        proposed_dag=ref(graph_new), proposed_dag_sha256=graph_sha,
        root_fraction_check=True, velocity_axis_checks=6,
        rounding_restored=True, global_tree_executed=False,
        receipt_summary=summary, dynamics_coverage_complete=False,
        registry_promoted=False, formal_certificate_allowed=False,
        broad_regression_run=False,
    )
    store.save(state)
    print(json.dumps({"revision": state.revision, "graph": graph_new.name,
                      "registry": len(state.registry), "formal_certificate_allowed": False}))


if __name__ == "__main__":
    main()
