"""Record the source-bound scalar aggregation repair and refreshed receipt."""
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
    if state.revision != 306 or state.registry:
        raise ValueError("revision-307 recorder requires revision 306 and empty registry")
    old = ROOT / "artifacts/routeb_6dof/block45-obligations-v260.json"
    new = ROOT / "artifacts/routeb_6dof/block45-obligations-v261.json"
    side = ROOT / "artifacts/task_FLT_scalar_aggregation_patch_20260908"
    report = side / "APPLIED_REPORT.md"
    focused = side / "focused_scalar_aggregation_check_canonical.after_index_fix.out"
    driver_log = ROOT / "artifacts/task_FLT_coverage_receipt_api_20260908/receipt_after_scalar_aggregation_driver.out"
    receipt = ROOT / "artifacts/task_FLT_coverage_receipt_api_20260908/receipt_after_scalar_aggregation.json"
    source = Path(r"C:\Users\z5242\Desktop\重构版\6dof_sos_optimized\6dof_sos_optimized\robot_final\routeB_interval_bounds.jl")
    driver = Path(r"C:\Users\z5242\Desktop\重构版\6dof_sos_optimized\6dof_sos_optimized\robot_final\routeB_interval_branch_bound.jl")
    if not all(p.is_file() for p in (old, report, focused, driver_log, receipt, source, driver)):
        raise ValueError("missing scalar aggregation evidence")
    source_sha = "03679c7b686842ef9504886614e3498fb9fbf4a6c1466f8e44dcc505d21e3609"
    driver_sha = "7c4967593203c3e808b81289032066f85f12d9dfaa319d26cf9979d5012941b5"
    if sha(source) != source_sha or sha(driver) != driver_sha:
        raise ValueError("canonical source hash mismatch")
    focused_text = focused.read_text(encoding="utf-8")
    for marker in ("directed scalar primitives |    2      2", "Cholesky and Krawczyk scalar guards |    5      5", "one real box_metrics call |    6      6", "PASS_FOCUSED_CANONICAL_SCALAR_AGGREGATION"):
        if marker not in focused_text:
            raise ValueError("focused scalar check failed: " + marker)
    summary = validate_coverage_receipt(json.loads(receipt.read_text(encoding="utf-8")))
    if summary["node_count"] != 1 or summary["pending_count"] != 1 or summary["complete_claim"]:
        raise ValueError("fresh receipt is not the expected incomplete fail-closed run")
    record = {
        "kind": "routeb_source_bound_scalar_aggregation_repair",
        "status": "PASS_FOCUSED_CANONICAL_SCALAR_AGGREGATION_COVERAGE_STILL_OPEN",
        "evidence_level": "source-hashed-julia-focused-check-plus-refreshed-structural-receipt",
        "files": [ref(report), ref(focused), ref(driver_log), ref(receipt)],
        "interval_source_sha256": source_sha,
        "driver_sha256": driver_sha,
        "repaired": ["proof_facing_scalar_sums", "coefficient_products", "kappa_row_sums", "h_endpoints", "nested_generator_index_capture"],
        "focused_test_counts": {"scalar_primitives": 2, "inverse_guards": 5, "box_metrics": 6},
        "receipt_node_count": summary["node_count"],
        "receipt_pending_count": summary["pending_count"],
        "dynamics_coverage_complete": False,
        "registry_promoted": False,
        "formal_certificate_allowed": False,
    }
    graph = json.loads(old.read_text(encoding="utf-8"))
    graph.setdefault("bottleneck_audits", []).append(record)
    graph.setdefault("external_intakes", []).append(record)
    graph.setdefault("open_frontier_updates", []).append({
        "node": "B45.rounding",
        "status": "scalar_aggregation_source_bound_repaired",
        "reason": "proof-facing sums/products and inverse guards are focused-tested on the canonical source; full source semantics and coverage remain open.",
    })
    graph.update(schema="routeb-proposed-proof-dag-v261", supersedes=old.name)
    new.write_text(json.dumps(graph, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    backup = ROOT / "artifacts/routeb_storage_checkpoint_20260908/state-before-revision307.json"
    if not backup.exists():
        backup.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(store.path, backup)
    digest = sha(new)
    state.graph_artifacts.append({
        "schema_version": 1,
        "algorithm": "routeb_revision307_scalar_aggregation_fix/v1",
        "graph_sha256": digest,
        "roots": [],
        "selected_nodes": [],
        "source": str(source),
        "evidence_sha256": sha(report),
        "canonical_source_sha256": source_sha,
        "canonical_driver_sha256": driver_sha,
        "focused_checks_pass": True,
        "fresh_receipt_structural_validation": True,
        "dynamics_coverage_complete": False,
        "registry_promoted": False,
        "formal_certificate_allowed": False,
    })
    state.event(
        "routeb_revision307_scalar_aggregation_fix_recorded",
        proposed_dag=ref(new),
        proposed_dag_sha256=digest,
        canonical_source_sha256=source_sha,
        canonical_driver_sha256=driver_sha,
        focused_checks_pass=True,
        fresh_receipt_structural_validation=True,
        dynamics_coverage_complete=False,
        registry_promoted=False,
        formal_certificate_allowed=False,
        broad_regression_run=False,
    )
    store.save(state)
    print(json.dumps({"revision": state.revision, "graph": new.name, "registry": len(state.registry)}))


if __name__ == "__main__":
    main()
