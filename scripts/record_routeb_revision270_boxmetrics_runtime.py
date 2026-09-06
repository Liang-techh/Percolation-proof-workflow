"""Persist the first isolated Julia runtime of the full-state API seam."""
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
    assert state.revision == 269 and not state.registry
    old = ROOT / "artifacts/routeb_6dof/block45-obligations-v223.json"
    new = ROOT / "artifacts/routeb_6dof/block45-obligations-v224.json"
    backup = ROOT / "artifacts/routeb_storage_checkpoint_20260907/state-before-revision270.json"
    sidecar = ROOT / "artifacts/task_GCU_boxmetrics_api_runtime_20260907"
    files = [sidecar / "REPORT.md", sidecar / "receipt.json", sidecar / "runtime.log",
             sidecar / "routeB_interval_bounds.jl", sidecar / "probe.jl", sidecar / "checker.py"]
    assert old.is_file() and not new.exists() and all(path.is_file() for path in files)
    receipt = json.loads((sidecar / "receipt.json").read_text(encoding="utf-8"))
    graph = json.loads(old.read_text(encoding="utf-8"))
    result = receipt.get("result", {})
    audit = {
        "kind": "routeb_boxmetrics_fullstate_api_runtime_sidecar",
        "status": receipt.get("status"),
        "evidence_level": "single-targeted-julia-execution-on-isolated-copy",
        "sidecar": str(sidecar.resolve()), "files": [ref(path) for path in files],
        "julia_version": receipt.get("julia_version"),
        "targeted_execution_count": receipt.get("targeted_execution_count"),
        "canonical_source_modified": False,
        "canonical_source_sha256": receipt.get("canonical_source_sha256"),
        "sidecar_source_sha256": receipt.get("sidecar_source_sha256"),
        "returned_fields": result.get("fields_exposed", []),
        "box_status": result.get("status"), "h_lo": result.get("h_lo"),
        "h_hi": result.get("h_hi"), "h_D": result.get("h_D"),
        "coverage_complete": False, "registry_promoted": False,
        "formal_certificate_allowed": False,
        "semantic_boundary": "One isolated patched-copy runtime only; no canonical source admission, interval theorem, coverage, residual absorption, flowpipe, terminal transfer, Lean or comparator closure.",
    }
    graph.setdefault("bottleneck_audits", []).append(audit)
    graph.setdefault("external_intakes", []).append({
        "kind": audit["kind"], "source": "isolated-sidecar:GCU-boxmetrics-runtime",
        "sidecar": audit["sidecar"], "files": audit["files"],
        "registry_promoted": False, "formal_certificate_allowed": False,
    })
    graph.setdefault("open_frontier_updates", []).append({
        "node": audit["kind"], "status": "runtime_seam_executed_canonical_admission_open",
        "reason": audit["semantic_boundary"],
    })
    graph.update(schema="routeb-proposed-proof-dag-v224", supersedes=old.name)
    new.write_text(json.dumps(graph, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if not backup.exists():
        backup.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(store.path, backup)
    digest = sha(new)
    state.graph_artifacts.append({
        "schema_version": 1, "algorithm": "routeb_revision270_boxmetrics_runtime/v1",
        "graph_sha256": digest, "roots": [], "selected_nodes": [],
        "source": "isolated-sidecar:GCU-boxmetrics-runtime",
        "evidence_sha256": sha(sidecar / "receipt.json"), "strict_compile": False,
        "registry_promoted": False, "formal_certificate_allowed": False,
    })
    state.event("routeb_revision270_boxmetrics_runtime_recorded",
                proposed_dag=ref(new), proposed_dag_sha256=digest,
                julia_version=receipt.get("julia_version"), targeted_execution_count=1,
                api_fields=result.get("fields_exposed", []), box_status=result.get("status"),
                canonical_source_modified=False, coverage_complete=False,
                registry_promoted=False, formal_certificate_allowed=False,
                broad_regression_run=False)
    store.save(state)
    print(json.dumps({"revision": state.revision, "graph": new.name,
                      "box_status": result.get("status"), "registry": len(state.registry)}))


if __name__ == "__main__":
    main()
