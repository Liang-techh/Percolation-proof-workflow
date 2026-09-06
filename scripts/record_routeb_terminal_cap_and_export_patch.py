"""Record terminal-cap leaf and reviewable source-export patch."""
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
    assert state.revision == 180 and not state.registry
    old_graph = ROOT / "artifacts/routeb_6dof/block45-obligations-v134.json"
    new_graph = ROOT / "artifacts/routeb_6dof/block45-obligations-v135.json"
    backup = ROOT / "artifacts/routeb_storage_checkpoint_20260906/state-before-revision181.json"
    assert old_graph.is_file() and not new_graph.exists()
    cap = ROOT / "examples/routeb_terminal_cap_ae"
    cap_files = {name: cap / name for name in ("TerminalCapAE.lean", "verify.sh", "README.md")}
    patch = ROOT / "artifacts/routeb_agent_s_d_export_source_patch_20260906T101500Z"
    patch_files = {name: patch / name for name in (
        "README.md", "routeB_export_traj_sd_source_patch.jl", "routeB_export_traj.unified.diff")}
    for path in (*cap_files.values(), *patch_files.values()):
        assert path.is_file(), path
    graph = json.loads(old_graph.read_text(encoding="utf-8"))
    graph.setdefault("bottleneck_audits", []).append({
        "kind": "routeb_terminal_cap_exact_leaf",
        "status": "LEAN_COMPILED_TERMINAL_CAP_LEAF",
        "evidence_level": "kernel_verified_exact_real_storage_inequality",
        "semantic_boundary": "storage evolution, flowpipe coverage and source binding remain open",
        "conclusion": "p<=24/5 implies qpoly<=12; p<=28/5 only implies qpoly<=14",
        "registry_promoted": False, "formal_certificate_allowed": False,
        "files": {key: {"path": ref(path), "sha256": sha(path)} for key, path in cap_files.items()},
    })
    graph.setdefault("open_frontier_updates", []).append({
        "node": "RouteBEnergyTube.tight_terminal_cap",
        "status": "leaf_verified_parent_open",
        "reason": "exact cap lemma is compiled; no proof yet that all trajectories satisfy p<=24/5 or direct storage bound",
    })
    graph.setdefault("bottleneck_audits", []).append({
        "kind": "routeb_s_d_export_source_patch",
        "status": "REVIEWABLE_PATCH_NOT_APPLIED",
        "evidence_level": "static_source_patch_review",
        "semantic_boundary": "Julia unavailable; no actual CSV witness or coverage certificate exists",
        "coverage_certificate": False, "promotion_allowed": False,
        "registry_promoted": False, "formal_certificate_allowed": False,
        "files": {key: {"path": ref(path), "sha256": sha(path)} for key, path in patch_files.items()},
    })
    graph["open_frontier_updates"].append({
        "node": "RouteBSchur.apply_s_D_export_patch",
        "status": "patch_review_open",
        "reason": "reviewable insertion point found in gen_trajectories inner loop; patch not applied and Julia runtime unavailable",
    })
    graph.update(schema="routeb-proposed-proof-dag-v135", supersedes=old_graph.name)
    new_graph.write_text(json.dumps(graph, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if not backup.exists():
        backup.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(store.path, backup)
    digest = sha(new_graph)
    for algorithm, source, extra in (
        ("routeb_terminal_cap_exact_leaf/v1", cap_files["TerminalCapAE.lean"], {"source_sha256": sha(cap_files["TerminalCapAE.lean"])}),
        ("routeb_s_d_export_source_patch/v1", patch_files["routeB_export_traj.unified.diff"], {"patch_sha256": sha(patch_files["routeB_export_traj.unified.diff"])}),
    ):
        state.graph_artifacts.append({
            "schema_version": 1, "algorithm": algorithm, "graph_sha256": digest,
            "roots": [], "selected_nodes": [], "source": str(source), **extra,
            "registry_promoted": False, "formal_certificate_allowed": False,
        })
    state.event(
        "routeb_terminal_cap_and_export_patch_recorded", proposed_dag=ref(new_graph),
        proposed_dag_sha256=digest, terminal_cap=ref(cap_files["TerminalCapAE.lean"]),
        terminal_cap_sha256=sha(cap_files["TerminalCapAE.lean"]), export_patch=ref(patch_files["routeB_export_traj.unified.diff"]),
        export_patch_sha256=sha(patch_files["routeB_export_traj.unified.diff"]),
        registry_promoted=False, formal_certificate_allowed=False, broad_regression_run=False,
    )
    store.save(state)
    print({"revision": state.revision, "graph": new_graph.name, "registry": len(state.registry)})


if __name__ == "__main__":
    main()
