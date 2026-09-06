"""Persist source comparator failure evidence without mutating source data."""
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
    assert state.revision == 236 and not state.registry
    old = ROOT / "artifacts/routeb_6dof/block45-obligations-v190.json"
    new = ROOT / "artifacts/routeb_6dof/block45-obligations-v191.json"
    backup = ROOT / "artifacts/routeb_storage_checkpoint_20260907/state-before-revision237.json"
    sidecar = ROOT / "artifacts/task_GAU_source_comparator_contract_20260907"
    files = [sidecar / "REPORT.md", sidecar / "manifest.json", sidecar / "checker.py"]
    assert old.is_file() and not new.exists() and all(path.is_file() for path in files)
    graph = json.loads(old.read_text(encoding="utf-8"))
    reason = (
        "Source comparator rejects the current candidate: original/candidate "
        "versions are undeclared, SHA-256 values mismatch, and the candidate "
        "does not match the pinned P3 snapshot. Consumer/index/mu/h fields pass."
    )
    audit = {
        "kind": "routeb_source_comparator_contract_audit", "status": "FAIL_CLOSED",
        "evidence_level": "independent_sidecar_frontier_audit",
        "semantic_boundary": reason, "sidecar": str(sidecar.resolve()),
        "files": [ref(path) for path in files], "registry_promoted": False,
        "formal_certificate_allowed": False,
    }
    graph.setdefault("bottleneck_audits", []).append(audit)
    graph.setdefault("external_intakes", []).append({
        "kind": audit["kind"], "source": "local-routeb-revision237-source-comparator",
        "sidecar": audit["sidecar"], "files": audit["files"],
        "registry_promoted": False, "formal_certificate_allowed": False,
    })
    graph.setdefault("open_frontier_updates", []).append({
        "node": audit["kind"], "status": "fail_closed", "reason": reason,
    })
    graph.update(schema="routeb-proposed-proof-dag-v191", supersedes=old.name)
    new.write_text(json.dumps(graph, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if not backup.exists():
        backup.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(store.path, backup)
    digest = sha(new)
    state.graph_artifacts.append({
        "schema_version": 1, "algorithm": "routeb_revision237_source_comparator/v1",
        "graph_sha256": digest, "roots": [], "selected_nodes": [],
        "source": "independent-sidecar:GAU-source-comparator",
        "evidence_sha256": sha(sidecar / "manifest.json"), "strict_compile": False,
        "registry_promoted": False, "formal_certificate_allowed": False,
    })
    state.event(
        "routeb_revision237_source_comparator_recorded", proposed_dag=ref(new),
        proposed_dag_sha256=digest, audit={"kind": audit["kind"], "status": audit["status"]},
        registry_promoted=False, formal_certificate_allowed=False, broad_regression_run=False,
    )
    store.save(state)
    print({"revision": state.revision, "graph": new.name, "registry": len(state.registry)})


if __name__ == "__main__":
    main()
