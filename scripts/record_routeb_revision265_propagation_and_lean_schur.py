"""Persist q1 inheritance frontier and the next pinned Lean Schur candidate."""
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
    assert state.revision == 264 and not state.registry
    old = ROOT / "artifacts/routeb_6dof/block45-obligations-v218.json"
    new = ROOT / "artifacts/routeb_6dof/block45-obligations-v219.json"
    backup = ROOT / "artifacts/routeb_storage_checkpoint_20260907/state-before-revision265.json"
    gcn = ROOT / "artifacts/task_GCN_q1_propagation_frontier_20260907"
    gcl = ROOT / "artifacts/task_GCL_lean_schur_next_20260907"
    files = [gcn / "REPORT.md", gcn / "receipt.json", gcn / "checker.py",
             gcl / "REPORT.md", gcl / "receipt.json", gcl / "SchurBlockIdentity.lean",
             gcl / "compile_strict.log", gcl / "checker.py"]
    assert old.is_file() and not new.exists() and all(path.is_file() for path in files)
    gcn_receipt = json.loads((gcn / "receipt.json").read_text(encoding="utf-8"))
    gcl_receipt = json.loads((gcl / "receipt.json").read_text(encoding="utf-8"))
    graph = json.loads(old.read_text(encoding="utf-8"))
    propagation = {
        "kind": "routeb_q1_nested_guard_inheritance_frontier",
        "status": gcn_receipt.get("status"),
        "evidence_level": "static-subset-inheritance-audit",
        "sidecar": str(gcn.resolve()), "files": [ref(path) for path in files[:3]],
        "nested_subcells_inheriting_parent_guard": len(gcn_receipt.get("reusable_q1_subcells", [])),
        "adjacent_translations_certified": 0,
        "open_frontier": gcn_receipt.get("open_frontier", []),
        "coverage_complete": False, "registry_promoted": False,
        "formal_certificate_allowed": False,
        "semantic_boundary": gcn_receipt.get("interpretation_boundary"),
    }
    lean = {
        "kind": "routeb_pinned_lean_schur_identity_candidate",
        "status": gcl_receipt.get("status"),
        "evidence_level": "current-pin-zero-sorry-candidate",
        "sidecar": str(gcl.resolve()), "files": [ref(path) for path in files[3:]],
        "theorems": gcl_receipt.get("candidate", {}).get("theorems", []),
        "strict_compile": gcl_receipt.get("strict_compile"),
        "reported_axioms": gcl_receipt.get("strict_compile", {}).get("reported_axioms", []),
        "reuse_boundary": gcl_receipt.get("reuse_boundary"),
        "registry_promoted": False, "formal_certificate_allowed": False,
        "semantic_boundary": "Abstract identity only; physical ell=MBD*aD binding, interval Schur residual, coverage and comparator remain open.",
    }
    graph.setdefault("bottleneck_audits", []).extend([propagation, lean])
    graph.setdefault("external_intakes", []).extend([
        {"kind": propagation["kind"], "source": "independent-sidecar:GCN-q1-propagation",
         "sidecar": propagation["sidecar"], "files": propagation["files"],
         "registry_promoted": False, "formal_certificate_allowed": False},
        {"kind": lean["kind"], "source": "independent-sidecar:GCL-lean-schur-next",
         "sidecar": lean["sidecar"], "files": lean["files"],
         "registry_promoted": False, "formal_certificate_allowed": False},
    ])
    graph.setdefault("open_frontier_updates", []).extend([
        {"node": propagation["kind"], "status": "nested_core_only_adjacent_open",
         "reason": propagation["semantic_boundary"]},
        {"node": lean["kind"], "status": "abstract_candidate_physical_binding_open",
         "reason": lean["semantic_boundary"]},
    ])
    graph.update(schema="routeb-proposed-proof-dag-v219", supersedes=old.name)
    new.write_text(json.dumps(graph, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if not backup.exists():
        backup.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(store.path, backup)
    digest = sha(new)
    state.graph_artifacts.append({
        "schema_version": 1, "algorithm": "routeb_revision265_propagation_and_lean_schur/v1",
        "graph_sha256": digest, "roots": [], "selected_nodes": [],
        "source": "independent-sidecars:GCN-plus-GCL",
        "evidence_sha256": sha(gcl / "receipt.json"), "strict_compile": True,
        "registry_promoted": False, "formal_certificate_allowed": False,
    })
    state.event("routeb_revision265_propagation_and_lean_schur_recorded",
                proposed_dag=ref(new), proposed_dag_sha256=digest,
                nested_guard_subcells=propagation["nested_subcells_inheriting_parent_guard"],
                adjacent_cells_certified=0, lean_candidate_count=len(lean["theorems"]),
                physical_binding_closed=False, registry_promoted=False,
                formal_certificate_allowed=False, broad_regression_run=False)
    store.save(state)
    print(json.dumps({"revision": state.revision, "graph": new.name,
                      "nested_guard_subcells": propagation["nested_subcells_inheriting_parent_guard"],
                      "lean_candidates": len(lean["theorems"]), "registry": len(state.registry)}))


if __name__ == "__main__":
    main()
