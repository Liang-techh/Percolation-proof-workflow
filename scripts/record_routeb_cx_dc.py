"""Record CX-DC results, including the controlled static P4 mutation."""
from __future__ import annotations

import hashlib
import json
import shutil
from pathlib import Path

from record_routeb_port_progress import ROOT, ref
from percolation_workflow.store import StateStore


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def ev(*names: str) -> dict[str, Path]:
    out = {}
    for n in names:
        p = ROOT / n
        assert p.is_file(), p
        out[n] = p
    return out


def main() -> None:
    store = StateStore(ROOT / "artifacts/routeb_6dof/state.json")
    state = store.load()
    assert state.revision == 200 and not state.registry
    old = ROOT / "artifacts/routeb_6dof/block45-obligations-v154.json"
    new = ROOT / "artifacts/routeb_6dof/block45-obligations-v155.json"
    backup = ROOT / "artifacts/routeb_storage_checkpoint_20260906/state-before-revision201.json"
    assert old.is_file() and not new.exists()
    target = Path(r"C:/Users/z5242/Desktop/重构版/6dof_sos_optimized/6dof_sos_optimized/robot_final/routeB_pmi_certificate.jl")
    target_backup = Path(r"C:/Users/z5242/Desktop/重构版/工作流/artifacts/backups/task_CZ_p4_hook_applied_20260906/routeB_pmi_certificate.jl.235f4876ed1a3343f6d84f83c0079b4d279886585dc36aeb55b9fc0289177a77.bak")
    assert target.is_file() and target_backup.is_file()
    audits = [
        ("routeb_schur_dN_computation", "NEIGHBOR_PASS_CELL16_FAIL_CLOSED", "C0-L/C0-R have exact d_N and rho_N<1; cell16 rho_N>1", ev("artifacts/task_CX_schur_dN_compute_20260906/REPORT.md", "artifacts/task_CX_schur_dN_compute_20260906/ledger.json", "artifacts/task_CX_schur_dN_compute_20260906/check.py")),
        ("routeb_p3_fd_error_decomposition", "OPEN_FAIL_CLOSED_NO_NUMERIC_BOUNDS", "FD input/rounding/libm/truncation/cancellation obligations are separated without invented bounds", ev("artifacts/task_CY_p3_fd_error_decomposition_20260906/README.md", "artifacts/task_CY_p3_fd_error_decomposition_20260906/receipt.json", "artifacts/task_CY_p3_fd_error_decomposition_20260906/checker.py")),
        ("routeb_p4_hook_controlled_apply", "STATIC_APPLY_POSTHASH_VERIFIED_RUNTIME_OPEN", "audited CB/BV hook applied after preimage gate with external backup; Julia/runtime/solver unverified", ev("artifacts/task_CZ_p4_hook_applied_20260906/REPORT.md", "artifacts/task_CZ_p4_hook_applied_20260906/POST_APPLY_VERIFICATION.md", str(target), str(target_backup))),
        ("routeb_flowpipe_source_receipt_gap", "OPEN_MISSING_CERTIFICATE_DATA", "source lines and adapter fields are bound, but numeric RHS/Lipschitz/Picard/coverage receipts are absent", ev("artifacts/task_DA_flowpipe_source_receipt_gap_20260906/REPORT.md")),
        ("routeb_p4_gram_export_linkage", "STRUCTURAL_LINKAGE_PASS_WITH_EXPLICIT_GAPS", "hook and validator link structurally; polynomial_object/Gram block binding and exact export remain absent", ev("artifacts/task_DB_p4_gram_export_link_20260906/REPORT.md", "artifacts/task_DB_p4_gram_export_link_20260906/check_p4_gram_linkage.py")),
        ("routeb_anthropic_spectral_adapter", "OPEN_COMPILE", "spectral adapter intake preserves provenance but current isolated environment lacks Mathlib module resolution", ev("artifacts/task_DC_anthropic_spectral_minimal_20260906/REPORT.md", "artifacts/task_DC_anthropic_spectral_minimal_20260906/PROVENANCE.md", "artifacts/task_DC_anthropic_spectral_minimal_20260906/COMPILE_RECEIPT.md")),
    ]
    graph = json.loads(old.read_text(encoding="utf-8"))
    for kind, status, reason, evidence in audits:
        graph.setdefault("bottleneck_audits", []).append({"kind": kind, "status": status, "evidence_level": "bounded_math_or_controlled_source_audit", "semantic_boundary": reason, "registry_promoted": False, "formal_certificate_allowed": False, "files": {k: {"path": ref(v), "sha256": sha(v)} for k, v in evidence.items()}})
        graph.setdefault("open_frontier_updates", []).append({"node": kind, "status": status.lower(), "reason": reason})
    graph.update(schema="routeb-proposed-proof-dag-v155", supersedes=old.name)
    new.write_text(json.dumps(graph, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if not backup.exists():
        backup.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(store.path, backup)
    digest = sha(new)
    for kind, _status, _reason, evidence in audits:
        first = next(iter(evidence.values()))
        state.graph_artifacts.append({"schema_version": 1, "algorithm": kind + "/v1", "graph_sha256": digest, "roots": [], "selected_nodes": [], "source": str(first), "evidence_sha256": sha(first), "registry_promoted": False, "formal_certificate_allowed": False})
    state.event("routeb_cx_dc_recorded", proposed_dag=ref(new), proposed_dag_sha256=digest, audits=[x[0] for x in audits], registry_promoted=False, formal_certificate_allowed=False, broad_regression_run=False)
    store.save(state)
    print({"revision": state.revision, "graph": new.name, "registry": len(state.registry), "target_hash": sha(target), "backup_hash": sha(target_backup)})


if __name__ == "__main__":
    main()
