"""Record the P3 DH trig contract and historical L0-L6 rebase audit."""
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
    assert state.revision == 189 and not state.registry
    old_graph = ROOT / "artifacts/routeb_6dof/block45-obligations-v143.json"
    new_graph = ROOT / "artifacts/routeb_6dof/block45-obligations-v144.json"
    backup = ROOT / "artifacts/routeb_storage_checkpoint_20260906/state-before-revision190.json"
    assert old_graph.is_file() and not new_graph.exists()
    target = Path(r"C:\Users\z5242\Desktop\重构版\6dof_sos_optimized\6dof_sos_optimized")
    aw_files = {
        "exact_contract": target / "routeB_dense_Mq/routeB_p3_dh_trig_chain_contract.py",
        "exact_report": target / "routeB_dense_Mq/P3_DH_TRIG_CHAIN_CONTRACT.md",
        "runtime_binding": target / "robot_final/routeB_p3_dh_trig_center_binding.jl",
        "runtime_report": target / "robot_final/P3_DH_TRIG_CENTER_FLOAT64_BINDING.md",
        "contract_csv": target / "routeB_dense_Mq/routeB_p3_dh_trig_chain_contract.csv",
    }
    ay = ROOT / "artifacts/task_AY_l0_l6_rebase_20260906"
    ay_files = {name: ay / name for name in (
        "REPORT.md", "snapshot.json", "rebased_proposal_revision187.json",
        "stale_snapshot_rejection.json", "checker_result.json")}
    for path in (*aw_files.values(), *ay_files.values()):
        assert path.is_file(), path
    graph = json.loads(old_graph.read_text(encoding="utf-8"))
    graph.setdefault("bottleneck_audits", []).append({
        "kind": "routeb_p3_dh_pi_over_2_trig_contract",
        "status": "CONDITIONAL_RUNTIME_BINDING_SOURCE_OPEN",
        "evidence_level": "exact_real_center_runtime_screen",
        "semantic_boundary": "Float64 pi/libm rounding, parameter arithmetic and full DH interval propagation remain open",
        "formal_certificate_allowed": False, "registry_promoted": False,
        "files": {key: {"path": ref(path), "sha256": sha(path)} for key, path in aw_files.items()},
    })
    graph.setdefault("open_frontier_updates", []).append({
        "node": "RouteBP3.DH_pi_over_2_trig_source_binding",
        "status": "conditional_center_screen_parent_open",
        "reason": "q=0 exact center rows and runtime screen pass; libm/Float64 rounding and interval propagation are not proved",
    })
    graph.setdefault("bottleneck_audits", []).append({
        "kind": "routeb_l0_l6_revision187_rebase_historical",
        "status": "DRY_RUN_REBASE_PASS_HISTORICAL_SNAPSHOT",
        "evidence_level": "snapshot_bound_dag_migration_audit",
        "semantic_boundary": "proposal is bound to revision 187 and was not installed into the live state",
        "registry_delta": 0, "registry_promoted": False, "formal_certificate_allowed": False,
        "files": {key: {"path": ref(path), "sha256": sha(path)} for key, path in ay_files.items()},
    })
    graph["open_frontier_updates"].append({
        "node": "Workflow.DAG.L0_L6_revision187_historical_rebase",
        "status": "historical_pass_live_rebase_required",
        "reason": "7-child proposal is acyclic and passes at revision 187; live revision 189 rebase is required before any authorized installation",
    })
    graph.update(schema="routeb-proposed-proof-dag-v144", supersedes=old_graph.name)
    new_graph.write_text(json.dumps(graph, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if not backup.exists():
        backup.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(store.path, backup)
    digest = sha(new_graph)
    for algorithm, source, extra in (
        ("routeb_p3_dh_pi_over_2_trig_contract/v1", aw_files["exact_contract"], {"source_sha256": sha(aw_files["exact_contract"])}),
        ("routeb_l0_l6_revision187_rebase_historical/v1", ay_files["rebased_proposal_revision187.json"], {"proposal_sha256": sha(ay_files["rebased_proposal_revision187.json"])}),
    ):
        state.graph_artifacts.append({
            "schema_version": 1, "algorithm": algorithm, "graph_sha256": digest,
            "roots": [], "selected_nodes": [], "source": str(source), **extra,
            "registry_promoted": False, "formal_certificate_allowed": False,
        })
    state.event(
        "routeb_aw_trig_and_ay_rebase_recorded", proposed_dag=ref(new_graph),
        proposed_dag_sha256=digest, trig_contract=ref(aw_files["exact_contract"]),
        trig_contract_sha256=sha(aw_files["exact_contract"]), historical_rebase=ref(ay_files["rebased_proposal_revision187.json"]),
        historical_rebase_sha256=sha(ay_files["rebased_proposal_revision187.json"]), registry_delta=0,
        registry_promoted=False, formal_certificate_allowed=False, broad_regression_run=False,
    )
    store.save(state)
    print({"revision": state.revision, "graph": new_graph.name, "registry": len(state.registry)})


if __name__ == "__main__":
    main()
