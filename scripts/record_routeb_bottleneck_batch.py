"""Record the next Route-B bottleneck batch without promoting any theorem.

This importer records replayable audits and explicit open-frontier reasons.
It intentionally never mutates the verified registry or closes a DAG node.
"""
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
    assert state.revision == 171 and not state.registry
    old_graph = ROOT / "artifacts/routeb_6dof/block45-obligations-v125.json"
    new_graph = ROOT / "artifacts/routeb_6dof/block45-obligations-v126.json"
    backup = ROOT / "artifacts/routeb_storage_checkpoint_20260906/state-before-revision172.json"
    assert old_graph.is_file()

    batch = [
        {
            "kind": "routeb_entry_contract_audit",
            "report": ROOT / "artifacts/routeb_agent_entry_contract_20260906_033947/REPORT.md",
            "replay": ROOT / "artifacts/routeb_agent_entry_contract_20260906_033947/entry_contract_replay.py",
            "replay_output": ROOT / "artifacts/routeb_agent_entry_contract_20260906_033947/replay_output.txt",
            "status": "ENTRY_AND_FIRST_EXIT_OPEN",
            "evidence_level": "contract_audit_replay",
            "reason": "requires 14-state ramp lift, full-X0 flowpipe, entry witness, first-exit continuation and sibling accounting",
        },
        {
            "kind": "routeb_p3_to_x0_bridge_audit",
            "report": ROOT / "artifacts/routeb_agent_p3_to_x0_20260906T033903Z/REPORT.md",
            "replay": ROOT / "artifacts/routeb_agent_p3_to_x0_20260906T033903Z/check_p3_to_x0.py",
            "status": "INITIAL_SET_DISJOINT_OPEN",
            "evidence_level": "set_geometry_audit",
            "reason": "P3 local positive cell is disjoint from X0; no matched full-state ramp entry or first-exit continuation",
        },
        {
            "kind": "routeb_schur_drow_correlated_screen",
            "report": ROOT / "artifacts/routeb_agent_schur_drow_contract_20260906T101500Z/AUDIT.md",
            "numbers": ROOT / "artifacts/routeb_agent_schur_drow_contract_20260906T101500Z/NUMBERS.json",
            "replay": ROOT / "artifacts/routeb_agent_schur_drow_contract_20260906T101500Z/derive_drow_contract.py",
            "status": "CONDITIONAL_DROW_SCREEN_OPEN",
            "evidence_level": "exact_rational_conditional_screen",
            "reason": "s_D source/trajectory envelope and deployed Float64 bridge are not proved",
        },
        {
            "kind": "routeb_p4_semantic_contract_audit",
            "report": ROOT / "artifacts/routeb_agent_p4_semantic_contract_20260906T100000Z/AUDIT_REPORT.md",
            "replay": ROOT / "artifacts/routeb_agent_p4_semantic_contract_20260906T100000Z/semantic_contract_checker.py",
            "replay_output": ROOT / "artifacts/routeb_agent_p4_semantic_contract_20260906T100000Z/checker_output.json",
            "status": "AUDIT_COMPLETE_WITH_SEMANTIC_BLOCKERS",
            "evidence_level": "source_semantic_audit",
            "reason": "DH/FD/Float64, regularizer, residual linking, D-row map, coverage and Gram recovery remain open",
        },
        {
            "kind": "routeb_parent_closure_contract",
            "report": ROOT / "artifacts/routeb_agent_parent_closure_contract_20260906T094500Z/REPORT.md",
            "schema": ROOT / "artifacts/routeb_agent_parent_closure_contract_20260906T094500Z/contract.schema.json",
            "replay": ROOT / "artifacts/routeb_agent_parent_closure_contract_20260906T094500Z/check_contract.py",
            "replay_input": ROOT / "artifacts/routeb_agent_parent_closure_contract_20260906T094500Z/contract-input.json",
            "status": "BLOCKED_FAIL_CLOSED",
            "evidence_level": "closure_gate_schema",
            "reason": "source comparator, parent reduction, global coverage, physical bridge and flowpipe/terminal premises absent",
        },
        {
            "kind": "routeb_condition_bridge_schema",
            "report": ROOT / "artifacts/routeb_condition_bridge_schema_20260906/README.md",
            "schema": ROOT / "artifacts/routeb_condition_bridge_schema_20260906/schema.json",
            "source": ROOT / "artifacts/routeb_condition_bridge_schema_20260906/ConditionBridgeClosure.lean",
            "receipt": ROOT / "artifacts/routeb_condition_bridge_schema_20260906/RECEIPT.md",
            "status": "LEAN_COMPILED_ARCHITECTURE_ONLY",
            "evidence_level": "compiled_condition_residual_goal_schema",
            "reason": "generic closure schema is verified, but Route-B source condition is not instantiated",
        },
        {
            "kind": "routeb_finite_cell_continuation_ledger",
            "report": ROOT / "artifacts/routeb_agent_finite_cell_ledger_20260906T094500Z/README.md",
            "ledger": ROOT / "artifacts/routeb_agent_finite_cell_ledger_20260906T094500Z/finite_cell_ledger.json",
            "replay": ROOT / "artifacts/routeb_agent_finite_cell_ledger_20260906T094500Z/finite_cell_ledger.py",
            "status": "FINITE_CELL_CONTINUATION_OPEN",
            "evidence_level": "topology_ledger_audit",
            "reason": "entry, exit-face and sibling coverage obligations remain open; P3-to-X0 is not a member",
        },
    ]
    for item in batch:
        for key, value in item.items():
            if isinstance(value, Path):
                assert value.is_file(), value

    graph = json.loads(old_graph.read_text(encoding="utf-8"))
    audits = graph.setdefault("bottleneck_audits", [])
    for item in batch:
        record = {
            "kind": item["kind"],
            "status": item["status"],
            "evidence_level": item["evidence_level"],
            "reason": item["reason"],
            "registry_promoted": False,
            "formal_certificate_allowed": False,
        }
        for key, value in item.items():
            if isinstance(value, Path):
                record[key] = {"path": ref(value), "sha256": sha(value)}
        audits.append(record)
    updates = graph.setdefault("open_frontier_updates", [])
    updates.extend({"node": item["kind"], "status": "open", "reason": item["reason"]} for item in batch)
    graph.update(schema="routeb-proposed-proof-dag-v126", supersedes=old_graph.name)
    json.loads(json.dumps(graph, ensure_ascii=False, allow_nan=False))
    new_graph.write_text(json.dumps(graph, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if not backup.exists():
        backup.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(store.path, backup)
    digest = sha(new_graph)
    state.graph_artifacts.append({
        "schema_version": 1,
        "algorithm": "routeb_bottleneck_batch/v1",
        "graph_sha256": digest,
        "roots": [],
        "selected_nodes": [],
        "source": "entry/geometry/D-row/P4/closure condition audits",
        "audit_count": len(batch),
        "registry_promoted": False,
        "formal_certificate_allowed": False,
    })
    state.event(
        "routeb_bottleneck_batch_recorded",
        proposed_dag=ref(new_graph),
        proposed_dag_sha256=digest,
        audit_count=len(batch),
        registry_promoted=False,
        formal_certificate_allowed=False,
        broad_regression_run=False,
    )
    store.save(state)
    print({"revision": state.revision, "graph": new_graph.name, "audits": len(batch), "registry": len(state.registry)})


if __name__ == "__main__":
    main()
