"""Persist the MBD interval-representation failure analysis."""
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
    assert state.revision == 261 and not state.registry
    old = ROOT / "artifacts/routeb_6dof/block45-obligations-v215.json"
    new = ROOT / "artifacts/routeb_6dof/block45-obligations-v216.json"
    backup = ROOT / "artifacts/routeb_storage_checkpoint_20260907/state-before-revision262.json"
    sidecar = ROOT / "artifacts/task_GCK_mbd_interval_failure_analysis_20260907"
    files = [sidecar / "REPORT.md", sidecar / "receipt.json", sidecar / "checker.py",
             sidecar / "fixture.py"]
    assert old.is_file() and not new.exists() and all(path.is_file() for path in files)
    receipt = json.loads((sidecar / "receipt.json").read_text(encoding="utf-8"))
    graph = json.loads(old.read_text(encoding="utf-8"))
    audit = {
        "kind": "routeb_mbd_interval_representation_contract",
        "status": receipt.get("status", "PASS_FAIL_CLOSED"),
        "evidence_level": "deterministic-receipt-analysis",
        "sidecar": str(sidecar.resolve()),
        "files": [ref(path) for path in files],
        "failure_class": "point_payload_not_contained_in_independently_generated_bigfloat_interval",
        "minimal_contract": "point and interval must share canonical numeric representation, source snapshot, and point key",
        "matrix_partition": {"D_one_based": [1, 2, 3, 6], "B_one_based": [4, 5]},
        "coverage_complete": False,
        "registry_promoted": False,
        "formal_certificate_allowed": False,
        "physical_action_claim": False,
    }
    graph.setdefault("bottleneck_audits", []).append(audit)
    graph.setdefault("external_intakes", []).append({
        "kind": audit["kind"], "source": "independent-sidecar:GCK-mbd-interval-analysis",
        "sidecar": audit["sidecar"], "files": audit["files"],
        "registry_promoted": False, "formal_certificate_allowed": False,
    })
    graph.setdefault("open_frontier_updates", []).append({
        "node": audit["kind"], "status": "representation_contract_open",
        "reason": audit["minimal_contract"],
    })
    graph.update(schema="routeb-proposed-proof-dag-v216", supersedes=old.name)
    new.write_text(json.dumps(graph, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if not backup.exists():
        backup.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(store.path, backup)
    digest = sha(new)
    state.graph_artifacts.append({
        "schema_version": 1, "algorithm": "routeb_revision262_mbd_interval_contract/v1",
        "graph_sha256": digest, "roots": [], "selected_nodes": [],
        "source": "independent-sidecar:GCK-mbd-interval-analysis",
        "evidence_sha256": sha(sidecar / "receipt.json"), "strict_compile": False,
        "registry_promoted": False, "formal_certificate_allowed": False,
    })
    state.event("routeb_revision262_mbd_interval_contract_recorded",
                proposed_dag=ref(new), proposed_dag_sha256=digest,
                representation_contract_open=True, physical_action_claim=False,
                registry_promoted=False, formal_certificate_allowed=False,
                broad_regression_run=False)
    store.save(state)
    print(json.dumps({"revision": state.revision, "graph": new.name,
                      "registry": len(state.registry), "formal_certificate_allowed": False}))


if __name__ == "__main__":
    main()
