"""Record terminal reduction and P3 source-seam sidecars."""
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
    assert state.revision == 178 and not state.registry
    old_graph = ROOT / "artifacts/routeb_6dof/block45-obligations-v132.json"
    new_graph = ROOT / "artifacts/routeb_6dof/block45-obligations-v133.json"
    backup = ROOT / "artifacts/routeb_storage_checkpoint_20260906/state-before-revision179.json"
    assert old_graph.is_file() and not new_graph.exists()
    terminal = ROOT / "artifacts/routeb_agent_terminal_reduction_leaf_20260906T100457Z"
    p3 = ROOT / "artifacts/routeb_agent_p3_source_interval_seam_20260906T100431Z"
    terminal_files = {name: terminal / name for name in (
        "LEAF.md", "OBLIGATIONS.md", "README.md", "RECEIPT.md", "SOURCES.md",
        "exact_prefix_to_terminal.py")}
    p3_files = {name: p3 / name for name in (
        "REPORT.md", "seam_ledger.json", "check_seam.py", "manifest.json")}
    p4_next = ROOT / "artifacts/routeb_agent_p4_next_semantic_repair_20260906T100414Z"
    p4_files = {name: p4_next / name for name in (
        "L45Repair.lean", "compare.py", "result.json", "README.md", "verify.ps1", "lean-toolchain")}
    export_plan = ROOT / "artifacts/routeb_agent_s_d_export_implementation_plan_20260906T100446Z"
    export_files = {name: export_plan / name for name in (
        "README.md", "column_schema.json", "export_interface_draft.jl",
        "manifest.template.json", "required_columns.csv", "SHA256SUMS.csv", "source_inventory.json")}
    entry_map = ROOT / "artifacts/routeb_agent_entry_dag_mapping_20260906T110000Z"
    entry_files = {name: entry_map / name for name in (
        "REPORT.md", "proposed_patch.json", "check_dependency_closure.py")}
    for path in (*terminal_files.values(), *p3_files.values(), *p4_files.values(), *export_files.values(), *entry_files.values()):
        assert path.is_file(), path
    graph = json.loads(old_graph.read_text(encoding="utf-8"))
    graph.setdefault("bottleneck_audits", []).append({
        "kind": "routeb_terminal_reduction_leaf",
        "status": "EXACT_REAL_PREFIX_TO_TERMINAL_REDUCTION",
        "evidence_level": "exact_real_leaf_with_explicit_premises",
        "semantic_boundary": "full flowpipe, deployed source binding, nonlinear remainder and coverage remain placeholders",
        "registry_promoted": False, "formal_certificate_allowed": False,
        "files": {key: {"path": ref(path), "sha256": sha(path)} for key, path in terminal_files.items()},
    })
    graph.setdefault("open_frontier_updates", []).append({
        "node": "RouteBEnergyTube.terminal_scalar_reduction_leaf",
        "status": "leaf_verified_parent_open",
        "reason": "exact prefix-to-terminal scalar gate compiles; PrefixTube and uniform deployed budget premises are absent",
    })
    graph.setdefault("bottleneck_audits", []).append({
        "kind": "routeb_p3_source_interval_seam",
        "status": "LOCAL_ATOMIC_TAYLOR_REMAINDER_POSSIBLE_SOURCE_OPEN",
        "evidence_level": "exact_rational_atomic_remainder_audit",
        "semantic_boundary": "DH chain derivatives, Float64 trig enclosure, q plus/minus h traces and C/G binding remain open",
        "registry_promoted": False, "formal_certificate_allowed": False,
        "files": {key: {"path": ref(path), "sha256": sha(path)} for key, path in p3_files.items()},
    })
    graph["open_frontier_updates"].append({
        "node": "RouteBP3.source_trig_fd_interval_bridge",
        "status": "atomic_remainder_open",
        "reason": "sin/cos and h^2/6 factors have rational remainders; full deployed DH/Float64/FD semantics remain unbound",
    })
    graph.setdefault("bottleneck_audits", []).append({
        "kind": "routeb_p4_l45_semantic_repair",
        "status": "LEAN_COMPILED_COMPARATOR_PASS_CONDITIONAL",
        "evidence_level": "exact_real_residual_binding_repair",
        "semantic_boundary": "D_elim_c, six-dimensional domain and coverage remain open",
        "registry_promoted": False, "formal_certificate_allowed": False,
        "files": {key: {"path": ref(path), "sha256": sha(path)} for key, path in p4_files.items()},
    })
    graph["open_frontier_updates"].append({
        "node": "RouteBP4.l45_source_residual_binding",
        "status": "repair_pass_parent_open",
        "reason": "l45 source/Lean binding matches; D_elim_c, domain and coverage contracts remain unresolved",
    })
    graph.setdefault("bottleneck_audits", []).append({
        "kind": "routeb_s_d_export_implementation_plan",
        "status": "EXPORT_SCHEMA_READY_WITNESS_MISSING",
        "evidence_level": "static_source_export_plan",
        "semantic_boundary": "no Julia execution or actual s_D witness was produced",
        "registry_promoted": False, "formal_certificate_allowed": False,
        "files": {key: {"path": ref(path), "sha256": sha(path)} for key, path in export_files.items()},
    })
    graph["open_frontier_updates"].append({
        "node": "RouteBSchur.s_D_export_implementation",
        "status": "schema_ready_witness_open",
        "reason": "23 field groups are specified; next run must emit jointly evaluated residual rows and coverage hashes",
    })
    graph.setdefault("bottleneck_audits", []).append({
        "kind": "routeb_entry_dag_mapping",
        "status": "PROPOSED_CHILD_MAPPING_OPEN",
        "evidence_level": "dag_mapping_audit",
        "semantic_boundary": "7 L0-L6 child proposals are not yet installed as verified theorem nodes",
        "registry_promoted": False, "formal_certificate_allowed": False,
        "files": {key: {"path": ref(path), "sha256": sha(path)} for key, path in entry_files.items()},
    })
    graph["open_frontier_updates"].append({
        "node": "RouteBEntry.L0_to_L6_child_mapping",
        "status": "proposal_open",
        "reason": "7 deterministic acyclic child IDs cover L0-L6; source witnesses and actual parent closure remain open",
    })
    graph.update(schema="routeb-proposed-proof-dag-v133", supersedes=old_graph.name)
    new_graph.write_text(json.dumps(graph, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if not backup.exists():
        backup.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(store.path, backup)
    digest = sha(new_graph)
    for algorithm, source, extra in (
        ("routeb_terminal_reduction_leaf/v1", terminal_files["LEAF.md"], {"receipt_sha256": sha(terminal_files["RECEIPT.md"])}),
        ("routeb_p3_source_interval_seam/v1", p3_files["seam_ledger.json"], {"ledger_sha256": sha(p3_files["seam_ledger.json"])}),
        ("routeb_p4_l45_semantic_repair/v1", p4_files["L45Repair.lean"], {"result_sha256": sha(p4_files["result.json"])}),
        ("routeb_s_d_export_implementation_plan/v1", export_files["column_schema.json"], {"schema_sha256": sha(export_files["column_schema.json"])}),
        ("routeb_entry_dag_mapping/v1", entry_files["proposed_patch.json"], {"proposal_sha256": sha(entry_files["proposed_patch.json"])}),
    ):
        state.graph_artifacts.append({
            "schema_version": 1, "algorithm": algorithm, "graph_sha256": digest,
            "roots": [], "selected_nodes": [], "source": str(source), **extra,
            "registry_promoted": False, "formal_certificate_allowed": False,
        })
    state.event(
        "routeb_terminal_and_p3_seams_recorded", proposed_dag=ref(new_graph),
        proposed_dag_sha256=digest, terminal_leaf=ref(terminal_files["LEAF.md"]),
        terminal_leaf_sha256=sha(terminal_files["LEAF.md"]), p3_seam=ref(p3_files["REPORT.md"]),
        p3_seam_sha256=sha(p3_files["REPORT.md"]), registry_promoted=False,
        formal_certificate_allowed=False, broad_regression_run=False,
    )
    store.save(state)
    print({"revision": state.revision, "graph": new_graph.name, "registry": len(state.registry)})


if __name__ == "__main__":
    main()
