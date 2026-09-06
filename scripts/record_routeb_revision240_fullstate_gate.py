"""Persist the full-state descriptor gate derived from the PMI obstruction."""
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
    assert state.revision == 239 and not state.registry
    old = ROOT / "artifacts/routeb_6dof/block45-obligations-v193.json"
    new = ROOT / "artifacts/routeb_6dof/block45-obligations-v194.json"
    backup = ROOT / "artifacts/routeb_storage_checkpoint_20260907/state-before-revision240.json"
    sidecar = ROOT / "artifacts/task_GBB_fullstate_descriptor_gate_20260907"
    files = [sidecar / "REPORT.md", sidecar / "contract.json"]
    assert old.is_file() and not new.exists() and all(path.is_file() for path in files)
    graph = json.loads(old.read_text(encoding="utf-8"))
    reason = (
        "Full-state descriptor/Schur gate is specified after the exact PMI "
        "projection obstruction: q,dq,w,aB,aD, both descriptor rows, MBD*aD, "
        "six residual channels and one-charge remainder are required; replacement remains undecided."
    )
    audit = {
        "kind": "routeb_fullstate_descriptor_gate_audit",
        "status": "OPEN_FAIL_CLOSED_DESIGN_ONLY",
        "evidence_level": "independent_sidecar_frontier_audit",
        "semantic_boundary": reason,
        "sidecar": str(sidecar.resolve()), "files": [ref(path) for path in files],
        "registry_promoted": False, "formal_certificate_allowed": False,
    }
    graph.setdefault("bottleneck_audits", []).append(audit)
    graph.setdefault("external_intakes", []).append({
        "kind": audit["kind"], "source": "local-routeb-revision240-fullstate-gate",
        "sidecar": audit["sidecar"], "files": audit["files"],
        "registry_promoted": False, "formal_certificate_allowed": False,
    })
    graph.setdefault("open_frontier_updates", []).append({
        "node": audit["kind"], "status": "open_fail_closed_design_only", "reason": reason,
    })
    graph.update(schema="routeb-proposed-proof-dag-v194", supersedes=old.name)
    new.write_text(json.dumps(graph, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if not backup.exists():
        backup.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(store.path, backup)
    digest = sha(new)
    state.graph_artifacts.append({
        "schema_version": 1, "algorithm": "routeb_revision240_fullstate_gate/v1",
        "graph_sha256": digest, "roots": [], "selected_nodes": [],
        "source": "independent-sidecar:GBB-fullstate-descriptor-gate",
        "evidence_sha256": sha(sidecar / "contract.json"), "strict_compile": False,
        "registry_promoted": False, "formal_certificate_allowed": False,
    })
    state.event(
        "routeb_revision240_fullstate_gate_recorded", proposed_dag=ref(new),
        proposed_dag_sha256=digest, audit={"kind": audit["kind"], "status": audit["status"]},
        registry_promoted=False, formal_certificate_allowed=False, broad_regression_run=False,
    )
    store.save(state)
    print({"revision": state.revision, "graph": new.name, "registry": len(state.registry)})


if __name__ == "__main__":
    main()
