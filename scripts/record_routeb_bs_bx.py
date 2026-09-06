"""Record the BS-BX research batch without admitting conditional evidence."""
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
    assert state.revision == 194 and not state.registry
    old = ROOT / "artifacts/routeb_6dof/block45-obligations-v148.json"
    new = ROOT / "artifacts/routeb_6dof/block45-obligations-v149.json"
    backup = ROOT / "artifacts/routeb_storage_checkpoint_20260906/state-before-revision195.json"
    assert old.is_file() and not new.exists()
    audits = [
        ("routeb_p3_tight_center_interval", "CONDITIONAL_INTERVAL_SOURCE_SEAM_OPEN", "degree-24 Fraction trig intervals improve the bound but do not bind deployed Float64/libm", ev("artifacts/task_BS_p3_tight_center_interval_20260906/REPORT.md", "artifacts/task_BS_p3_tight_center_interval_20260906/p3_tight_center_intervals.json", "artifacts/task_BS_p3_tight_center_interval_20260906/derive_intervals.py")),
        ("routeb_full_x0_receipt_adapter", "ADAPTER_READY_NUMERIC_RECEIPT_OPEN", "v2-to-strict adapter rejects absent cell/source/coverage evidence", ev("artifacts/task_BN_full_x0_checker_integration_20260906/REPORT.md", "artifacts/task_BW_flowpipe_receipt_adapter_20260906/adapter.py", "artifacts/task_BW_flowpipe_receipt_adapter_20260906/receipt_schema.json", "artifacts/task_BW_flowpipe_receipt_adapter_20260906/test_adapter.py")),
        ("routeb_p4_runtime_export_hook", "PATCH_DRAFT_FAIL_CLOSED", "semantic D0/c1/c2 and Gram export hook is drafted; Float64 is not rational evidence", ev("artifacts/task_BO_p4_runtime_export_plan_20260906/README.md", "artifacts/task_BO_p4_runtime_export_plan_20260906/routeB_pmi_runtime_hook.unified.diff", "artifacts/task_BO_p4_runtime_export_plan_20260906/check_runtime_hook.py")),
        ("routeb_s_d_inverse_difference", "CONDITIONAL_BRIDGE_BOUND_OPEN", "resolvent identity is exact; physical outward-rounded block receipts are absent", ev("artifacts/task_BU_sd_inverse_difference_20260906/DERIVATION.md", "artifacts/task_BU_sd_inverse_difference_20260906/check_inverse_difference.py", "artifacts/task_BU_sd_inverse_difference_20260906/README.md")),
        ("routeb_p4_export_hook_strict_checker", "CHECKER_READY_PAYLOAD_OPEN", "strict export hook checker preserves UNAVAILABLE_FLOAT64_ONLY", ev("artifacts/task_BV_p4_export_hook_patch_20260906/README.md", "artifacts/task_BV_p4_export_hook_patch_20260906/routeB_p4_export_hook.unified.diff", "artifacts/task_BV_p4_export_hook_patch_20260906/check_p4_export.py")),
        ("routeb_flowpipe_receipt_adapter", "FAIL_CLOSED_ADAPTER_ONLY", "adapter tests pass but no numerical RHS receipt is created", ev("artifacts/task_BW_flowpipe_receipt_adapter_20260906/README.md", "artifacts/task_BW_flowpipe_receipt_adapter_20260906/adapter.py", "artifacts/task_BW_flowpipe_receipt_adapter_20260906/test_adapter.py")),
        ("routeb_core_statement_comparator", "INTEGRATED_FAIL_CLOSED_GATE", "admission now checks source, normalization, coverage and target identity", ev("src/percolation_workflow/comparator_gate.py", "tests/test_comparator_gate.py", "tests/test_comparator_acceptance.py", "artifacts/task_BX_comparator_core_integration_20260906/REPORT.md")),
    ]
    graph = json.loads(old.read_text(encoding="utf-8"))
    for kind, status, reason, evidence in audits:
        graph.setdefault("bottleneck_audits", []).append({
            "kind": kind, "status": status, "evidence_level": "bounded_sidecar_or_core_patch",
            "semantic_boundary": reason, "registry_promoted": False,
            "formal_certificate_allowed": False,
            "files": {k: {"path": ref(v), "sha256": sha(v)} for k, v in evidence.items()},
        })
        graph.setdefault("open_frontier_updates", []).append({"node": kind, "status": status.lower(), "reason": reason})
    graph.update(schema="routeb-proposed-proof-dag-v149", supersedes=old.name)
    new.write_text(json.dumps(graph, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if not backup.exists():
        backup.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(store.path, backup)
    digest = sha(new)
    for kind, _status, _reason, evidence in audits:
        first = next(iter(evidence.values()))
        state.graph_artifacts.append({"schema_version": 1, "algorithm": kind + "/v1", "graph_sha256": digest, "roots": [], "selected_nodes": [], "source": str(first), "evidence_sha256": sha(first), "registry_promoted": False, "formal_certificate_allowed": False})
    state.event("routeb_bs_bx_recorded", proposed_dag=ref(new), proposed_dag_sha256=digest, audits=[x[0] for x in audits], registry_promoted=False, formal_certificate_allowed=False, broad_regression_run=False)
    store.save(state)
    print({"revision": state.revision, "graph": new.name, "registry": len(state.registry)})


if __name__ == "__main__":
    main()
