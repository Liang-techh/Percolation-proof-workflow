"""Persist the conditional prefix-assembly contract."""
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
    assert state.revision == 238 and not state.registry
    old = ROOT / "artifacts/routeb_6dof/block45-obligations-v192.json"
    new = ROOT / "artifacts/routeb_6dof/block45-obligations-v193.json"
    backup = ROOT / "artifacts/routeb_storage_checkpoint_20260907/state-before-revision239.json"
    sidecar = ROOT / "artifacts/task_GAX_direct_output_prefix_20260907"
    files = [sidecar / "REPORT.md", sidecar / "theorem_contract.json"]
    assert old.is_file() and not new.exists() and all(path.is_file() for path in files)
    graph = json.loads(old.read_text(encoding="utf-8"))
    reason = (
        "Conditional direct-output prefix contract preserves arbitrary pre-exit "
        "horizon, curve regularity, source/eta and implementation-defect premises; "
        "coverage and FirstExitSafe remain open."
    )
    audit = {
        "kind": "routeb_direct_output_prefix_contract_audit", "status": "OPEN_FAIL_CLOSED",
        "evidence_level": "independent_sidecar_frontier_audit",
        "semantic_boundary": reason, "sidecar": str(sidecar.resolve()),
        "files": [ref(path) for path in files], "registry_promoted": False,
        "formal_certificate_allowed": False,
    }
    graph.setdefault("bottleneck_audits", []).append(audit)
    graph.setdefault("external_intakes", []).append({
        "kind": audit["kind"], "source": "local-routeb-revision239-prefix-contract",
        "sidecar": audit["sidecar"], "files": audit["files"],
        "registry_promoted": False, "formal_certificate_allowed": False,
    })
    graph.setdefault("open_frontier_updates", []).append({
        "node": audit["kind"], "status": "open_fail_closed", "reason": reason,
    })
    graph.update(schema="routeb-proposed-proof-dag-v193", supersedes=old.name)
    new.write_text(json.dumps(graph, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if not backup.exists():
        backup.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(store.path, backup)
    digest = sha(new)
    state.graph_artifacts.append({
        "schema_version": 1, "algorithm": "routeb_revision239_prefix_contract/v1",
        "graph_sha256": digest, "roots": [], "selected_nodes": [],
        "source": "independent-sidecar:GAX-prefix-contract",
        "evidence_sha256": sha(sidecar / "theorem_contract.json"), "strict_compile": False,
        "registry_promoted": False, "formal_certificate_allowed": False,
    })
    state.event(
        "routeb_revision239_prefix_contract_recorded", proposed_dag=ref(new),
        proposed_dag_sha256=digest, audit={"kind": audit["kind"], "status": audit["status"]},
        registry_promoted=False, formal_certificate_allowed=False, broad_regression_run=False,
    )
    store.save(state)
    print({"revision": state.revision, "graph": new.name, "registry": len(state.registry)})


if __name__ == "__main__":
    main()
