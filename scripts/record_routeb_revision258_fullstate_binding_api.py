"""Persist the keyed full-state binding API and source seam audit."""
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
    assert state.revision == 257 and not state.registry
    old = ROOT / "artifacts/routeb_6dof/block45-obligations-v211.json"
    new = ROOT / "artifacts/routeb_6dof/block45-obligations-v212.json"
    backup = ROOT / "artifacts/routeb_storage_checkpoint_20260907/state-before-revision258.json"
    gce = ROOT / "artifacts/task_GCE_full_state_binding_api_20260907"
    gcd = ROOT / "artifacts/task_GCD_mbd_ad_patch_seam_20260907"
    files = {
        "GCE": [gce / "REPORT.md", gce / "evidence.json"],
        "GCD": [gcd / "REPORT.md", gcd / "receipt.json", gcd / "patch.diff", gcd / "instrument.jl"],
    }
    local = [ROOT / "src/percolation_workflow/residual_ledger.py",
             ROOT / "src/percolation_workflow/__init__.py",
             ROOT / "tests/test_residual_ledger.py"]
    assert old.is_file() and not new.exists()
    assert all(path.is_file() for paths in files.values() for path in paths + local[:0])
    evidence = json.loads((gce / "evidence.json").read_text(encoding="utf-8"))
    seam = json.loads((gcd / "receipt.json").read_text(encoding="utf-8"))
    graph = json.loads(old.read_text(encoding="utf-8"))
    audits = [
        {
            "kind": "routeb_keyed_full_state_binding_api",
            "status": evidence["status"],
            "evidence_level": "focused-structural-api-tests",
            "semantic_boundary": (
                "The workflow now checks one full_state_key/source_snapshot for "
                "q,dq,t,w,a,aB,aD,MBD,MBD_aD and descriptor rows; this is only a "
                "schema gate and never a physical proof."
            ),
            "sidecar": str(gce.resolve()),
            "files": [ref(path) for path in files["GCE"] + local],
            "required_payloads": evidence["required_payloads"],
            "focused_tests": evidence["focused_tests"],
            "registry_promoted": False,
            "formal_certificate_allowed": False,
        },
        {
            "kind": "routeb_mbd_ad_canonical_source_patch_seam",
            "status": seam.get("status", seam.get("decision", "FAIL_CLOSED")),
            "evidence_level": "isolated-source-patch-static-audit",
            "semantic_boundary": (
                "A copy-only patch seam can expose aD, MBD and MBD_aD from the "
                "existing box_metrics Mq/a values, but Julia execution and "
                "canonical-source admission remain open."
            ),
            "sidecar": str(gcd.resolve()),
            "files": [ref(path) for path in files["GCD"]],
            "targeted_execution_count": seam.get(
                "targeted_execution_count", seam.get("anchor_execution_count", 0)),
            "canonical_source_modified": False,
            "registry_promoted": False,
            "formal_certificate_allowed": False,
        },
    ]
    graph.setdefault("bottleneck_audits", []).extend(audits)
    graph.setdefault("external_intakes", []).extend({
        "kind": audit["kind"], "source": "local-fullstate-binding-and-source-seam",
        "sidecar": audit.get("sidecar"), "files": audit["files"],
        "registry_promoted": False, "formal_certificate_allowed": False,
    } for audit in audits)
    graph.setdefault("open_frontier_updates", []).extend({
        "node": audit["kind"], "status": "schema_or_source_seam_only",
        "reason": audit["semantic_boundary"],
    } for audit in audits)
    graph.update(schema="routeb-proposed-proof-dag-v212", supersedes=old.name)
    new.write_text(json.dumps(graph, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if not backup.exists():
        backup.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(store.path, backup)
    digest = sha(new)
    state.graph_artifacts.append({
        "schema_version": 1,
        "algorithm": "routeb_revision258_fullstate_binding_api/v1",
        "graph_sha256": digest, "roots": [], "selected_nodes": [],
        "source": "local-GCE+independent-sidecar:GCD",
        "evidence_sha256": {name: {path.name: sha(path) for path in paths}
                             for name, paths in files.items()},
        "strict_compile": False, "registry_promoted": False,
        "formal_certificate_allowed": False,
    })
    state.event(
        "routeb_revision258_fullstate_binding_api_recorded",
        proposed_dag=ref(new), proposed_dag_sha256=digest,
        audits=[{"kind": audit["kind"], "status": audit["status"]} for audit in audits],
        registry_promoted=False, formal_certificate_allowed=False,
        broad_regression_run=False,
    )
    store.save(state)
    print({"revision": state.revision, "graph": new.name, "registry": len(state.registry)})


if __name__ == "__main__":
    main()
