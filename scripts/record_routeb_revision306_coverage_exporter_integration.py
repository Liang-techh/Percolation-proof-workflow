"""Record canonical coverage exporter and shared validator integration."""
from __future__ import annotations

import hashlib
import json
import shutil
from pathlib import Path

from record_routeb_port_progress import ROOT, ref
from percolation_workflow.store import StateStore
from percolation_workflow.coverage_receipt import validate_coverage_receipt


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    store = StateStore(ROOT / "artifacts/routeb_6dof/state.json")
    state = store.load()
    if state.revision != 305 or state.registry:
        raise ValueError("revision-306 recorder requires revision 305 and empty registry")
    old = ROOT / "artifacts/routeb_6dof/block45-obligations-v259.json"
    new = ROOT / "artifacts/routeb_6dof/block45-obligations-v260.json"
    side = ROOT / "artifacts/task_FLT_coverage_receipt_api_20260908"
    module = ROOT / "src/percolation_workflow/coverage_receipt.py"
    tests = ROOT / "tests/test_coverage_receipt.py"
    report = side / "INTEGRATION_REPORT.md"
    receipt = side / "receipt_probe_exact.json"
    driver = Path(r"C:\Users\z5242\Desktop\重构版\6dof_sos_optimized\6dof_sos_optimized\robot_final\routeB_interval_branch_bound.jl")
    interval = Path(r"C:\Users\z5242\Desktop\重构版\6dof_sos_optimized\6dof_sos_optimized\robot_final\routeB_interval_bounds.jl")
    if not all(p.is_file() for p in (old, module, tests, report, receipt, driver, interval)):
        raise ValueError("missing coverage exporter integration evidence")
    summary = validate_coverage_receipt(json.loads(receipt.read_text(encoding="utf-8")))
    if summary["node_count"] != 1 or summary["pending_count"] != 1 or summary["complete_claim"]:
        raise ValueError("expected intentionally incomplete max-nodes=0 receipt")
    record = {
        "kind": "routeb_canonical_coverage_exporter_api_integration",
        "status": "PASS_CANONICAL_RECEIPT_STRUCTURAL_VALIDATION_INCOMPLETE_RUN",
        "evidence_level": "canonical-julia-receipt-plus-shared-fail-closed-python-validator",
        "files": [ref(module), ref(tests), ref(report), ref(receipt)],
        "canonical_driver_sha256": sha(driver),
        "interval_source_sha256": sha(interval),
        "receipt_sha256": sha(receipt),
        "receipt_schema": "routeB.interval.coverage_receipt.v1",
        "validator_schema": "routeb-coverage-receipt-v1",
        "node_count": summary["node_count"],
        "pending_count": summary["pending_count"],
        "dynamics_coverage_complete": False,
        "registry_promoted": False,
        "formal_certificate_allowed": False,
    }
    graph = json.loads(old.read_text(encoding="utf-8"))
    graph.setdefault("bottleneck_audits", []).append(record)
    graph.setdefault("external_intakes", []).append(record)
    graph.setdefault("open_frontier_updates", []).append({
        "node": "B45.coverage",
        "status": "canonical_receipt_validator_bound_incomplete",
        "reason": "canonical exporter emits exact-string endpoints and complete source hashes; max-nodes=0 receipt validates structurally but remains pending and cannot close dynamics coverage.",
    })
    graph.update(schema="routeb-proposed-proof-dag-v260", supersedes=old.name)
    new.write_text(json.dumps(graph, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    backup = ROOT / "artifacts/routeb_storage_checkpoint_20260908/state-before-revision306.json"
    if not backup.exists():
        backup.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(store.path, backup)
    digest = sha(new)
    state.graph_artifacts.append({
        "schema_version": 1,
        "algorithm": "routeb_revision306_coverage_exporter_integration/v1",
        "graph_sha256": digest,
        "roots": [],
        "selected_nodes": [],
        "source": str(module),
        "evidence_sha256": sha(report),
        "canonical_driver_sha256": sha(driver),
        "receipt_sha256": sha(receipt),
        "receipt_structural_validation": True,
        "incomplete_run": True,
        "dynamics_coverage_complete": False,
        "registry_promoted": False,
        "formal_certificate_allowed": False,
    })
    state.event(
        "routeb_revision306_coverage_exporter_integration_recorded",
        proposed_dag=ref(new),
        proposed_dag_sha256=digest,
        canonical_driver_sha256=sha(driver),
        receipt_sha256=sha(receipt),
        receipt_structural_validation=True,
        incomplete_run=True,
        dynamics_coverage_complete=False,
        registry_promoted=False,
        formal_certificate_allowed=False,
        broad_regression_run=False,
    )
    store.save(state)
    print(json.dumps({"revision": state.revision, "graph": new.name, "registry": len(state.registry)}))


if __name__ == "__main__":
    main()
