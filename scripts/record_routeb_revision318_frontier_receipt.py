"""Record a replayable Prove2Me-style frontier receipt."""
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
    if state.revision != 317 or state.registry:
        raise ValueError("revision-318 recorder requires revision 317 and empty registry")
    side = ROOT / "artifacts/task_routeb_frontier_binding_current"
    receipt = side / "FRONTIER_RECEIPT_V1.json"
    replay = side / "REPLAY_RESULT.json"
    checker = side / "verify_frontier_receipt.py"
    schema = side / "RECEIPT_SCHEMA.md"
    report = ROOT / "artifacts/task_routeb_revision318_frontier_receipt/REPORT.md"
    if not all(p.is_file() for p in (receipt, replay, checker, schema, report)):
        raise ValueError("missing frontier receipt evidence")
    rec = json.loads(receipt.read_text(encoding="utf-8"))
    result = json.loads(replay.read_text(encoding="utf-8"))
    if (rec.get("schema") != "prove2me-routeb-frontier-receipt-v1"
            or rec.get("source_binding", {}).get("state_revision") != 317
            or rec.get("frontier", {}).get("unique_count") != 49
            or rec.get("frontier", {}).get("duplicate_count") != 3
            or result.get("status") != "PASS"
            or not result.get("replayable")):
        raise ValueError("frontier receipt replay did not pass")

    old = ROOT / "artifacts/routeb_6dof/block45-obligations-v271.json"
    new = ROOT / "artifacts/routeb_6dof/block45-obligations-v272.json"
    graph = json.loads(old.read_text(encoding="utf-8"))
    record = {
        "kind": "routeb_frontier_receipt_replay",
        "status": "PASS_REPLAYABLE_FRONTIER_RECEIPT",
        "evidence_level": "state-dag-node-evidence-hash-bound-replay",
        "files": [ref(report), ref(receipt), ref(replay), ref(checker), ref(schema)],
        "state_revision": 317,
        "frontier_input_count": 52,
        "frontier_unique_count": 49,
        "duplicate_claim_count": 3,
        "dag_node_binding_count": 49,
        "replayable": True,
        "registry_promoted": False,
        "formal_certificate_allowed": False,
    }
    graph.setdefault("bottleneck_audits", []).append(record)
    graph.setdefault("workflow_hardening", []).append(record)
    graph.setdefault("open_frontier_updates", []).append({
        "node": "workflow_frontier_provenance",
        "status": "receipt_replay_closed_math_frontier_open",
        "reason": "state/DAG/node/evidence identity is now replayable; mathematical claims remain independently open",
        "evidence": ref(replay),
    })
    graph.update(schema="routeb-proposed-proof-dag-v272", supersedes=old.name)
    new.write_text(json.dumps(graph, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    checkpoint = ROOT / "artifacts/routeb_storage_checkpoint_20260908/state-before-revision318.json"
    if not checkpoint.exists():
        checkpoint.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(store.path, checkpoint)
    graph_sha = sha(new)
    state.graph_artifacts.append({
        "schema_version": 1,
        "algorithm": "routeb_revision318_frontier_receipt/v1",
        "graph_sha256": graph_sha, "roots": [], "selected_nodes": [],
        "evidence_sha256": sha(report), "receipt_sha256": sha(receipt),
        "replay_sha256": sha(replay), "checker_sha256": sha(checker),
        "state_revision_bound": 317, "frontier_unique_count": 49,
        "replayable": True, "registry_promoted": False,
        "formal_certificate_allowed": False,
    })
    state.event(
        "routeb_revision318_frontier_receipt_recorded",
        proposed_dag=ref(new), proposed_dag_sha256=graph_sha,
        state_revision_bound=317, frontier_input_count=52,
        frontier_unique_count=49, duplicate_claim_count=3,
        dag_node_binding_count=49, replayable=True,
        registry_promoted=False, formal_certificate_allowed=False,
        broad_regression_run=False,
    )
    store.save(state)
    print(json.dumps({"revision": state.revision, "graph": new.name,
                      "registry": len(state.registry),
                      "formal_certificate_allowed": False}))


if __name__ == "__main__":
    main()
