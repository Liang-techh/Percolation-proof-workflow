"""Record the pinned Anthropic FLT reuse classification audit."""
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
    if state.revision != 322 or state.registry:
        raise ValueError("revision-323 recorder requires revision 322 and empty registry")
    side = ROOT / "artifacts/task_FLT_routeb_reuse_next_current"
    report, candidates, receipt = (side / n for n in ("REPORT.md", "candidates.json", "RECEIPT.json"))
    out_report = ROOT / "artifacts/task_routeb_revision323_flt_reuse_audit/REPORT.md"
    if not all(p.is_file() for p in (report, candidates, receipt, out_report)):
        raise ValueError("missing FLT reuse audit evidence")
    data = json.loads(candidates.read_text(encoding="utf-8"))
    rec = json.loads(receipt.read_text(encoding="utf-8"))
    counts = rec.get("classification_counts", {})
    if (counts.get("direct reuse") != 0 or counts.get("light modification") != 4
            or counts.get("architecture-only") != 1
            or rec.get("state_registry_mutated") is not False
            or rec.get("verification", {}).get("semantic_routeb_binding") != "not established"
            or len(data.get("candidates", [])) != 5):
        raise ValueError("FLT reuse audit classification or boundary drifted")

    old = ROOT / "artifacts/routeb_6dof/block45-obligations-v276.json"
    new = ROOT / "artifacts/routeb_6dof/block45-obligations-v277.json"
    graph = json.loads(old.read_text(encoding="utf-8"))
    record = {
        "kind": "anthropic_flt_routeb_reuse_audit",
        "status": "PASS_PINNED_CLASSIFICATION_NO_DIRECT_REUSE",
        "evidence_level": "pinned-source-read-only-audit",
        "files": [ref(out_report), ref(report), ref(candidates), ref(receipt)],
        "source_commit": rec["source_commit"],
        "classification_counts": counts,
        "direct_reuse": 0,
        "semantic_routeb_binding": False,
        "state_registry_mutated": False,
        "registry_promoted": False,
        "formal_certificate_allowed": False,
    }
    graph.setdefault("external_intakes", []).append(record)
    graph.setdefault("bottleneck_audits", []).append(record)
    graph.setdefault("workflow_hardening", []).append(record)
    graph.setdefault("open_frontier_updates", []).append({
        "node": "anthropic_flt_reuse_projection",
        "status": "classification_closed_routeb_adapter_open",
        "reason": "four light-modification and one architecture-only pattern are identified; no direct physical Route-B theorem is admitted",
        "evidence": ref(receipt),
    })
    graph.update(schema="routeb-proposed-proof-dag-v277", supersedes=old.name)
    new.write_text(json.dumps(graph, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    checkpoint = ROOT / "artifacts/routeb_storage_checkpoint_20260908/state-before-revision323.json"
    if not checkpoint.exists():
        checkpoint.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(store.path, checkpoint)
    graph_sha = sha(new)
    state.graph_artifacts.append({
        "schema_version": 1,
        "algorithm": "routeb_revision323_flt_reuse_audit/v1",
        "graph_sha256": graph_sha, "roots": [], "selected_nodes": [],
        "evidence_sha256": sha(out_report), "report_sha256": sha(report),
        "candidates_sha256": sha(candidates), "receipt_sha256": sha(receipt),
        "source_commit": rec["source_commit"], "direct_reuse": 0,
        "light_modification": 4, "architecture_only": 1,
        "registry_promoted": False, "formal_certificate_allowed": False,
    })
    state.event(
        "routeb_revision323_flt_reuse_audit_recorded",
        proposed_dag=ref(new), proposed_dag_sha256=graph_sha,
        source_commit=rec["source_commit"], direct_reuse=0,
        light_modification=4, architecture_only=1,
        semantic_routeb_binding=False, registry_promoted=False,
        formal_certificate_allowed=False, broad_regression_run=False,
    )
    store.save(state)
    print(json.dumps({"revision": state.revision, "graph": new.name,
                      "registry": len(state.registry),
                      "formal_certificate_allowed": False}))


if __name__ == "__main__":
    main()
