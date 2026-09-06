"""Record the portable P4 verifier refresh without changing theorem status."""
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
    assert state.revision == 174 and not state.registry
    old_graph = ROOT / "artifacts/routeb_6dof/block45-obligations-v128.json"
    new_graph = ROOT / "artifacts/routeb_6dof/block45-obligations-v129.json"
    backup = ROOT / "artifacts/routeb_storage_checkpoint_20260906/state-before-revision175.json"
    assert old_graph.is_file() and not new_graph.exists()
    base = ROOT / "artifacts/routeb_agent_p4_source_bridge_next_20260906T092639Z"
    semantic = ROOT / "artifacts/routeb_agent_p4_semantic_contract_20260906T100000Z"
    files = {
        "verifier": base / "verify.ps1",
        "compile_log": base / "run-pinned/compile.log",
        "verify_log": base / "run-pinned/verify.log",
        "source_olean": base / "run-pinned/SourceToP4Bridge.olean",
        "p4_olean": base / "run-pinned/P4InterfacePMI.olean",
        "semantic_checker": semantic / "semantic_contract_checker.py",
        "semantic_output": semantic / "checker_output.json",
    }
    for path in files.values():
        assert path.is_file(), path
    graph = json.loads(old_graph.read_text(encoding="utf-8"))
    graph.setdefault("bottleneck_audits", []).append({
        "kind": "routeb_p4_verifier_portability_refresh",
        "status": "PINNED_REPLAY_PASS_CONDITIONAL",
        "evidence_level": "replay_freshness",
        "semantic_boundary": "portable replay does not supply DH/Float64/source equivalence or coverage",
        "registry_promoted": False,
        "formal_certificate_allowed": False,
        "working_directories": ["workflow_root", "source_bridge_artifact"],
        "files": {key: {"path": ref(path), "sha256": sha(path)} for key, path in files.items()},
    })
    graph.setdefault("open_frontier_updates", []).append({
        "node": "RouteBP4.verifier_replay_portability",
        "status": "replay_fixed_parent_open",
        "reason": "pinned replay is portable and passes; physical source bridge, comparator, coverage and terminal premises remain open",
    })
    graph.update(schema="routeb-proposed-proof-dag-v129", supersedes=old_graph.name)
    new_graph.write_text(json.dumps(graph, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if not backup.exists():
        backup.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(store.path, backup)
    digest = sha(new_graph)
    state.graph_artifacts.append({
        "schema_version": 1,
        "algorithm": "routeb_p4_verifier_refresh/v1",
        "graph_sha256": digest,
        "roots": [], "selected_nodes": [],
        "source": "portable pinned verifier and semantic checker replay",
        "verifier_sha256": sha(files["verifier"]),
        "registry_promoted": False, "formal_certificate_allowed": False,
    })
    state.event(
        "routeb_p4_verifier_refresh_recorded", proposed_dag=ref(new_graph),
        proposed_dag_sha256=digest, verifier=ref(files["verifier"]),
        verifier_sha256=sha(files["verifier"]), verify_log=ref(files["verify_log"]),
        verify_log_sha256=sha(files["verify_log"]), status="PINNED_REPLAY_PASS_CONDITIONAL",
        registry_promoted=False, formal_certificate_allowed=False, broad_regression_run=False,
    )
    store.save(state)
    print({"revision": state.revision, "graph": new_graph.name, "registry": len(state.registry)})


if __name__ == "__main__":
    main()
