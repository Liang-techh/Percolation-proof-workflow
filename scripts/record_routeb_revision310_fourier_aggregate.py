"""Record the exact per-body Fourier aggregation seam as non-authoritative."""
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
    if state.revision != 309 or state.registry:
        raise ValueError("revision-310 recorder requires revision 309 and empty registry")
    side = ROOT / "artifacts/task_routeb_fourier_aggregate_current"
    report = ROOT / "artifacts/task_routeb_revision310_fourier_aggregate/REPORT.md"
    manifest_path = side / "manifest.json"
    checker = side / "check_current.py"
    body_trace = side / "routeB_fourier_mass_body_trace.csv"
    aggregate = side / "routeB_fourier_mass_aggregate_from_trace.csv"
    if not all(p.is_file() for p in (report, manifest_path, checker, body_trace, aggregate)):
        raise ValueError("missing revision-310 evidence")
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    checks = manifest.get("checks", {})
    if (manifest.get("status") != "PASS"
            or checks.get("aggregate_body_mismatch_count") != 0
            or not checks.get("aggregate_equals_sum_body_exact")
            or not checks.get("aggregate_vs_frozen_csv_exact")
            or checks.get("body_trace_data_rows") != 727
            or checks.get("aggregate_data_rows") != 610):
        raise ValueError("Fourier aggregation manifest did not pass")
    old = ROOT / "artifacts/routeb_6dof/block45-obligations-v263.json"
    new = ROOT / "artifacts/routeb_6dof/block45-obligations-v264.json"
    record = {
        "kind": "routeb_exact_per_body_fourier_aggregate_seam",
        "status": "PASS_EXACT_PAYLOAD_AGGREGATION_SOURCE_BINDING_OPEN",
        "evidence_level": "artifact_local_exact_fraction_checker",
        "files": [ref(report), ref(manifest_path), ref(checker), ref(body_trace), ref(aggregate)],
        "body_count": 6,
        "body_trace_rows": checks["body_trace_data_rows"],
        "aggregate_rows": checks["aggregate_data_rows"],
        "aggregate_equals_sum_body_exact": True,
        "aggregate_vs_frozen_csv_exact": True,
        "max_float_diagnostic_error": checks.get("max_float_evaluation_error"),
        "canonical_generator_modified": False,
        "deployed_source_binding_complete": False,
        "registry_promoted": False,
        "formal_certificate_allowed": False,
    }
    graph = json.loads(old.read_text(encoding="utf-8"))
    graph.setdefault("bottleneck_audits", []).append(record)
    graph.setdefault("workflow_optimizations", []).append(record)
    graph.setdefault("open_frontier_updates", []).append({
        "node": "B45-1_source_mass_fourier_aggregation_seam",
        "status": "exact_payload_aggregate_sum_body_verified",
        "reason": "six-body exact coefficient sum is independently checked; deployed Julia body trace and Float64/source comparator remain open.",
    })
    graph.update(schema="routeb-proposed-proof-dag-v264", supersedes=old.name)
    new.write_text(json.dumps(graph, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    checkpoint = ROOT / "artifacts/routeb_storage_checkpoint_20260908/state-before-revision310.json"
    if not checkpoint.exists():
        checkpoint.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(store.path, checkpoint)
    graph_sha = sha(new)
    state.graph_artifacts.append({
        "schema_version": 1,
        "algorithm": "routeb_revision310_fourier_aggregate/v1",
        "graph_sha256": graph_sha,
        "roots": [], "selected_nodes": [],
        "evidence_sha256": sha(report),
        "manifest_sha256": sha(manifest_path),
        "body_trace_sha256": sha(body_trace),
        "aggregate_sha256": sha(aggregate),
        "exact_payload_aggregation": True,
        "deployed_source_binding_complete": False,
        "registry_promoted": False,
        "formal_certificate_allowed": False,
    })
    state.event(
        "routeb_revision310_fourier_aggregate_recorded",
        proposed_dag=ref(new), proposed_dag_sha256=graph_sha,
        body_count=6, body_trace_rows=checks["body_trace_data_rows"],
        aggregate_rows=checks["aggregate_data_rows"],
        exact_payload_aggregation=True, deployed_source_binding_complete=False,
        registry_promoted=False, formal_certificate_allowed=False,
        broad_regression_run=False,
    )
    store.save(state)
    print(json.dumps({"revision": state.revision, "graph": new.name,
                      "registry": len(state.registry), "formal_certificate_allowed": False}))


if __name__ == "__main__":
    main()
