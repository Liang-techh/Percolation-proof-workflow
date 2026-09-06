"""Persist the q1 coverage-ledger alignment audit."""
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
    assert state.revision == 265 and not state.registry
    old = ROOT / "artifacts/routeb_6dof/block45-obligations-v219.json"
    new = ROOT / "artifacts/routeb_6dof/block45-obligations-v220.json"
    backup = ROOT / "artifacts/routeb_storage_checkpoint_20260907/state-before-revision266.json"
    sidecar = ROOT / "artifacts/task_GCQ_q1_coverage_ledger_audit_20260907"
    files = [sidecar / "REPORT.md", sidecar / "receipt.json", sidecar / "checker.py"]
    assert old.is_file() and not new.exists() and all(path.is_file() for path in files)
    receipt = json.loads((sidecar / "receipt.json").read_text(encoding="utf-8"))
    graph = json.loads(old.read_text(encoding="utf-8"))
    audit = {
        "kind": "routeb_q1_coverage_ledger_alignment",
        "status": receipt.get("status"),
        "evidence_level": "static-ledger-audit",
        "sidecar": str(sidecar.resolve()), "files": [ref(path) for path in files],
        "nested_cells_are_parent_coverage": False,
        "q1_parent_remainder_closed": False,
        "adjacent_gaps_closed": False,
        "q2_q6_aligned_receipts": False,
        "coverage_complete": False, "registry_promoted": False,
        "formal_certificate_allowed": False,
        "semantic_boundary": "The ledger explicitly separates nested inheritance, parent coverage, adjacent gaps, and q2-q6 coverage.",
    }
    graph.setdefault("bottleneck_audits", []).append(audit)
    graph.setdefault("external_intakes", []).append({
        "kind": audit["kind"], "source": "independent-sidecar:GCQ-q1-coverage-ledger",
        "sidecar": audit["sidecar"], "files": audit["files"],
        "registry_promoted": False, "formal_certificate_allowed": False,
    })
    graph.setdefault("open_frontier_updates", []).append({
        "node": audit["kind"], "status": "ledger_aligned_coverage_open",
        "reason": audit["semantic_boundary"],
    })
    graph.update(schema="routeb-proposed-proof-dag-v220", supersedes=old.name)
    new.write_text(json.dumps(graph, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if not backup.exists():
        backup.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(store.path, backup)
    digest = sha(new)
    state.graph_artifacts.append({
        "schema_version": 1, "algorithm": "routeb_revision266_coverage_ledger/v1",
        "graph_sha256": digest, "roots": [], "selected_nodes": [],
        "source": "independent-sidecar:GCQ-q1-coverage-ledger",
        "evidence_sha256": sha(sidecar / "receipt.json"), "strict_compile": False,
        "registry_promoted": False, "formal_certificate_allowed": False,
    })
    state.event("routeb_revision266_coverage_ledger_recorded",
                proposed_dag=ref(new), proposed_dag_sha256=digest,
                nested_inheritance_separated=True, parent_coverage_closed=False,
                adjacent_gaps_closed=False, q2_q6_aligned=False,
                registry_promoted=False, formal_certificate_allowed=False,
                broad_regression_run=False)
    store.save(state)
    print(json.dumps({"revision": state.revision, "graph": new.name,
                      "registry": len(state.registry), "formal_certificate_allowed": False}))


if __name__ == "__main__":
    main()
