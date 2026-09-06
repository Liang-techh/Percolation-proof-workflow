"""Persist the structural residual-ledger schema and its repaired checker."""
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
    assert state.revision == 242 and not state.registry
    old = ROOT / "artifacts/routeb_6dof/block45-obligations-v196.json"
    new = ROOT / "artifacts/routeb_6dof/block45-obligations-v197.json"
    backup = ROOT / "artifacts/routeb_storage_checkpoint_20260907/state-before-revision243.json"
    sidecar = ROOT / "artifacts/task_GBC_residual_ledger_schema_20260907"
    files = [sidecar / "ledger.json", sidecar / "REPORT.md", sidecar / "checker.py"]
    assert old.is_file() and not new.exists() and all(path.is_file() for path in files)
    graph = json.loads(old.read_text(encoding="utf-8"))
    reason = (
        "Structural residual-ledger schema checker passes after path/wording repair: "
        "six rho channels, full-state key, canonical remainder decomposition and "
        "exactly-once charge are checked; this remains external evidence only."
    )
    audit = {
        "kind": "routeb_residual_ledger_schema_audit", "status": "STRUCTURAL_PASS_EXTERNAL_EVIDENCE_ONLY",
        "evidence_level": "independent_sidecar_frontier_audit",
        "semantic_boundary": reason, "sidecar": str(sidecar.resolve()),
        "files": [ref(path) for path in files], "registry_promoted": False,
        "formal_certificate_allowed": False,
    }
    graph.setdefault("bottleneck_audits", []).append(audit)
    graph.setdefault("external_intakes", []).append({
        "kind": audit["kind"], "source": "local-routeb-revision243-residual-schema",
        "sidecar": audit["sidecar"], "files": audit["files"],
        "registry_promoted": False, "formal_certificate_allowed": False,
    })
    graph.setdefault("open_frontier_updates", []).append({
        "node": audit["kind"], "status": "structural_pass_external_evidence_only", "reason": reason,
    })
    graph.update(schema="routeb-proposed-proof-dag-v197", supersedes=old.name)
    new.write_text(json.dumps(graph, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if not backup.exists():
        backup.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(store.path, backup)
    digest = sha(new)
    state.graph_artifacts.append({
        "schema_version": 1, "algorithm": "routeb_revision243_residual_schema/v1",
        "graph_sha256": digest, "roots": [], "selected_nodes": [],
        "source": "independent-sidecar:GBC-residual-ledger-schema",
        "evidence_sha256": sha(sidecar / "ledger.json"), "strict_compile": False,
        "registry_promoted": False, "formal_certificate_allowed": False,
    })
    state.event(
        "routeb_revision243_residual_schema_recorded", proposed_dag=ref(new),
        proposed_dag_sha256=digest, audit={"kind": audit["kind"], "status": audit["status"]},
        registry_promoted=False, formal_certificate_allowed=False, broad_regression_run=False,
    )
    store.save(state)
    print({"revision": state.revision, "graph": new.name, "registry": len(state.registry)})


if __name__ == "__main__":
    main()
