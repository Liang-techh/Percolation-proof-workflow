"""Record the batch-closure optimization and two narrow contract audits."""
from __future__ import annotations

import hashlib
import json
import shutil
from pathlib import Path

from record_routeb_port_progress import ROOT, ref
from percolation_workflow.store import StateStore


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    store = StateStore(ROOT / "artifacts/routeb_6dof/state.json")
    state = store.load()
    assert state.revision == 220 and not state.registry
    old = ROOT / "artifacts/routeb_6dof/block45-obligations-v174.json"
    new = ROOT / "artifacts/routeb_6dof/block45-obligations-v175.json"
    backup = ROOT / "artifacts/routeb_storage_checkpoint_20260907/state-before-revision221.json"
    assert old.is_file() and not new.exists()

    code_files = [
        ROOT / "src/percolation_workflow/reduction_batch.py",
        ROOT / "tests/test_reduction_batch.py",
        ROOT / "src/percolation_workflow/__init__.py",
    ]
    fw = ROOT / "artifacts/task_FW_true_dh_formal_bridge_20260907"
    fx = ROOT / "artifacts/task_FX_partition_receipt_contract_20260907"
    fw_files = [fw / n for n in ("REPORT.md", "obligations.json", "provenance.md", "SchurBridgeConditional.lean")]
    fx_files = [fx / n for n in ("REPORT.md", "schema.json", "provenance.md", "validate.py")]
    assert all(p.is_file() for p in code_files + fw_files + fx_files)

    graph = json.loads(old.read_text(encoding="utf-8"))
    optimization = {
        "kind": "reduction_closure_batch_projection",
        "status": "FOCUSED_TEST_PASS_NON_ADMISSION",
        "evidence_level": "read_only_workflow_optimization",
        "semantic_boundary": "Deterministic batch projection only; receipt promotion, registry admission, and parent closure remain existing gated operations.",
        "files": [ref(p) for p in code_files],
        "test_command": "PYTHONPATH=src; python -m pytest -q tests/test_reduction_batch.py",
        "test_result": "3 passed",
        "registry_promoted": False,
        "formal_certificate_allowed": False,
    }
    graph.setdefault("workflow_optimizations", []).append(optimization)
    graph.setdefault("bottleneck_audits", []).extend([
        {
            "kind": "routeb_true_dh_formal_bridge_contract",
            "status": "OPEN_FAIL_CLOSED",
            "evidence_level": "sidecar_contract_audit",
            "semantic_boundary": "Generic finite-dimensional Schur receipt contract; physical true-DH binding and full coverage remain open.",
            "sidecar": str(fw.resolve()),
            "files": [ref(p) for p in fw_files],
            "lean_compile_status": "blocked_missing_mathlib_search_path",
            "registry_promoted": False,
            "formal_certificate_allowed": False,
        },
        {
            "kind": "routeb_partition_receipt_contract",
            "status": "OPEN_FAIL_CLOSED",
            "evidence_level": "sidecar_schema_validator_audit",
            "semantic_boundary": "Deterministic 33^4 partition receipt contract and fail-closed validator design; no coverage data is asserted.",
            "sidecar": str(fx.resolve()),
            "files": [ref(p) for p in fx_files],
            "validator_status": "schema_and_narrow_validator_present",
            "registry_promoted": False,
            "formal_certificate_allowed": False,
        },
    ])
    graph.setdefault("external_intakes", []).extend([
        {
            "kind": "routeb_true_dh_formal_bridge_contract",
            "source": "local-routeb-formal-bridge-audit",
            "sidecar": str(fw.resolve()),
            "payload_sha256": sha(fw / "obligations.json"),
            "registry_promoted": False,
            "formal_certificate_allowed": False,
        },
        {
            "kind": "routeb_partition_receipt_contract",
            "source": "local-routeb-partition-contract-audit",
            "sidecar": str(fx.resolve()),
            "payload_sha256": sha(fx / "schema.json"),
            "registry_promoted": False,
            "formal_certificate_allowed": False,
        },
    ])
    graph.setdefault("open_frontier_updates", []).extend([
        {"node": "routeb_true_dh_formal_bridge_contract", "status": "open_fail_closed", "reason": "physical binding and Mathlib-pinned Lean compilation remain unresolved"},
        {"node": "routeb_partition_receipt_contract", "status": "open_fail_closed", "reason": "contract exists but complete cell receipts and coverage witnesses are absent"},
    ])
    graph.update(schema="routeb-proposed-proof-dag-v175", supersedes=old.name)
    new.write_text(json.dumps(graph, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if not backup.exists():
        backup.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(store.path, backup)

    digest = sha(new)
    state.graph_artifacts.append({
        "schema_version": 1,
        "algorithm": "routeb_batch_and_contract_improvements/v1",
        "graph_sha256": digest,
        "roots": [],
        "selected_nodes": [],
        "source": "reduction-batch-optimization plus FW/FX sidecars",
        "evidence_sha256": sha(code_files[0]),
        "registry_promoted": False,
        "formal_certificate_allowed": False,
    })
    state.event(
        "routeb_batch_and_contract_improvements_recorded",
        proposed_dag=ref(new),
        proposed_dag_sha256=digest,
        optimization=optimization,
        audits=["routeb_true_dh_formal_bridge_contract", "routeb_partition_receipt_contract"],
        registry_promoted=False,
        formal_certificate_allowed=False,
        broad_regression_run=False,
    )
    store.save(state)
    print({"revision": state.revision, "graph": new.name, "registry": len(state.registry)})


if __name__ == "__main__":
    main()
