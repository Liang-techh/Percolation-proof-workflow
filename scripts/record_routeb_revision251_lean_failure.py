"""Persist the failed Lean adapter attempt as a repair-loop frontier item."""
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
    assert state.revision == 250 and not state.registry
    old = ROOT / "artifacts/routeb_6dof/block45-obligations-v204.json"
    new = ROOT / "artifacts/routeb_6dof/block45-obligations-v205.json"
    backup = ROOT / "artifacts/routeb_storage_checkpoint_20260907/state-before-revision251.json"
    sidecar = ROOT / "artifacts/task_GBM_lean_local_obstruction_20260907"
    files = [sidecar / "RouteBLocalObstructionAdapter.lean",
             sidecar / "REPORT.md", sidecar / "receipt.json"]
    assert old.is_file() and not new.exists() and all(path.is_file() for path in files)
    receipt = json.loads((sidecar / "receipt.json").read_text(encoding="utf-8"))
    graph = json.loads(old.read_text(encoding="utf-8"))
    reason = (
        "Pinned Lean compilation failed with parser errors and unsolved goals; "
        "no olean was produced and parser-recovery sorryAx prevents any theorem "
        "admission. The draft remains a repair-loop input."
    )
    audit = {
        "kind": "routeb_lean_local_obstruction_adapter_attempt",
        "status": "OPEN_COMPILE_OBSTRUCTION",
        "evidence_level": "failed-pinned-lean-attempt",
        "semantic_boundary": reason,
        "sidecar": str(sidecar.resolve()),
        "files": [ref(path) for path in files],
        "compile": receipt["compile"],
        "source_sha256": receipt["source_sha256"],
        "olean_exists": False,
        "registry_promoted": False,
        "formal_certificate_allowed": False,
    }
    graph.setdefault("bottleneck_audits", []).append(audit)
    graph.setdefault("external_intakes", []).append({
        "kind": audit["kind"], "source": "independent-sidecar:GBM-lean-local-obstruction",
        "sidecar": audit["sidecar"], "files": audit["files"],
        "registry_promoted": False, "formal_certificate_allowed": False,
    })
    graph.setdefault("open_frontier_updates", []).append({
        "node": audit["kind"], "status": "open_compile_obstruction", "reason": reason,
        "repair_inputs": receipt.get("failure_summary", []),
    })
    graph.update(schema="routeb-proposed-proof-dag-v205", supersedes=old.name)
    new.write_text(json.dumps(graph, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if not backup.exists():
        backup.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(store.path, backup)
    digest = sha(new)
    state.graph_artifacts.append({
        "schema_version": 1,
        "algorithm": "routeb_revision251_lean_failure/v1",
        "graph_sha256": digest, "roots": [], "selected_nodes": [],
        "source": "independent-sidecar:GBM-lean-local-obstruction",
        "evidence_sha256": sha(sidecar / "receipt.json"),
        "strict_compile": False, "registry_promoted": False,
        "formal_certificate_allowed": False,
    })
    state.event(
        "routeb_revision251_lean_failure_recorded",
        proposed_dag=ref(new), proposed_dag_sha256=digest,
        audit={"kind": audit["kind"], "status": audit["status"]},
        repair_inputs=receipt.get("failure_summary", []),
        registry_promoted=False, formal_certificate_allowed=False,
        broad_regression_run=False,
    )
    store.save(state)
    print({"revision": state.revision, "graph": new.name, "registry": len(state.registry)})


if __name__ == "__main__":
    main()
