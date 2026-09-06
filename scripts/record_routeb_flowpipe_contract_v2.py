"""Refresh the full-X0 flowpipe contract to schema v2."""
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
    assert state.revision == 186 and not state.registry
    old_graph = ROOT / "artifacts/routeb_6dof/block45-obligations-v140.json"
    new_graph = ROOT / "artifacts/routeb_6dof/block45-obligations-v141.json"
    backup = ROOT / "artifacts/routeb_storage_checkpoint_20260906/state-before-revision187.json"
    assert old_graph.is_file() and not new_graph.exists()
    base = ROOT / "artifacts/routeb_agent_full_x0_flowpipe_contract_20260906"
    files = {name: base / name for name in (
        "full_x0_flowpipe_contract.json", "check_full_x0_flowpipe_contract.py", "README.md")}
    for path in files.values():
        assert path.is_file(), path
    contract = json.loads(files["full_x0_flowpipe_contract.json"].read_text(encoding="utf-8"))
    assert contract.get("schema", "").endswith("v2") and contract.get("verified") is False
    graph = json.loads(old_graph.read_text(encoding="utf-8"))
    graph.setdefault("bottleneck_audits", []).append({
        "kind": "routeb_full_x0_flowpipe_contract_v2",
        "status": "OPEN_NEEDS_ODE_RECEIPTS",
        "evidence_level": "source_bound_fail_closed_receipt_schema",
        "semantic_boundary": "no produced RHS enclosure, continuation receipt or full coverage exists",
        "registry_promoted": False, "formal_certificate_allowed": False,
        "files": {key: {"path": ref(path), "sha256": sha(path)} for key, path in files.items()},
    })
    graph.setdefault("open_frontier_updates", []).append({
        "node": "RouteBEntry.full_X0_flowpipe_receipt_schema_v2",
        "status": "schema_v2_ready_receipts_open",
        "reason": "RHS-local-Lipschitz and cell interval-RHS fields are explicit; actual outward enclosures and continuation witnesses are missing",
    })
    graph.update(schema="routeb-proposed-proof-dag-v141", supersedes=old_graph.name)
    new_graph.write_text(json.dumps(graph, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if not backup.exists():
        backup.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(store.path, backup)
    digest = sha(new_graph)
    state.graph_artifacts.append({
        "schema_version": 1, "algorithm": "routeb_full_x0_flowpipe_contract_v2/v1",
        "graph_sha256": digest, "roots": [], "selected_nodes": [],
        "source": "schema-v2 source-bound full-X0 flowpipe receipt contract",
        "contract_sha256": sha(files["full_x0_flowpipe_contract.json"]),
        "registry_promoted": False, "formal_certificate_allowed": False,
    })
    state.event(
        "routeb_full_x0_flowpipe_contract_v2_recorded", proposed_dag=ref(new_graph),
        proposed_dag_sha256=digest, contract=ref(files["full_x0_flowpipe_contract.json"]),
        contract_sha256=sha(files["full_x0_flowpipe_contract.json"]), status="OPEN_NEEDS_ODE_RECEIPTS",
        registry_promoted=False, formal_certificate_allowed=False, broad_regression_run=False,
    )
    store.save(state)
    print({"revision": state.revision, "graph": new_graph.name, "registry": len(state.registry)})


if __name__ == "__main__":
    main()
