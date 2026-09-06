"""Record the failed GZ matrix-Schur compile without discarding the idea."""
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
    assert state.revision == 226 and not state.registry
    old = ROOT / "artifacts/routeb_6dof/block45-obligations-v180.json"
    new = ROOT / "artifacts/routeb_6dof/block45-obligations-v181.json"
    backup = ROOT / "artifacts/routeb_storage_checkpoint_20260907/state-before-revision227.json"
    sidecar = ROOT / "artifacts/task_GZ_matrix_schur_lean_20260907"
    names = ["MatrixSchur.lean", "compile_strict.log", "compile_result.log", "compile_strict_lean4331.log", "STATUS.md", "lakefile.toml", "lean-toolchain"]
    files = [sidecar / name for name in names]
    assert old.is_file() and not new.exists() and all(path.is_file() for path in files)
    audit = {
        "kind": "routeb_matrix_schur_lean_failure",
        "status": "OPEN_FAIL_CLOSED",
        "evidence_level": "failed_isolated_lean_compile",
        "semantic_boundary": "A stronger explicit matrix 2+4 Schur candidate was not compiled because the current pinned Mathlib cache/olean build failed with access errors; no theorem admission is claimed.",
        "sidecar": str(sidecar.resolve()),
        "files": [ref(path) for path in files],
        "failure_class": "pinned_mathlib_cache_permission_or_incompatible_olean",
        "valid_olean": False,
        "registry_promoted": False,
        "formal_certificate_allowed": False,
    }
    graph = json.loads(old.read_text(encoding="utf-8"))
    graph.setdefault("bottleneck_audits", []).append(audit)
    graph.setdefault("external_intakes", []).append({
        "kind": audit["kind"], "source": "local-routeb-matrix-schur-failure",
        "sidecar": audit["sidecar"], "files": audit["files"],
        "valid_olean": False, "registry_promoted": False, "formal_certificate_allowed": False,
    })
    graph.setdefault("open_frontier_updates", []).append({
        "node": audit["kind"], "status": "open_fail_closed", "reason": audit["semantic_boundary"],
    })
    graph.update(schema="routeb-proposed-proof-dag-v181", supersedes=old.name)
    new.write_text(json.dumps(graph, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if not backup.exists():
        backup.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(store.path, backup)
    digest = sha(new)
    state.graph_artifacts.append({
        "schema_version": 1, "algorithm": "routeb_gz_matrix_schur_failure/v1",
        "graph_sha256": digest, "roots": [], "selected_nodes": [],
        "source": str(sidecar), "evidence_sha256": sha(sidecar / "STATUS.md"),
        "valid_olean": False, "registry_promoted": False, "formal_certificate_allowed": False,
    })
    state.event(
        "routeb_gz_matrix_schur_failure_recorded", proposed_dag=ref(new),
        proposed_dag_sha256=digest, sidecar=str(sidecar.resolve()),
        failure_class=audit["failure_class"], valid_olean=False,
        registry_promoted=False, formal_certificate_allowed=False,
        broad_regression_run=False,
    )
    store.save(state)
    print({"revision": state.revision, "graph": new.name, "registry": len(state.registry)})


if __name__ == "__main__":
    main()
