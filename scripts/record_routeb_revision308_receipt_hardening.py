"""Record receipt-gate hardening without promoting mathematical evidence."""
from __future__ import annotations

import hashlib
import json
import shutil
from pathlib import Path

from record_routeb_port_progress import ROOT, ref
from percolation_workflow.coverage_receipt import validate_coverage_receipt
from percolation_workflow.store import StateStore


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    store = StateStore(ROOT / "artifacts/routeb_6dof/state.json")
    state = store.load()
    if state.revision != 307 or state.registry:
        raise ValueError("revision-308 recorder requires revision 307 and empty registry")
    old = ROOT / "artifacts/routeb_6dof/block45-obligations-v261.json"
    new = ROOT / "artifacts/routeb_6dof/block45-obligations-v262.json"
    report = ROOT / "artifacts/task_routeb_revision308_receipt_hardening/REPORT.md"
    receipt = ROOT / "artifacts/task_FLT_coverage_receipt_api_20260908/receipt_after_scalar_aggregation.json"
    source = ROOT / "src/percolation_workflow/coverage_receipt.py"
    tests = ROOT / "tests/test_coverage_receipt.py"
    advisory = ROOT / "src/percolation_workflow/advisory_reuse.py"
    if not all(p.is_file() for p in (old, report, receipt, source, tests, advisory)):
        raise ValueError("missing revision-308 evidence")
    summary = validate_coverage_receipt(json.loads(receipt.read_text(encoding="utf-8")))
    expected = {"node_count": 1, "pending_count": 1, "complete_claim": False,
                "structurally_closed": False}
    if any(summary.get(k) != v for k, v in expected.items()):
        raise ValueError(f"unexpected canonical receipt summary: {summary}")
    graph = json.loads(old.read_text(encoding="utf-8"))
    record = {
        "kind": "routeb_receipt_gate_hardening",
        "status": "PASS_FOCUSED_FAIL_CLOSED_RECEIPT_HARDENING",
        "evidence_level": "structural-validator-and-advisory-contract",
        "files": [ref(report), ref(source), ref(tests), ref(advisory), ref(receipt)],
        "focused_test_count": 34,
        "current_receipt_summary": summary,
        "registry_promoted": False,
        "formal_certificate_allowed": False,
    }
    graph.setdefault("workflow_hardening", []).append(record)
    graph.setdefault("bottleneck_audits", []).append(record)
    graph.setdefault("open_frontier_updates", []).append({
        "node": "B45.coverage_receipt_gate",
        "status": "validator_hardened_global_coverage_still_open",
        "reason": "complete-claim bypasses and canonical fallback were closed; the actual receipt remains pending and cannot promote a theorem.",
    })
    graph.update(schema="routeb-proposed-proof-dag-v262", supersedes=old.name)
    new.write_text(json.dumps(graph, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    backup = ROOT / "artifacts/routeb_storage_checkpoint_20260908/state-before-revision308.json"
    if not backup.exists():
        backup.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(store.path, backup)
    graph_sha = sha(new)
    state.graph_artifacts.append({
        "schema_version": 1,
        "algorithm": "routeb_revision308_receipt_hardening/v1",
        "graph_sha256": graph_sha,
        "roots": [],
        "selected_nodes": [],
        "evidence_sha256": sha(report),
        "validator_source_sha256": sha(source),
        "validator_tests_sha256": sha(tests),
        "advisory_reuse_source_sha256": sha(advisory),
        "receipt_structural_validation": True,
        "dynamics_coverage_complete": False,
        "registry_promoted": False,
        "formal_certificate_allowed": False,
    })
    state.event(
        "routeb_revision308_receipt_hardening_recorded",
        proposed_dag=ref(new), proposed_dag_sha256=graph_sha,
        receipt_summary=summary, focused_test_count=34,
        dynamics_coverage_complete=False, registry_promoted=False,
        formal_certificate_allowed=False, broad_regression_run=False,
    )
    store.save(state)
    print(json.dumps({"revision": state.revision, "graph": new.name,
                      "registry": len(state.registry), "formal_certificate_allowed": False}))


if __name__ == "__main__":
    main()
