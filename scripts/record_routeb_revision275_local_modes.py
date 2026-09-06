"""Persist the targeted CG enclosure mode comparison without opening registry gates."""
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
    assert state.revision == 274 and not state.registry
    old = ROOT / "artifacts/routeb_6dof/block45-obligations-v228.json"
    new = ROOT / "artifacts/routeb_6dof/block45-obligations-v229.json"
    backup = ROOT / "artifacts/routeb_storage_checkpoint_20260907/state-before-revision275.json"
    side = ROOT / "artifacts/task_local_cg_modes_20260907"
    files = [side / "REPORT.md", side / "receipt.json", side / "probe.jl"]
    assert old.is_file() and not new.exists() and all(path.is_file() for path in files)
    receipt = json.loads((side / "receipt.json").read_text(encoding="utf-8"))
    graph = json.loads(old.read_text(encoding="utf-8"))
    audit = {
        "kind": "routeb_cg_mode_comparison_does_not_close_bracket",
        "status": "BOX_BRACKET_LOWER_NONNEGATIVE_FOR_ALL_NONNATURAL_MODES",
        "evidence_level": "single-cell-four-mode-targeted-julia-runtime",
        "sidecar": str(side.resolve()),
        "files": [ref(path) for path in files],
        "source_sha256": receipt["source_sha256"],
        "results": receipt["results"],
        "coverage_complete": False,
        "registry_promoted": False,
        "formal_certificate_allowed": False,
        "semantic_boundary": "Changing CG enclosure mode does not close the local h bracket; soundness and residual decomposition remain open.",
    }
    graph.setdefault("bottleneck_audits", []).append(audit)
    graph.setdefault("external_intakes", []).append({
        "kind": audit["kind"], "source": "targeted-runtime:local-cg-modes",
        "sidecar": audit["sidecar"], "files": audit["files"],
        "registry_promoted": False, "formal_certificate_allowed": False,
    })
    graph.setdefault("open_frontier_updates", []).append({
        "node": audit["kind"], "status": "cg_mode_not_a_closure", "reason": audit["semantic_boundary"]
    })
    graph.update(schema="routeb-proposed-proof-dag-v229", supersedes=old.name)
    new.write_text(json.dumps(graph, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if not backup.exists():
        backup.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(store.path, backup)
    digest = sha(new)
    state.graph_artifacts.append({
        "schema_version": 1, "algorithm": "routeb_revision275_local_cg_modes/v1",
        "graph_sha256": digest, "roots": [], "selected_nodes": [],
        "source": "targeted-runtime:local-cg-modes", "evidence_sha256": sha(side / "receipt.json"),
        "strict_compile": False, "registry_promoted": False, "formal_certificate_allowed": False,
    })
    state.event("routeb_revision275_local_cg_modes_recorded",
                proposed_dag=ref(new), proposed_dag_sha256=digest,
                natural_fd_open=True, meanvalue_fd_open=True,
                meanvalue_qdq_open=True, taylor2_fd_open=True,
                coverage_complete=False, registry_promoted=False,
                formal_certificate_allowed=False, broad_regression_run=False)
    store.save(state)
    print(json.dumps({"revision": state.revision, "graph": new.name, "registry": len(state.registry)}))


if __name__ == "__main__":
    main()
