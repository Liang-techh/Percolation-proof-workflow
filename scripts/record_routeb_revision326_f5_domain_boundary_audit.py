"""Record the fail-closed F5/domain-boundary audit."""
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
    if state.revision != 325 or state.registry:
        raise ValueError("revision-326 recorder requires revision 325 and empty registry")
    side = ROOT / "artifacts/task_routeb_aligned_cover_f5_domain_boundary_audit_current"
    report, checker, result = (side / n for n in ("REPORT.md", "checker.py", "CHECK_RESULT.json"))
    out_report = ROOT / "artifacts/task_routeb_revision326_f5_domain_boundary_audit/REPORT.md"
    if not all(p.is_file() for p in (report, checker, result, out_report)):
        raise ValueError("missing F5/domain-boundary evidence")
    check = json.loads(result.read_text(encoding="utf-8"))
    obligations = check.get("obligations", {})
    aligned = check.get("verified", {}).get("aligned_root_containment", {})
    boundary = obligations.get("domain_boundary", {})
    if (check.get("coverage_complete") is not False
            or check.get("registry_promoted") is not False
            or not aligned.get("all_coordinate_square_bounds_pass")
            or boundary.get("status") != "OPEN"
            or boundary.get("unknown_domain_boundary_leaf_count") != 3):
        raise ValueError("F5 audit boundary drifted")
    old = ROOT / "artifacts/routeb_6dof/block45-obligations-v279.json"
    new = ROOT / "artifacts/routeb_6dof/block45-obligations-v280.json"
    graph = json.loads(old.read_text(encoding="utf-8"))
    record = {
        "kind": "routeb_f5_aligned_cover_domain_boundary_audit",
        "status": "PASS_ROOT_CONTAINMENT_F5_OPEN",
        "evidence_level": "targeted-aligned-root-and-boundary-audit",
        "files": [ref(out_report), ref(report), ref(checker), ref(result)],
        "eta_exact": aligned["eta_exact"],
        "proof_weights": aligned["proof_weights"],
        "aligned_root_containment": True,
        "unknown_domain_boundary_leaf_count": 3,
        "coverage_complete": False,
        "first_exit_closed": False,
        "registry_promoted": False,
        "formal_certificate_allowed": False,
    }
    graph.setdefault("bottleneck_audits", []).append(record)
    graph.setdefault("workflow_hardening", []).append(record)
    graph.setdefault("open_frontier_updates", []).append({
        "node": "GCN-F5-aligned-cover-domain-boundary",
        "status": "root_geometry_closed_dynamics_boundary_open",
        "reason": "aligned root containment passes, but three UNKNOWN_DOMAIN_BOUNDARY leaves still lack source-faithful trajectory and face accounting",
        "evidence": ref(result),
    })
    graph.update(schema="routeb-proposed-proof-dag-v280", supersedes=old.name)
    new.write_text(json.dumps(graph, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    checkpoint = ROOT / "artifacts/routeb_storage_checkpoint_20260908/state-before-revision326.json"
    if not checkpoint.exists():
        checkpoint.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(store.path, checkpoint)
    graph_sha = sha(new)
    state.graph_artifacts.append({
        "schema_version": 1,
        "algorithm": "routeb_revision326_f5_domain_boundary_audit/v1",
        "graph_sha256": graph_sha, "roots": [], "selected_nodes": [],
        "evidence_sha256": sha(out_report), "checker_sha256": sha(checker),
        "result_sha256": sha(result), "aligned_root_containment": True,
        "coverage_complete": False, "unknown_domain_boundary_leaf_count": 3,
        "registry_promoted": False, "formal_certificate_allowed": False,
    })
    state.event(
        "routeb_revision326_f5_domain_boundary_audit_recorded",
        proposed_dag=ref(new), proposed_dag_sha256=graph_sha,
        aligned_root_containment=True, eta_exact=aligned["eta_exact"],
        unknown_domain_boundary_leaf_count=3, coverage_complete=False,
        first_exit_closed=False, registry_promoted=False,
        formal_certificate_allowed=False, broad_regression_run=False,
    )
    store.save(state)
    print(json.dumps({"revision": state.revision, "graph": new.name,
                      "registry": len(state.registry),
                      "formal_certificate_allowed": False}))


if __name__ == "__main__":
    main()
