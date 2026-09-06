"""Record the ramp-to-cell interface while keeping coverage open."""
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
    assert state.revision == 175 and not state.registry
    old_graph = ROOT / "artifacts/routeb_6dof/block45-obligations-v129.json"
    new_graph = ROOT / "artifacts/routeb_6dof/block45-obligations-v130.json"
    backup = ROOT / "artifacts/routeb_storage_checkpoint_20260906/state-before-revision176.json"
    assert old_graph.is_file() and not new_graph.exists()
    base = ROOT / "artifacts/routeb_agent_ramp_cell_interface_20260906T035404Z"
    files = {name: base / name for name in (
        "ramp_cell_interface.json", "RampCellInterface.lean", "RampCellInterface.olean",
        "check_ramp_cell_interface.py", "verify.ps1", "README.md")}
    for path in files.values():
        assert path.is_file(), path
    graph = json.loads(old_graph.read_text(encoding="utf-8"))
    graph.setdefault("bottleneck_audits", []).append({
        "kind": "routeb_ramp_cell_interface",
        "status": "LEAN_COMPILED_INTERFACE_OPEN",
        "evidence_level": "kernel_verified_cell_interface",
        "semantic_boundary": "cell flowpipe coverage, entry/exit witnesses and terminal transfer remain open",
        "registry_promoted": False,
        "formal_certificate_allowed": False,
        "flowpipe_covered": False,
        "files": {key: {"path": ref(path), "sha256": sha(path)} for key, path in files.items()},
    })
    graph.setdefault("open_frontier_updates", []).append({
        "node": "RouteBEntry.cell_14state_interface",
        "status": "interface_compiled_parent_open",
        "reason": "three cell contracts type-check; no validated ODE flowpipe or entry/exit face witness is supplied",
    })
    graph.update(schema="routeb-proposed-proof-dag-v130", supersedes=old_graph.name)
    new_graph.write_text(json.dumps(graph, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if not backup.exists():
        backup.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(store.path, backup)
    digest = sha(new_graph)
    state.graph_artifacts.append({
        "schema_version": 1, "algorithm": "routeb_ramp_cell_interface/v1",
        "graph_sha256": digest, "roots": [], "selected_nodes": [],
        "source": "pinned Lean ramp-to-cell interface",
        "source_sha256": sha(files["RampCellInterface.lean"]),
        "olean_sha256": sha(files["RampCellInterface.olean"]),
        "flowpipe_covered": False, "registry_promoted": False,
        "formal_certificate_allowed": False,
    })
    state.event(
        "routeb_ramp_cell_interface_recorded", proposed_dag=ref(new_graph),
        proposed_dag_sha256=digest, source=ref(files["RampCellInterface.lean"]),
        source_sha256=sha(files["RampCellInterface.lean"]),
        olean=ref(files["RampCellInterface.olean"]),
        olean_sha256=sha(files["RampCellInterface.olean"]),
        status="LEAN_COMPILED_INTERFACE_OPEN", flowpipe_covered=False,
        registry_promoted=False, formal_certificate_allowed=False, broad_regression_run=False,
    )
    store.save(state)
    print({"revision": state.revision, "graph": new_graph.name, "registry": len(state.registry)})


if __name__ == "__main__":
    main()
