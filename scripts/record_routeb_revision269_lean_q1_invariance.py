"""Persist the pinned Lean q1 block-invariance candidate."""
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
    assert state.revision == 268 and not state.registry
    old = ROOT / "artifacts/routeb_6dof/block45-obligations-v222.json"
    new = ROOT / "artifacts/routeb_6dof/block45-obligations-v223.json"
    backup = ROOT / "artifacts/routeb_storage_checkpoint_20260907/state-before-revision269.json"
    sidecar = ROOT / "artifacts/task_GCR_lean_q1_invariance_candidate_20260907"
    files = [sidecar / "REPORT.md", sidecar / "receipt.json", sidecar / "Q1MassInvarianceCandidate.lean",
             sidecar / "compile_strict.log", sidecar / "checker.py"]
    assert old.is_file() and not new.exists() and all(path.is_file() for path in files)
    receipt = json.loads((sidecar / "receipt.json").read_text(encoding="utf-8"))
    graph = json.loads(old.read_text(encoding="utf-8"))
    audit = {
        "kind": "routeb_lean_q1_block_invariance_candidate",
        "status": receipt.get("status"),
        "evidence_level": "pinned-zero-sorry-lean-candidate",
        "sidecar": str(sidecar.resolve()), "files": [ref(path) for path in files],
        "theorems": receipt.get("candidate", {}).get("theorems", []),
        "strict_compile": receipt.get("strict_compile"),
        "toolchain": receipt.get("toolchain"),
        "proved_boundary": receipt.get("proved", []),
        "unclosed_boundaries": receipt.get("unclosed_boundaries", []),
        "source_semantics_formalized": False,
        "coverage_complete": False, "registry_promoted": False,
        "formal_certificate_allowed": False,
        "semantic_boundary": "Abstract q1-invariance premise only; canonical Julia DH semantics and interval soundness remain unbound.",
    }
    graph.setdefault("bottleneck_audits", []).append(audit)
    graph.setdefault("external_intakes", []).append({
        "kind": audit["kind"], "source": "independent-sidecar:GCR-lean-q1-invariance",
        "sidecar": audit["sidecar"], "files": audit["files"],
        "registry_promoted": False, "formal_certificate_allowed": False,
    })
    graph.setdefault("open_frontier_updates", []).append({
        "node": audit["kind"], "status": "abstract_invariance_compiled_source_binding_open",
        "reason": audit["semantic_boundary"],
    })
    graph.update(schema="routeb-proposed-proof-dag-v223", supersedes=old.name)
    new.write_text(json.dumps(graph, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if not backup.exists():
        backup.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(store.path, backup)
    digest = sha(new)
    state.graph_artifacts.append({
        "schema_version": 1, "algorithm": "routeb_revision269_lean_q1_invariance/v1",
        "graph_sha256": digest, "roots": [], "selected_nodes": [],
        "source": "independent-sidecar:GCR-lean-q1-invariance",
        "evidence_sha256": sha(sidecar / "receipt.json"), "strict_compile": True,
        "registry_promoted": False, "formal_certificate_allowed": False,
    })
    state.event("routeb_revision269_lean_q1_invariance_recorded",
                proposed_dag=ref(new), proposed_dag_sha256=digest,
                theorem_count=len(audit["theorems"]), strict_compile=True,
                source_semantics_formalized=False, interval_soundness_closed=False,
                registry_promoted=False, formal_certificate_allowed=False,
                broad_regression_run=False)
    store.save(state)
    print(json.dumps({"revision": state.revision, "graph": new.name,
                      "theorem_count": len(audit["theorems"]), "registry": len(state.registry)}))


if __name__ == "__main__":
    main()
