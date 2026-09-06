"""Record the finite-cell successor/continuation accounting contract."""
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
    assert state.revision == 188 and not state.registry
    old_graph = ROOT / "artifacts/routeb_6dof/block45-obligations-v142.json"
    new_graph = ROOT / "artifacts/routeb_6dof/block45-obligations-v143.json"
    backup = ROOT / "artifacts/routeb_storage_checkpoint_20260906/state-before-revision189.json"
    assert old_graph.is_file() and not new_graph.exists()
    base = ROOT / "artifacts/task_AX_finite_cell_ledger_v2"
    files = {name: base / name for name in (
        "finite_cell_ledger.schema.json", "check_finite_cell_ledger.py",
        "finite_cell_ledger_v2.json", "README.md")}
    files["test_task_ax_finite_cell_ledger.py"] = ROOT / "tests/test_task_ax_finite_cell_ledger.py"
    for path in files.values():
        assert path.is_file(), path
    ledger = json.loads(files["finite_cell_ledger_v2.json"].read_text(encoding="utf-8"))
    assert ledger.get("status") == "OPEN" and ledger.get("policy", {}).get("no_flowpipe_generated") is True
    graph = json.loads(old_graph.read_text(encoding="utf-8"))
    graph.setdefault("bottleneck_audits", []).append({
        "kind": "routeb_finite_cell_ledger_v2",
        "status": "OPEN_CONTINUATION_RECEIPTS_MISSING",
        "evidence_level": "fail_closed_successor_accounting_schema",
        "semantic_boundary": "no produced flowpipe or actual matched successor receipt exists",
        "registry_promoted": False, "formal_certificate_allowed": False,
        "files": {key: {"path": ref(path), "sha256": sha(path)} for key, path in files.items()},
    })
    graph.setdefault("open_frontier_updates", []).append({
        "node": "RouteBFlowpipe.finite_cell_successor_accounting_v2",
        "status": "schema_ready_receipts_open",
        "reason": "missing continuation receipts cannot create successor edges or close candidates; positive step and unique accounting are enforced",
    })
    graph.update(schema="routeb-proposed-proof-dag-v143", supersedes=old_graph.name)
    new_graph.write_text(json.dumps(graph, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if not backup.exists():
        backup.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(store.path, backup)
    digest = sha(new_graph)
    state.graph_artifacts.append({
        "schema_version": 1, "algorithm": "routeb_finite_cell_ledger_v2/v1",
        "graph_sha256": digest, "roots": [], "selected_nodes": [],
        "source": "fail-closed finite-cell continuation accounting",
        "schema_sha256": sha(files["finite_cell_ledger.schema.json"]),
        "ledger_sha256": sha(files["finite_cell_ledger_v2.json"]),
        "flowpipe_constructed": False, "registry_promoted": False,
        "formal_certificate_allowed": False,
    })
    state.event(
        "routeb_finite_cell_ledger_v2_recorded", proposed_dag=ref(new_graph),
        proposed_dag_sha256=digest, ledger=ref(files["finite_cell_ledger_v2.json"]),
        ledger_sha256=sha(files["finite_cell_ledger_v2.json"]), status="OPEN_CONTINUATION_RECEIPTS_MISSING",
        flowpipe_constructed=False, registry_promoted=False, formal_certificate_allowed=False,
        broad_regression_run=False,
    )
    store.save(state)
    print({"revision": state.revision, "graph": new_graph.name, "registry": len(state.registry)})


if __name__ == "__main__":
    main()
