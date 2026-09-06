"""Record receipt-tooling and frontier-ranking progress for Route-B."""
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
    assert state.revision == 209 and not state.registry
    old = ROOT / "artifacts/routeb_6dof/block45-obligations-v163.json"
    new = ROOT / "artifacts/routeb_6dof/block45-obligations-v164.json"
    backup = ROOT / "artifacts/routeb_storage_checkpoint_20260907/state-before-revision210.json"
    assert old.is_file() and not new.exists()

    audits = [
        (
            "routeb_physical_receipt_search",
            "OPEN_MISSING_DATA",
            "no same-domain A>mu, coupling, rho_reg, complete coverage or outward receipt was found; candidate algebra remains non-admitting",
            ev(
                "artifacts/task_EN_physical_receipt_search_20260907/REPORT.md",
                "artifacts/task_EN_physical_receipt_search_20260907/ledger.json",
            ),
        ),
        (
            "routeb_indexed_receipt_materializer",
            "TOOL_READY_INPUT_REQUIRED_FAIL_CLOSED",
            "materializer only canonicalizes existing sparse records, rejects malformed input and never enumerates 33^4",
            ev(
                "scripts/record_routeb_indexed_receipts.py",
                "tests/test_routeb_indexed_receipts.py",
                "docs/routeb-indexed-receipts-README.md",
                "docs/routeb-indexed-receipts-REPORT.md",
            ),
        ),
        (
            "routeb_p3_binary64_identity_helper",
            "HELPER_READY_UNPROVED_AND_NOT_CLAIMED",
            "bit-pattern and q1-q6 identity checks are available, while Taylor-to-Julia/libm equivalence remains unproved",
            ev(
                "scripts/task_p3_binary64_identity.py",
                "artifacts/task_EO_p3_binary64_identity_20260907/receipt_schema.json",
                "artifacts/task_EO_p3_binary64_identity_20260907/REPORT.md",
                "artifacts/task_EO_p3_binary64_identity_20260907/test_identity.py",
            ),
        ),
        (
            "routeb_p4_environment_probe",
            "PARSE_PASS_EXACT_DATA_OPEN",
            "local Julia 1.10.4 parses the target, but exact coefficient/Gram/source-binding/coverage receipts remain absent",
            ev(
                "artifacts/task_EP_p4_environment_probe_20260907/REPORT.md",
                "artifacts/task_EP_p4_environment_probe_20260907/ledger.json",
            ),
        ),
        (
            "routeb_flowpipe_receipt_tool",
            "TOOL_READY_NUMERIC_INPUT_REQUIRED_FAIL_CLOSED",
            "strict validator is ready for real 14-dimensional numeric receipts and rejects missing or placeholder data",
            ev(
                "scripts/record_routeb_flowpipe_numeric_receipt.py",
                "artifacts/task_EQ_flowpipe_receipt_tool_20260907/REPORT.md",
                "artifacts/task_EQ_flowpipe_receipt_tool_20260907/test_receipt_tool.py",
            ),
        ),
        (
            "routeb_frontier_math_ranking",
            "RANKING_PASS_FRONTIER_OPEN",
            "top closure bottlenecks are source/comparator binding, complete flowpipe coverage, and B45-5 descriptor-Schur residual closure",
            ev(
                "artifacts/task_ER_frontier_math_ranking_20260907/REPORT.md",
                "artifacts/task_ER_frontier_math_ranking_20260907/ranking.json",
                "artifacts/task_ER_frontier_math_ranking_20260907/check_frontier_ranking.py",
            ),
        ),
    ]

    graph = json.loads(old.read_text(encoding="utf-8"))
    for kind, status, reason, evidence in audits:
        graph.setdefault("bottleneck_audits", []).append(
            {
                "kind": kind,
                "status": status,
                "evidence_level": "bounded_tooling_or_source_search",
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

    graph.update(schema="routeb-proposed-proof-dag-v164", supersedes=old.name)
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
        "routeb_en_er_recorded",
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
