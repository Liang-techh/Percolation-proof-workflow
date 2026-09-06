"""Record the explicit P4 constant/residual-map repair as conditional evidence."""
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
    assert state.revision == 176 and not state.registry
    old_graph = ROOT / "artifacts/routeb_6dof/block45-obligations-v130.json"
    new_graph = ROOT / "artifacts/routeb_6dof/block45-obligations-v131.json"
    backup = ROOT / "artifacts/routeb_storage_checkpoint_20260906/state-before-revision177.json"
    assert old_graph.is_file() and not new_graph.exists()
    base = ROOT / "artifacts/routeb_agent_p4_repair_constants_20260906T095405Z"
    files = {name: base / name for name in (
        "P4RepairConstants.lean", "compare.py", "result.json", "README.md",
        "verify.ps1", "lean-toolchain")}
    for path in files.values():
        assert path.is_file(), path
    result = json.loads(files["result.json"].read_text(encoding="utf-8"))
    assert result["status"] == "PASS" and not result["mismatch_fields"]
    condition_base = ROOT / "artifacts/routeb_agent_p4_condition_instantiation_20260906T103000Z"
    condition_files = {name: condition_base / name for name in (
        "RouteBP4ConditionInstantiation.lean", "ConditionBridgeClosure.lean", "RECEIPT.md",
        "axiom_check.log", "compile.log", "static_scan.log", "README.md")}
    rational_base = ROOT / "artifacts/routeb_agent_p3_rational_reencode_20260906T100500Z"
    rational_files = {name: rational_base / name for name in (
        "REPORT.md", "directed_snapshot.json", "rational_evidence.json",
        "replay_rational.py", "check_rational.py", "source_coefficients.json")}
    for path in (*condition_files.values(), *rational_files.values()):
        assert path.is_file(), path
    graph = json.loads(old_graph.read_text(encoding="utf-8"))
    graph.setdefault("bottleneck_audits", []).append({
        "kind": "routeb_p4_explicit_constants_repair",
        "status": "LEAN_COMPILED_COMPARATOR_PASS_CONDITIONAL",
        "evidence_level": "exact_real_source_surface_repair",
        "semantic_boundary": "DH semantics, coverage, Float64 rounding, SOS/Gram and terminal transfer remain open",
        "formal_claim": False, "dh_proved": False, "coverage_proved": False,
        "registry_promoted": False, "formal_certificate_allowed": False,
        "files": {key: {"path": ref(path), "sha256": sha(path)} for key, path in files.items()},
    })
    graph.setdefault("open_frontier_updates", []).append({
        "node": "RouteBP4.explicit_source_constant_surface",
        "status": "repair_pass_parent_open",
        "reason": "M0 block, FD step and residual map are explicit; DH/source equivalence and coverage remain absent",
    })
    graph.setdefault("bottleneck_audits", []).append({
        "kind": "routeb_p4_condition_instantiation",
        "status": "LEAN_COMPILED_CONDITIONAL",
        "evidence_level": "kernel_verified_condition_residual_goal_instance",
        "semantic_boundary": "descriptor, D-row and Float64 snapshot bindings are explicit placeholders",
        "registry_promoted": False, "formal_certificate_allowed": False,
        "files": {key: {"path": ref(path), "sha256": sha(path)} for key, path in condition_files.items()},
    })
    graph.setdefault("open_frontier_updates", []).append({
        "node": "RouteBP4.condition_residual_goal_instance",
        "status": "compiled_conditional_parent_open",
        "reason": "condition-to-residual-to-goal reduction compiles; descriptor/DH/Float64/coverage premises remain placeholders",
    })
    graph.setdefault("bottleneck_audits", []).append({
        "kind": "routeb_p3_exact_rational_endpoint_reencode",
        "status": "RATIONAL_LOCAL_CANDIDATE_GLOBAL_OPEN",
        "evidence_level": "exact_rational_outer_endpoint_reencode",
        "semantic_boundary": "Julia trigonometric and central-FD source semantics are not replaced by a pure rational proof",
        "registry_promoted": False, "formal_certificate_allowed": False,
        "files": {key: {"path": ref(path), "sha256": sha(path)} for key, path in rational_files.items()},
    })
    graph.setdefault("open_frontier_updates", []).append({
        "node": "RouteBP3.local_rational_endpoint_bridge",
        "status": "local_positive_global_open",
        "reason": "rational endpoints certify only the existing one-cell enclosure; source-level semantics and X0 flowpipe coverage remain open",
    })
    graph.update(schema="routeb-proposed-proof-dag-v131", supersedes=old_graph.name)
    new_graph.write_text(json.dumps(graph, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if not backup.exists():
        backup.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(store.path, backup)
    digest = sha(new_graph)
    state.graph_artifacts.append({
        "schema_version": 1, "algorithm": "routeb_p4_explicit_constants_repair/v1",
        "graph_sha256": digest, "roots": [], "selected_nodes": [],
        "source": "pinned Lean explicit deployed constant/residual surface",
        "source_sha256": sha(files["P4RepairConstants.lean"]),
        "result_sha256": sha(files["result.json"]),
        "registry_promoted": False, "formal_certificate_allowed": False,
    })
    state.graph_artifacts.append({
        "schema_version": 1, "algorithm": "routeb_p4_condition_instantiation/v1",
        "graph_sha256": digest, "roots": [], "selected_nodes": [],
        "source": "pinned Lean condition-residual-goal instance",
        "source_sha256": sha(condition_files["RouteBP4ConditionInstantiation.lean"]),
        "registry_promoted": False, "formal_certificate_allowed": False,
    })
    state.graph_artifacts.append({
        "schema_version": 1, "algorithm": "routeb_p3_rational_endpoint_reencode/v1",
        "graph_sha256": digest, "roots": [], "selected_nodes": [],
        "source": "exact rational outer endpoint replay of local P3 enclosure",
        "evidence_sha256": sha(rational_files["rational_evidence.json"]),
        "registry_promoted": False, "formal_certificate_allowed": False,
    })
    state.event(
        "routeb_p4_explicit_constants_repair_recorded", proposed_dag=ref(new_graph),
        proposed_dag_sha256=digest, source=ref(files["P4RepairConstants.lean"]),
        source_sha256=sha(files["P4RepairConstants.lean"]), result=ref(files["result.json"]),
        result_sha256=sha(files["result.json"]), status="LEAN_COMPILED_COMPARATOR_PASS_CONDITIONAL",
        formal_claim=False, dh_proved=False, coverage_proved=False,
        registry_promoted=False, formal_certificate_allowed=False, broad_regression_run=False,
    )
    store.save(state)
    print({"revision": state.revision, "graph": new_graph.name, "registry": len(state.registry)})


if __name__ == "__main__":
    main()
