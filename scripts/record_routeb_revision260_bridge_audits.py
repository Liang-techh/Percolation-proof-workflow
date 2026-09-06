"""Persist the q1 box-metrics bridge and full-state harness audits."""
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
    assert state.revision == 259 and not state.registry
    old = ROOT / "artifacts/routeb_6dof/block45-obligations-v213.json"
    new = ROOT / "artifacts/routeb_6dof/block45-obligations-v214.json"
    backup = ROOT / "artifacts/routeb_storage_checkpoint_20260907/state-before-revision260.json"
    gch = ROOT / "artifacts/task_GCH_q1_boxmetrics_bridge_20260907"
    gci = ROOT / "artifacts/task_GCI_fullstate_harness_audit_20260907"
    files = [gch / "REPORT.md", gch / "receipt.json", gch / "checker.py",
             gci / "REPORT.md", gci / "receipt.json", gci / "fixture.py",
             gci / "checker.py"]
    assert old.is_file() and not new.exists() and all(path.is_file() for path in files)
    gch_receipt = json.loads((gch / "receipt.json").read_text(encoding="utf-8"))
    gci_receipt = json.loads((gci / "receipt.json").read_text(encoding="utf-8"))
    graph = json.loads(old.read_text(encoding="utf-8"))
    bridge_reason = (
        "q1=1/64 closes only the local inverse guard; the live box_metrics contract "
        "still exposes aggregate h and hides h_B/h_D, Cdq/Gq, aD, MBD and MBD_aD. "
        "Julia is unavailable, so no full residual or Schur runtime claim is admitted."
    )
    bridge = {
        "kind": "routeb_q1_boxmetrics_bridge_audit",
        "status": gch_receipt.get("status"),
        "evidence_level": "static-source-plus-prior-receipts",
        "semantic_boundary": bridge_reason,
        "sidecar": str(gch.resolve()),
        "files": [ref(path) for path in files[:3]],
        "source_sha256": gch_receipt.get("source_sha256"),
        "targeted_execution_count": gch_receipt.get("targeted_execution_count", 0),
        "missing_runtime_fields": ["h_B", "h_D", "Cdq", "Gq", "aD", "MBD", "MBD_aD"],
        "coverage_complete": False,
        "registry_promoted": False,
        "formal_certificate_allowed": False,
    }
    harness = {
        "kind": "routeb_full_state_binding_harness_audit",
        "status": "PASS_FAIL_CLOSED",
        "evidence_level": "deterministic-structural-fixture",
        "semantic_boundary": "The harness rejects key/source/action/envelope drift; it does not prove physical bounds or runtime execution.",
        "sidecar": str(gci.resolve()),
        "files": [ref(path) for path in files[3:]],
        "source_snapshot": gci_receipt.get("source_snapshot"),
        "case_count": gci_receipt.get("case_count"),
        "coverage_complete": False,
        "registry_promoted": False,
        "formal_certificate_allowed": False,
    }
    graph.setdefault("bottleneck_audits", []).extend([bridge, harness])
    graph.setdefault("external_intakes", []).extend([
        {"kind": bridge["kind"], "source": "independent-sidecar:GCH-q1-boxmetrics-bridge",
         "sidecar": bridge["sidecar"], "files": bridge["files"],
         "registry_promoted": False, "formal_certificate_allowed": False},
        {"kind": harness["kind"], "source": "independent-sidecar:GCI-fullstate-harness",
         "sidecar": harness["sidecar"], "files": harness["files"],
         "registry_promoted": False, "formal_certificate_allowed": False},
    ])
    graph.setdefault("open_frontier_updates", []).extend([
        {"node": bridge["kind"], "status": "open_runtime_boxmetrics_contract", "reason": bridge_reason},
        {"node": harness["kind"], "status": "structural_harness_closed_physical_open",
         "reason": harness["semantic_boundary"]},
    ])
    graph.update(schema="routeb-proposed-proof-dag-v214", supersedes=old.name)
    new.write_text(json.dumps(graph, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if not backup.exists():
        backup.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(store.path, backup)
    digest = sha(new)
    state.graph_artifacts.append({
        "schema_version": 1, "algorithm": "routeb_revision260_bridge_audits/v1",
        "graph_sha256": digest, "roots": [], "selected_nodes": [],
        "source": "independent-sidecars:GCH-plus-GCI", "evidence_sha256": sha(gci / "receipt.json"),
        "strict_compile": False, "registry_promoted": False,
        "formal_certificate_allowed": False,
    })
    state.event("routeb_revision260_bridge_audits_recorded",
                proposed_dag=ref(new), proposed_dag_sha256=digest,
                audits=[bridge["kind"], harness["kind"]],
                local_guard_closed=True, runtime_boxmetrics_closed=False,
                structural_harness_closed=True, physical_fullstate_closed=False,
                registry_promoted=False, formal_certificate_allowed=False,
                broad_regression_run=False)
    store.save(state)
    print(json.dumps({"revision": state.revision, "graph": new.name,
                      "registry": len(state.registry), "formal_certificate_allowed": False}))


if __name__ == "__main__":
    main()
