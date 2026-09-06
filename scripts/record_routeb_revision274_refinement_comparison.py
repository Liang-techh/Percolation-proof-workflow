"""Persist q6/q2q3 refinement and CG enclosure comparison results."""
from __future__ import annotations

import hashlib
import json
import shutil
from pathlib import Path

from record_routeb_port_progress import ROOT, ref
from percolation_workflow.store import StateStore


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> None:
    store = StateStore(ROOT / "artifacts/routeb_6dof/state.json")
    state = store.load()
    assert state.revision == 273 and not state.registry
    old = ROOT / "artifacts/routeb_6dof/block45-obligations-v227.json"
    new = ROOT / "artifacts/routeb_6dof/block45-obligations-v228.json"
    backup = ROOT / "artifacts/routeb_storage_checkpoint_20260907/state-before-revision274.json"
    gda = ROOT / "artifacts/task_GDA_q6_refinement_block45_20260907"
    gdb = ROOT / "artifacts/task_GDB_q2q3_refinement_block45_20260907"
    gdc = ROOT / "artifacts/task_GDC_cg_enclosure_comparison_20260907"
    files = [gda / "REPORT.md", gda / "receipt.json", gda / "runtime.log", gda / "probe.jl", gda / "checker.py",
             gdb / "REPORT.md", gdb / "receipt.json", gdb / "runtime.log", gdb / "probe.jl", gdb / "checker.py",
             gdc / "REPORT.md", gdc / "receipt.json", gdc / "runtime.log", gdc / "probe.jl", gdc / "checker.py"]
    assert old.is_file() and not new.exists() and all(path.is_file() for path in files)
    da, db, dc = load(gda / "receipt.json"), load(gdb / "receipt.json"), load(gdc / "receipt.json")
    graph = load(old)
    q6 = {
        "kind": "routeb_q6_refinement_does_not_close_bracket",
        "status": da.get("status"), "evidence_level": "three-targeted-julia-runtimes",
        "sidecar": str(gda.resolve()), "files": [ref(path) for path in files[:5]],
        "q6_half_widths": da.get("q6_half_widths"), "results": da.get("results"),
        "inverse_guard_closed": True, "bracket_closed": False,
        "coverage_complete": False, "registry_promoted": False, "formal_certificate_allowed": False,
        "semantic_boundary": "q6 contraction barely changes the bracket; it does not close residual absorption or coverage.",
    }
    q2q3 = {
        "kind": "routeb_q2q3_refinement_bracket_remains_open",
        "status": db.get("status"), "evidence_level": "four-targeted-julia-runtimes",
        "sidecar": str(gdb.resolve()), "files": [ref(path) for path in files[5:10]],
        "probes": db.get("probes"), "inverse_guard_closed": True, "bracket_closed": False,
        "coverage_complete": False, "registry_promoted": False, "formal_certificate_allowed": False,
        "semantic_boundary": "q2/q3 shrinkage improves width but every tested h interval still crosses zero.",
    }
    cg = {
        "kind": "routeb_meanvalue_fd_closes_local_bracket_candidate",
        "status": dc.get("status"), "evidence_level": "two-mode-targeted-julia-runtime",
        "sidecar": str(gdc.resolve()), "files": [ref(path) for path in files[10:]],
        "results": dc.get("results"), "comparison": dc.get("comparison"),
        "local_candidate": "meanvalue_fd yields h_lo>0 on one fixed q1=1/64 cell",
        "coverage_complete": False, "registry_promoted": False, "formal_certificate_allowed": False,
        "semantic_boundary": "Local meanvalue_fd bracket candidate only; interval soundness, coverage, residual theorem and comparator remain open.",
    }
    graph.setdefault("bottleneck_audits", []).extend([q6, q2q3, cg])
    graph.setdefault("external_intakes", []).extend([
        {"kind": q6["kind"], "source": "canonical-runtime:GDA-q6-refinement", "sidecar": q6["sidecar"], "files": q6["files"], "registry_promoted": False, "formal_certificate_allowed": False},
        {"kind": q2q3["kind"], "source": "canonical-runtime:GDB-q2q3-refinement", "sidecar": q2q3["sidecar"], "files": q2q3["files"], "registry_promoted": False, "formal_certificate_allowed": False},
        {"kind": cg["kind"], "source": "canonical-runtime:GDC-cg-comparison", "sidecar": cg["sidecar"], "files": cg["files"], "registry_promoted": False, "formal_certificate_allowed": False},
    ])
    graph.setdefault("open_frontier_updates", []).extend([
        {"node": q6["kind"], "status": "q6_not_dominant_bracket_width_open", "reason": q6["semantic_boundary"]},
        {"node": q2q3["kind"], "status": "q2q3_improves_but_crosses_zero", "reason": q2q3["semantic_boundary"]},
        {"node": cg["kind"], "status": "meanvalue_fd_local_bracket_candidate_global_open", "reason": cg["semantic_boundary"]},
    ])
    graph.update(schema="routeb-proposed-proof-dag-v228", supersedes=old.name)
    new.write_text(json.dumps(graph, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if not backup.exists():
        backup.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(store.path, backup)
    digest = sha(new)
    state.graph_artifacts.append({
        "schema_version": 1, "algorithm": "routeb_revision274_refinement_comparison/v1",
        "graph_sha256": digest, "roots": [], "selected_nodes": [],
        "source": "canonical-runtimes:GDA-GDB-GDC", "evidence_sha256": sha(gdc / "receipt.json"),
        "strict_compile": False, "registry_promoted": False, "formal_certificate_allowed": False,
    })
    state.event("routeb_revision274_refinement_comparison_recorded",
                proposed_dag=ref(new), proposed_dag_sha256=digest,
                q6_bracket_closed=False, q2q3_bracket_closed=False,
                meanvalue_fd_local_bracket_candidate=True, global_coverage_closed=False,
                registry_promoted=False, formal_certificate_allowed=False, broad_regression_run=False)
    store.save(state)
    print(json.dumps({"revision": state.revision, "graph": new.name,
                      "q6_bracket_closed": False, "q2q3_bracket_closed": False,
                      "meanvalue_fd_local_candidate": True, "registry": len(state.registry)}))


if __name__ == "__main__":
    main()
