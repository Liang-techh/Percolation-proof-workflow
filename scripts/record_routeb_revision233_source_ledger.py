"""Persist the stricter source-ledger manifest as a new frontier snapshot."""
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
    assert state.revision == 232 and not state.registry
    old = ROOT / "artifacts/routeb_6dof/block45-obligations-v186.json"
    new = ROOT / "artifacts/routeb_6dof/block45-obligations-v187.json"
    backup = ROOT / "artifacts/routeb_storage_checkpoint_20260907/state-before-revision233.json"
    sidecar = ROOT / "artifacts/routeb_source_ledger_contract_20260906_v5"
    files = [
        sidecar / "manifest.json",
        sidecar / "REPORT.md",
        ROOT / "scripts/routeb_source_ledger_contract.py",
        ROOT / "scripts/record_routeb_source_ledger_contract_20260906.py",
        ROOT / "tests/test_routeb_source_ledger_contract.py",
    ]
    assert old.is_file() and not new.exists() and all(p.is_file() for p in files)

    graph = json.loads(old.read_text(encoding="utf-8"))
    reason = (
        "The stricter exporter binds source bytes and expected hashes and leaves "
        "one interval-bounds source plus 14 physical receipt fields missing; "
        "recorder exits 2 and cannot promote a candidate."
    )
    audit = {
        "kind": "routeb_source_ledger_contract_v5_audit",
        "status": "FAIL_CLOSED",
        "evidence_level": "independent_sidecar_frontier_audit",
        "semantic_boundary": reason,
        "sidecar": str(sidecar.resolve()),
        "files": [ref(p) for p in files],
        "registry_promoted": False,
        "formal_certificate_allowed": False,
    }
    graph.setdefault("bottleneck_audits", []).append(audit)
    graph.setdefault("external_intakes", []).append({
        "kind": audit["kind"],
        "source": "local-routeb-revision233-source-ledger",
        "sidecar": audit["sidecar"],
        "files": audit["files"],
        "registry_promoted": False,
        "formal_certificate_allowed": False,
    })
    graph.setdefault("open_frontier_updates", []).append({
        "node": audit["kind"], "status": "fail_closed", "reason": reason,
    })
    graph.update(schema="routeb-proposed-proof-dag-v187", supersedes=old.name)
    new.write_text(json.dumps(graph, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if not backup.exists():
        backup.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(store.path, backup)

    digest = sha(new)
    state.graph_artifacts.append({
        "schema_version": 1,
        "algorithm": "routeb_revision233_source_ledger/v1",
        "graph_sha256": digest,
        "roots": [], "selected_nodes": [],
        "source": "independent-sidecar:source-ledger-contract-v5",
        "evidence_sha256": sha(sidecar / "manifest.json"),
        "strict_compile": False,
        "registry_promoted": False,
        "formal_certificate_allowed": False,
    })
    state.event(
        "routeb_revision233_source_ledger_recorded",
        proposed_dag=ref(new), proposed_dag_sha256=digest,
        audit={"kind": audit["kind"], "status": audit["status"]},
        registry_promoted=False, formal_certificate_allowed=False,
        broad_regression_run=False,
    )
    store.save(state)
    print({"revision": state.revision, "graph": new.name, "registry": len(state.registry)})


if __name__ == "__main__":
    main()
