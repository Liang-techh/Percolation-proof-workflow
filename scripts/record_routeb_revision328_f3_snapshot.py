"""Freeze the current F3 evidence before further mutable artifact updates."""
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
    if state.revision != 327 or state.registry:
        raise ValueError("revision-328 recorder requires revision 327 and empty registry")
    side = ROOT / "artifacts/task_routeb_f3_q1_invariance_current"
    names = ("CHECK_RESULT.json", "check_exact.py", "FourierQ1Invariance.lean",
             "compile_strict.log", "support_witness.json")
    source_files = [side / n for n in names]
    report = ROOT / "artifacts/task_routeb_revision328_f3_snapshot/REPORT.md"
    if not report.is_file() or not all(p.is_file() for p in source_files):
        raise ValueError("missing F3 snapshot inputs")
    result = json.loads((side / "CHECK_RESULT.json").read_text(encoding="utf-8"))
    if (result.get("status") != "PASS_MINIMAL_EXACT_PAYLOAD_WITNESS__TRUE_DH_BINDING_OPEN"
            or result.get("coverage") is not False
            or result.get("registry_eligible") is not False
            or result.get("formal_certificate_allowed") is not False):
        raise ValueError("F3 result boundary drifted")
    snap = ROOT / "artifacts/task_routeb_revision328_f3_snapshot/evidence"
    snap.mkdir(parents=True, exist_ok=True)
    for path in source_files:
        shutil.copy2(path, snap / path.name)
    manifest = {p.name: {"path": ref(snap / p.name), "sha256": sha(snap / p.name)}
                for p in source_files}
    (snap / "SNAPSHOT_MANIFEST.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    old = ROOT / "artifacts/routeb_6dof/block45-obligations-v281.json"
    new = ROOT / "artifacts/routeb_6dof/block45-obligations-v282.json"
    graph = json.loads(old.read_text(encoding="utf-8"))
    record = {
        "kind": "routeb_f3_immutable_evidence_snapshot",
        "status": "PASS_SNAPSHOT_FINITE_PAYLOAD_Q1_INVARIANCE",
        "evidence_level": "immutable-strict-lean-support-witness",
        "files": [ref(report), ref(snap / "SNAPSHOT_MANIFEST.json")],
        "snapshot_manifest_sha256": sha(snap / "SNAPSHOT_MANIFEST.json"),
        "aggregate_rows": 610,
        "body_trace_rows": 727,
        "nu1_nonzero_aggregate_rows": 0,
        "nu1_nonzero_body_rows": 0,
        "true_dh_source_binding": False,
        "coverage": False,
        "registry_promoted": False,
        "formal_certificate_allowed": False,
    }
    graph.setdefault("bottleneck_audits", []).append(record)
    graph.setdefault("workflow_hardening", []).append(record)
    graph.setdefault("open_frontier_updates", []).append({
        "node": "GCN-F3-q1-invariance",
        "status": "immutable_finite_payload_receipt_closed_true_dh_open",
        "reason": "F3 artifacts are frozen against mutable current-file drift; source semantic equality remains open",
        "evidence": ref(snap / "SNAPSHOT_MANIFEST.json"),
    })
    graph.update(schema="routeb-proposed-proof-dag-v282", supersedes=old.name)
    new.write_text(json.dumps(graph, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    checkpoint = ROOT / "artifacts/routeb_storage_checkpoint_20260908/state-before-revision328.json"
    if not checkpoint.exists():
        checkpoint.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(store.path, checkpoint)
    graph_sha = sha(new)
    state.graph_artifacts.append({
        "schema_version": 1,
        "algorithm": "routeb_revision328_f3_snapshot/v1",
        "graph_sha256": graph_sha, "roots": [], "selected_nodes": [],
        "evidence_sha256": sha(report),
        "snapshot_manifest_sha256": sha(snap / "SNAPSHOT_MANIFEST.json"),
        "snapshot_files": {name: item["sha256"] for name, item in manifest.items()},
        "strict_lean_finite_payload": True, "true_dh_source_binding": False,
        "coverage": False, "registry_promoted": False,
        "formal_certificate_allowed": False,
    })
    state.event(
        "routeb_revision328_f3_snapshot_recorded",
        proposed_dag=ref(new), proposed_dag_sha256=graph_sha,
        snapshot_manifest_sha256=sha(snap / "SNAPSHOT_MANIFEST.json"),
        aggregate_rows=610, body_trace_rows=727, nu1_nonzero_aggregate_rows=0,
        nu1_nonzero_body_rows=0, strict_lean_finite_payload=True,
        true_dh_source_binding=False, coverage=False, registry_promoted=False,
        formal_certificate_allowed=False, broad_regression_run=False,
    )
    store.save(state)
    print(json.dumps({"revision": state.revision, "graph": new.name,
                      "registry": len(state.registry),
                      "formal_certificate_allowed": False}))


if __name__ == "__main__":
    main()
