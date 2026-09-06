"""Record the CL-CQ bounded source and workflow improvements."""
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
    assert state.revision == 198 and not state.registry
    old = ROOT / "artifacts/routeb_6dof/block45-obligations-v152.json"
    new = ROOT / "artifacts/routeb_6dof/block45-obligations-v153.json"
    backup = ROOT / "artifacts/routeb_storage_checkpoint_20260906/state-before-revision199.json"
    assert old.is_file() and not new.exists()
    audits = [
        ("routeb_p3_libm_interval_receipt", "NO_CERTIFIED_LIBM_PROOF_AVAILABLE", "P3 source receipt binds BZ/CG/BS hashes but no certified Julia libm interval", ev("artifacts/task_CL_p3_libm_interval_receipt_20260906/README.md", "artifacts/task_CL_p3_libm_interval_receipt_20260906/receipt.json")),
        ("routeb_schur_mass_source_extraction", "SOURCE_AVAILABLE_SYMBOLIC_ENTRIES", "all 16 M_DD(q) symbolic entries and source ranges are authenticated; d_N evaluation remains open", ev("artifacts/task_CM_schur_mass_source_extraction_20260906/REPORT.md")),
        ("routeb_p4_export_apply_plan", "RECOVERABLE_APPLY_PLAN_ONLY", "11 callsite edits and preimage/rollback requirements are planned but unapplied", ev("artifacts/task_CN_p4_export_apply_plan_20260906/PLAN.md")),
        ("routeb_picard_interval_inclusion", "SCHEMA_READY_CERTIFICATE_DATA_OPEN", "initial/step/continuation/terminal inclusion obligations are explicit without numeric endpoints", ev("artifacts/task_CO_picard_interval_inclusion_20260906/README.md", "artifacts/task_CO_picard_interval_inclusion_20260906/ca_ci_picard_extension.json", "artifacts/task_CO_picard_interval_inclusion_20260906/check_extension.py")),
        ("routeb_frontier_receipt_projection", "READ_ONLY_FRONTIER_RECEIPT", "lane, blocker, evidence hash and priority are exposed without changing formal admission", ev("src/percolation_workflow/math_frontier.py", "src/percolation_workflow/__init__.py", "tests/test_frontier_receipt_projection.py", "artifacts/task_CP_frontier_persistence_20260906/REPORT.md")),
        ("routeb_anthropic_transport_compile_receipt", "PINNED_LEAN_COMPILE_RECEIPT", "Anthropic quotient/continuous-linear adapter source hash and compile command are recorded without build caches", ev("artifacts/task_CQ_anthropic_transport_compile_20260906/PROVENANCE.md", "artifacts/task_CQ_anthropic_transport_compile_20260906/COMPILE_RECEIPT.json", "artifacts/task_CQ_anthropic_transport_compile_20260906/README.md")),
    ]
    graph = json.loads(old.read_text(encoding="utf-8"))
    for kind, status, reason, evidence in audits:
        graph.setdefault("bottleneck_audits", []).append({"kind": kind, "status": status, "evidence_level": "bounded_source_receipt_or_workflow_integration", "semantic_boundary": reason, "registry_promoted": False, "formal_certificate_allowed": False, "files": {k: {"path": ref(v), "sha256": sha(v)} for k, v in evidence.items()}})
        graph.setdefault("open_frontier_updates", []).append({"node": kind, "status": status.lower(), "reason": reason})
    graph.update(schema="routeb-proposed-proof-dag-v153", supersedes=old.name)
    new.write_text(json.dumps(graph, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if not backup.exists():
        backup.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(store.path, backup)
    digest = sha(new)
    for kind, _status, _reason, evidence in audits:
        first = next(iter(evidence.values()))
        state.graph_artifacts.append({"schema_version": 1, "algorithm": kind + "/v1", "graph_sha256": digest, "roots": [], "selected_nodes": [], "source": str(first), "evidence_sha256": sha(first), "registry_promoted": False, "formal_certificate_allowed": False})
    state.event("routeb_cl_cq_recorded", proposed_dag=ref(new), proposed_dag_sha256=digest, audits=[x[0] for x in audits], registry_promoted=False, formal_certificate_allowed=False, broad_regression_run=False)
    store.save(state)
    print({"revision": state.revision, "graph": new.name, "registry": len(state.registry)})


if __name__ == "__main__":
    main()
