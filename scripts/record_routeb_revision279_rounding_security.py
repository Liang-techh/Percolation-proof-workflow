"""Persist rounding, Schur witness, frontier priority, and callback hardening."""
from __future__ import annotations

import hashlib
import json
import shutil
from pathlib import Path

from record_routeb_port_progress import ROOT, ref
from percolation_workflow.store import StateStore


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> None:
    store = StateStore(ROOT / "artifacts/routeb_6dof/state.json")
    state = store.load()
    assert state.revision == 278 and not state.registry
    old = ROOT / "artifacts/routeb_6dof/block45-obligations-v232.json"
    new = ROOT / "artifacts/routeb_6dof/block45-obligations-v233.json"
    backup = ROOT / "artifacts/routeb_storage_checkpoint_20260907/state-before-revision279.json"
    dirs = {
        "rounding": ROOT / "artifacts/task_GDH_outward_rounding_patch_20260907",
        "security": ROOT / "artifacts/task_GDJ_host_bridge_security_audit_20260907",
        "schur": ROOT / "artifacts/task_GDK_schur_witness_repair_20260907",
        "priority": ROOT / "artifacts/task_GDL_frontier_priority_sign_20260907",
    }
    required = [old,
                dirs["rounding"] / "report.md", dirs["rounding"] / "receipt.json", dirs["rounding"] / "isolated.patch",
                dirs["security"] / "report.md", dirs["security"] / "receipt.json",
                dirs["schur"] / "report.md", dirs["schur"] / "receipt.json", dirs["schur"] / "isolated.diff",
                dirs["priority"] / "report.md", dirs["priority"] / "receipt.json"]
    assert all(path.is_file() for path in required) and not new.exists()
    receipts = {key: load(path / "receipt.json") for key, path in dirs.items()}
    graph = load(old)
    audits = [
        {"kind": "routeb_outward_rounding_isolated_patch", "receipt": receipts["rounding"], "side": dirs["rounding"],
         "files": [dirs["rounding"] / "report.md", dirs["rounding"] / "receipt.json", dirs["rounding"] / "isolated.patch"],
         "reason": "Safe endpoint-direction changes are isolated and improve h/kappa by tiny margins; primitive trig, MVInt and source bridge remain open."},
        {"kind": "host_bridge_security_residual_audit", "receipt": receipts["security"], "side": dirs["security"],
         "files": [dirs["security"] / "report.md", dirs["security"] / "receipt.json"],
         "reason": "The audit identified callback project/replay/legacy and reduction recovery risks; coordinator binding and fail-closed replay/exception handling were patched and focused tests pass."},
        {"kind": "routeb_schur_witness_isolated_repair", "receipt": receipts["schur"], "side": dirs["schur"],
         "files": [dirs["schur"] / "report.md", dirs["schur"] / "receipt.json", dirs["schur"] / "isolated.diff"],
         "reason": "Isolated smoke fixes m_lower propagation and preconditioner norm naming; canonical physical source is unchanged."},
        {"kind": "frontier_priority_sign_normalization_audit", "receipt": receipts["priority"], "side": dirs["priority"],
         "files": [dirs["priority"] / "report.md", dirs["priority"] / "receipt.json"],
         "reason": "Scheduler priority still needs explicit sign-normalized/source-soundness ordering; known q2/q3 no-closure diagnostics should remain low priority."},
    ]
    for audit in audits:
        record = {
            "kind": audit["kind"], "status": audit["receipt"].get("status"),
            "evidence_level": "targeted-sidecar-audit", "sidecar": str(audit["side"].resolve()),
            "files": [ref(path) for path in audit["files"]],
            "receipt_sha256": sha(audit["side"] / "receipt.json"),
            "registry_promoted": False, "formal_certificate_allowed": False,
            "semantic_boundary": audit["reason"],
        }
        graph.setdefault("bottleneck_audits", []).append(record)
        graph.setdefault("workflow_repairs", []).append(record)
        graph.setdefault("external_intakes", []).append({
            "kind": audit["kind"], "source": "targeted-sidecar", "sidecar": record["sidecar"],
            "files": record["files"], "registry_promoted": False, "formal_certificate_allowed": False,
        })
        graph.setdefault("open_frontier_updates", []).append({
            "node": audit["kind"], "status": "retained_fail_closed", "reason": audit["reason"]
        })
    graph.update(schema="routeb-proposed-proof-dag-v233", supersedes=old.name)
    new.write_text(json.dumps(graph, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if not backup.exists():
        backup.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(store.path, backup)
    digest = sha(new)
    state.graph_artifacts.append({
        "schema_version": 1, "algorithm": "routeb_revision279_rounding_security/v1",
        "graph_sha256": digest, "roots": [], "selected_nodes": [],
        "source": "sidecars:GDH-GDJ-GDK-GDL",
        "evidence_sha256": sha(dirs["security"] / "receipt.json"),
        "strict_compile": True, "registry_promoted": False, "formal_certificate_allowed": False,
    })
    state.event("routeb_revision279_rounding_security_recorded",
                proposed_dag=ref(new), proposed_dag_sha256=digest,
                rounding_isolated_only=True, schur_repair_isolated_only=True,
                coordinator_project_binding=True, replay_sidecar_rejected=True,
                reduction_exception_recovery=True, registry_promoted=False,
                formal_certificate_allowed=False, broad_regression_run=False)
    store.save(state)
    print(json.dumps({"revision": state.revision, "graph": new.name, "registry": len(state.registry)}))


if __name__ == "__main__":
    main()
