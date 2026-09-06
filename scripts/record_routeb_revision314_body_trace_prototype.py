"""Record the bounded artifact-local body-trace aggregation prototype."""
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
    if state.revision != 313 or state.registry:
        raise ValueError("revision-314 recorder requires revision 313 and empty registry")

    side = ROOT / "artifacts/task_routeb_body_trace_sink_current"
    report = ROOT / "artifacts/task_routeb_revision314_body_trace_prototype/REPORT.md"
    manifest = side / "manifest.json"
    checker = side / "exact_aggregation_checker.py"
    result = side / "CHECK_RESULT_recheck.json"
    if not all(p.is_file() for p in (report, manifest, checker, result)):
        raise ValueError("missing revision-314 body-trace evidence")
    check = json.loads(result.read_text(encoding="utf-8"))
    if (check.get("status") != "PASS"
            or check.get("trace_rows") != 727
            or check.get("aggregate_rows") != 610
            or not check.get("aggregate_equals_sum_body_exact")
            or not check.get("aggregate_vs_reference_exact")):
        raise ValueError("body-trace exact aggregation gate did not pass")
    meta = json.loads(manifest.read_text(encoding="utf-8"))
    if meta.get("status") != "PROTOTYPE_PASS_DEPLOYED_BINDING_OPEN":
        raise ValueError("body-trace binding boundary changed unexpectedly")

    old = ROOT / "artifacts/routeb_6dof/block45-obligations-v267.json"
    new = ROOT / "artifacts/routeb_6dof/block45-obligations-v268.json"
    graph = json.loads(old.read_text(encoding="utf-8"))
    record = {
        "kind": "routeb_artifact_local_body_trace_aggregation",
        "status": "PASS_PROTOTYPE_DEPLOYED_BINDING_OPEN",
        "evidence_level": "exact-sparse-aggregation-interface",
        "files": [ref(report), ref(manifest), ref(checker), ref(result)],
        "body_trace_rows": check["trace_rows"],
        "aggregate_rows": check["aggregate_rows"],
        "aggregate_equals_sum_body_exact": True,
        "aggregate_vs_reference_exact": True,
        "deployed_julia_to_exact_fourier_safe_binding": False,
        "registry_promoted": False,
        "formal_certificate_allowed": False,
    }
    graph.setdefault("bottleneck_audits", []).append(record)
    graph.setdefault("workflow_hardening", []).append(record)
    graph.setdefault("open_frontier_updates", []).append({
        "node": "B45-1_610_body_trace_binding_obstruction",
        "status": "prototype_aggregation_closed_deployed_semantics_open",
        "reason": "exact body trace and aggregate are internally consistent, but deployed Julia Float64 to exact Fourier semantic binding remains open",
        "evidence": ref(result),
    })
    graph.update(schema="routeb-proposed-proof-dag-v268", supersedes=old.name)
    new.write_text(json.dumps(graph, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    checkpoint = ROOT / "artifacts/routeb_storage_checkpoint_20260908/state-before-revision314.json"
    if not checkpoint.exists():
        checkpoint.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(store.path, checkpoint)
    graph_sha = sha(new)
    state.graph_artifacts.append({
        "schema_version": 1,
        "algorithm": "routeb_revision314_body_trace_prototype/v1",
        "graph_sha256": graph_sha,
        "roots": [],
        "selected_nodes": [],
        "evidence_sha256": sha(report),
        "manifest_sha256": sha(manifest),
        "checker_sha256": sha(checker),
        "result_sha256": sha(result),
        "body_trace_rows": 727,
        "aggregate_rows": 610,
        "deployed_source_binding_complete": False,
        "registry_promoted": False,
        "formal_certificate_allowed": False,
    })
    state.event(
        "routeb_revision314_body_trace_prototype_recorded",
        proposed_dag=ref(new),
        proposed_dag_sha256=graph_sha,
        body_trace_rows=727,
        aggregate_rows=610,
        aggregate_equals_sum_body_exact=True,
        aggregate_vs_reference_exact=True,
        deployed_source_binding_complete=False,
        registry_promoted=False,
        formal_certificate_allowed=False,
        broad_regression_run=False,
    )
    store.save(state)
    print(json.dumps({
        "revision": state.revision,
        "graph": new.name,
        "registry": len(state.registry),
        "formal_certificate_allowed": False,
    }))


if __name__ == "__main__":
    main()
