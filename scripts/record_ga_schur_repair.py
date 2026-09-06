"""Append the successful GA Schur sidecar repair without promoting it."""
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
    assert state.revision == 223 and not state.registry
    old = ROOT / "artifacts/routeb_6dof/block45-obligations-v177.json"
    new = ROOT / "artifacts/routeb_6dof/block45-obligations-v178.json"
    backup = ROOT / "artifacts/routeb_storage_checkpoint_20260907/state-before-revision224.json"
    sidecar = ROOT / "artifacts/task_GA_schur_block_lean_20260907"
    olean = sidecar / ".lake/build/lib/lean/SchurBlockLowerBound.olean"
    names = [
        "SchurBlockLowerBound.lean", "compile_final_receipt.log", "axioms.txt",
        "REPORT.md", "provenance.md", "lakefile.toml", "lean-toolchain",
    ]
    files = [sidecar / name for name in names]
    assert old.is_file() and not new.exists() and olean.is_file() and all(path.is_file() for path in files)

    audit = {
        "kind": "routeb_schur_block_lean_repair",
        "status": "CURRENT_PIN_STRICT_COMPILE_PASS_CANDIDATE_ONLY",
        "evidence_level": "isolated_lean_kernel_compile",
        "semantic_boundary": "Generic finite-dimensional rational block inequality is compiled; physical DH binding, cell coverage, residual accounting, and parent admission remain open.",
        "sidecar": str(sidecar.resolve()),
        "files": [ref(path) for path in files],
        "olean": {"path": str(olean.resolve()), "sha256": sha(olean)},
        "lean_toolchain": "leanprover/lean4:v4.33.1",
        "strict_compile": True,
        "axioms": ["propext", "Classical.choice", "Quot.sound"],
        "registry_promoted": False,
        "formal_certificate_allowed": False,
    }
    graph = json.loads(old.read_text(encoding="utf-8"))
    graph.setdefault("bottleneck_audits", []).append(audit)
    graph.setdefault("external_intakes", []).append({
        "kind": audit["kind"], "source": "local-routeb-schur-repair",
        "sidecar": audit["sidecar"], "files": audit["files"], "olean": audit["olean"],
        "strict_compile": True, "registry_promoted": False, "formal_certificate_allowed": False,
    })
    graph.setdefault("open_frontier_updates", []).append({
        "node": audit["kind"], "status": "candidate_compile_pass_physical_bridge_open",
        "reason": audit["semantic_boundary"],
    })
    graph.update(schema="routeb-proposed-proof-dag-v178", supersedes=old.name)
    new.write_text(json.dumps(graph, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if not backup.exists():
        backup.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(store.path, backup)
    digest = sha(new)
    state.graph_artifacts.append({
        "schema_version": 1, "algorithm": "routeb_ga_schur_repair/v1",
        "graph_sha256": digest, "roots": [], "selected_nodes": [],
        "source": str(sidecar), "evidence_sha256": sha(sidecar / "compile_final_receipt.log"),
        "strict_compile": True, "registry_promoted": False, "formal_certificate_allowed": False,
    })
    state.event(
        "routeb_ga_schur_repair_recorded", proposed_dag=ref(new),
        proposed_dag_sha256=digest, sidecar=str(sidecar.resolve()),
        strict_compile=True, registry_promoted=False,
        formal_certificate_allowed=False, broad_regression_run=False,
    )
    store.save(state)
    print({"revision": state.revision, "graph": new.name, "registry": len(state.registry)})


if __name__ == "__main__":
    main()
