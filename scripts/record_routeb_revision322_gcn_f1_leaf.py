"""Record the conditional exact-rational GCN-F1 leaf."""
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
    if state.revision != 321 or state.registry:
        raise ValueError("revision-322 recorder requires revision 321 and empty registry")
    side = ROOT / "artifacts/task_routeb_gcn_f1_leaf_current"
    report, checker, result, witness = (side / n for n in ("REPORT.md", "checker.py", "CHECK_RESULT.json", "leaf_witness.json"))
    out_report = ROOT / "artifacts/task_routeb_revision322_gcn_f1_leaf/REPORT.md"
    if not all(p.is_file() for p in (report, checker, result, witness, out_report)):
        raise ValueError("missing GCN-F1 evidence")
    check = json.loads(result.read_text(encoding="utf-8"))
    exact = check.get("exact_results", {})
    if (check.get("status") != "PASS_EXACT_RATIONAL_CONDITIONAL_GCN_F1_LEAF"
            or not check.get("fraction_only_verdict")
            or not check.get("leaf_closed")
            or check.get("source_interval_membership_closed") is not False
            or check.get("coverage") is not False
            or check.get("registry") is not False
            or check.get("formal_certificate_allowed") is not False
            or exact.get("contraction_upper") != "21/100"
            or exact.get("schur_coercivity_lower") != "3/100"):
        raise ValueError("GCN-F1 checker did not pass with the required boundary")

    old = ROOT / "artifacts/routeb_6dof/block45-obligations-v275.json"
    new = ROOT / "artifacts/routeb_6dof/block45-obligations-v276.json"
    graph = json.loads(old.read_text(encoding="utf-8"))
    record = {
        "kind": "routeb_gcn_f1_exact_rational_leaf",
        "status": check["status"],
        "evidence_level": "fraction-only-conditional-finite-matrix-leaf",
        "files": [ref(out_report), ref(report), ref(checker), ref(result), ref(witness)],
        "cell": check["cell"],
        "witness_sha256": check["witness_sha256"],
        "contraction_upper": exact["contraction_upper"],
        "inverse_weighted_norm_strict_upper": exact["inverse_weighted_norm_strict_upper"],
        "schur_coercivity_lower": exact["schur_coercivity_lower"],
        "source_interval_membership_closed": False,
        "coverage": False,
        "registry_promoted": False,
        "formal_certificate_allowed": False,
    }
    graph.setdefault("bottleneck_audits", []).append(record)
    graph.setdefault("workflow_hardening", []).append(record)
    graph.setdefault("open_frontier_updates", []).append({
        "node": "GCN-F1-fixed-preconditioner-export",
        "status": "one_conditional_leaf_closed_source_and_global_premises_open",
        "reason": "exact rational contraction and Schur witness replay for one exported cell; interval soundness and coverage are not established",
        "evidence": ref(result),
    })
    graph.update(schema="routeb-proposed-proof-dag-v276", supersedes=old.name)
    new.write_text(json.dumps(graph, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    checkpoint = ROOT / "artifacts/routeb_storage_checkpoint_20260908/state-before-revision322.json"
    if not checkpoint.exists():
        checkpoint.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(store.path, checkpoint)
    graph_sha = sha(new)
    state.graph_artifacts.append({
        "schema_version": 1,
        "algorithm": "routeb_revision322_gcn_f1_leaf/v1",
        "graph_sha256": graph_sha, "roots": [], "selected_nodes": [],
        "evidence_sha256": sha(out_report), "checker_sha256": sha(checker),
        "result_sha256": sha(result), "witness_sha256": sha(witness),
        "cell": check["cell"], "conditional_leaf": True,
        "source_interval_membership_closed": False, "coverage": False,
        "registry_promoted": False, "formal_certificate_allowed": False,
    })
    state.event(
        "routeb_revision322_gcn_f1_leaf_recorded",
        proposed_dag=ref(new), proposed_dag_sha256=graph_sha,
        cell=check["cell"], contraction_upper=exact["contraction_upper"],
        schur_coercivity_lower=exact["schur_coercivity_lower"],
        conditional_leaf=True, source_interval_membership_closed=False,
        coverage=False, registry_promoted=False,
        formal_certificate_allowed=False, broad_regression_run=False,
    )
    store.save(state)
    print(json.dumps({"revision": state.revision, "graph": new.name,
                      "registry": len(state.registry),
                      "formal_certificate_allowed": False}))


if __name__ == "__main__":
    main()
