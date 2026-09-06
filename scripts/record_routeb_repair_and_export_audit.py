"""Record repair classification and reject the incomplete S-D export diff."""
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
    assert state.revision == 185 and not state.registry
    old_graph = ROOT / "artifacts/routeb_6dof/block45-obligations-v139.json"
    new_graph = ROOT / "artifacts/routeb_6dof/block45-obligations-v140.json"
    backup = ROOT / "artifacts/routeb_storage_checkpoint_20260906/state-before-revision186.json"
    assert old_graph.is_file() and not new_graph.exists()
    repair_files = {
        "module": ROOT / "src/percolation_workflow/repair_classification.py",
        "cli": ROOT / "src/percolation_workflow/cli.py",
        "test": ROOT / "tests/test_repair_classification.py",
        "plan": ROOT / "artifacts/repair_loop_error_classification_repair_plan_20260906.json",
    }
    export_audit = ROOT / "artifacts/routeb_agent_s_d_export_patch_audit_20260906/REPORT.md"
    for path in (*repair_files.values(), export_audit):
        assert path.is_file(), path
    graph = json.loads(old_graph.read_text(encoding="utf-8"))
    graph.setdefault("bottleneck_audits", []).append({
        "kind": "routeb_repair_loop_error_classification_module",
        "status": "DRY_RUN_REPAIR_REQUESTS_PASS",
        "evidence_level": "fail_closed_repair_classification",
        "semantic_boundary": "repair requests do not verify children or close parents",
        "registry_promoted": False, "formal_certificate_allowed": False,
        "files": {key: {"path": ref(path), "sha256": sha(path)} for key, path in repair_files.items()},
    })
    graph.setdefault("open_frontier_updates", []).append({
        "node": "Workflow.RepairLoop.classified_requests",
        "status": "dry_run_pass_parent_open",
        "reason": "syntax/API/semantic/comparator/coverage requests are classified without state mutation; final proof gates remain authoritative",
    })
    graph.setdefault("bottleneck_audits", []).append({
        "kind": "routeb_s_d_export_patch_semantic_rejection",
        "status": "REJECTED_PENDING_SEMANTIC_REPAIR",
        "evidence_level": "static_patch_semantic_audit",
        "semantic_boundary": "patch does not yet bind same source state, regularization, field order, manifest hash or coverage cell semantics",
        "registry_promoted": False, "formal_certificate_allowed": False,
        "file": {"path": ref(export_audit), "sha256": sha(export_audit)},
    })
    graph["open_frontier_updates"].append({
        "node": "RouteBSchur.s_D_export_patch",
        "status": "rejected_semantic_repair_required",
        "reason": "same-call q/dq/w binding, regularized-vs-physical M_DD, column order, helper/manifest completeness and fail-safe finalization are unresolved",
    })
    graph.update(schema="routeb-proposed-proof-dag-v140", supersedes=old_graph.name)
    new_graph.write_text(json.dumps(graph, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if not backup.exists():
        backup.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(store.path, backup)
    digest = sha(new_graph)
    state.graph_artifacts.append({
        "schema_version": 1, "algorithm": "routeb_repair_classification/v1",
        "graph_sha256": digest, "roots": [], "selected_nodes": [],
        "source": "fail-closed repair request classifier", "module_sha256": sha(repair_files["module"]),
        "registry_promoted": False, "formal_certificate_allowed": False,
    })
    state.graph_artifacts.append({
        "schema_version": 1, "algorithm": "routeb_s_d_export_patch_audit/v1",
        "graph_sha256": digest, "roots": [], "selected_nodes": [],
        "source": "semantic rejection of incomplete S-D export patch", "audit_sha256": sha(export_audit),
        "registry_promoted": False, "formal_certificate_allowed": False,
    })
    state.event(
        "routeb_repair_and_export_audit_recorded", proposed_dag=ref(new_graph),
        proposed_dag_sha256=digest, repair_module=ref(repair_files["module"]),
        repair_module_sha256=sha(repair_files["module"]), export_audit=ref(export_audit),
        export_audit_sha256=sha(export_audit), status="REJECTED_PENDING_SEMANTIC_REPAIR",
        registry_promoted=False, formal_certificate_allowed=False, broad_regression_run=False,
    )
    store.save(state)
    print({"revision": state.revision, "graph": new_graph.name, "registry": len(state.registry)})


if __name__ == "__main__":
    main()
