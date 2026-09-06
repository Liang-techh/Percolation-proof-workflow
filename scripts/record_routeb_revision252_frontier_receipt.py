"""Persist the deterministic frontier dispatch receipt."""
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
    assert state.revision == 251 and not state.registry
    old = ROOT / "artifacts/routeb_6dof/block45-obligations-v205.json"
    new = ROOT / "artifacts/routeb_6dof/block45-obligations-v206.json"
    backup = ROOT / "artifacts/routeb_storage_checkpoint_20260907/state-before-revision252.json"
    sidecar = ROOT / "artifacts/task_GBQ_frontier_dispatch_receipt_20260907"
    files = [sidecar / "REPORT.md", sidecar / "receipt.json", sidecar / "checker.py"]
    assert old.is_file() and not new.exists() and all(path.is_file() for path in files)
    receipt = json.loads((sidecar / "receipt.json").read_text(encoding="utf-8"))
    graph = json.loads(old.read_text(encoding="utf-8"))
    reason = (
        "The deterministic revision-251 frontier receipt confirms 54 leaves, "
        "28 obstruction-eligible formalizable dispatches, 26 blocked leaves, "
        "and explicit Lean/source lane classification; q1 remains advisory-only."
    )
    audit = {
        "kind": "routeb_frontier_dispatch_receipt",
        "status": "PASS_READ_ONLY_FAIL_CLOSED_ADMISSION",
        "evidence_level": "deterministic-frontier-receipt",
        "semantic_boundary": reason,
        "sidecar": str(sidecar.resolve()),
        "files": [ref(path) for path in files],
        "state_revision": receipt["state_revision"],
        "frontier_count": receipt["frontier"]["count"],
        "formalizable_count": receipt["frontier"]["formalizable_count"],
        "obstruction_gate": receipt["frontier"]["obstruction_gate"],
        "classification": receipt["frontier"]["explicit_verification_domain_classification"],
        "projection_read_only": receipt["invariants"]["projection_read_only"],
        "registry_promoted": False,
        "formal_certificate_allowed": False,
    }
    graph.setdefault("bottleneck_audits", []).append(audit)
    graph.setdefault("external_intakes", []).append({
        "kind": audit["kind"], "source": "independent-sidecar:GBQ-frontier-dispatch",
        "sidecar": audit["sidecar"], "files": audit["files"],
        "registry_promoted": False, "formal_certificate_allowed": False,
    })
    graph.setdefault("open_frontier_updates", []).append({
        "node": audit["kind"], "status": "advisory_receipt_only", "reason": reason,
    })
    graph.update(schema="routeb-proposed-proof-dag-v206", supersedes=old.name)
    new.write_text(json.dumps(graph, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if not backup.exists():
        backup.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(store.path, backup)
    digest = sha(new)
    state.graph_artifacts.append({
        "schema_version": 1,
        "algorithm": "routeb_revision252_frontier_receipt/v1",
        "graph_sha256": digest, "roots": [], "selected_nodes": [],
        "source": "independent-sidecar:GBQ-frontier-dispatch",
        "evidence_sha256": sha(sidecar / "receipt.json"),
        "strict_compile": False, "registry_promoted": False,
        "formal_certificate_allowed": False,
    })
    state.event(
        "routeb_revision252_frontier_receipt_recorded",
        proposed_dag=ref(new), proposed_dag_sha256=digest,
        audit={"kind": audit["kind"], "status": audit["status"]},
        registry_promoted=False, formal_certificate_allowed=False,
        broad_regression_run=False,
    )
    store.save(state)
    print({"revision": state.revision, "graph": new.name, "registry": len(state.registry)})


if __name__ == "__main__":
    main()
