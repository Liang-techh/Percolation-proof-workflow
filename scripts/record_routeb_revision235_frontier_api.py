"""Persist the read-only frontier-cut API improvement."""
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
    assert state.revision == 234 and not state.registry
    old = ROOT / "artifacts/routeb_6dof/block45-obligations-v188.json"
    new = ROOT / "artifacts/routeb_6dof/block45-obligations-v189.json"
    backup = ROOT / "artifacts/routeb_storage_checkpoint_20260907/state-before-revision235.json"
    files = [
        ROOT / "src/percolation_workflow/math_frontier.py",
        ROOT / "src/percolation_workflow/__init__.py",
        ROOT / "tests/test_math_frontier_policy.py",
    ]
    assert old.is_file() and not new.exists() and all(path.is_file() for path in files)
    graph = json.loads(old.read_text(encoding="utf-8"))
    reason = (
        "Added a read-only deterministic frontier cut grouped by Lean/source/"
        "numeric/other lanes with obstruction eligibility and cut hash; it does "
        "not mutate theorem or admission state."
    )
    audit = {
        "kind": "routeb_frontier_cut_api_audit",
        "status": "IMPLEMENTED_FOCUSED_TEST_PASS",
        "evidence_level": "workflow_api_change",
        "semantic_boundary": reason,
        "sidecar": str((ROOT / "src/percolation_workflow/math_frontier.py").resolve()),
        "files": [ref(path) for path in files],
        "registry_promoted": False,
        "formal_certificate_allowed": False,
    }
    graph.setdefault("bottleneck_audits", []).append(audit)
    graph.setdefault("external_intakes", []).append({
        "kind": audit["kind"], "source": "local-routeb-revision235-frontier-api",
        "sidecar": audit["sidecar"], "files": audit["files"],
        "registry_promoted": False, "formal_certificate_allowed": False,
    })
    graph.setdefault("open_frontier_updates", []).append({
        "node": audit["kind"], "status": "implemented_focused_test_pass", "reason": reason,
    })
    graph.update(schema="routeb-proposed-proof-dag-v189", supersedes=old.name)
    new.write_text(json.dumps(graph, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if not backup.exists():
        backup.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(store.path, backup)
    digest = sha(new)
    state.graph_artifacts.append({
        "schema_version": 1, "algorithm": "routeb_revision235_frontier_api/v1",
        "graph_sha256": digest, "roots": [], "selected_nodes": [],
        "source": "workflow-api:build_frontier_cut",
        "evidence_sha256": sha(ROOT / "tests/test_math_frontier_policy.py"),
        "strict_compile": False, "registry_promoted": False,
        "formal_certificate_allowed": False,
    })
    state.event(
        "routeb_revision235_frontier_api_recorded", proposed_dag=ref(new),
        proposed_dag_sha256=digest, audit={"kind": audit["kind"], "status": audit["status"]},
        registry_promoted=False, formal_certificate_allowed=False, broad_regression_run=False,
    )
    store.save(state)
    print({"revision": state.revision, "graph": new.name, "registry": len(state.registry)})


if __name__ == "__main__":
    main()
