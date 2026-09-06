"""Record the exact terminal-transfer contract and its open premises."""
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
    assert state.revision == 177 and not state.registry
    old_graph = ROOT / "artifacts/routeb_6dof/block45-obligations-v131.json"
    new_graph = ROOT / "artifacts/routeb_6dof/block45-obligations-v132.json"
    backup = ROOT / "artifacts/routeb_storage_checkpoint_20260906/state-before-revision178.json"
    assert old_graph.is_file() and not new_graph.exists()
    base = ROOT / "artifacts/routeb_agent_terminal_transfer_contract_20260906T100050Z"
    files = {name: base / name for name in (
        "REPORT.md", "RouteBTerminalTransferContract.lean", "verify.sh")}
    for path in files.values():
        assert path.is_file(), path
    graph = json.loads(old_graph.read_text(encoding="utf-8"))
    graph.setdefault("bottleneck_audits", []).append({
        "kind": "routeb_terminal_transfer_contract",
        "status": "LEAN_COMPILED_CONDITIONAL_TERMINAL_GATE",
        "evidence_level": "kernel_verified_prefix_tube_reduction",
        "semantic_boundary": "prefix flowpipe, domain coverage, deployed dynamics and uniform residual budget remain open",
        "tube_cap_counterexample": "p<=28/5 implies only qpoly<=14; target qpoly<=12 needs p<=24/5 or a direct storage comparison",
        "registry_promoted": False, "formal_certificate_allowed": False,
        "files": {key: {"path": ref(path), "sha256": sha(path)} for key, path in files.items()},
    })
    graph.setdefault("open_frontier_updates", []).append({
        "node": "RouteBEnergyTube.prefix_to_terminal_transfer",
        "status": "conditional_gate_parent_open",
        "reason": "exact PrefixTube/TubeInside reduction compiles; current domain cap is too weak and full-X0 flowpipe premise is absent",
    })
    graph.update(schema="routeb-proposed-proof-dag-v132", supersedes=old_graph.name)
    new_graph.write_text(json.dumps(graph, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if not backup.exists():
        backup.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(store.path, backup)
    digest = sha(new_graph)
    state.graph_artifacts.append({
        "schema_version": 1, "algorithm": "routeb_terminal_transfer_contract/v1",
        "graph_sha256": digest, "roots": [], "selected_nodes": [],
        "source": "pinned Lean exact-real prefix-tube terminal reduction",
        "source_sha256": sha(files["RouteBTerminalTransferContract.lean"]),
        "registry_promoted": False, "formal_certificate_allowed": False,
    })
    state.event(
        "routeb_terminal_transfer_contract_recorded", proposed_dag=ref(new_graph),
        proposed_dag_sha256=digest, source=ref(files["RouteBTerminalTransferContract.lean"]),
        source_sha256=sha(files["RouteBTerminalTransferContract.lean"]),
        status="LEAN_COMPILED_CONDITIONAL_TERMINAL_GATE", registry_promoted=False,
        formal_certificate_allowed=False, broad_regression_run=False,
    )
    store.save(state)
    print({"revision": state.revision, "graph": new_graph.name, "registry": len(state.registry)})


if __name__ == "__main__":
    main()
