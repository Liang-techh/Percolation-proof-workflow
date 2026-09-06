"""Persist block45 runtime, provenance drift, and independent adapter refresh."""
from __future__ import annotations

import hashlib
import json
import shutil
from pathlib import Path

from record_routeb_port_progress import ROOT, ref
from percolation_workflow.store import StateStore


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> None:
    store = StateStore(ROOT / "artifacts/routeb_6dof/state.json")
    state = store.load()
    assert state.revision == 272 and not state.registry
    old = ROOT / "artifacts/routeb_6dof/block45-obligations-v226.json"
    # GCX recorded revision 272 from v226; append this batch to that graph.
    new = ROOT / "artifacts/routeb_6dof/block45-obligations-v227.json"
    backup = ROOT / "artifacts/routeb_storage_checkpoint_20260907/state-before-revision273.json"
    gcw = ROOT / "artifacts/task_GCW_real_cell_boxmetrics_runtime_20260907"
    gcz = ROOT / "artifacts/task_GCZ_block45_q1_runtime_20260907"
    gcy = ROOT / "artifacts/task_GCY_independent_adapter_refresh_20260907"
    files = [gcw / "REPORT.md", gcw / "receipt.json", gcw / "runtime.log", gcw / "checker.py",
             gcz / "REPORT.md", gcz / "receipt.json", gcz / "runtime.log", gcz / "checker.py",
             gcy / "REPORT.md", gcy / "audit.json", gcy / "checker.py"]
    assert old.is_file() and not new.exists() and all(path.is_file() for path in files)
    gcw_r, gcz_r, gcy_r = load(gcw / "receipt.json"), load(gcz / "receipt.json"), load(gcy / "audit.json")
    graph = load(old)
    current_source = "16b01d424ecb4b95fa18363b4e3a2f8eb9adb9d7ebf7239e52142c143c8bf56e"
    historical = {
        "kind": "routeb_q1_real_cell_runtime_pre_seam_snapshot",
        "status": gcw_r.get("status"),
        "evidence_level": "historical-single-cell-julia-runtime-stale-source-binding",
        "sidecar": str(gcw.resolve()), "files": [ref(path) for path in files[:4]],
        "runtime_source_sha256": gcw_r.get("source_hashes", {}).get("routeB_interval_bounds.jl"),
        "current_canonical_source_sha256": current_source,
        "provenance_current": False,
        "result": gcw_r.get("result"),
        "interpretation": "Historical result is retained but cannot be reused after the canonical API seam changed the source hash.",
        "coverage_complete": False, "registry_promoted": False, "formal_certificate_allowed": False,
    }
    block45 = {
        "kind": "routeb_block45_q1_cell_inverse_resolved_bracket_open",
        "status": gcz_r.get("status"),
        "evidence_level": "single-targeted-julia-runtime-current-canonical-source",
        "sidecar": str(gcz.resolve()), "files": [ref(path) for path in files[4:8]],
        "result": gcz_r.get("result"), "cell": gcz_r.get("cell"),
        "solver": gcz_r.get("solver"), "julia_version": gcz_r.get("julia_version"),
        "inverse_guard_closed": True, "bracket_closed": False,
        "coverage_complete": False, "registry_promoted": False, "formal_certificate_allowed": False,
        "semantic_boundary": "block45 resolves inverse on one real cell, but wide-domain h interval remains UNKNOWN_BRACKET.",
    }
    adapter = {
        "kind": "independent_formal_adapter_refresh",
        "status": gcy_r.get("result"),
        "evidence_level": "independent-source-olean-toolchain-audit",
        "sidecar": str(gcy.resolve()), "files": [ref(path) for path in files[8:]],
        "independent_admissible": [item.get("id") for item in gcy_r.get("admissible_now", [])],
        "candidate_only": [item.get("id") for item in gcy_r.get("candidate_only", [])],
        "routeb_physical_registry_mutated": False,
        "registry_promoted": False, "formal_certificate_allowed": False,
        "semantic_boundary": "GCP may be admitted only to an independent adapter lane; GCR is stale-source candidate-only and neither binds Route-B physics.",
    }
    graph.setdefault("bottleneck_audits", []).extend([historical, block45, adapter])
    graph.setdefault("external_intakes", []).extend([
        {"kind": historical["kind"], "source": "historical-sidecar:GCW-pre-seam-runtime",
         "sidecar": historical["sidecar"], "files": historical["files"],
         "registry_promoted": False, "formal_certificate_allowed": False},
        {"kind": block45["kind"], "source": "canonical-runtime:GCZ-block45-q1",
         "sidecar": block45["sidecar"], "files": block45["files"],
         "registry_promoted": False, "formal_certificate_allowed": False},
        {"kind": adapter["kind"], "source": "independent-sidecar:GCY-adapter-refresh",
         "sidecar": adapter["sidecar"], "files": adapter["files"],
         "registry_promoted": False, "formal_certificate_allowed": False},
    ])
    graph.setdefault("open_frontier_updates", []).extend([
        {"node": historical["kind"], "status": "historical_stale_source_retained",
         "reason": historical["interpretation"]},
        {"node": block45["kind"], "status": "inverse_closed_bracket_open",
         "reason": block45["semantic_boundary"]},
        {"node": adapter["kind"], "status": "independent_lane_only",
         "reason": adapter["semantic_boundary"]},
    ])
    graph.update(schema="routeb-proposed-proof-dag-v226", supersedes=old.name)
    new.write_text(json.dumps(graph, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if not backup.exists():
        backup.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(store.path, backup)
    digest = sha(new)
    state.graph_artifacts.append({
        "schema_version": 1, "algorithm": "routeb_revision273_runtime_adapter_refresh/v1",
        "graph_sha256": digest, "roots": [], "selected_nodes": [],
        "source": "sidecars:GCW-GCZ-GCY", "evidence_sha256": sha(gcz / "receipt.json"),
        "strict_compile": False, "registry_promoted": False, "formal_certificate_allowed": False,
    })
    state.event("routeb_revision273_runtime_adapter_refresh_recorded",
                proposed_dag=ref(new), proposed_dag_sha256=digest,
                historical_stale_runtime_retained=True, block45_inverse_closed=True,
                block45_bracket_closed=False, independent_adapter_count=len(adapter["independent_admissible"]),
                candidate_only_count=len(adapter["candidate_only"]), routeb_registry_mutated=False,
                registry_promoted=False, formal_certificate_allowed=False, broad_regression_run=False)
    store.save(state)
    print(json.dumps({"revision": state.revision, "graph": new.name,
                      "block45_inverse_closed": True, "block45_bracket_closed": False,
                      "independent_adapters": len(adapter["independent_admissible"]),
                      "registry": len(state.registry)}))


if __name__ == "__main__":
    main()
