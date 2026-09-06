"""Record the revision-bound L0-L6 dry-run rebind."""
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
    assert state.revision == 182 and not state.registry
    old_graph = ROOT / "artifacts/routeb_6dof/block45-obligations-v136.json"
    new_graph = ROOT / "artifacts/routeb_6dof/block45-obligations-v137.json"
    backup = ROOT / "artifacts/routeb_storage_checkpoint_20260906/state-before-revision183.json"
    assert old_graph.is_file() and not new_graph.exists()
    base = ROOT / "artifacts/task_AL_l0_l6_rebind_20260906"
    files = {name: base / name for name in (
        "snapshot.json", "rebased_proposal_revision182.json", "stale_proposal_rejection.json",
        "rebase_proposal_check.json", "REPORT.md")}
    for path in files.values():
        assert path.is_file(), path
    check = json.loads(files["rebase_proposal_check.json"].read_text(encoding="utf-8"))
    assert check.get("failures", []) == []
    graph = json.loads(old_graph.read_text(encoding="utf-8"))
    graph.setdefault("bottleneck_audits", []).append({
        "kind": "routeb_l0_l6_revision_rebind",
        "status": "DRY_RUN_REBASE_PASS_NO_INSTALL",
        "evidence_level": "snapshot_bound_proposal_check",
        "semantic_boundary": "child installation and registry admission were not performed",
        "stale_proposal_rejected": True, "registry_delta": 0,
        "registry_promoted": False, "formal_certificate_allowed": False,
        "files": {key: {"path": ref(path), "sha256": sha(path)} for key, path in files.items()},
    })
    graph.setdefault("open_frontier_updates", []).append({
        "node": "Workflow.DAG.L0_L6_revision_rebind",
        "status": "fresh_dry_run_parent_open",
        "reason": "revision-182 rebase has zero structural failures; actual theorem installation remains a separate state mutation",
    })
    graph.update(schema="routeb-proposed-proof-dag-v137", supersedes=old_graph.name)
    new_graph.write_text(json.dumps(graph, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if not backup.exists():
        backup.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(store.path, backup)
    digest = sha(new_graph)
    state.graph_artifacts.append({
        "schema_version": 1, "algorithm": "routeb_l0_l6_revision_rebind/v1",
        "graph_sha256": digest, "roots": [], "selected_nodes": [],
        "source": "revision-182 snapshot-bound L0-L6 dry-run rebind",
        "proposal_sha256": sha(files["rebased_proposal_revision182.json"]),
        "registry_delta": 0, "registry_promoted": False,
        "formal_certificate_allowed": False,
    })
    state.event(
        "routeb_l0_l6_revision_rebind_recorded", proposed_dag=ref(new_graph),
        proposed_dag_sha256=digest, proposal=ref(files["rebased_proposal_revision182.json"]),
        proposal_sha256=sha(files["rebased_proposal_revision182.json"]),
        stale_rejection=ref(files["stale_proposal_rejection.json"]),
        stale_rejection_sha256=sha(files["stale_proposal_rejection.json"]),
        status="DRY_RUN_REBASE_PASS_NO_INSTALL", registry_delta=0,
        registry_promoted=False, formal_certificate_allowed=False, broad_regression_run=False,
    )
    store.save(state)
    print({"revision": state.revision, "graph": new_graph.name, "registry": len(state.registry)})


if __name__ == "__main__":
    main()
