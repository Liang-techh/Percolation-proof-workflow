"""Record the BM-BR bottleneck batch into the proposed DAG, fail-closed."""
from __future__ import annotations

import hashlib
import json
import shutil
from pathlib import Path

from record_routeb_port_progress import ROOT, ref
from percolation_workflow.store import StateStore


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def collect(*names: str) -> dict[str, Path]:
    result = {}
    for name in names:
        path = ROOT / name
        assert path.is_file(), path
        result[name] = path
    return result


def main() -> None:
    store = StateStore(ROOT / "artifacts/routeb_6dof/state.json")
    state = store.load()
    assert state.revision == 193 and not state.registry
    old_graph = ROOT / "artifacts/routeb_6dof/block45-obligations-v147.json"
    new_graph = ROOT / "artifacts/routeb_6dof/block45-obligations-v148.json"
    backup = ROOT / "artifacts/routeb_storage_checkpoint_20260906/state-before-revision194.json"
    assert old_graph.is_file() and not new_graph.exists()
    audits = [
        ("routeb_p3_rational_trig_enclosure", "CONDITIONAL_INTERVAL_SOURCE_SEAM_OPEN", "pure Fraction DH interval is replayed; deployed Float64/libm source is unbound", collect("artifacts/task_BM_p3_rational_trig_enclosure_20260906/result.json", "artifacts/task_BM_p3_rational_trig_enclosure_20260906/enclosure.py", "artifacts/task_BM_p3_rational_trig_enclosure_20260906/check.py")),
        ("routeb_full_x0_checker_compatibility", "MISMATCH_REPORT_ONLY", "strict receipt and flowpipe v2 lack compatible cell/source/coverage bindings", collect("artifacts/task_BN_full_x0_checker_integration_20260906/REPORT.md")),
        ("routeb_p4_runtime_export_hook", "PATCH_DRAFT_FAIL_CLOSED", "runtime numpoly/Float64 chain cannot yet emit canonical rational D0/c1/c2", collect("artifacts/task_BO_p4_runtime_export_plan_20260906/README.md", "artifacts/task_BO_p4_runtime_export_plan_20260906/routeB_pmi_runtime_hook.unified.diff", "artifacts/task_BO_p4_runtime_export_plan_20260906/check_runtime_hook.py")),
        ("routeb_schur_neighbor_refinement", "ONE_CELL_PLUS_OPEN_NEIGHBORS", "refinement condition rho_N<1 is exact; neighbor data and global cover are missing", collect("artifacts/task_BP_schur_refinement_bound_20260906/REPORT.md", "artifacts/task_BP_schur_refinement_bound_20260906/refinement_ledger.json", "artifacts/task_BP_schur_refinement_bound_20260906/check_refinement.py")),
        ("routeb_s_d_physical_regularization_bridge", "BLOCKED_MISSING_PHYSICAL_REGULARIZATION_BRIDGE", "M_DD(mu) bridge does not bound the physical inverse difference term", collect("artifacts/task_BQ_sd_physical_bridge_20260906/AUDIT.md", "artifacts/task_BQ_sd_physical_bridge_20260906/check_bridge.py", "artifacts/task_BQ_sd_physical_bridge_20260906/README.md")),
        ("routeb_statement_comparator_gate", "FIXTURE_READY_NO_MUTATION", "comparator ordering rejects source, coverage and normalization drift before admission", collect("artifacts/task_BR_comparator_gate_20260906/REPORT.md", "artifacts/task_BR_comparator_gate_20260906/statement_comparator_gate_fixture.json")),
    ]
    graph = json.loads(old_graph.read_text(encoding="utf-8"))
    for kind, status, reason, evidence in audits:
        graph.setdefault("bottleneck_audits", []).append({
            "kind": kind, "status": status, "evidence_level": "bounded_sidecar_audit",
            "semantic_boundary": reason, "registry_promoted": False,
            "formal_certificate_allowed": False,
            "files": {k: {"path": ref(v), "sha256": sha(v)} for k, v in evidence.items()},
        })
        graph.setdefault("open_frontier_updates", []).append({
            "node": kind, "status": status.lower(), "reason": reason,
        })
    graph.update(schema="routeb-proposed-proof-dag-v148", supersedes=old_graph.name)
    new_graph.write_text(json.dumps(graph, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if not backup.exists():
        backup.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(store.path, backup)
    digest = sha(new_graph)
    for kind, _status, _reason, evidence in audits:
        first = next(iter(evidence.values()))
        state.graph_artifacts.append({
            "schema_version": 1, "algorithm": kind + "/v1", "graph_sha256": digest,
            "roots": [], "selected_nodes": [], "source": str(first),
            "evidence_sha256": sha(first), "registry_promoted": False,
            "formal_certificate_allowed": False,
        })
    state.event(
        "routeb_bm_br_recorded", proposed_dag=ref(new_graph), proposed_dag_sha256=digest,
        audits=[kind for kind, _status, _reason, _evidence in audits],
        registry_promoted=False, formal_certificate_allowed=False,
        broad_regression_run=False,
    )
    store.save(state)
    print({"revision": state.revision, "graph": new_graph.name, "registry": len(state.registry)})


if __name__ == "__main__":
    main()
