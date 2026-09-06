"""Record CF-CK frontier evidence without promoting conditional results."""
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
    assert state.revision == 197 and not state.registry
    old = ROOT / "artifacts/routeb_6dof/block45-obligations-v151.json"
    new = ROOT / "artifacts/routeb_6dof/block45-obligations-v152.json"
    backup = ROOT / "artifacts/routeb_storage_checkpoint_20260906/state-before-revision198.json"
    assert old.is_file() and not new.exists()
    audits = [
        ("routeb_p3_binary64_hex_reuse", "NO_NEW_ARTIFACT_REUSED_BZ", "CF found no new artifact; existing BZ exact binary64 table and source gaps remain authoritative", ev("artifacts/task_BZ_p3_binary64_binding_20260906/REPORT.md", "artifacts/task_BZ_p3_binary64_binding_20260906/binding_report.json")),
        ("routeb_p3_fd_semantics_receipt", "SOURCE_TRACE_OPEN", "q plus/minus h and central-FD call chain is hashed, but rounding/domain/cancellation evidence is missing", ev("artifacts/task_CG_p3_fd_semantics_20260906/gap_report.md", "artifacts/task_CG_p3_fd_semantics_20260906/source_line_hash_receipt_schema.md")),
        ("routeb_schur_dN_existing_data", "OPEN_MISSING_DATA", "C0-L and C0-R have no neighbor d_N data; anchor C0 only", ev("artifacts/task_CH_schur_dN_existing_data_20260906/REPORT.md", "artifacts/task_CH_schur_dN_existing_data_20260906/ledger.json", "artifacts/task_CH_schur_dN_existing_data_20260906/check.py")),
        ("routeb_picard_core_adapter", "ADAPTER_MISMATCH_CERTIFICATE_OPEN", "Picard ref alone lacks strict produced receipt state/time/source/coverage fields", ev("artifacts/task_CI_picard_core_adapter_20260906/README.md", "artifacts/task_CI_picard_core_adapter_20260906/adapter.py", "artifacts/task_CA_flowpipe_picard_contract_20260906/picard_flowpipe_schema.json", "artifacts/task_CI_picard_core_adapter_20260906/test_adapter.py")),
        ("routeb_p4_hook_callsite_coverage", "STATIC_COVERAGE_11_OF_11", "BV and CB together cover all 11 actual pmi_block call families; patch remains unapplied", ev("artifacts/task_CJ_p4_hook_callsite_audit_20260906/README.md", "artifacts/task_CJ_p4_hook_callsite_audit_20260906/check_callsite_audit.py")),
        ("routeb_frontier_math_lane_projection", "PRIORITY_PROJECTION_READ_ONLY", "source semantics precedes coverage, physical bridge, lean adapter and engineering", ev("artifacts/task_CK_frontier_scheduler_math_lanes_20260906/REPORT.md", "artifacts/task_CK_frontier_scheduler_math_lanes_20260906/priority_projection.json", "artifacts/task_CK_frontier_scheduler_math_lanes_20260906/check_frontier_priority.py")),
    ]
    graph = json.loads(old.read_text(encoding="utf-8"))
    for kind, status, reason, evidence in audits:
        graph.setdefault("bottleneck_audits", []).append({"kind": kind, "status": status, "evidence_level": "bounded_source_or_scheduler_audit", "semantic_boundary": reason, "registry_promoted": False, "formal_certificate_allowed": False, "files": {k: {"path": ref(v), "sha256": sha(v)} for k, v in evidence.items()}})
        graph.setdefault("open_frontier_updates", []).append({"node": kind, "status": status.lower(), "reason": reason})
    graph.update(schema="routeb-proposed-proof-dag-v152", supersedes=old.name)
    new.write_text(json.dumps(graph, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if not backup.exists():
        backup.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(store.path, backup)
    digest = sha(new)
    for kind, _status, _reason, evidence in audits:
        first = next(iter(evidence.values()))
        state.graph_artifacts.append({"schema_version": 1, "algorithm": kind + "/v1", "graph_sha256": digest, "roots": [], "selected_nodes": [], "source": str(first), "evidence_sha256": sha(first), "registry_promoted": False, "formal_certificate_allowed": False})
    state.event("routeb_cf_ck_recorded", proposed_dag=ref(new), proposed_dag_sha256=digest, audits=[x[0] for x in audits], registry_promoted=False, formal_certificate_allowed=False, broad_regression_run=False)
    store.save(state)
    print({"revision": state.revision, "graph": new.name, "registry": len(state.registry)})


if __name__ == "__main__":
    main()
