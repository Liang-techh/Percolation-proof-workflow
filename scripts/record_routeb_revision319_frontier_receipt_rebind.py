"""Record the state-aware frontier receipt rebind and replay pass."""
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
    if state.revision != 318 or state.registry:
        raise ValueError("revision-319 recorder requires revision 318 and empty registry")
    side = ROOT / "artifacts/task_routeb_frontier_binding_current"
    receipt, replay = side / "FRONTIER_RECEIPT_V1.json", side / "REPLAY_RESULT.json"
    builder, verifier = side / "build_frontier_receipt.py", side / "verify_frontier_receipt.py"
    report = ROOT / "artifacts/task_routeb_revision319_frontier_receipt_rebind/REPORT.md"
    if not all(p.is_file() for p in (receipt, replay, builder, verifier, report)):
        raise ValueError("missing revision-319 frontier rebind evidence")
    rec = json.loads(receipt.read_text(encoding="utf-8"))
    result = json.loads(replay.read_text(encoding="utf-8"))
    source = rec.get("source_binding", {})
    frontier = rec.get("frontier", {})
    if (source.get("state_revision") != 318
            or not source.get("state_checksum_replayed")
            or not source.get("dag_path", "").endswith("block45-obligations-v272.json")
            or frontier.get("unique_count") != 49
            or frontier.get("duplicate_count") != 3
            or result.get("status") != "PASS"
            or not result.get("replayable")):
        raise ValueError("rebound frontier receipt did not replay")

    old = ROOT / "artifacts/routeb_6dof/block45-obligations-v272.json"
    new = ROOT / "artifacts/routeb_6dof/block45-obligations-v273.json"
    graph = json.loads(old.read_text(encoding="utf-8"))
    record = {
        "kind": "routeb_frontier_receipt_lifecycle_rebind",
        "status": "PASS_STATE_AWARE_REPLAY_AFTER_REVISION_ADVANCE",
        "evidence_level": "exact-state-dag-event-hash-bound-replay",
        "files": [ref(report), ref(receipt), ref(replay), ref(builder), ref(verifier)],
        "state_revision": 318,
        "dag": "block45-obligations-v272.json",
        "frontier_unique_count": 49,
        "duplicate_claim_count": 3,
        "replayable": True,
        "old_receipt_fail_closed_on_revision_mismatch": True,
        "registry_promoted": False,
        "formal_certificate_allowed": False,
    }
    graph.setdefault("bottleneck_audits", []).append(record)
    graph.setdefault("workflow_hardening", []).append(record)
    graph.setdefault("open_frontier_updates", []).append({
        "node": "workflow_frontier_provenance",
        "status": "receipt_lifecycle_repaired_math_frontier_open",
        "reason": "receipt generation and replay now bind the exact current state/DAG event instead of a stale revision",
        "evidence": ref(replay),
    })
    graph.update(schema="routeb-proposed-proof-dag-v273", supersedes=old.name)
    new.write_text(json.dumps(graph, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    checkpoint = ROOT / "artifacts/routeb_storage_checkpoint_20260908/state-before-revision319.json"
    if not checkpoint.exists():
        checkpoint.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(store.path, checkpoint)
    graph_sha = sha(new)
    state.graph_artifacts.append({
        "schema_version": 1,
        "algorithm": "routeb_revision319_frontier_receipt_rebind/v1",
        "graph_sha256": graph_sha, "roots": [], "selected_nodes": [],
        "evidence_sha256": sha(report), "receipt_sha256": sha(receipt),
        "replay_sha256": sha(replay), "builder_sha256": sha(builder),
        "verifier_sha256": sha(verifier), "state_revision_bound": 318,
        "frontier_unique_count": 49, "replayable": True,
        "registry_promoted": False, "formal_certificate_allowed": False,
    })
    state.event(
        "routeb_revision319_frontier_receipt_rebind_recorded",
        proposed_dag=ref(new), proposed_dag_sha256=graph_sha,
        state_revision_bound=318, frontier_unique_count=49,
        duplicate_claim_count=3, replayable=True,
        stale_receipt_fail_closed=True, registry_promoted=False,
        formal_certificate_allowed=False, broad_regression_run=False,
    )
    store.save(state)
    print(json.dumps({"revision": state.revision, "graph": new.name,
                      "registry": len(state.registry),
                      "formal_certificate_allowed": False}))


if __name__ == "__main__":
    main()
