"""Record the D-elimination coefficient/Gram witness gap."""
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
    assert state.revision == 183 and not state.registry
    old_graph = ROOT / "artifacts/routeb_6dof/block45-obligations-v137.json"
    new_graph = ROOT / "artifacts/routeb_6dof/block45-obligations-v138.json"
    backup = ROOT / "artifacts/routeb_storage_checkpoint_20260906/state-before-revision184.json"
    assert old_graph.is_file() and not new_graph.exists()
    base = ROOT / "artifacts/routeb_agent_p4_delim_c_binding_20260906T041523Z"
    files = {name: base / name for name in ("P4DElimCBinding.lean", "compare.py", "result.json")}
    for path in files.values():
        assert path.is_file(), path
    result = json.loads(files["result.json"].read_text(encoding="utf-8"))
    assert result["status"] == "PASS_EXPLICIT_BINDING_WITH_COEFFICIENT_GAP"
    graph = json.loads(old_graph.read_text(encoding="utf-8"))
    graph.setdefault("bottleneck_audits", []).append({
        "kind": "routeb_p4_d_elim_coefficient_binding",
        "status": "PASS_EXPLICIT_BINDING_WITH_COEFFICIENT_GAP",
        "evidence_level": "kernel_verified_symbolic_binding",
        "semantic_boundary": "runtime SOS coefficients and verified Gram witness are not exported or reified",
        "registry_promoted": False, "formal_certificate_allowed": False,
        "files": {key: {"path": ref(path), "sha256": sha(path)} for key, path in files.items()},
    })
    graph.setdefault("open_frontier_updates", []).append({
        "node": "RouteBP4.D_elim_c_coefficient_reification",
        "status": "binding_pass_coefficient_gap_open",
        "reason": "D0/c1/c2/D_elim_c symbolic binding compiles; concrete SOS coefficient export and exact Gram verification are absent",
    })
    graph.update(schema="routeb-proposed-proof-dag-v138", supersedes=old_graph.name)
    new_graph.write_text(json.dumps(graph, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if not backup.exists():
        backup.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(store.path, backup)
    digest = sha(new_graph)
    state.graph_artifacts.append({
        "schema_version": 1, "algorithm": "routeb_p4_delim_coefficient_binding/v1",
        "graph_sha256": digest, "roots": [], "selected_nodes": [],
        "source": "symbolic D-elimination binding with coefficient/Gram gap",
        "source_sha256": sha(files["P4DElimCBinding.lean"]),
        "result_sha256": sha(files["result.json"]), "registry_promoted": False,
        "formal_certificate_allowed": False,
    })
    state.event(
        "routeb_p4_delim_coefficient_binding_recorded", proposed_dag=ref(new_graph),
        proposed_dag_sha256=digest, source=ref(files["P4DElimCBinding.lean"]),
        source_sha256=sha(files["P4DElimCBinding.lean"]), result=ref(files["result.json"]),
        result_sha256=sha(files["result.json"]), status="PASS_EXPLICIT_BINDING_WITH_COEFFICIENT_GAP",
        registry_promoted=False, formal_certificate_allowed=False, broad_regression_run=False,
    )
    store.save(state)
    print({"revision": state.revision, "graph": new_graph.name, "registry": len(state.registry)})


if __name__ == "__main__":
    main()
