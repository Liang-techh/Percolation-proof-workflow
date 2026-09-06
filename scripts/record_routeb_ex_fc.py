"""Record real-input entrypoints and handoff tooling for Route-B."""
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
    assert state.revision == 211 and not state.registry
    old = ROOT / "artifacts/routeb_6dof/block45-obligations-v165.json"
    new = ROOT / "artifacts/routeb_6dof/block45-obligations-v166.json"
    backup = ROOT / "artifacts/routeb_storage_checkpoint_20260907/state-before-revision212.json"
    assert old.is_file() and not new.exists()

    audits = [
        (
            "routeb_p4_payload_probe",
            "PARSE_PASS_STATIC_PAYLOAD_ONLY",
            "local Julia Meta.parseall and AST extraction pass without executing source, solver or optimizer; payload is not a proof receipt",
            ev(
                "artifacts/task_EX_p4_payload_probe_20260907/REPORT.md",
                "artifacts/task_EX_p4_payload_probe_20260907/ledger.json",
                "artifacts/task_EX_p4_payload_probe_20260907/hashes.sha256",
            ),
        ),
        (
            "routeb_indexed_coverage_adapter",
            "TOOL_READY_SPARSE_INPUT_REQUIRED_FAIL_CLOSED",
            "adapter checks ET partition metadata, rank, adjacency and hashes without enumerating 33^4 or creating witnesses",
            ev(
                "scripts/routeb_indexed_coverage_adapter.py",
                "tests/test_routeb_indexed_coverage_adapter.py",
                "artifacts/task_EY_indexed_coverage_adapter_20260907/REPORT.md",
            ),
        ),
        (
            "routeb_flowpipe_capture_contract",
            "CONTRACT_READY_EXPLICIT_INTERVAL_REQUIRED_FAIL_CLOSED",
            "capture contract requires explicit interval objects, outward rounding, witness and provenance hashes; point values are rejected",
            ev(
                "scripts/routeb_flowpipe_capture_contract.py",
                "tests/test_routeb_flowpipe_capture_contract.py",
                "artifacts/task_EZ_flowpipe_capture_contract_20260907/REPORT.md",
            ),
        ),
        (
            "routeb_source_binding_preflight",
            "PREFLIGHT_READY_BINDING_CONCLUSION_NULL",
            "14-state ordering and source/domain/eta/FD/Float64 preflight is strict but cannot claim source binding",
            ev(
                "artifacts/task_FA_source_binding_preflight_20260907/REPORT.md",
                "artifacts/task_FA_source_binding_preflight_20260907/schema.json",
                "artifacts/task_FA_source_binding_preflight_20260907/checker.py",
            ),
        ),
        (
            "routeb_physical_data_entrypoints",
            "CANDIDATES_ONLY_MISSING_SAME_DOMAIN_RECEIPT",
            "eight candidate data entrances were identified, but none binds A>mu, two-way coupling, metric, outward rounding and complete coverage together",
            ev(
                "artifacts/task_FB_physical_data_entrypoints_20260907/REPORT.md",
                "artifacts/task_FB_physical_data_entrypoints_20260907/ledger.json",
            ),
        ),
        (
            "routeb_handoff_chain",
            "HANDOFF_AUDIT_PASS_INTEGRATION_OPEN",
            "source binding to sparse cells to flowpipe to residual to comparator is mapped, but validators are not yet wired into scheduler/registry dispatch",
            ev(
                "artifacts/task_FC_handoff_chain_20260907/REPORT.md",
                "artifacts/task_FC_handoff_chain_20260907/chain.json",
                "artifacts/task_FC_handoff_chain_20260907/checker.py",
            ),
        ),
    ]

    graph = json.loads(old.read_text(encoding="utf-8"))
    for kind, status, reason, evidence in audits:
        graph.setdefault("bottleneck_audits", []).append(
            {
                "kind": kind,
                "status": status,
                "evidence_level": "bounded_runtime_probe_or_strict_contract",
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

    graph.update(schema="routeb-proposed-proof-dag-v166", supersedes=old.name)
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
        "routeb_ex_fc_recorded",
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
