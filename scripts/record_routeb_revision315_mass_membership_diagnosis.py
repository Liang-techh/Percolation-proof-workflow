"""Record the focused diagnosis of the Fourier/canonical interval mismatch."""
from __future__ import annotations

import hashlib
import json
import shutil
from pathlib import Path

from record_routeb_port_progress import ROOT, ref
from percolation_workflow.store import StateStore


CANONICAL_SHA = "03679c7b686842ef9504886614e3498fb9fbf4a6c1466f8e44dcc505d21e3609"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    store = StateStore(ROOT / "artifacts/routeb_6dof/state.json")
    state = store.load()
    if state.revision != 314 or state.registry:
        raise ValueError("revision-315 recorder requires revision 314 and empty registry")
    side = ROOT / "artifacts/task_routeb_mass_membership_diagnosis_current"
    report, result = side / "REPORT.md", side / "CHECK_RESULT.json"
    if not report.is_file() or not result.is_file():
        raise ValueError("missing mass-membership diagnosis evidence")
    check = json.loads(result.read_text(encoding="utf-8"))
    if check.get("status") != "DIAGNOSIS_PASS_INTERVAL_EXPRESSION_OVERAPPROXIMATION":
        raise ValueError("unexpected diagnosis status")
    if check.get("inputs", {}).get("canonical_interval_source_sha256") != CANONICAL_SHA:
        raise ValueError("canonical source hash drifted")
    focused = check.get("focused_repaired_obligation", {})
    if focused.get("status") != "PASS_M33_FOURIER_CELL_BOX_SUBSET_CANONICAL_BOX":
        raise ValueError("focused M33 repaired obligation did not pass")
    if check.get("claim_boundary", {}).get("full_matrix_repaired_direction_checked"):
        raise ValueError("diagnosis unexpectedly claims full matrix closure")

    old = ROOT / "artifacts/routeb_6dof/block45-obligations-v268.json"
    new = ROOT / "artifacts/routeb_6dof/block45-obligations-v269.json"
    graph = json.loads(old.read_text(encoding="utf-8"))
    record = {
        "kind": "routeb_mass_membership_dependency_diagnosis",
        "status": "PASS_M33_FOCUSED_REPAIRED_DIRECTION_ONLY",
        "evidence_level": "exact-focused-cell-diagnosis",
        "files": [ref(report), ref(result)],
        "canonical_interval_source_sha256": CANONICAL_SHA,
        "original_direction_failed": True,
        "original_failed_entry_count": check["original_check"]["failed_entry_count"],
        "m33_fourier_cell_subset_canonical": True,
        "full_matrix_repaired_direction_closed": False,
        "deployed_source_extensional_equivalence_proved": False,
        "registry_promoted": False,
        "formal_certificate_allowed": False,
    }
    graph.setdefault("bottleneck_audits", []).append(record)
    graph.setdefault("repair_audits", []).append({
        "kind": "mass_membership_direction_repaired_for_focused_cell",
        "status": "partial",
        "closed_scope": "M33 on one pinned q1=0 GCZ cell",
        "open_scope": "full 36-entry exact source binding and deployed Julia extensionality",
        "evidence": ref(result),
        "registry_promoted": False,
        "formal_certificate_allowed": False,
    })
    graph.setdefault("open_frontier_updates", []).append({
        "node": "B45-1_bind_regularized_mass_entries_to_Fourier_evaluator",
        "status": "M33_local_direction_repaired_full_matrix_open",
        "reason": "natural-expression interval may be wider than global Fourier L1 envelope; correct source-membership direction is exact cell enclosure subset canonical",
        "evidence": ref(result),
    })
    graph.update(schema="routeb-proposed-proof-dag-v269", supersedes=old.name)
    new.write_text(json.dumps(graph, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    checkpoint = ROOT / "artifacts/routeb_storage_checkpoint_20260908/state-before-revision315.json"
    if not checkpoint.exists():
        checkpoint.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(store.path, checkpoint)
    graph_sha = sha(new)
    state.graph_artifacts.append({
        "schema_version": 1,
        "algorithm": "routeb_revision315_mass_membership_diagnosis/v1",
        "graph_sha256": graph_sha, "roots": [], "selected_nodes": [],
        "evidence_sha256": sha(report), "result_sha256": sha(result),
        "canonical_interval_source_sha256": CANONICAL_SHA,
        "m33_focused_repaired_direction": True,
        "full_matrix_repaired_direction_closed": False,
        "registry_promoted": False, "formal_certificate_allowed": False,
    })
    state.event(
        "routeb_revision315_mass_membership_diagnosis_recorded",
        proposed_dag=ref(new), proposed_dag_sha256=graph_sha,
        original_direction_failed=True, m33_focused_repaired_direction=True,
        full_matrix_repaired_direction_closed=False,
        deployed_source_extensional_equivalence_proved=False,
        registry_promoted=False, formal_certificate_allowed=False,
        broad_regression_run=False,
    )
    store.save(state)
    print(json.dumps({"revision": state.revision, "graph": new.name,
                      "registry": len(state.registry),
                      "formal_certificate_allowed": False}))


if __name__ == "__main__":
    main()
