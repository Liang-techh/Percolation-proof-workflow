"""Record the strictly compiled abstract Route-B finite-sum adapter."""
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
    if state.revision != 326 or state.registry:
        raise ValueError("revision-327 recorder requires revision 326 and empty registry")
    side = ROOT / "artifacts/task_routeb_lean_reuse_leaf_current"
    source, report, compile_log = (side / n for n in
        ("RouteBFiniteAggregationAdapterProposal.lean", "ADAPTER_PROPOSAL.md", "compile.log"))
    out_report = ROOT / "artifacts/task_routeb_revision327_lean_adapter/REPORT.md"
    if not all(p.is_file() for p in (source, report, compile_log, out_report)):
        raise ValueError("missing Lean adapter evidence")
    text = source.read_text(encoding="utf-8")
    log = compile_log.read_text(encoding="utf-8")
    if ("theorem aggregate_body_interval" not in text
            or "RouteBFiniteAggregationLeaf.sum_mem h_body" not in text
            or "error:" in log.lower()):
        raise ValueError("Lean adapter source or compile evidence is invalid")

    old = ROOT / "artifacts/routeb_6dof/block45-obligations-v280.json"
    new = ROOT / "artifacts/routeb_6dof/block45-obligations-v281.json"
    graph = json.loads(old.read_text(encoding="utf-8"))
    record = {
        "kind": "routeb_lean_finite_aggregation_adapter",
        "status": "PASS_ABSTRACT_ONLY_NOT_REGISTRY_PROMOTED",
        "evidence_level": "pinned-lean-zero-error-adapter-application",
        "files": [ref(out_report), ref(report), ref(source), ref(compile_log)],
        "lean_toolchain": "leanprover/lean4:v4.33.1",
        "warning_as_error": True,
        "compile_exit_code": 0,
        "child_theorem": "RouteBFiniteAggregationAdapterProposal.aggregate_body_interval",
        "source_premise_binding": False,
        "registry_promoted": False,
        "formal_certificate_allowed": False,
    }
    graph.setdefault("bottleneck_audits", []).append(record)
    graph.setdefault("workflow_hardening", []).append(record)
    graph.setdefault("open_frontier_updates", []).append({
        "node": "B45-1_source_mass_table_exact",
        "status": "abstract_adapter_compiled_source_body_premise_open",
        "reason": "Fin 6 aggregation child compiles under the pinned Lean environment; actual body interval premises remain source-binding obligations",
        "evidence": ref(source),
    })
    graph.update(schema="routeb-proposed-proof-dag-v281", supersedes=old.name)
    new.write_text(json.dumps(graph, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    checkpoint = ROOT / "artifacts/routeb_storage_checkpoint_20260908/state-before-revision327.json"
    if not checkpoint.exists():
        checkpoint.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(store.path, checkpoint)
    graph_sha = sha(new)
    state.graph_artifacts.append({
        "schema_version": 1,
        "algorithm": "routeb_revision327_lean_adapter/v1",
        "graph_sha256": graph_sha, "roots": [], "selected_nodes": [],
        "evidence_sha256": sha(out_report), "source_sha256": sha(source),
        "compile_log_sha256": sha(compile_log), "compile_exit_code": 0,
        "abstract_only": True, "registry_promoted": False,
        "formal_certificate_allowed": False,
    })
    state.event(
        "routeb_revision327_lean_adapter_recorded",
        proposed_dag=ref(new), proposed_dag_sha256=graph_sha,
        child_theorem="RouteBFiniteAggregationAdapterProposal.aggregate_body_interval",
        lean_toolchain="leanprover/lean4:v4.33.1", compile_exit_code=0,
        abstract_only=True, source_premise_binding=False,
        registry_promoted=False, formal_certificate_allowed=False,
        broad_regression_run=False,
    )
    store.save(state)
    print(json.dumps({"revision": state.revision, "graph": new.name,
                      "registry": len(state.registry),
                      "formal_certificate_allowed": False}))


if __name__ == "__main__":
    main()
