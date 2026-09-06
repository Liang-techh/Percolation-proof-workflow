"""Record EH-EM mathematical bottleneck receipts and API hardening."""
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
    assert state.revision == 208 and not state.registry
    old = ROOT / "artifacts/routeb_6dof/block45-obligations-v162.json"
    new = ROOT / "artifacts/routeb_6dof/block45-obligations-v163.json"
    backup = ROOT / "artifacts/routeb_storage_checkpoint_20260907/state-before-revision209.json"
    assert old.is_file() and not new.exists()

    audits = [
        (
            "routeb_physical_schur_bridge",
            "FAIL_CLOSED_MISSING_SAME_DOMAIN_RECEIPTS",
            "exact physical Schur conditions are explicit; same-domain A>mu, compatible coupling, BU bridge and coverage receipts are absent",
            ev(
                "artifacts/task_EH_physical_schur_bridge_20260907/REPORT.md",
                "artifacts/task_EH_physical_schur_bridge_20260907/ledger.json",
            ),
        ),
        (
            "routeb_cell16_indexed_receipt_schema",
            "OPEN_INDEXED_RECEIPT_SCHEMA_ONLY",
            "sparse 33^4 address and closure invariants are defined without enumerating or claiming child numerical receipts",
            ev(
                "artifacts/task_EI_cell16_receipt_schema_20260907/REPORT.md",
                "artifacts/task_EI_cell16_receipt_schema_20260907/ledger.json",
                "artifacts/task_EI_cell16_receipt_schema_20260907/checker.py",
            ),
        ),
        (
            "routeb_p3_statement_identity",
            "FAIL_CLOSED_STATEMENT_IDENTITY_UNPROVED",
            "Taylor evaluator schema is distinct from original Julia Float64/libm comparator and cannot promote it",
            ev(
                "artifacts/task_EJ_p3_statement_identity_20260907/REPORT.md",
                "artifacts/task_EJ_p3_statement_identity_20260907/receipt_schema.json",
                "artifacts/task_EJ_p3_statement_identity_20260907/check.py",
            ),
        ),
        (
            "routeb_p4_runtime_boundary",
            "OPEN_RUNTIME_FLOAT64_BOUNDARY",
            "static post-apply and Float64-only checks pass; runtime parse, exact Gram/coefficient binding and coverage remain open",
            ev(
                "artifacts/task_EK_p4_runtime_boundary_20260907/REPORT.md",
                "artifacts/task_EE_p4_static_postapply_replay_20260907/REPLAY_REPORT.md",
            ),
        ),
        (
            "routeb_flowpipe_numeric_contract",
            "FAIL_CLOSED_MISSING_NUMERIC_RECEIPT",
            "14-dimensional flowpipe parent schema is strict, but no numeric RHS/Lipschitz/Picard/terminal receipt exists",
            ev(
                "artifacts/task_EL_flowpipe_numeric_contract_20260907/REPORT.md",
                "artifacts/task_EL_flowpipe_numeric_contract_20260907/schema.json",
                "artifacts/task_EL_flowpipe_numeric_contract_20260907/checker.py",
            ),
        ),
        (
            "routeb_repair_api_hardening",
            "NARROW_TEST_PASS_FAIL_CLOSED_ADMISSION_UNCHANGED",
            "max_rounds, complete relative DO paths and exact envelope fields are hardened; registry and admission remain isolated",
            ev(
                "artifacts/task_EM_repair_api_hardening_20260907/REPORT.md",
                "src/percolation_workflow/repair.py",
                "src/percolation_workflow/disjoint.py",
                "tests/test_repair_api_hardening.py",
            ),
        ),
    ]

    graph = json.loads(old.read_text(encoding="utf-8"))
    for kind, status, reason, evidence in audits:
        graph.setdefault("bottleneck_audits", []).append(
            {
                "kind": kind,
                "status": status,
                "evidence_level": "bounded_math_or_workflow_audit",
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

    graph.update(schema="routeb-proposed-proof-dag-v163", supersedes=old.name)
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
        "routeb_eh_em_recorded",
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
