"""Record the exact-real 14-state ramp lift as a verified child candidate."""
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
    assert state.revision == 173 and not state.registry
    old_graph = ROOT / "artifacts/routeb_6dof/block45-obligations-v127.json"
    new_graph = ROOT / "artifacts/routeb_6dof/block45-obligations-v128.json"
    backup = ROOT / "artifacts/routeb_storage_checkpoint_20260906/state-before-revision174.json"
    assert old_graph.is_file() and not new_graph.exists()
    base = ROOT / "artifacts/routeb_agent_ramp_lift_20260906T170000Z"
    files = {name: base / name for name in ("RampLift.lean", "RampLift.olean", "README.md", "RECEIPT.md")}
    for path in files.values():
        assert path.is_file(), path
    export_base = ROOT / "artifacts/routeb_agent_s_d_export_contract_20260906T095120Z"
    export_files = {name: export_base / name for name in (
        "README.md", "contract.json", "manifest.template.json",
        "required_columns.csv", "AUDIT.md")}
    for path in export_files.values():
        assert path.is_file(), path
    graph = json.loads(old_graph.read_text(encoding="utf-8"))
    graph.setdefault("bottleneck_audits", []).append({
        "kind": "routeb_ramp_lift_exact_real",
        "status": "LEAN_COMPILED_CHILD_CANDIDATE",
        "evidence_level": "kernel_verified_exact_real_leaf",
        "semantic_boundary": "ODE existence, full flowpipe coverage, P3 entry and terminal transfer remain open",
        "registry_promoted": False,
        "formal_certificate_allowed": False,
        "files": {key: {"path": ref(path), "sha256": sha(path)} for key, path in files.items()},
    })
    graph.setdefault("open_frontier_updates", []).append({
        "node": "RouteBEntry.L1_ramp_lift",
        "status": "child_compiled_open_parent",
        "reason": "14-state ramp equations and projection are proved; flowpipe/entry/first-exit obligations remain open",
    })
    graph.setdefault("bottleneck_audits", []).append({
        "kind": "routeb_s_d_export_contract",
        "status": "FAIL_CLOSED_S_D_WITNESS_MISSING",
        "evidence_level": "source_export_contract",
        "semantic_boundary": "existing exports omit the jointly evaluated D-row residual and coverage witness",
        "registry_promoted": False,
        "formal_certificate_allowed": False,
        "files": {key: {"path": ref(path), "sha256": sha(path)} for key, path in export_files.items()},
    })
    graph["open_frontier_updates"].append({
        "node": "RouteBSchur.s_D_source_export",
        "status": "open",
        "reason": "next Julia run must export r_D, M_DB*a_B, M_DD*a_D, s_D, residual identities and cell coverage with hashes",
    })
    graph.update(schema="routeb-proposed-proof-dag-v128", supersedes=old_graph.name)
    new_graph.write_text(json.dumps(graph, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if not backup.exists():
        backup.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(store.path, backup)
    digest = sha(new_graph)
    state.graph_artifacts.append({
        "schema_version": 1,
        "algorithm": "routeb_ramp_lift/v1",
        "graph_sha256": digest,
        "roots": [], "selected_nodes": [],
        "source": "pinned Lean exact-real 14-state ramp lift",
        "source_sha256": sha(files["RampLift.lean"]),
        "olean_sha256": sha(files["RampLift.olean"]),
        "registry_promoted": False, "formal_certificate_allowed": False,
    })
    state.graph_artifacts.append({
        "schema_version": 1,
        "algorithm": "routeb_s_d_export_contract/v1",
        "graph_sha256": digest,
        "roots": [], "selected_nodes": [],
        "source": "fail-closed required export contract for correlated D-row residual",
        "contract_sha256": sha(export_files["contract.json"]),
        "registry_promoted": False, "formal_certificate_allowed": False,
    })
    state.event(
        "routeb_ramp_lift_recorded", proposed_dag=ref(new_graph),
        proposed_dag_sha256=digest, source=ref(files["RampLift.lean"]),
        source_sha256=sha(files["RampLift.lean"]), olean=ref(files["RampLift.olean"]),
        olean_sha256=sha(files["RampLift.olean"]), status="LEAN_COMPILED_CHILD_CANDIDATE",
        registry_promoted=False, formal_certificate_allowed=False, broad_regression_run=False,
    )
    store.save(state)
    print({"revision": state.revision, "graph": new_graph.name, "registry": len(state.registry)})


if __name__ == "__main__":
    main()
