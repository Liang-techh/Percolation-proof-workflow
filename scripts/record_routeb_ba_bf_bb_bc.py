"""Record live rebase, registry rejection, P3 seam and S-D checker audits."""
from __future__ import annotations

import hashlib
import json
import shutil
from pathlib import Path

from record_routeb_port_progress import ROOT, ref
from percolation_workflow.store import StateStore


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    store = StateStore(ROOT / "artifacts/routeb_6dof/state.json")
    state = store.load()
    assert state.revision == 190 and not state.registry
    old_graph = ROOT / "artifacts/routeb_6dof/block45-obligations-v144.json"
    new_graph = ROOT / "artifacts/routeb_6dof/block45-obligations-v145.json"
    backup = ROOT / "artifacts/routeb_storage_checkpoint_20260906/state-before-revision191.json"
    assert old_graph.is_file() and not new_graph.exists()
    ba = ROOT / "artifacts/task_BA_l0_l6_live_dry_run_rebase_20260906"
    ba_files = {name: ba / name for name in (
        "checker_result.json", "rebased_proposal_revision190.json", "REPORT.md",
        "run_dry_run.py", "snapshot.json", "stale_snapshot_rejection.json", "SUMMARY.json")}
    bf = ROOT / "artifacts/task_BF_verified_registry_child_admission_dry_run_20260906.md"
    bb = ROOT / "artifacts/task_BB_p3_pi_over_2_minimal_source_bound_20260906"
    bb_files = {name: bb / name for name in ("REPORT.md", "contract.json", "contract.py")}
    bc = ROOT / "artifacts/task_AT_sd_export_patch_20260906"
    bc_files = {name: bc / name for name in ("check_sd_export_v2.py", "CHECKER_REPORT.md")}
    for path in (*ba_files.values(), bf, *bb_files.values(), *bc_files.values()):
        assert path.is_file(), path
    ba_check = json.loads(ba_files["checker_result.json"].read_text(encoding="utf-8"))
    assert ba_check.get("failures", []) == []
    graph = json.loads(old_graph.read_text(encoding="utf-8"))
    graph.setdefault("bottleneck_audits", []).append({
        "kind": "routeb_l0_l6_live_rebase_revision190",
        "status": "DRY_RUN_REBASE_PASS_NO_INSTALL",
        "evidence_level": "snapshot_bound_dag_migration_audit",
        "semantic_boundary": "proposal remains uninstalled and registry delta is zero",
        "registry_delta": 0, "registry_promoted": False, "formal_certificate_allowed": False,
        "files": {key: {"path": ref(path), "sha256": sha(path)} for key, path in ba_files.items()},
    })
    graph.setdefault("open_frontier_updates", []).append({
        "node": "Workflow.DAG.L0_L6_live_rebase_revision190",
        "status": "dry_run_pass_parent_open",
        "reason": "64 checks pass and combined DAG is acyclic; no child is installed or registry-verified",
    })
    graph.setdefault("bottleneck_audits", []).append({
        "kind": "routeb_verified_registry_admission_dry_run",
        "status": "REJECT",
        "evidence_level": "fail_closed_registry_admission_audit",
        "semantic_boundary": "source comparator, coverage, physical bridge and child closure are absent",
        "registry_delta": 0, "registry_promoted": False, "formal_certificate_allowed": False,
        "file": {"path": ref(bf), "sha256": sha(bf)},
    })
    graph.setdefault("open_frontier_updates", []).append({
        "node": "Workflow.Registry.child_admission",
        "status": "rejected_parent_open",
        "reason": "admission dry-run correctly rejects all current conditional leaves",
    })
    graph.setdefault("bottleneck_audits", []).append({
        "kind": "routeb_p3_pi_over_2_minimal_source_bound",
        "status": "CONDITIONAL_REMAINDER_ONLY_SOURCE_BOUND_OPEN",
        "evidence_level": "exact_rational_atomic_remainder_contract",
        "semantic_boundary": "Float64 pi/libm, operation rounding, q plus/minus h trace and quotient rounding remain open",
        "registry_promoted": False, "formal_certificate_allowed": False,
        "files": {key: {"path": ref(path), "sha256": sha(path)} for key, path in bb_files.items()},
    })
    graph["open_frontier_updates"].append({
        "node": "RouteBP3.pi_over_2_source_bound",
        "status": "conditional_remainder_parent_open",
        "reason": "rational Taylor factors are checked; deployed Float64/libm and central-FD source semantics are not bound",
    })
    graph.setdefault("bottleneck_audits", []).append({
        "kind": "routeb_s_d_export_v2_checker",
        "status": "FAIL_CLOSED_PAYLOAD_MISSING",
        "evidence_level": "source_export_contract_checker",
        "semantic_boundary": "no runtime payload, manifest or COMMIT witness exists",
        "registry_promoted": False, "formal_certificate_allowed": False,
        "files": {key: {"path": ref(path), "sha256": sha(path)} for key, path in bc_files.items()},
    })
    graph["open_frontier_updates"].append({
        "node": "RouteBSchur.s_D_export_v2_checker",
        "status": "checker_ready_payload_open",
        "reason": "checker covers same-source state, residuals, hashes and atomic publish; actual source payload is missing",
    })
    graph.update(schema="routeb-proposed-proof-dag-v145", supersedes=old_graph.name)
    new_graph.write_text(json.dumps(graph, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if not backup.exists():
        backup.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(store.path, backup)
    digest = sha(new_graph)
    for algorithm, source, extra in (
        ("routeb_l0_l6_live_rebase_revision190/v1", ba_files["rebased_proposal_revision190.json"], {"proposal_sha256": sha(ba_files["rebased_proposal_revision190.json"])}),
        ("routeb_registry_admission_dry_run/v1", bf, {"report_sha256": sha(bf)}),
        ("routeb_p3_pi_over_2_minimal_source_bound/v1", bb_files["contract.json"], {"contract_sha256": sha(bb_files["contract.json"])}),
        ("routeb_s_d_export_v2_checker/v1", bc_files["check_sd_export_v2.py"], {"checker_sha256": sha(bc_files["check_sd_export_v2.py"])}),
    ):
        state.graph_artifacts.append({
            "schema_version": 1, "algorithm": algorithm, "graph_sha256": digest,
            "roots": [], "selected_nodes": [], "source": str(source), **extra,
            "registry_promoted": False, "formal_certificate_allowed": False,
        })
    state.event(
        "routeb_ba_bf_bb_bc_recorded", proposed_dag=ref(new_graph),
        proposed_dag_sha256=digest, live_rebase=ref(ba_files["rebased_proposal_revision190.json"]),
        live_rebase_sha256=sha(ba_files["rebased_proposal_revision190.json"]), registry_admission=ref(bf),
        registry_admission_sha256=sha(bf), p3_source_bound=ref(bb_files["contract.json"]),
        p3_source_bound_sha256=sha(bb_files["contract.json"]), sd_checker=ref(bc_files["check_sd_export_v2.py"]),
        sd_checker_sha256=sha(bc_files["check_sd_export_v2.py"]), registry_promoted=False,
        formal_certificate_allowed=False, broad_regression_run=False,
    )
    store.save(state)
    print({"revision": state.revision, "graph": new_graph.name, "registry": len(state.registry)})


if __name__ == "__main__":
    main()
