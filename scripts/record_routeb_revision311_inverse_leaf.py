"""Record the conditional gauge-fixed finite-matrix inverse leaf."""
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
    if state.revision != 310 or state.registry:
        raise ValueError("revision-311 recorder requires revision 310 and empty registry")
    side = ROOT / "artifacts/task_routeb_inverse_bottleneck_current"
    report = ROOT / "artifacts/task_routeb_revision311_inverse_leaf/REPORT.md"
    checker = side / "check_gauge_leaf.py"
    result = side / "CHECK_RESULT.json"
    if not all(p.is_file() for p in (report, checker, result)):
        raise ValueError("missing revision-311 evidence")
    check = json.loads(result.read_text(encoding="utf-8"))
    exact = check.get("exact_rational_weakening", {})
    if (check.get("status") != "PASS_CONDITIONAL_CURRENT_CANONICAL_MASS_LEAF"
            or not check.get("leaf_closed")
            or exact.get("kappa_upper") != "103/1000"
            or exact.get("inverse_weighted_norm_upper") != "64000/897"
            or exact.get("M_BD_infinity_norm_upper") != "3/25"
            or exact.get("Schur_euclidean_coercivity_lower") != "37/1000"):
        raise ValueError("inverse leaf checker did not pass")
    old = ROOT / "artifacts/routeb_6dof/block45-obligations-v264.json"
    new = ROOT / "artifacts/routeb_6dof/block45-obligations-v265.json"
    source_sha = check.get("canonical_source_sha256")
    record = {
        "kind": "routeb_gauge_fixed_inverse_schur_leaf",
        "status": "PASS_CONDITIONAL_FINITE_MATRIX_LEAF_SOURCE_MEMBERSHIP_OPEN",
        "evidence_level": "current-source-hashed-julia-plus-exact-fraction-replay",
        "files": [ref(report), ref(checker), ref(result)],
        "domain": check.get("domain"),
        "canonical_interval_source_sha256": source_sha,
        "exact_rational_weakening": exact,
        "q1_gauge_transport_assumed": True,
        "physical_source_interval_membership_closed": False,
        "global_coverage_closed": False,
        "bracket_closed": False,
        "registry_promoted": False,
        "formal_certificate_allowed": False,
    }
    graph = json.loads(old.read_text(encoding="utf-8"))
    graph.setdefault("bottleneck_audits", []).append(record)
    graph.setdefault("workflow_hardening", []).append(record)
    graph.setdefault("open_frontier_updates", []).append({
        "node": "B45-5_gauge_fixed_inverse_schur_leaf",
        "status": "conditional_mass_inverse_schur_leaf_closed",
        "reason": "q1 gauge-fixed exact Fraction replay closes finite-matrix arithmetic; source interval membership and RHS/acceleration remain open.",
    })
    graph.update(schema="routeb-proposed-proof-dag-v265", supersedes=old.name)
    new.write_text(json.dumps(graph, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    checkpoint = ROOT / "artifacts/routeb_storage_checkpoint_20260908/state-before-revision311.json"
    if not checkpoint.exists():
        checkpoint.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(store.path, checkpoint)
    graph_sha = sha(new)
    state.graph_artifacts.append({
        "schema_version": 1,
        "algorithm": "routeb_revision311_inverse_leaf/v1",
        "graph_sha256": graph_sha,
        "roots": [], "selected_nodes": [],
        "evidence_sha256": sha(report),
        "checker_sha256": sha(checker),
        "checker_result_sha256": sha(result),
        "canonical_interval_source_sha256": source_sha,
        "conditional_inverse_schur_leaf": True,
        "physical_source_interval_membership_closed": False,
        "dynamics_coverage_complete": False,
        "registry_promoted": False,
        "formal_certificate_allowed": False,
    })
    state.event(
        "routeb_revision311_inverse_leaf_recorded",
        proposed_dag=ref(new), proposed_dag_sha256=graph_sha,
        kappa_upper="103/1000", inverse_weighted_norm_upper="64000/897",
        M_BD_infinity_norm_upper="3/25", Schur_euclidean_coercivity_lower="37/1000",
        q1_gauge_transport_assumed=True, physical_source_interval_membership_closed=False,
        dynamics_coverage_complete=False, registry_promoted=False,
        formal_certificate_allowed=False, broad_regression_run=False,
    )
    store.save(state)
    print(json.dumps({"revision": state.revision, "graph": new.name,
                      "registry": len(state.registry), "formal_certificate_allowed": False}))


if __name__ == "__main__":
    main()
