"""Record DJ-DO mathematical and workflow progress without promotion."""
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
    assert state.revision == 204 and not state.registry
    old = ROOT / "artifacts/routeb_6dof/block45-obligations-v158.json"
    new = ROOT / "artifacts/routeb_6dof/block45-obligations-v159.json"
    backup = ROOT / "artifacts/routeb_storage_checkpoint_20260906/state-before-revision205.json"
    assert old.is_file() and not new.exists()
    audits = [
        ("routeb_schur_coupling_bound", "CONDITIONAL_CROSS_BLOCK_BOUND_PHYSICAL_OPEN", "analytic CSV gives b_BD=206741/800000 and b_DB=823751/2400000; a>mu/e_mu/full cover absent", ev("artifacts/task_DJ_schur_coupling_bound_20260906/REPORT.md", "artifacts/task_DJ_schur_coupling_bound_20260906/cross_block_rows.csv")),
        ("routeb_cell16_anisotropic_partition", "CONDITIONAL_33_TO_4D_PARTITION_COVER_OPEN", "active split vector (1,33,33,33,1,1) reduces candidate combinations to 33^4; child receipts and cover absent", ev("artifacts/task_DK_cell16_anisotropic_partition_20260906/REPORT.md", "artifacts/task_DK_cell16_anisotropic_partition_20260906/ledger.json", "artifacts/task_DK_cell16_anisotropic_partition_20260906/checker.py")),
        ("routeb_p3_verified_trig_branch", "CONDITIONAL_OPEN_FAIL_CLOSED", "explicit Taylor/rational evaluator is specified, but comparator to deployed Julia/libm remains open", ev("artifacts/task_DL_p3_verified_trig_branch_20260906/README.md", "artifacts/task_DL_p3_verified_trig_branch_20260906/contract.json", "artifacts/task_DL_p3_verified_trig_branch_20260906/check.py")),
        ("routeb_p4_post_apply_gate", "STATIC_POST_APPLY_GATE_PASS_RUNTIME_OPEN", "applied hook passes 11/11 metadata, backup and Float64-only checks; no Julia/solver receipt", ev("artifacts/task_DM_p4_post_apply_gate_20260906/POST_APPLY_GATE.md", "artifacts/task_CZ_p4_hook_applied_20260906/POST_APPLY_VERIFICATION.md")),
        ("routeb_true_dh_flowpipe_receipt", "SCHEMA_READY_NUMERIC_RECEIPT_OPEN", "initial/step/continuation/terminal dependency fields are explicit; no numeric RHS/Lipschitz receipt", ev("artifacts/task_DN_true_dh_flowpipe_receipt_20260906/RECEIPT.md", "artifacts/task_DN_true_dh_flowpipe_receipt_20260906/receipt_schema.json")),
        ("routeb_checker_repair_loop", "DESIGN_READY_NO_LIVE_MUTATION", "deterministic path/schema/hash/manual-review classification and idempotent receipt are specified", ev("artifacts/task_DO_checker_repair_loop_20260906/README.md", "artifacts/task_DO_checker_repair_loop_20260906/repair_receipt.schema.json", "artifacts/task_DO_checker_repair_loop_20260906/sample-repair-receipt.json")),
    ]
    graph = json.loads(old.read_text(encoding="utf-8"))
    for kind, status, reason, evidence in audits:
        graph.setdefault("bottleneck_audits", []).append({"kind": kind, "status": status, "evidence_level": "bounded_math_or_static_gate", "semantic_boundary": reason, "registry_promoted": False, "formal_certificate_allowed": False, "files": {k: {"path": ref(v), "sha256": sha(v)} for k, v in evidence.items()}})
        graph.setdefault("open_frontier_updates", []).append({"node": kind, "status": status.lower(), "reason": reason})
    graph.update(schema="routeb-proposed-proof-dag-v159", supersedes=old.name)
    new.write_text(json.dumps(graph, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if not backup.exists():
        backup.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(store.path, backup)
    digest = sha(new)
    for kind, _status, _reason, evidence in audits:
        first = next(iter(evidence.values()))
        state.graph_artifacts.append({"schema_version": 1, "algorithm": kind + "/v1", "graph_sha256": digest, "roots": [], "selected_nodes": [], "source": str(first), "evidence_sha256": sha(first), "registry_promoted": False, "formal_certificate_allowed": False})
    state.event("routeb_dj_do_recorded", proposed_dag=ref(new), proposed_dag_sha256=digest, audits=[x[0] for x in audits], registry_promoted=False, formal_certificate_allowed=False, broad_regression_run=False)
    store.save(state)
    print({"revision": state.revision, "graph": new.name, "registry": len(state.registry)})


if __name__ == "__main__":
    main()
