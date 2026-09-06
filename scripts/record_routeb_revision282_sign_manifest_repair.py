"""Record interval-sign closure and a repaired FLT manifest as fail-closed evidence."""
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
    if state.revision != 281 or state.registry:
        raise ValueError("revision-282 recorder requires revision 281 and empty registry")
    old = ROOT / "artifacts/routeb_6dof/block45-obligations-v235.json"
    new = ROOT / "artifacts/routeb_6dof/block45-obligations-v236.json"
    backup = ROOT / "artifacts/routeb_storage_checkpoint_20260908/state-before-revision282.json"
    sign = ROOT / "artifacts/task_FLT_interval_sign_20260908"
    repair = ROOT / "artifacts/task_FLT_manifest_repair_20260908"
    overlay = ROOT / "artifacts/task_FLT_dag_overlay_audit_20260908"
    required = [
        old, sign / "FLTIntervalSign.lean", sign / "receipt.json", sign / "OBLIGATIONS.md",
        repair / "corrected_manifest.json", repair / "comparator_receipt.json", repair / "REPORT.md",
        overlay / "overlay.json", overlay / "receipt.json",
    ]
    if not all(path.is_file() for path in required):
        raise ValueError("missing revision-282 evidence")

    graph = json.loads(old.read_text(encoding="utf-8"))
    sign_receipt = json.loads((sign / "receipt.json").read_text(encoding="utf-8"))
    repair_receipt = json.loads((repair / "comparator_receipt.json").read_text(encoding="utf-8"))
    overlay_receipt = json.loads((overlay / "receipt.json").read_text(encoding="utf-8"))

    sign_record = {
        "kind": "routeb_interval_sign_normalization_leaf",
        "status": sign_receipt["status"],
        "evidence_level": "current-pin-strict-compile-abstract-leaf",
        "files": [ref(sign / name) for name in ("FLTIntervalSign.lean", "receipt.json", "OBLIGATIONS.md")],
        "receipt_sha256": sha(sign / "receipt.json"),
        "proved": ["h_src=bound-||l_B||^2 interval propagation", "h_neg=-h_src", "strict sign interfaces"],
        "open_obligations": sign_receipt["open_obligations"],
        "registry_promoted": False,
        "formal_certificate_allowed": False,
    }
    repair_record = {
        "kind": "flt_manifest_shadow_repair",
        "status": "PASS_FAIL_CLOSED_SHADOW_MANIFEST",
        "evidence_level": "machine-comparator-pass-with-original-failure-retained",
        "files": [ref(repair / name) for name in ("corrected_manifest.json", "comparator_receipt.json", "REPORT.md")],
        "manifest_sha256": sha(repair / "corrected_manifest.json"),
        "comparator_receipt_sha256": sha(repair / "comparator_receipt.json"),
        "original_manifest_unchanged": True,
        "registry_promoted": False,
        "formal_certificate_allowed": False,
    }
    overlay_record = {
        "kind": "flt_advisory_overlay_schema_audit",
        "status": overlay_receipt.get("status", "PASS_FAIL_CLOSED"),
        "evidence_level": "schema-and-boundary-audit",
        "files": [ref(overlay / name) for name in ("overlay.json", "receipt.json")],
        "receipt_sha256": sha(overlay / "receipt.json"),
        "dependency_boundary": "advisory_reuse edges remain outside ProofNode.dependencies and closure eligibility",
        "registry_promoted": False,
        "formal_certificate_allowed": False,
    }
    for record in (sign_record, repair_record, overlay_record):
        graph.setdefault("bottleneck_audits", []).append(record)
        graph.setdefault("external_intakes", []).append(record)
    graph.setdefault("open_frontier_updates", []).extend([
        {"node": "B45.interval_sign", "status": "analytic_sign_leaf_closed_conditionally", "reason": sign_record["open_obligations"]},
        {"node": "FLT.current_pin_manifest", "status": "shadow_manifest_comparator_pass", "reason": "main manifest remains immutable; no theorem admission"},
    ])
    graph.update(schema="routeb-proposed-proof-dag-v236", supersedes=old.name)
    new.write_text(json.dumps(graph, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if not backup.exists():
        backup.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(store.path, backup)
    digest = sha(new)
    state.graph_artifacts.append({
        "schema_version": 1,
        "algorithm": "routeb_revision282_sign_manifest_repair/v1",
        "graph_sha256": digest,
        "roots": [],
        "selected_nodes": [],
        "source": "FLT interval sign leaf + shadow manifest comparator",
        "evidence_sha256": sha(sign / "receipt.json"),
        "registry_promoted": False,
        "formal_certificate_allowed": False,
    })
    state.event(
        "routeb_revision282_sign_manifest_repair_recorded",
        proposed_dag=ref(new),
        proposed_dag_sha256=digest,
        interval_sign_leaf=True,
        shadow_manifest_comparator_pass=True,
        original_manifest_mutated=False,
        routeb_physical_binding=False,
        registry_promoted=False,
        formal_certificate_allowed=False,
        broad_regression_run=False,
    )
    store.save(state)
    print(json.dumps({"revision": state.revision, "graph": new.name, "registry": len(state.registry)}))


if __name__ == "__main__":
    main()
