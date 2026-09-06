"""Persist the minimal source/API seam for full-state Route-B evidence."""
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
    assert state.revision == 263 and not state.registry
    old = ROOT / "artifacts/routeb_6dof/block45-obligations-v217.json"
    new = ROOT / "artifacts/routeb_6dof/block45-obligations-v218.json"
    backup = ROOT / "artifacts/routeb_storage_checkpoint_20260907/state-before-revision264.json"
    sidecar = ROOT / "artifacts/task_GCM_boxmetrics_api_patch_plan_20260907"
    files = [sidecar / "REPORT.md", sidecar / "patch.diff", sidecar / "receipt.json",
             sidecar / "checker.py"]
    assert old.is_file() and not new.exists() and all(path.is_file() for path in files)
    receipt = json.loads((sidecar / "receipt.json").read_text(encoding="utf-8"))
    graph = json.loads(old.read_text(encoding="utf-8"))
    audit = {
        "kind": "routeb_boxmetrics_fullstate_api_seam_plan",
        "status": receipt.get("status", "PASS_FAIL_CLOSED"),
        "evidence_level": "static-diff-plan-source-bound",
        "sidecar": str(sidecar.resolve()),
        "files": [ref(path) for path in files],
        "source_sha256": receipt.get("canonical_source_sha256"),
        "proposed_return_fields": ["Cdq", "Gq", "aD", "MBD", "MBD_aD", "h_B", "h_D"],
        "h_D_semantics": "nothing_until_a separately defined and proved D-side residual is available",
        "runtime_execution": False,
        "canonical_source_modified": False,
        "coverage_complete": False,
        "registry_promoted": False,
        "formal_certificate_allowed": False,
        "semantic_boundary": "API exposure only; no interval enclosure, residual absorption, Schur theorem, or trajectory claim.",
    }
    graph.setdefault("bottleneck_audits", []).append(audit)
    graph.setdefault("external_intakes", []).append({
        "kind": audit["kind"], "source": "independent-sidecar:GCM-boxmetrics-api-plan",
        "sidecar": audit["sidecar"], "files": audit["files"],
        "registry_promoted": False, "formal_certificate_allowed": False,
    })
    graph.setdefault("open_frontier_updates", []).append({
        "node": audit["kind"], "status": "source_patch_pending_runtime_validation",
        "reason": audit["semantic_boundary"],
    })
    graph.update(schema="routeb-proposed-proof-dag-v218", supersedes=old.name)
    new.write_text(json.dumps(graph, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if not backup.exists():
        backup.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(store.path, backup)
    digest = sha(new)
    state.graph_artifacts.append({
        "schema_version": 1, "algorithm": "routeb_revision264_boxmetrics_api_plan/v1",
        "graph_sha256": digest, "roots": [], "selected_nodes": [],
        "source": "independent-sidecar:GCM-boxmetrics-api-plan",
        "evidence_sha256": sha(sidecar / "receipt.json"), "strict_compile": False,
        "registry_promoted": False, "formal_certificate_allowed": False,
    })
    state.event("routeb_revision264_boxmetrics_api_plan_recorded",
                proposed_dag=ref(new), proposed_dag_sha256=digest,
                proposed_fields=audit["proposed_return_fields"], h_D_semantics="undefined-kept-nothing",
                runtime_execution=False, canonical_source_modified=False,
                registry_promoted=False, formal_certificate_allowed=False,
                broad_regression_run=False)
    store.save(state)
    print(json.dumps({"revision": state.revision, "graph": new.name,
                      "registry": len(state.registry), "formal_certificate_allowed": False}))


if __name__ == "__main__":
    main()
