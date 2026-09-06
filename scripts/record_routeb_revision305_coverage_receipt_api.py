"""Record the shared structural coverage-receipt API."""
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
    if state.revision != 304 or state.registry:
        raise ValueError("revision-305 recorder requires revision 304 and empty registry")
    old = ROOT / "artifacts/routeb_6dof/block45-obligations-v258.json"
    new = ROOT / "artifacts/routeb_6dof/block45-obligations-v259.json"
    module = ROOT / "src/percolation_workflow/coverage_receipt.py"
    tests = ROOT / "tests/test_coverage_receipt.py"
    report = ROOT / "artifacts/task_FLT_coverage_receipt_api_20260908/REPORT.md"
    if not all(p.is_file() for p in (old, module, tests, report)):
        raise ValueError("missing coverage API evidence")
    record = {
        "kind": "routeb_shared_coverage_receipt_validator",
        "status": "PASS_STRUCTURAL_API_FOCUSED_TESTS_DYNAMICS_OPEN",
        "evidence_level": "fail-closed-python-api-plus-focused-tests",
        "files": [ref(module), ref(tests), ref(report)],
        "schema": "routeb-coverage-receipt-v1",
        "dimensions": 13,
        "checks": ["exact_rational_endpoints", "tree_parent_child_closure", "split_cut_geometry", "pending_discarded_accounting", "source_sha256", "complete_claim_gate"],
        "focused_test_count": 12,
        "dynamics_coverage_complete": False,
        "registry_promoted": False,
        "formal_certificate_allowed": False,
    }
    graph = json.loads(old.read_text(encoding="utf-8"))
    graph.setdefault("bottleneck_audits", []).append(record)
    graph.setdefault("external_intakes", []).append(record)
    graph.setdefault("open_frontier_updates", []).append({
        "node": "B45.coverage",
        "status": "structural_receipt_api_ready_exporter_open",
        "reason": "shared validator now exists and rejects malformed/overclaimed receipts; canonical adaptive exporter and dynamics completeness remain open.",
    })
    graph.update(schema="routeb-proposed-proof-dag-v259", supersedes=old.name)
    new.write_text(json.dumps(graph, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    backup = ROOT / "artifacts/routeb_storage_checkpoint_20260908/state-before-revision305.json"
    if not backup.exists():
        backup.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(store.path, backup)
    digest = sha(new)
    state.graph_artifacts.append({
        "schema_version": 1,
        "algorithm": "routeb_revision305_coverage_receipt_api/v1",
        "graph_sha256": digest,
        "roots": [],
        "selected_nodes": [],
        "source": str(module),
        "evidence_sha256": sha(report),
        "focused_test_count": 12,
        "structural_only": True,
        "dynamics_coverage_complete": False,
        "registry_promoted": False,
        "formal_certificate_allowed": False,
    })
    state.event(
        "routeb_revision305_coverage_receipt_api_recorded",
        proposed_dag=ref(new),
        proposed_dag_sha256=digest,
        structural_api=True,
        focused_test_count=12,
        dynamics_coverage_complete=False,
        registry_promoted=False,
        formal_certificate_allowed=False,
        broad_regression_run=False,
    )
    store.save(state)
    print(json.dumps({"revision": state.revision, "graph": new.name, "registry": len(state.registry)}))


if __name__ == "__main__":
    main()
