"""Record the core D-row source bridge as conditional evidence."""
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
    assert state.revision == 172 and not state.registry
    old_graph = ROOT / "artifacts/routeb_6dof/block45-obligations-v126.json"
    new_graph = ROOT / "artifacts/routeb_6dof/block45-obligations-v127.json"
    backup = ROOT / "artifacts/routeb_storage_checkpoint_20260906/state-before-revision173.json"
    assert old_graph.is_file() and not new_graph.exists()
    base = ROOT / "artifacts/routeb_agent_s_d_source_bridge_20260906T160000Z"
    files = {
        "report": base / "AUDIT.md",
        "source": base / "SDSourceBridge.lean",
        "receipt": base / "COMPILE_RECEIPT.md",
        "verifier": base / "verify.ps1",
        "checker": base / "audit_checker.py",
        "checker_output": base / "checker_output.json",
        "csv_semantic_audit": base / "CSV_SEMANTIC_AUDIT.csv",
        "source_index_audit": base / "SOURCE_INDEX_AUDIT.csv",
        "compile_log": base / "lean_compile.log",
    }
    comparator = ROOT / "artifacts/routeb_agent_source_comparator_20260906T181500Z"
    comparator_files = {
        "comparator": comparator / "compare.py",
        "comparator_result": comparator / "result.json",
        "comparator_readme": comparator / "README.md",
    }
    files.update(comparator_files)
    for path in files.values():
        assert path.is_file(), path
    graph = json.loads(old_graph.read_text(encoding="utf-8"))
    graph.setdefault("bottleneck_audits", []).append({
        "kind": "routeb_s_d_source_bridge",
        "status": "LEAN_COMPILED_CONDITIONAL",
        "evidence_level": "core_exact_real_drow_identity",
        "semantic_boundary": "source residual envelope and deployment binding remain open",
        "registry_promoted": False,
        "formal_certificate_allowed": False,
        "files": {key: {"path": ref(path), "sha256": sha(path)} for key, path in files.items()},
    })
    graph.setdefault("bottleneck_audits", []).append({
        "kind": "routeb_source_statement_comparator",
        "status": "FAIL_CLOSED_MISMATCH",
        "evidence_level": "source_comparator_audit",
        "semantic_boundary": "conditional Lean bridge is not statement-equivalent to deployed source",
        "registry_promoted": False,
        "formal_certificate_allowed": False,
        "files": {key: {"path": ref(path), "sha256": sha(path)} for key, path in comparator_files.items()},
    })
    graph.setdefault("open_frontier_updates", []).append({
        "node": "RouteBSchur.drow_correlated_force_envelope",
        "status": "open",
        "reason": "s_D identity compiled; source-exported r_D and rigorous global s_D envelope are still absent",
    })
    graph["open_frontier_updates"].append({
        "node": "RouteBP4.source_statement_comparator",
        "status": "open",
        "reason": "M0[5,5], central-FD h, l45, D_elim_c, six-dimensional domain and coverage premises mismatch",
    })
    graph.update(schema="routeb-proposed-proof-dag-v127", supersedes=old_graph.name)
    new_graph.write_text(json.dumps(graph, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if not backup.exists():
        backup.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(store.path, backup)
    digest = sha(new_graph)
    state.graph_artifacts.append({
        "schema_version": 1,
        "algorithm": "routeb_s_d_source_bridge/v1",
        "graph_sha256": digest,
        "roots": [],
        "selected_nodes": [],
        "source": "core exact-real D-row identity with source-export audit",
        "source_sha256": sha(files["source"]),
        "registry_promoted": False,
        "formal_certificate_allowed": False,
    })
    state.event(
        "routeb_s_d_source_bridge_recorded",
        proposed_dag=ref(new_graph), proposed_dag_sha256=digest,
        source=ref(files["source"]), source_sha256=sha(files["source"]),
        receipt=ref(files["receipt"]), receipt_sha256=sha(files["receipt"]),
        status="LEAN_COMPILED_CONDITIONAL", registry_promoted=False,
        formal_certificate_allowed=False, broad_regression_run=False,
    )
    store.save(state)
    print({"revision": state.revision, "graph": new_graph.name, "registry": len(state.registry)})


if __name__ == "__main__":
    main()
