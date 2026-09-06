"""Persist the next Route-B frontier without promoting any theorem.

This recorder is intentionally append-only at the workflow level: it creates
the next proposed DAG snapshot and records independent sidecar evidence while
leaving the verified registry and formal-certificate gate untouched.
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
    assert state.revision == 231 and not state.registry
    old = ROOT / "artifacts/routeb_6dof/block45-obligations-v185.json"
    new = ROOT / "artifacts/routeb_6dof/block45-obligations-v186.json"
    backup = ROOT / "artifacts/routeb_storage_checkpoint_20260907/state-before-revision232.json"
    assert old.is_file() and not new.exists()

    specs = [
        (
            "routeb_source_ledger_contract_20260906_v4",
            ["manifest.json", "REPORT.md"],
            "source_ledger_contract_v2",
            "FAIL_CLOSED",
            "Manifest reduces source drift to one missing interval-bounds binding, but all 14 physical receipt fields remain absent.",
        ),
        (
            "task_GAL_julia_single_cell_replay_20260907",
            ["single_cell_replay.jl", "receipt.json", "check_receipt.py", "README.md", "bounds_cell16.csv"],
            "julia_single_cell_replay",
            "OPEN_MISSING_DATA",
            "Exactly one rank-0 cell is replayed with source hashes and outward geometry; rho/inverse/Schur guards remain unknown and coverage is false.",
        ),
        (
            "task_GAO_schur_terminal_bridge_20260907",
            ["SchurTerminalBridge.lean", "compile_strict.log", "axioms.txt", "REPORT.md", "sha256.txt"],
            "schur_terminal_bridge",
            "CURRENT_PIN_STRICT_COMPILE_PASS_CANDIDATE_ONLY",
            "Current-pin Lean composition of the matrix Schur lower bound and conditional terminal transfer compiles with only standard axioms; physical binding remains open.",
        ),
        (
            "task_GAO_receipt_m4_attachment_validator_20260906",
            ["validate.py", "fixture.json", "REPORT.md", "README.md", "provenance.md"],
            "receipt_m4_attachment_validator",
            "OPEN_FAIL_CLOSED",
            "M4 attachment checks parent/child identity, cell/domain/source hashes, six physical premises, and independent comparator/registry gates without promotion.",
        ),
        (
            "task_GAP_residual_decomposition_audit_20260907",
            ["REPORT.md"],
            "residual_decomposition_audit",
            "OPEN_FAIL_CLOSED",
            "Exact six-term Lean algebra is conditional on hdesc; deployed DH/Float64 source binding and a uniform full-state residual bound are still open.",
        ),
    ]

    graph = json.loads(old.read_text(encoding="utf-8"))
    audits = []
    for dirname, names, node, status, reason in specs:
        sidecar = ROOT / "artifacts" / dirname
        files = [sidecar / name for name in names]
        assert all(path.is_file() for path in files), (dirname, names)
        audit = {
            "kind": f"routeb_{node}_audit",
            "status": status,
            "evidence_level": "independent_sidecar_frontier_audit",
            "semantic_boundary": reason,
            "sidecar": str(sidecar.resolve()),
            "files": [ref(path) for path in files],
            "registry_promoted": False,
            "formal_certificate_allowed": False,
        }
        audits.append(audit)
        graph.setdefault("bottleneck_audits", []).append(audit)
        graph.setdefault("external_intakes", []).append({
            "kind": audit["kind"],
            "source": "local-routeb-revision232-frontier",
            "sidecar": audit["sidecar"],
            "files": audit["files"],
            "registry_promoted": False,
            "formal_certificate_allowed": False,
        })
        graph.setdefault("open_frontier_updates", []).append({
            "node": audit["kind"],
            "status": status.lower(),
            "reason": reason,
        })

    graph.update(schema="routeb-proposed-proof-dag-v186", supersedes=old.name)
    new.write_text(json.dumps(graph, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if not backup.exists():
        backup.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(store.path, backup)

    digest = sha(new)
    state.graph_artifacts.append({
        "schema_version": 1,
        "algorithm": "routeb_revision232_frontier/v1",
        "graph_sha256": digest,
        "roots": [],
        "selected_nodes": [],
        "source": "independent-sidecars:source-ledger,GAL,GAO, GAP",
        "evidence_sha256": sha(ROOT / "artifacts/task_GAO_schur_terminal_bridge_20260907/compile_strict.log"),
        "strict_compile": True,
        "registry_promoted": False,
        "formal_certificate_allowed": False,
    })
    state.event(
        "routeb_revision232_frontier_recorded",
        proposed_dag=ref(new),
        proposed_dag_sha256=digest,
        audits=[{"kind": x["kind"], "status": x["status"]} for x in audits],
        registry_promoted=False,
        formal_certificate_allowed=False,
        broad_regression_run=False,
    )
    store.save(state)
    print({"revision": state.revision, "graph": new.name, "audits": len(audits), "registry": len(state.registry)})


if __name__ == "__main__":
    main()
