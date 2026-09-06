"""Record workflow handoff guards and the fail-closed dry-run."""
from __future__ import annotations

import hashlib
import json
import shutil
from pathlib import Path

from record_routeb_port_progress import ROOT, ref
from percolation_workflow.store import StateStore


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def ev(*names: str) -> dict[str, Path]:
    result: dict[str, Path] = {}
    for name in names:
        path = ROOT / name
        assert path.is_file(), path
        result[name] = path
    return result


def main() -> None:
    store = StateStore(ROOT / "artifacts/routeb_6dof/state.json")
    state = store.load()
    assert state.revision == 212 and not state.registry
    old = ROOT / "artifacts/routeb_6dof/block45-obligations-v166.json"
    new = ROOT / "artifacts/routeb_6dof/block45-obligations-v167.json"
    backup = ROOT / "artifacts/routeb_storage_checkpoint_20260907/state-before-revision213.json"
    assert old.is_file() and not new.exists()

    audits = [
        (
            "routeb_receipt_frontier_bridge",
            "ADVISORY_BRIDGE_READY_VERIFIED_FALSE",
            "receipt outcomes are mapped to scheduler advisory data only; NodeStatus, EvidenceStage, registry and admission are untouched",
            ev(
                "src/percolation_workflow/receipt_bridge.py",
                "tests/test_receipt_bridge.py",
                "docs/receipt-bridge-README.md",
            ),
        ),
        (
            "routeb_frontier_job_contract",
            "CONTRACT_PASS_FAIL_CLOSED_REGISTRY_DISABLED",
            "job payload requires parent/child, lane, attempt, paths, hashes and fixed validator interface; incomplete payload fails closed",
            ev(
                "artifacts/task_FG_frontier_job_contract_20260907/REPORT.md",
                "artifacts/task_FG_frontier_job_contract_20260907/schema.json",
                "artifacts/task_FG_frontier_job_contract_20260907/checker.py",
            ),
        ),
        (
            "routeb_comparator_handoff_guard",
            "GUARD_READY_REVIEWABLE_ONLY_ALL_EVIDENCE_REQUIRED",
            "handoff is reviewable only with all five evidence classes; missing or invalid evidence returns structured blockers",
            ev(
                "src/percolation_workflow/comparator_handoff.py",
                "tests/test_comparator_handoff.py",
                "artifacts/task_FH_comparator_handoff_20260907/REPORT.md",
            ),
        ),
        (
            "routeb_lean_verification_boundary",
            "BOUNDARY_PASS_PROPOSED_DAG_NOT_KERNEL_CHECKED",
            "v166 and EX-FC outputs remain advisory; compiled candidate, comparator and pinned zero-sorry Lean gates are still required",
            ev(
                "artifacts/task_FI_verification_boundary_20260907/REPORT.md",
                "artifacts/task_FI_verification_boundary_20260907/matrix.json",
                "artifacts/task_FI_verification_boundary_20260907/checker.py",
            ),
        ),
        (
            "routeb_validator_retry_policy",
            "POLICY_PASS_FAIL_CLOSED_MANUAL_REVIEW",
            "only bounded compile errors may retry after prerequisites; missing/hash/path/statement/physical blockers stop or require manual review",
            ev(
                "artifacts/task_FJ_validator_retry_policy_20260907/REPORT.md",
                "artifacts/task_FJ_validator_retry_policy_20260907/policy.json",
                "artifacts/task_FJ_validator_retry_policy_20260907/checker.py",
            ),
        ),
        (
            "routeb_fail_closed_pipeline_dryrun",
            "DRYRUN_PASS_REGISTRY_UNTOUCHED_FORMAL_DISABLED",
            "source through comparator dry-run blocks at every incomplete stage without fake receipts or admission mutation",
            ev(
                "artifacts/task_FK_fail_closed_pipeline_dryrun_20260907/REPORT.md",
                "artifacts/task_FK_fail_closed_pipeline_dryrun_20260907/trace.json",
                "artifacts/task_FK_fail_closed_pipeline_dryrun_20260907/check.py",
            ),
        ),
    ]

    graph = json.loads(old.read_text(encoding="utf-8"))
    for kind, status, reason, evidence in audits:
        graph.setdefault("bottleneck_audits", []).append(
            {
                "kind": kind,
                "status": status,
                "evidence_level": "strict_workflow_guard_or_boundary_audit",
                "semantic_boundary": reason,
                "registry_promoted": False,
                "formal_certificate_allowed": False,
                "files": {
                    key: {"path": ref(path), "sha256": sha(path)}
                    for key, path in evidence.items()
                },
            }
        )
        graph.setdefault("open_frontier_updates", []).append(
            {"node": kind, "status": status.lower(), "reason": reason}
        )

    graph.update(schema="routeb-proposed-proof-dag-v167", supersedes=old.name)
    new.write_text(json.dumps(graph, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if not backup.exists():
        backup.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(store.path, backup)

    digest = sha(new)
    for kind, _status, _reason, evidence in audits:
        first = next(iter(evidence.values()))
        state.graph_artifacts.append(
            {
                "schema_version": 1,
                "algorithm": kind + "/v1",
                "graph_sha256": digest,
                "roots": [],
                "selected_nodes": [],
                "source": str(first),
                "evidence_sha256": sha(first),
                "registry_promoted": False,
                "formal_certificate_allowed": False,
            }
        )
    state.event(
        "routeb_fg_fk_recorded",
        proposed_dag=ref(new),
        proposed_dag_sha256=digest,
        audits=[item[0] for item in audits],
        registry_promoted=False,
        formal_certificate_allowed=False,
        broad_regression_run=False,
    )
    store.save(state)
    print({"revision": state.revision, "graph": new.name, "registry": len(state.registry)})


if __name__ == "__main__":
    main()
