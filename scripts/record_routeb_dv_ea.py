"""Record DV-EA progress, including bounded repair-loop integration."""
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
    assert state.revision == 206 and not state.registry
    old = ROOT / "artifacts/routeb_6dof/block45-obligations-v160.json"
    new = ROOT / "artifacts/routeb_6dof/block45-obligations-v161.json"
    backup = ROOT / "artifacts/routeb_storage_checkpoint_20260907/state-before-revision207.json"
    assert old.is_file() and not new.exists()
    audits = [
        ("routeb_physical_a_receipt_search", "OPEN_MISSING_DATA", "no qualified same-domain physical a>mu, rho_phys or outward receipt found", ev("artifacts/task_DV_physical_a_receipt_search_20260907/REPORT.md")),
        ("routeb_cell16_indexed_child_contract", "OPEN_INDEXED_CHILD_CONTRACT_ONLY", "33^4 child address space and sparse receipt checks are defined without coverage claim", ev("artifacts/task_DW_cell16_indexed_child_contract_20260907/REPORT.md", "artifacts/task_DW_cell16_indexed_child_contract_20260907/ledger.json", "artifacts/task_DW_cell16_indexed_child_contract_20260907/checker.py")),
        ("routeb_p3_explicit_evaluator_receipt", "DISTINCT_STATEMENT_FAIL_CLOSED", "Taylor evaluator is not interchangeable with Julia/libm runtime expression", ev("artifacts/task_DX_p3_explicit_evaluator_receipt_20260907/README.md", "artifacts/task_DX_p3_explicit_evaluator_receipt_20260907/receipt.json", "artifacts/task_DX_p3_explicit_evaluator_receipt_20260907/check.py")),
        ("routeb_p4_static_parse_receipt", "OPEN_RUNTIME_PARSE", "static and metadata gates pass; Julia unavailable on PATH", ev("artifacts/task_DY_p4_static_parse_receipt_20260907/STATIC_PARSE_READINESS_RECEIPT.md")),
        ("routeb_repair_loop_disjoint_integration", "INTEGRATED_BOUNDED_REPAIR_RECEIPT", "build_repair_do and audit_do are emitted in repair_requested without changing admission/registry", ev("artifacts/task_DZ_repair_loop_disjoint_integration_20260907/REPORT.md", "src/percolation_workflow/disjoint.py", "src/percolation_workflow/repair.py", "src/percolation_workflow/__init__.py", "tests/test_disjoint.py", "tests/test_workflow.py")),
        ("routeb_anthropic_reuse_boundary", "QUOTIENT_PASS_SPECTRAL_OPEN_COMPILE", "generic quotient/continuous-linear adapter is reusable; spectral duplicate remains Mathlib-resolution open", ev("artifacts/task_EA_anthropic_mathlib_reuse_boundary_20260907/REPORT.md", "artifacts/task_EA_anthropic_mathlib_reuse_boundary_20260907/PROVENANCE.md", "artifacts/task_EA_anthropic_mathlib_reuse_boundary_20260907/HASHES.txt")),
    ]
    graph = json.loads(old.read_text(encoding="utf-8"))
    for kind, status, reason, evidence in audits:
        graph.setdefault("bottleneck_audits", []).append({"kind": kind, "status": status, "evidence_level": "bounded_math_or_core_repair_integration", "semantic_boundary": reason, "registry_promoted": False, "formal_certificate_allowed": False, "files": {k: {"path": ref(v), "sha256": sha(v)} for k, v in evidence.items()}})
        graph.setdefault("open_frontier_updates", []).append({"node": kind, "status": status.lower(), "reason": reason})
    graph.update(schema="routeb-proposed-proof-dag-v161", supersedes=old.name)
    new.write_text(json.dumps(graph, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if not backup.exists():
        backup.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(store.path, backup)
    digest = sha(new)
    for kind, _status, _reason, evidence in audits:
        first = next(iter(evidence.values()))
        state.graph_artifacts.append({"schema_version": 1, "algorithm": kind + "/v1", "graph_sha256": digest, "roots": [], "selected_nodes": [], "source": str(first), "evidence_sha256": sha(first), "registry_promoted": False, "formal_certificate_allowed": False})
    state.event("routeb_dv_ea_recorded", proposed_dag=ref(new), proposed_dag_sha256=digest, audits=[x[0] for x in audits], registry_promoted=False, formal_certificate_allowed=False, broad_regression_run=False)
    store.save(state)
    print({"revision": state.revision, "graph": new.name, "registry": len(state.registry)})


if __name__ == "__main__":
    main()
