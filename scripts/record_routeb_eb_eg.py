"""Record EB-EG source bridges, partitions, and repair-loop audit."""
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
    assert state.revision == 207 and not state.registry
    old = ROOT / "artifacts/routeb_6dof/block45-obligations-v161.json"
    new = ROOT / "artifacts/routeb_6dof/block45-obligations-v162.json"
    backup = ROOT / "artifacts/routeb_storage_checkpoint_20260907/state-before-revision208.json"
    assert old.is_file() and not new.exists()
    audits = [
        ("routeb_schur_child_source_bridge", "CONDITIONAL_SOURCE_BOUND_SCHUR_OPEN", "CR/CX/DJ/DD algebra, hashes, coupling and child inverse are combined; physical A>mu/coverage absent", ev("artifacts/task_EB_schur_child_source_bridge_20260907/REPORT.md", "artifacts/task_EB_schur_child_source_bridge_20260907/ledger.json", "artifacts/task_EB_schur_child_source_bridge_20260907/source_hashes.json")),
        ("routeb_cell16_indexed_child_count", "OPEN_INDEXED_PARTITION_COUNT_AUDIT", "33^4=1185921 address space and receipt invariants are checked without enumerating children", ev("artifacts/task_EC_cell16_partition_count_20260907/REPORT.md", "artifacts/task_EC_cell16_partition_count_20260907/ledger.json")),
        ("routeb_p3_taylor_binary64_boundary", "OPEN_FAIL_CLOSED_STATEMENT_BOUNDARY", "explicit evaluator and binary64 receipt are separated from runtime/libm/FMA equivalence", ev("artifacts/task_ED_p3_taylor_binary64_boundary_20260907/README.md", "artifacts/task_ED_p3_taylor_binary64_boundary_20260907/receipt.json", "artifacts/task_ED_p3_taylor_binary64_boundary_20260907/check.py")),
        ("routeb_p4_static_postapply_replay", "STATIC_POST_APPLY_REPLAY_RUNTIME_OPEN", "target/backup/callsites/Float64-only gate pass; Julia runtime and solver remain open", ev("artifacts/task_EE_p4_static_postapply_replay_20260907/REPLAY_REPORT.md")),
        ("routeb_true_dh_flowpipe_parent_receipt", "PARENT_CHAIN_READY_NUMERIC_RECEIPT_OPEN", "initial-step-continuation-terminal chain is explicit and fails closed without numeric receipt", ev("artifacts/task_EF_flowpipe_parent_receipt_20260907/REPORT.md", "artifacts/task_EF_flowpipe_parent_receipt_20260907/parent_receipt.json", "artifacts/task_EF_flowpipe_parent_receipt_20260907/checker.py")),
        ("routeb_repair_receipt_api_audit", "API_AUDIT_PASS_FOLLOWUPS_OPEN", "disjoint repair receipt API is isolated; envelope/max_rounds/basename followups remain", ev("artifacts/task_EG_repair_receipt_api_audit_20260907/REPORT.md")),
    ]
    graph = json.loads(old.read_text(encoding="utf-8"))
    for kind, status, reason, evidence in audits:
        graph.setdefault("bottleneck_audits", []).append({"kind": kind, "status": status, "evidence_level": "bounded_source_bridge_or_workflow_audit", "semantic_boundary": reason, "registry_promoted": False, "formal_certificate_allowed": False, "files": {k: {"path": ref(v), "sha256": sha(v)} for k, v in evidence.items()}})
        graph.setdefault("open_frontier_updates", []).append({"node": kind, "status": status.lower(), "reason": reason})
    graph.update(schema="routeb-proposed-proof-dag-v162", supersedes=old.name)
    new.write_text(json.dumps(graph, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if not backup.exists():
        backup.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(store.path, backup)
    digest = sha(new)
    for kind, _status, _reason, evidence in audits:
        first = next(iter(evidence.values()))
        state.graph_artifacts.append({"schema_version": 1, "algorithm": kind + "/v1", "graph_sha256": digest, "roots": [], "selected_nodes": [], "source": str(first), "evidence_sha256": sha(first), "registry_promoted": False, "formal_certificate_allowed": False})
    state.event("routeb_eb_eg_recorded", proposed_dag=ref(new), proposed_dag_sha256=digest, audits=[x[0] for x in audits], registry_promoted=False, formal_certificate_allowed=False, broad_regression_run=False)
    store.save(state)
    print({"revision": state.revision, "graph": new.name, "registry": len(state.registry)})


if __name__ == "__main__":
    main()
