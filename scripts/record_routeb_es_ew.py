"""Record full binding, flowpipe, and B45-5 closure bottlenecks."""
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
    assert state.revision == 210 and not state.registry
    old = ROOT / "artifacts/routeb_6dof/block45-obligations-v164.json"
    new = ROOT / "artifacts/routeb_6dof/block45-obligations-v165.json"
    backup = ROOT / "artifacts/routeb_storage_checkpoint_20260907/state-before-revision211.json"
    assert old.is_file() and not new.exists()

    audits = [
        (
            "routeb_full_source_binding_gap",
            "OPEN_14_STATE_BINDING_GAPS",
            "all 14-state source/comparator, domain, eta, FD, regularization and index-map obligations remain unbound",
            ev(
                "artifacts/task_ES_full_source_binding_gap_20260907/REPORT.md",
                "artifacts/task_ES_full_source_binding_gap_20260907/gap.json",
                "artifacts/task_ES_full_source_binding_gap_20260907/check_gap.py",
            ),
        ),
        (
            "routeb_flowpipe_coverage_protocol",
            "PROTOCOL_READY_NUMERIC_COVERAGE_OPEN",
            "coverage/first-exit schema is mechanically specified; actual finite partition, inclusion and exit witnesses are absent",
            ev(
                "artifacts/task_ET_flowpipe_coverage_protocol_20260907/REPORT.md",
                "artifacts/task_ET_flowpipe_coverage_protocol_20260907/schema.json",
                "artifacts/task_ET_flowpipe_coverage_protocol_20260907/checker.py",
            ),
        ),
        (
            "routeb_descriptor_schur_residual_closure",
            "FAIL_CLOSED_B45_5_PHYSICAL_CLOSURE_OPEN",
            "B45-5 C0-L/C0-R remain open pending A>mu, same-domain coupling, regularizer, margin, coverage, first-exit and terminal receipts",
            ev(
                "artifacts/task_EU_descriptor_schur_closure_20260907/REPORT.md",
                "artifacts/task_EU_descriptor_schur_closure_20260907/ledger.json",
                "artifacts/task_EU_descriptor_schur_closure_20260907/narrow_check.py",
            ),
        ),
        (
            "routeb_source_binding_manifest_tool",
            "TOOL_READY_BINDING_CONCLUSION_NULL",
            "strict 14-state source manifest validator is available, but it emits no binding conclusion and does not touch admission",
            ev(
                "scripts/routeb_source_binding_manifest.py",
                "tests/test_routeb_source_binding_manifest.py",
                "docs/routeb-source-binding-manifest-README.md",
            ),
        ),
        (
            "routeb_flowpipe_continuation_gap",
            "OPEN_GAPS_REMAIN_11_BLOCKERS",
            "single-cell receipts do not yet imply shared boundaries, complete time coverage, ODE bridge, first-exit contradiction or terminal transfer",
            ev(
                "artifacts/task_EV_flowpipe_continuation_gap_20260907/REPORT.md",
                "artifacts/task_EV_flowpipe_continuation_gap_20260907/gap.json",
                "artifacts/task_EV_flowpipe_continuation_gap_20260907/checker.py",
            ),
        ),
        (
            "routeb_residual_closure_tool",
            "TOOL_READY_PHYSICAL_INPUT_REQUIRED_FAIL_CLOSED",
            "strict B45-5 receipt validator is ready; missing dimensions, A>mu, coupling, outward, hash or coverage cannot pass",
            ev(
                "scripts/routeb_residual_closure_receipt.py",
                "artifacts/task_EW_residual_closure_tool_20260907/REPORT.md",
                "artifacts/task_EW_residual_closure_tool_20260907/test_routeb_residual_closure_receipt.py",
            ),
        ),
    ]

    graph = json.loads(old.read_text(encoding="utf-8"))
    for kind, status, reason, evidence in audits:
        graph.setdefault("bottleneck_audits", []).append(
            {
                "kind": kind,
                "status": status,
                "evidence_level": "bounded_gap_audit_or_strict_tool",
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

    graph.update(schema="routeb-proposed-proof-dag-v165", supersedes=old.name)
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
        "routeb_es_ew_recorded",
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
