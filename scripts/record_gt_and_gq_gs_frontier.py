"""Record GQ/GR/GT/GS evidence and the fail-closed batch fix."""
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
    assert state.revision == 224 and not state.registry
    old = ROOT / "artifacts/routeb_6dof/block45-obligations-v178.json"
    new = ROOT / "artifacts/routeb_6dof/block45-obligations-v179.json"
    backup = ROOT / "artifacts/routeb_storage_checkpoint_20260907/state-before-revision225.json"
    assert old.is_file() and not new.exists()

    code_files = [
        ROOT / "src/percolation_workflow/reduction_batch.py",
        ROOT / "tests/test_reduction_batch.py",
        ROOT / "src/percolation_workflow/__init__.py",
    ]
    specs = [
        ("task_GQ_ltrue_ledger_20260907", ["REPORT.md", "ledger.json", "provenance.md"], "ltrue_ledger", "OPEN_FAIL_CLOSED", "Exact l_true decomposition and one-time Float64/FD/solve/remote charge ledger; no accepted same-domain bound."),
        ("task_GR_single_cell_materializer_20260907", ["REPORT.md", "receipt_or_missing.json", "provenance.md", "checker.py"], "single_cell_materializer", "BLOCKED", "A single indexed cell remains missing geometry, inverse replay, source binding, witnesses, and payload hash; no synthetic receipt or coverage claim."),
        ("task_GT_batch_closure_audit_20260907", ["REPORT.md", "cases.json", "provenance.md"], "batch_closure_safety_audit", "OPEN_FAIL_CLOSED", "Audit identified registry-status false positive and duplicate child IDs; both are now guarded by focused tests and production validation."),
        ("task_GS_routeb_schur_adapter_20260907", ["RouteBSchurAdapter.lean", "RouteBSchurAdapter.olean", "compile_warningAsError.log", "axioms.txt", "REPORT.md", "provenance.md"], "routeb_schur_adapter", "CURRENT_PIN_STRICT_COMPILE_PASS_CANDIDATE_ONLY", "Generic GA Schur lemma specialized to explicit 2+4 dimensions; no physical DH, coverage, or admission claim."),
    ]
    graph = json.loads(old.read_text(encoding="utf-8"))
    optimization = {
        "kind": "reduction_closure_batch_fail_closed_fix",
        "status": "FOCUSED_TEST_PASS_NON_ADMISSION",
        "evidence_level": "targeted_workflow_safety_fix",
        "semantic_boundary": "Batch projection reports verified only when node status, statement identity, and audit_registry currentness all agree; duplicate child IDs are rejected.",
        "files": [ref(path) for path in code_files],
        "test_command": "PYTHONPATH=src; python -m pytest -q tests/test_reduction_batch.py",
        "test_result": "4 passed",
        "registry_promoted": False,
        "formal_certificate_allowed": False,
    }
    graph.setdefault("workflow_optimizations", []).append(optimization)
    graph.setdefault("bottleneck_audits", []).append(optimization)
    graph.setdefault("open_frontier_updates", []).append({
        "node": optimization["kind"], "status": "focused_fix_pass_non_admission", "reason": optimization["semantic_boundary"]
    })
    audits = []
    for dirname, names, node, status, reason in specs:
        sidecar = ROOT / "artifacts" / dirname
        files = [sidecar / name for name in names]
        assert all(path.is_file() for path in files)
        audit = {
            "kind": f"routeb_{node}_audit",
            "status": status,
            "evidence_level": "independent_sidecar_frontier_audit",
            "semantic_boundary": reason,
            "sidecar": str(sidecar.resolve()),
            "files": [ref(path) for path in files],
            "registry_promoted": False,
            "formal_certificate_allowed": False,
        }
        audits.append(audit)
        graph.setdefault("bottleneck_audits", []).append(audit)
        graph.setdefault("external_intakes", []).append({
            "kind": audit["kind"], "source": "local-routeb-gq-gr-gt-gs-frontier",
            "sidecar": audit["sidecar"], "files": audit["files"],
            "registry_promoted": False, "formal_certificate_allowed": False,
        })
        graph.setdefault("open_frontier_updates", []).append({
            "node": audit["kind"], "status": status.lower(), "reason": reason,
        })
    graph.update(schema="routeb-proposed-proof-dag-v179", supersedes=old.name)
    new.write_text(json.dumps(graph, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if not backup.exists():
        backup.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(store.path, backup)
    digest = sha(new)
    state.graph_artifacts.append({
        "schema_version": 1, "algorithm": "routeb_gt_gq_gr_gs_frontier/v1",
        "graph_sha256": digest, "roots": [], "selected_nodes": [],
        "source": "batch-fix plus sidecars:GQ,GR,GT,GS",
        "evidence_sha256": sha(code_files[0]),
        "strict_compile": True, "registry_promoted": False, "formal_certificate_allowed": False,
    })
    state.event(
        "routeb_gt_gq_gr_gs_frontier_recorded", proposed_dag=ref(new),
        proposed_dag_sha256=digest, optimization=optimization,
        audits=[{"kind": x["kind"], "status": x["status"]} for x in audits],
        registry_promoted=False, formal_certificate_allowed=False,
        broad_regression_run=False,
    )
    store.save(state)
    print({"revision": state.revision, "graph": new.name, "audits": len(audits), "registry": len(state.registry)})


if __name__ == "__main__":
    main()
