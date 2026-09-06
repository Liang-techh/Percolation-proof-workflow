"""Record durable snapshot-based replay for frontier receipts."""
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
    if state.revision != 319 or state.registry:
        raise ValueError("revision-320 recorder requires revision 319 and empty registry")
    side = ROOT / "artifacts/task_routeb_frontier_binding_current"
    receipt, replay = side / "FRONTIER_RECEIPT_V1.json", side / "REPLAY_RESULT.json"
    snapshot = side / "state_snapshot_rev319.json"
    builder, verifier = side / "build_frontier_receipt.py", side / "verify_frontier_receipt.py"
    report = ROOT / "artifacts/task_routeb_revision320_frontier_snapshot_lifecycle/REPORT.md"
    if not all(p.is_file() for p in (receipt, replay, snapshot, builder, verifier, report)):
        raise ValueError("missing revision-320 lifecycle evidence")
    rec = json.loads(receipt.read_text(encoding="utf-8"))
    result = json.loads(replay.read_text(encoding="utf-8"))
    source = rec.get("source_binding", {})
    if (source.get("state_revision") != 319
            or source.get("state_path") != "artifacts/task_routeb_frontier_binding_current/state_snapshot_rev319.json"
            or source.get("state_sha256") != sha(snapshot)
            or not source.get("state_checksum_replayed")
            or result.get("status") != "PASS"
            or not result.get("replayable")):
        raise ValueError("snapshot frontier receipt did not replay")

    old = ROOT / "artifacts/routeb_6dof/block45-obligations-v273.json"
    new = ROOT / "artifacts/routeb_6dof/block45-obligations-v274.json"
    graph = json.loads(old.read_text(encoding="utf-8"))
    record = {
        "kind": "routeb_immutable_frontier_snapshot_receipt",
        "status": "PASS_DURABLE_REPLAYABLE_SNAPSHOT",
        "evidence_level": "immutable-state-snapshot-and-dag-event-hash-bound-replay",
        "files": [ref(report), ref(receipt), ref(replay), ref(snapshot), ref(builder), ref(verifier)],
        "state_revision": 319,
        "state_snapshot_sha256": sha(snapshot),
        "dag": "block45-obligations-v273.json",
        "frontier_unique_count": 49,
        "duplicate_claim_count": 3,
        "replayable": True,
        "history_preserved": True,
        "registry_promoted": False,
        "formal_certificate_allowed": False,
    }
    graph.setdefault("bottleneck_audits", []).append(record)
    graph.setdefault("workflow_hardening", []).append(record)
    graph.setdefault("open_frontier_updates", []).append({
        "node": "workflow_frontier_provenance",
        "status": "immutable_snapshot_replay_closed_math_frontier_open",
        "reason": "historical frontier receipts survive later state events without weakening revision/hash binding",
        "evidence": ref(replay),
    })
    graph.update(schema="routeb-proposed-proof-dag-v274", supersedes=old.name)
    new.write_text(json.dumps(graph, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    checkpoint = ROOT / "artifacts/routeb_storage_checkpoint_20260908/state-before-revision320.json"
    if not checkpoint.exists():
        checkpoint.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(store.path, checkpoint)
    graph_sha = sha(new)
    state.graph_artifacts.append({
        "schema_version": 1,
        "algorithm": "routeb_revision320_frontier_snapshot_lifecycle/v1",
        "graph_sha256": graph_sha, "roots": [], "selected_nodes": [],
        "evidence_sha256": sha(report), "receipt_sha256": sha(receipt),
        "replay_sha256": sha(replay), "snapshot_sha256": sha(snapshot),
        "builder_sha256": sha(builder), "verifier_sha256": sha(verifier),
        "state_revision_bound": 319, "replayable": True,
        "registry_promoted": False, "formal_certificate_allowed": False,
    })
    state.event(
        "routeb_revision320_frontier_snapshot_lifecycle_recorded",
        proposed_dag=ref(new), proposed_dag_sha256=graph_sha,
        state_revision_bound=319, immutable_snapshot=True,
        frontier_unique_count=49, duplicate_claim_count=3,
        replayable=True, registry_promoted=False,
        formal_certificate_allowed=False, broad_regression_run=False,
    )
    store.save(state)
    print(json.dumps({"revision": state.revision, "graph": new.name,
                      "registry": len(state.registry),
                      "formal_certificate_allowed": False}))


if __name__ == "__main__":
    main()
