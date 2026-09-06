"""Record DD-DI bounded progress and preserve all fail-closed boundaries."""
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
        out[str(n)] = p
    return out


def main() -> None:
    store = StateStore(ROOT / "artifacts/routeb_6dof/state.json")
    state = store.load()
    assert state.revision == 202 and not state.registry
    old = ROOT / "artifacts/routeb_6dof/block45-obligations-v156.json"
    new = ROOT / "artifacts/routeb_6dof/block45-obligations-v157.json"
    backup = ROOT / "artifacts/routeb_storage_checkpoint_20260906/state-before-revision203.json"
    assert old.is_file() and not new.exists()
    target = Path(r"C:/Users/z5242/Desktop/重构版/6dof_sos_optimized/6dof_sos_optimized/robot_final/routeB_pmi_certificate.jl")
    audits = [
        ("routeb_schur_child_inverse_replay", "CONDITIONAL_NEUMANN_REPLAY_SOURCE_BRIDGE_OPEN", "C0-L/C0-R inverse bounds replay exactly; coupling/source/physical Schur margins remain absent", ev("artifacts/task_DD_schur_child_inverse_replay_20260906/REPORT.md", "artifacts/task_DD_schur_child_inverse_replay_20260906/ledger.json", "artifacts/task_DD_schur_child_inverse_replay_20260906/check.py")),
        ("routeb_cell16_subdivision_bound", "CONDITIONAL_SUBDIVISION_M_GE_33_COVERAGE_OPEN", "uniform m>=33 is a conservative radius condition only; child data and complete cover are not witnessed", ev("artifacts/task_DE_cell16_subdivision_bound_20260906/ledger.json", "artifacts/task_DE_cell16_subdivision_bound_20260906/checker.py")),
        ("routeb_p3_trig_rounding_contract", "OPEN_FAIL_CLOSED_NO_LIBM_BOUND", "rational Taylor, binary64 receipt and FD obligations are unified without correct-rounding evidence", ev("artifacts/task_DF_p3_trig_rounding_contract_20260906/README.md", "artifacts/task_DF_p3_trig_rounding_contract_20260906/contract.json", "artifacts/task_DF_p3_trig_rounding_contract_20260906/checker.py")),
        ("routeb_p4_static_runtime_gate", "STATIC_GATE_REUSED_POSTHASH_VERIFIED", "DG produced no new artifact; existing CZ/CJ evidence confirms 11/11 metadata callsite coverage, runtime remains open", ev("artifacts/task_CZ_p4_hook_applied_20260906/POST_APPLY_VERIFICATION.md", "artifacts/task_CJ_p4_hook_callsite_audit_20260906/README.md", target)),
        ("routeb_obstruction_history_receipt_integration", "READ_ONLY_SNAPSHOT_INTEGRATION_PASS", "CW adapter preserves attempts, errors, events and chained hashes from state snapshots without admission mutation", ev("artifacts/task_CW_obstruction_history_receipt_20260906/REPORT.md", "artifacts/task_CW_obstruction_history_receipt_20260906/adapter.py", "artifacts/task_CW_obstruction_history_receipt_20260906/checker.py", "artifacts/task_CW_obstruction_history_receipt_20260906/build_receipt.py")),
        ("routeb_anthropic_spectral_provenance_dedup", "DEDUPLICATED_OPEN_COMPILE", "minimal spectral source/provenance is retained; isolated Mathlib resolution failure remains explicit", ev("artifacts/task_DI_anthropic_spectral_provenance_20260906/REPORT.md", "artifacts/task_DI_anthropic_spectral_provenance_20260906/PROVENANCE.md", "artifacts/task_DI_anthropic_spectral_provenance_20260906/COMPILE_RECEIPT.md", "artifacts/task_DI_anthropic_spectral_provenance_20260906/SpectralMinimal.lean")),
    ]
    graph = json.loads(old.read_text(encoding="utf-8"))
    for kind, status, reason, evidence in audits:
        graph.setdefault("bottleneck_audits", []).append({"kind": kind, "status": status, "evidence_level": "bounded_math_or_read_only_integration", "semantic_boundary": reason, "registry_promoted": False, "formal_certificate_allowed": False, "files": {k: {"path": ref(v), "sha256": sha(v)} for k, v in evidence.items()}})
        graph.setdefault("open_frontier_updates", []).append({"node": kind, "status": status.lower(), "reason": reason})
    graph.update(schema="routeb-proposed-proof-dag-v157", supersedes=old.name)
    new.write_text(json.dumps(graph, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if not backup.exists():
        backup.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(store.path, backup)
    digest = sha(new)
    for kind, _status, _reason, evidence in audits:
        first = next(iter(evidence.values()))
        state.graph_artifacts.append({"schema_version": 1, "algorithm": kind + "/v1", "graph_sha256": digest, "roots": [], "selected_nodes": [], "source": str(first), "evidence_sha256": sha(first), "registry_promoted": False, "formal_certificate_allowed": False})
    state.event("routeb_dd_di_recorded", proposed_dag=ref(new), proposed_dag_sha256=digest, audits=[x[0] for x in audits], registry_promoted=False, formal_certificate_allowed=False, broad_regression_run=False)
    store.save(state)
    print({"revision": state.revision, "graph": new.name, "registry": len(state.registry), "target": ref(target)})


if __name__ == "__main__":
    main()
