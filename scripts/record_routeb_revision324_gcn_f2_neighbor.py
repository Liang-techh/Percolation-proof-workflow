"""Record the conditional exact-rational GCN-F2 right-neighbor leaf."""
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
    if state.revision != 323 or state.registry:
        raise ValueError("revision-324 recorder requires revision 323 and empty registry")
    side = ROOT / "artifacts/task_routeb_gcn_f2_neighbor_current"
    report, checker, result, witness = (side / n for n in ("REPORT.md", "checker.py", "CHECK_RESULT.json", "neighbor_witness.json"))
    out_report = ROOT / "artifacts/task_routeb_revision324_gcn_f2_neighbor/REPORT.md"
    if not all(p.is_file() for p in (report, checker, result, witness, out_report)):
        raise ValueError("missing GCN-F2 evidence")
    check = json.loads(result.read_text(encoding="utf-8"))
    exact = check.get("exact_results", {})
    if (check.get("status") != "PASS_EXACT_RATIONAL_CONDITIONAL_GCN_F2_RIGHT_NEIGHBOR"
            or not check.get("fraction_only_verdict")
            or check.get("source_interval_membership_closed") is not False
            or check.get("coverage") is not False
            or check.get("registry") is not False
            or check.get("formal_certificate_allowed") is not False
            or exact.get("contraction_upper") != "21/100"
            or exact.get("schur_coercivity_lower") != "3/100"):
        raise ValueError("GCN-F2 checker did not pass with the required boundary")

    old = ROOT / "artifacts/routeb_6dof/block45-obligations-v277.json"
    new = ROOT / "artifacts/routeb_6dof/block45-obligations-v278.json"
    graph = json.loads(old.read_text(encoding="utf-8"))
    record = {
        "kind": "routeb_gcn_f2_exact_rational_neighbor_leaf",
        "status": check["status"],
        "evidence_level": "fraction-only-conditional-adjacent-cell-leaf",
        "files": [ref(out_report), ref(report), ref(checker), ref(result), ref(witness)],
        "cell": check["cell"],
        "f1_witness_sha256": check["f1_witness_sha256"],
        "neighbor_witness_sha256": check["neighbor_witness_sha256"],
        "contraction_upper": exact["contraction_upper"],
        "schur_coercivity_lower": exact["schur_coercivity_lower"],
        "preconditioner_reused_and_revalidated": True,
        "residual_recomputed": True,
        "source_interval_membership_closed": False,
        "coverage": False,
        "registry_promoted": False,
        "formal_certificate_allowed": False,
    }
    graph.setdefault("bottleneck_audits", []).append(record)
    graph.setdefault("workflow_hardening", []).append(record)
    graph.setdefault("open_frontier_updates", []).append({
        "node": "GCN-F2-adjacent-cell-propagation",
        "status": "one_shared_boundary_neighbor_closed_global_propagation_open",
        "reason": "one right neighbor independently replays with reused X/weights and recomputed residual/Schur; cover-wide F2 remains open",
        "evidence": ref(result),
    })
    graph.update(schema="routeb-proposed-proof-dag-v278", supersedes=old.name)
    new.write_text(json.dumps(graph, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    checkpoint = ROOT / "artifacts/routeb_storage_checkpoint_20260908/state-before-revision324.json"
    if not checkpoint.exists():
        checkpoint.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(store.path, checkpoint)
    graph_sha = sha(new)
    state.graph_artifacts.append({
        "schema_version": 1,
        "algorithm": "routeb_revision324_gcn_f2_neighbor/v1",
        "graph_sha256": graph_sha, "roots": [], "selected_nodes": [],
        "evidence_sha256": sha(out_report), "checker_sha256": sha(checker),
        "result_sha256": sha(result), "witness_sha256": sha(witness),
        "cell": check["cell"], "conditional_leaf": True,
        "source_interval_membership_closed": False, "coverage": False,
        "registry_promoted": False, "formal_certificate_allowed": False,
    })
    state.event(
        "routeb_revision324_gcn_f2_neighbor_recorded",
        proposed_dag=ref(new), proposed_dag_sha256=graph_sha,
        cell=check["cell"], contraction_upper=exact["contraction_upper"],
        schur_coercivity_lower=exact["schur_coercivity_lower"],
        shared_boundary=True, preconditioner_reused=True,
        residual_recomputed=True, conditional_leaf=True,
        source_interval_membership_closed=False, coverage=False,
        registry_promoted=False, formal_certificate_allowed=False,
        broad_regression_run=False,
    )
    store.save(state)
    print(json.dumps({"revision": state.revision, "graph": new.name,
                      "registry": len(state.registry),
                      "formal_certificate_allowed": False}))


if __name__ == "__main__":
    main()
