"""Record the BZ-CE batch and preserve fail-closed admission semantics."""
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
    assert state.revision == 196 and not state.registry
    old = ROOT / "artifacts/routeb_6dof/block45-obligations-v150.json"
    new = ROOT / "artifacts/routeb_6dof/block45-obligations-v151.json"
    backup = ROOT / "artifacts/routeb_storage_checkpoint_20260906/state-before-revision197.json"
    assert old.is_file() and not new.exists()
    audits = [
        ("routeb_p3_binary64_binding", "FAIL_CLOSED_BINARY64_SOURCE_OPEN", "q1-q4 are not authenticated exact binary64 rationals; libm and central-FD remain open", ev("artifacts/task_BZ_p3_binary64_binding_20260906/REPORT.md", "artifacts/task_BZ_p3_binary64_binding_20260906/binding_report.json", "artifacts/task_BZ_p3_binary64_binding_20260906/check_binary64_binding.py")),
        ("routeb_picard_flowpipe_contract", "SCHEMA_READY_CERTIFICATE_DATA_OPEN", "finite-step Picard inclusion and continuation schema exists without numeric RHS receipts", ev("artifacts/task_CA_flowpipe_picard_contract_20260906/README.md", "artifacts/task_CA_flowpipe_picard_contract_20260906/picard_flowpipe_schema.json", "artifacts/task_CA_flowpipe_picard_contract_20260906/check_picard_flowpipe_contract.py")),
        ("routeb_p4_hook_semantic_review", "PATCH_REVIEWED_FAIL_CLOSED", "nine pmi_block call families are accounted for; Float64 remains numerical-only", ev("artifacts/task_CB_p4_hook_semantic_review_20260906/README.md", "artifacts/task_CB_p4_hook_semantic_review_20260906/routeB_p4_hook_semantic_refinement.diff", "artifacts/task_CB_p4_hook_semantic_review_20260906/check_p4_hook_semantic_refinement.py")),
        ("routeb_schur_physical_bridge_contract", "BLOCKED_PHYSICAL_RECEIPTS_OPEN", "physical positivity, block bounds, rho and outward-rounded coverage are missing", ev("artifacts/task_CC_schur_physical_bridge_contract_20260906/CONTRACT.md", "artifacts/task_CC_schur_physical_bridge_contract_20260906/contract.json", "artifacts/task_CC_schur_physical_bridge_contract_20260906/check_contract.py")),
        ("routeb_registry_gate_integration", "ADMISSION_BYPASS_FIXED_FAIL_CLOSED", "decomposition and child admission require comparator context; conditional evidence cannot enter registry", ev("artifacts/task_CD_registry_gate_integration_20260906/REPORT.md", "artifacts/task_CD_registry_gate_integration_20260906/check_registry_gate_integration.py", "src/percolation_workflow/decomposition.py")),
        ("routeb_anthropic_quotient_continuous_linear_equiv", "LEAN_COMPILED_ADAPTER_NOT_ROUTE_CERTIFICATE", "generic quotient/continuous-linear transport adapter compiles at pinned Lean; physical obligations remain explicit", ev("artifacts/task_CE_anthropic_adapter_reuse_20260906/INTAKE_REPORT.md", "artifacts/task_CE_anthropic_adapter_reuse_20260906/PROVENANCE.md", "artifacts/task_CE_anthropic_adapter_reuse_20260906/RouteBQuotientContinuousLinearEquiv.lean")),
    ]
    graph = json.loads(old.read_text(encoding="utf-8"))
    for kind, status, reason, evidence in audits:
        graph.setdefault("bottleneck_audits", []).append({"kind": kind, "status": status, "evidence_level": "bounded_sidecar_or_pinned_adapter", "semantic_boundary": reason, "registry_promoted": False, "formal_certificate_allowed": False, "files": {k: {"path": ref(v), "sha256": sha(v)} for k, v in evidence.items()}})
        graph.setdefault("open_frontier_updates", []).append({"node": kind, "status": status.lower(), "reason": reason})
    graph.update(schema="routeb-proposed-proof-dag-v151", supersedes=old.name)
    new.write_text(json.dumps(graph, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if not backup.exists():
        backup.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(store.path, backup)
    digest = sha(new)
    for kind, _status, _reason, evidence in audits:
        first = next(iter(evidence.values()))
        state.graph_artifacts.append({"schema_version": 1, "algorithm": kind + "/v1", "graph_sha256": digest, "roots": [], "selected_nodes": [], "source": str(first), "evidence_sha256": sha(first), "registry_promoted": False, "formal_certificate_allowed": False})
    state.event("routeb_bz_ce_recorded", proposed_dag=ref(new), proposed_dag_sha256=digest, audits=[x[0] for x in audits], registry_promoted=False, formal_certificate_allowed=False, broad_regression_run=False)
    store.save(state)
    print({"revision": state.revision, "graph": new.name, "registry": len(state.registry)})


if __name__ == "__main__":
    main()
