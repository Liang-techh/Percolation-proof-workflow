"""Record the explicit D-elimination repair and repair-loop error plan."""
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
    assert state.revision == 181 and not state.registry
    old_graph = ROOT / "artifacts/routeb_6dof/block45-obligations-v135.json"
    new_graph = ROOT / "artifacts/routeb_6dof/block45-obligations-v136.json"
    backup = ROOT / "artifacts/routeb_storage_checkpoint_20260906/state-before-revision182.json"
    assert old_graph.is_file() and not new_graph.exists()
    dbase = ROOT / "artifacts/routeb_agent_p4_d_elim_c_20260906T110000Z"
    d_files = {name: dbase / name for name in ("DElimCRepair.lean", "compare.py", "README.md", "result.json")}
    eplan = ROOT / "artifacts/repair_loop_error_classification_repair_plan_20260906.json"
    ah = ROOT / "artifacts/task_AH_l0_l6_freshness_20260906"
    ah_files = {name: ah / name for name in (
        "SUMMARY.md", "freshness_snapshot.json", "proposed_patch_revision181.json",
        "old_revision178_rejection.json", "new_revision181_report.json")}
    for path in (*d_files.values(), eplan, *ah_files.values()):
        assert path.is_file(), path
    result = json.loads(d_files["result.json"].read_text(encoding="utf-8"))
    assert result["status"] == "PASS_LOCAL_REPAIR_WITH_EXPLICIT_CONDITIONS"
    graph = json.loads(old_graph.read_text(encoding="utf-8"))
    graph.setdefault("bottleneck_audits", []).append({
        "kind": "routeb_p4_d_elim_c_repair",
        "status": "LEAN_COMPILED_COMPARATOR_PASS_CONDITIONAL",
        "evidence_level": "exact_real_explicit_d_elim_condition",
        "semantic_boundary": "nonnegative deployed D_elim_c, Float64 binding, SOS feasibility and coverage remain open",
        "registry_promoted": False, "formal_certificate_allowed": False,
        "files": {key: {"path": ref(path), "sha256": sha(path)} for key, path in d_files.items()},
    })
    graph.setdefault("open_frontier_updates", []).append({
        "node": "RouteBP4.D_elim_c_source_binding",
        "status": "repair_pass_parent_open",
        "reason": "D0-c1-c2 definition and positivity assumptions are explicit; deployed nonnegative witness and coverage remain open",
    })
    graph.setdefault("bottleneck_audits", []).append({
        "kind": "routeb_repair_loop_error_classification",
        "status": "FAIL_CLOSED_PLAN_READY",
        "evidence_level": "repair_plan_schema",
        "semantic_boundary": "classification plan does not itself prove any child or parent theorem",
        "registry_promoted": False, "formal_certificate_allowed": False,
        "file": {"path": ref(eplan), "sha256": sha(eplan)},
    })
    graph.setdefault("open_frontier_updates", []).append({
        "node": "Workflow.RepairLoop.error_classification",
        "status": "plan_ready_parent_open",
        "reason": "five failure classes are recorded; comparator and coverage outcomes still need durable attempt wiring",
    })
    graph.setdefault("bottleneck_audits", []).append({
        "kind": "routeb_l0_l6_freshness_dry_run",
        "status": "SAFE_TO_INSTALL_DRY_RUN_ONLY",
        "evidence_level": "snapshot_bound_dag_migration_audit",
        "semantic_boundary": "child installation is not performed and no registry admission occurs",
        "registry_promoted": False, "formal_certificate_allowed": False,
        "files": {key: {"path": ref(path), "sha256": sha(path)} for key, path in ah_files.items()},
    })
    graph.setdefault("open_frontier_updates", []).append({
        "node": "Workflow.DAG.L0_L6_dry_run_migration",
        "status": "dry_run_safe_install_parent_open",
        "reason": "revision-181 proposal has fresh snapshot, no cycles and closed gates; actual child installation remains separate",
    })
    graph.update(schema="routeb-proposed-proof-dag-v136", supersedes=old_graph.name)
    new_graph.write_text(json.dumps(graph, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if not backup.exists():
        backup.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(store.path, backup)
    digest = sha(new_graph)
    state.graph_artifacts.append({
        "schema_version": 1, "algorithm": "routeb_p4_d_elim_c_repair/v1",
        "graph_sha256": digest, "roots": [], "selected_nodes": [],
        "source": "explicit D-elimination condition repair",
        "source_sha256": sha(d_files["DElimCRepair.lean"]),
        "result_sha256": sha(d_files["result.json"]), "registry_promoted": False,
        "formal_certificate_allowed": False,
    })
    state.graph_artifacts.append({
        "schema_version": 1, "algorithm": "routeb_repair_error_classification/v1",
        "graph_sha256": digest, "roots": [], "selected_nodes": [],
        "source": "fail-closed repair plan schema", "plan_sha256": sha(eplan),
        "registry_promoted": False, "formal_certificate_allowed": False,
    })
    state.graph_artifacts.append({
        "schema_version": 1, "algorithm": "routeb_l0_l6_freshness_dry_run/v1",
        "graph_sha256": digest, "roots": [], "selected_nodes": [],
        "source": "snapshot-bound dry-run theorem DAG migration",
        "proposal_sha256": sha(ah_files["proposed_patch_revision181.json"]),
        "registry_promoted": False, "formal_certificate_allowed": False,
    })
    state.event(
        "routeb_d_elim_and_repair_plan_recorded", proposed_dag=ref(new_graph),
        proposed_dag_sha256=digest, d_elim=ref(d_files["DElimCRepair.lean"]),
        d_elim_sha256=sha(d_files["DElimCRepair.lean"]), repair_plan=ref(eplan),
        repair_plan_sha256=sha(eplan), registry_promoted=False,
        formal_certificate_allowed=False, broad_regression_run=False,
    )
    store.save(state)
    print({"revision": state.revision, "graph": new_graph.name, "registry": len(state.registry)})


if __name__ == "__main__":
    main()
