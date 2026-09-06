"""Record the CR-CW batch without promoting non-kernel evidence."""
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
    assert state.revision == 199 and not state.registry
    old = ROOT / "artifacts/routeb_6dof/block45-obligations-v153.json"
    new = ROOT / "artifacts/routeb_6dof/block45-obligations-v154.json"
    backup = ROOT / "artifacts/routeb_storage_checkpoint_20260906/state-before-revision200.json"
    assert old.is_file() and not new.exists()
    audits = [
        ("routeb_schur_dN_from_symbols", "SOURCE_AVAILABLE_SYMBOLIC_ENTRIES_DN_OPEN", "16 M_DD(q) entries yield a rational first-order envelope, but neighbor geometry and norm/rounding inputs are absent", ev("artifacts/task_CR_schur_dN_from_symbols_20260906/REPORT.md", "artifacts/task_CR_schur_dN_from_symbols_20260906/coefficients.csv")),
        ("routeb_p3_float64_source_receipt", "RECORDED_FAIL_CLOSED_SOURCE_RECEIPT", "binary64 literals and pi/2 source lines are hashed; libm correctness, FD rounding and sin/cos enclosure remain open", ev("artifacts/task_CS_p3_float64_source_receipt_20260906/README.md", "artifacts/task_CS_p3_float64_source_receipt_20260906/receipt.json", "artifacts/task_CS_p3_float64_source_receipt_20260906/record_receipt.py")),
        ("routeb_p4_export_recovery_readiness", "READY_FOR_EXPLICIT_APPLY", "preimage/backup/callsite/hash gates pass, but target Julia patch remains unapplied", ev("artifacts/task_CT_p4_export_recovery_check_20260906/APPLY_READINESS_REPORT.md", "artifacts/task_CT_p4_export_recovery_check_20260906/check_recovery_readiness.py")),
        ("routeb_picard_terminal_budget", "SCHEMA_READY_CERTIFICATE_DATA_OPEN", "finite-step terminal budget and continuation matching are structurally checked without numeric flowpipe data", ev("artifacts/task_CU_picard_terminal_budget_20260906/README.md", "artifacts/task_CU_picard_terminal_budget_20260906/terminal_budget_schema.json", "artifacts/task_CU_picard_terminal_budget_20260906/check_terminal_budget.py")),
        ("routeb_obstruction_history_receipt", "RECEIPT_SCHEMA_READY_READ_ONLY", "failed/timeout/compile-error/blocked attempts and chained evidence hashes can be preserved from snapshots", ev("artifacts/task_CW_obstruction_history_receipt_20260906/REPORT.md", "artifacts/task_CW_obstruction_history_receipt_20260906/receipt_schema.json", "artifacts/task_CW_obstruction_history_receipt_20260906/build_receipt.py", "artifacts/task_CW_obstruction_history_receipt_20260906/README.md")),
    ]
    graph = json.loads(old.read_text(encoding="utf-8"))
    for kind, status, reason, evidence in audits:
        graph.setdefault("bottleneck_audits", []).append({"kind": kind, "status": status, "evidence_level": "bounded_source_or_state_receipt_audit", "semantic_boundary": reason, "registry_promoted": False, "formal_certificate_allowed": False, "files": {k: {"path": ref(v), "sha256": sha(v)} for k, v in evidence.items()}})
        graph.setdefault("open_frontier_updates", []).append({"node": kind, "status": status.lower(), "reason": reason})
    graph.update(schema="routeb-proposed-proof-dag-v154", supersedes=old.name)
    new.write_text(json.dumps(graph, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if not backup.exists():
        backup.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(store.path, backup)
    digest = sha(new)
    for kind, _status, _reason, evidence in audits:
        first = next(iter(evidence.values()))
        state.graph_artifacts.append({"schema_version": 1, "algorithm": kind + "/v1", "graph_sha256": digest, "roots": [], "selected_nodes": [], "source": str(first), "evidence_sha256": sha(first), "registry_promoted": False, "formal_certificate_allowed": False})
    state.event("routeb_cr_cw_recorded", proposed_dag=ref(new), proposed_dag_sha256=digest, audits=[x[0] for x in audits], registry_promoted=False, formal_certificate_allowed=False, broad_regression_run=False)
    store.save(state)
    print({"revision": state.revision, "graph": new.name, "registry": len(state.registry)})


if __name__ == "__main__":
    main()
