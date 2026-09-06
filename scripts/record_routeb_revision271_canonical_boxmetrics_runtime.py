"""Persist the canonical Route-B box_metrics seam runtime and backup binding."""
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
    assert state.revision == 270 and not state.registry
    old = ROOT / "artifacts/routeb_6dof/block45-obligations-v224.json"
    new = ROOT / "artifacts/routeb_6dof/block45-obligations-v225.json"
    backup = ROOT / "artifacts/routeb_storage_checkpoint_20260907/state-before-revision271.json"
    sidecar = ROOT / "artifacts/task_GCV_canonical_boxmetrics_runtime_20260907"
    files = [sidecar / "REPORT.md", sidecar / "receipt.json", sidecar / "runtime.log",
             sidecar / "probe.jl", sidecar / "checker.py",
             ROOT / "artifacts/routeb_canonical_backup_20260907/routeB_interval_bounds.jl.before_gcu"]
    assert old.is_file() and not new.exists() and all(path.is_file() for path in files)
    receipt = json.loads((sidecar / "receipt.json").read_text(encoding="utf-8"))
    graph = json.loads(old.read_text(encoding="utf-8"))
    audit = {
        "kind": "routeb_canonical_boxmetrics_fullstate_runtime",
        "status": receipt.get("status"),
        "evidence_level": "single-targeted-julia-execution-canonical-source",
        "sidecar": str(sidecar.resolve()), "files": [ref(path) for path in files],
        "julia_version": receipt.get("julia_version"),
        "targeted_execution_count": receipt.get("targeted_execution_count"),
        "canonical_source_sha256_before": receipt.get("canonical_source_sha256_before"),
        "canonical_source_sha256_after": receipt.get("canonical_source_sha256_after"),
        "backup_sha256": receipt.get("backup_sha256"),
        "returned_fields": receipt.get("result", {}).get("fields_exposed", []),
        "box_status": receipt.get("result", {}).get("status"),
        "h_lo": receipt.get("result", {}).get("h_lo"),
        "h_hi": receipt.get("result", {}).get("h_hi"),
        "h_D": receipt.get("result", {}).get("h_D"),
        "coverage_complete": False, "registry_promoted": False,
        "formal_certificate_allowed": False,
        "semantic_boundary": "Canonical one-box API runtime only; interval soundness, coverage, residual absorption, flowpipe, terminal transfer, Lean, comparator and registry remain open.",
    }
    graph.setdefault("bottleneck_audits", []).append(audit)
    graph.setdefault("external_intakes", []).append({
        "kind": audit["kind"], "source": "canonical-runtime:GCV-boxmetrics-seam",
        "sidecar": audit["sidecar"], "files": audit["files"],
        "registry_promoted": False, "formal_certificate_allowed": False,
    })
    graph.setdefault("open_frontier_updates", []).append({
        "node": audit["kind"], "status": "canonical_api_runtime_closed_global_certificate_open",
        "reason": audit["semantic_boundary"],
    })
    graph.update(schema="routeb-proposed-proof-dag-v225", supersedes=old.name)
    new.write_text(json.dumps(graph, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if not backup.exists():
        backup.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(store.path, backup)
    digest = sha(new)
    state.graph_artifacts.append({
        "schema_version": 1, "algorithm": "routeb_revision271_canonical_boxmetrics_runtime/v1",
        "graph_sha256": digest, "roots": [], "selected_nodes": [],
        "source": "canonical-runtime:GCV-boxmetrics-seam",
        "evidence_sha256": sha(sidecar / "receipt.json"), "strict_compile": False,
        "registry_promoted": False, "formal_certificate_allowed": False,
    })
    state.event("routeb_revision271_canonical_boxmetrics_runtime_recorded",
                proposed_dag=ref(new), proposed_dag_sha256=digest,
                canonical_source_modified=True, backup_verified=True,
                julia_version=receipt.get("julia_version"), targeted_execution_count=1,
                api_fields=audit["returned_fields"], box_status=audit["box_status"],
                h_D_defined=False, coverage_complete=False, registry_promoted=False,
                formal_certificate_allowed=False, broad_regression_run=False)
    store.save(state)
    print(json.dumps({"revision": state.revision, "graph": new.name,
                      "box_status": audit["box_status"], "registry": len(state.registry)}))


if __name__ == "__main__":
    main()
