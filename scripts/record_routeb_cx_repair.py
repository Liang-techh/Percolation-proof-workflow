"""Record the CX checker path-resolution repair and its replay evidence."""
from __future__ import annotations

import hashlib
import json
import shutil
from pathlib import Path

from record_routeb_port_progress import ROOT, ref
from percolation_workflow.store import StateStore


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def main() -> None:
    store = StateStore(ROOT / "artifacts/routeb_6dof/state.json")
    state = store.load()
    assert state.revision == 201 and not state.registry
    old = ROOT / "artifacts/routeb_6dof/block45-obligations-v155.json"
    new = ROOT / "artifacts/routeb_6dof/block45-obligations-v156.json"
    backup = ROOT / "artifacts/routeb_storage_checkpoint_20260906/state-before-revision202.json"
    checker = ROOT / "artifacts/task_CX_schur_dN_compute_20260906/check.py"
    report = ROOT / "artifacts/task_CX_schur_dN_compute_20260906/REPORT.md"
    ledger = ROOT / "artifacts/task_CX_schur_dN_compute_20260906/ledger.json"
    assert old.is_file() and not new.exists() and checker.is_file() and report.is_file() and ledger.is_file()
    graph = json.loads(old.read_text(encoding="utf-8"))
    graph.setdefault("repair_audits", []).append({
        "kind": "routeb_cx_checker_path_resolution",
        "status": "REPAIRED_ROOT_REPLAY_PASS",
        "error_class": "tooling_path_resolution",
        "before": "relative ledger.json lookup fails outside sidecar cwd",
        "after": "ledger resolved relative to checker __file__",
        "replay": "TASK_CX_BOUNDED_COMPUTATION_OK_FAIL_CLOSED",
        "registry_promoted": False, "formal_certificate_allowed": False,
        "files": {k: {"path": ref(v), "sha256": sha(v)} for k, v in {"checker": checker, "report": report, "ledger": ledger}.items()},
    })
    graph.setdefault("open_frontier_updates", []).append({"node": "RouteBSchur.dN_checker_reproducibility", "status": "repaired_root_replay_pass", "reason": "path-resolution repair preserves fail-closed mathematical verdict and evidence hash"})
    graph.update(schema="routeb-proposed-proof-dag-v156", supersedes=old.name)
    new.write_text(json.dumps(graph, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if not backup.exists():
        backup.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(store.path, backup)
    digest = sha(new)
    state.graph_artifacts.append({"schema_version": 1, "algorithm": "routeb_cx_checker_path_resolution/v1", "graph_sha256": digest, "roots": [], "selected_nodes": [], "source": str(checker), "evidence_sha256": sha(checker), "repair_class": "tooling_path_resolution", "registry_promoted": False, "formal_certificate_allowed": False})
    state.event("routeb_cx_checker_repaired", proposed_dag=ref(new), proposed_dag_sha256=digest, checker=ref(checker), checker_sha256=sha(checker), replay="TASK_CX_BOUNDED_COMPUTATION_OK_FAIL_CLOSED", registry_promoted=False, formal_certificate_allowed=False, broad_regression_run=False)
    store.save(state)
    print({"revision": state.revision, "graph": new.name, "registry": len(state.registry)})


if __name__ == "__main__":
    main()
