"""Record the fail-closed adaptive coverage audit."""
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
    if state.revision != 296 or state.registry:
        raise ValueError("revision-297 recorder requires revision 296 and empty registry")
    old = ROOT / "artifacts/routeb_6dof/block45-obligations-v250.json"
    new = ROOT / "artifacts/routeb_6dof/block45-obligations-v251.json"
    side = ROOT / "artifacts/task_FLT_coverage_audit_20260908"
    report = side / "REPORT.md"
    checker = side / "coverage_receipt_checker_draft.py"
    if not all(path.is_file() for path in (old, report, checker)):
        raise ValueError("missing coverage audit evidence")
    compile(checker.read_text(encoding="utf-8"), str(checker), "exec")
    record = {
        "kind": "routeb_adaptive_coverage_audit",
        "status": "GEOMETRY_RECEIPT_ONLY_ADAPTIVE_UNION_UNCHECKABLE",
        "evidence_level": "read-only-schema-audit-plus-isolated-checker-draft",
        "files": [ref(report), ref(checker)],
        "geometry_coverage_complete": True,
        "dynamics_coverage_complete": False,
        "adaptive_union_mechanically_checkable": False,
        "missing_receipt_fields": ["13d_box_endpoints", "split_axis", "split_cut", "child_ids", "pending_ids"],
        "minimal_next_receipt_schema": "routeB-coverage-receipt-v1",
        "registry_promoted": False,
        "formal_certificate_allowed": False,
    }
    graph = json.loads(old.read_text(encoding="utf-8"))
    graph.setdefault("bottleneck_audits", []).append(record)
    graph.setdefault("external_intakes", []).append(record)
    graph.setdefault("open_frontier_updates", []).append({
        "node": "B45.coverage",
        "status": "adaptive_union_uncheckable",
        "reason": "legacy adaptive CSV omits 13-dimensional boxes, split tree, and pending queue; geometry-only receipt cannot close dynamics coverage.",
    })
    graph.update(schema="routeb-proposed-proof-dag-v251", supersedes=old.name)
    new.write_text(json.dumps(graph, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    backup = ROOT / "artifacts/routeb_storage_checkpoint_20260908/state-before-revision297.json"
    if not backup.exists():
        backup.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(store.path, backup)
    digest = sha(new)
    state.graph_artifacts.append({
        "schema_version": 1,
        "algorithm": "routeb_revision297_coverage_audit/v1",
        "graph_sha256": digest,
        "roots": [],
        "selected_nodes": [],
        "source": str(side),
        "evidence_sha256": sha(report),
        "audit_only": True,
        "geometry_coverage_complete": True,
        "dynamics_coverage_complete": False,
        "adaptive_union_mechanically_checkable": False,
        "registry_promoted": False,
        "formal_certificate_allowed": False,
    })
    state.event(
        "routeb_revision297_coverage_audit_recorded",
        proposed_dag=ref(new),
        proposed_dag_sha256=digest,
        audit_only=True,
        geometry_coverage_complete=True,
        dynamics_coverage_complete=False,
        adaptive_union_mechanically_checkable=False,
        required_receipt_schema="routeB-coverage-receipt-v1",
        registry_promoted=False,
        formal_certificate_allowed=False,
        broad_regression_run=False,
    )
    store.save(state)
    print(json.dumps({"revision": state.revision, "graph": new.name, "registry": len(state.registry)}))


if __name__ == "__main__":
    main()
