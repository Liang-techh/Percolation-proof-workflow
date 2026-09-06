"""Persist the PMI feasibility gate without deciding model replacement."""
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
    assert state.revision == 235 and not state.registry
    old = ROOT / "artifacts/routeb_6dof/block45-obligations-v189.json"
    new = ROOT / "artifacts/routeb_6dof/block45-obligations-v190.json"
    backup = ROOT / "artifacts/routeb_storage_checkpoint_20260907/state-before-revision236.json"
    sidecar = ROOT / "artifacts/task_GAW_pmi_domain_feasibility_20260907"
    files = [sidecar / "REPORT.md", sidecar / "evidence.json"]
    assert old.is_file() and not new.exists() and all(path.is_file() for path in files)
    graph = json.loads(old.read_text(encoding="utf-8"))
    reason = (
        "PMI feasibility remains OPEN_FAIL_CLOSED: current block-only domain "
        "does not supply a uniform full-state C/G or remote M_BD a_D bound; "
        "evidence is recorded only as input to the replacement decision gate."
    )
    audit = {
        "kind": "routeb_pmi_domain_feasibility_audit", "status": "OPEN_FAIL_CLOSED",
        "evidence_level": "independent_sidecar_frontier_audit",
        "semantic_boundary": reason, "sidecar": str(sidecar.resolve()),
        "files": [ref(path) for path in files], "registry_promoted": False,
        "formal_certificate_allowed": False,
    }
    graph.setdefault("bottleneck_audits", []).append(audit)
    graph.setdefault("external_intakes", []).append({
        "kind": audit["kind"], "source": "local-routeb-revision236-pmi-feasibility",
        "sidecar": audit["sidecar"], "files": audit["files"],
        "registry_promoted": False, "formal_certificate_allowed": False,
    })
    graph.setdefault("open_frontier_updates", []).append({
        "node": audit["kind"], "status": "open_fail_closed", "reason": reason,
    })
    graph.update(schema="routeb-proposed-proof-dag-v190", supersedes=old.name)
    new.write_text(json.dumps(graph, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if not backup.exists():
        backup.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(store.path, backup)
    digest = sha(new)
    state.graph_artifacts.append({
        "schema_version": 1, "algorithm": "routeb_revision236_pmi_feasibility/v1",
        "graph_sha256": digest, "roots": [], "selected_nodes": [],
        "source": "independent-sidecar:GAW-pmi-feasibility",
        "evidence_sha256": sha(sidecar / "evidence.json"), "strict_compile": False,
        "registry_promoted": False, "formal_certificate_allowed": False,
    })
    state.event(
        "routeb_revision236_pmi_feasibility_recorded", proposed_dag=ref(new),
        proposed_dag_sha256=digest, audit={"kind": audit["kind"], "status": audit["status"]},
        registry_promoted=False, formal_certificate_allowed=False, broad_regression_run=False,
    )
    store.save(state)
    print({"revision": state.revision, "graph": new.name, "registry": len(state.registry)})


if __name__ == "__main__":
    main()
