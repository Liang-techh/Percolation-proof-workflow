"""Record the full 36-entry pinned-cell Fourier enclosure result."""
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
    if state.revision != 320 or state.registry:
        raise ValueError("revision-321 recorder requires revision 320 and empty registry")
    side = ROOT / "artifacts/task_routeb_fourier_cell_enclosure_current"
    report, checker, result = (side / n for n in ("REPORT.md", "check_enclosures.py", "CHECK_RESULT.json"))
    if not all(p.is_file() for p in (report, checker, result)):
        raise ValueError("missing full Fourier-cell evidence")
    check = json.loads(result.read_text(encoding="utf-8"))
    scope, summary, inputs = check.get("scope", {}), check.get("summary", {}), check.get("inputs", {})
    if (check.get("status") != "PASS_ALL_36_FOURIER_CELL_SUBSET_CANONICAL"
            or scope.get("matrix_entries_checked") != 36
            or summary.get("passed_entry_count") != 36
            or summary.get("blocked_entry_count") != 0
            or inputs.get("canonical") != CANONICAL_SHA
            or check.get("claim_boundary", {}).get("deployed_julia_extensional_equivalence_proved") is not False):
        raise ValueError("full Fourier-cell checker did not pass with the required boundary")

    old = ROOT / "artifacts/routeb_6dof/block45-obligations-v274.json"
    new = ROOT / "artifacts/routeb_6dof/block45-obligations-v275.json"
    graph = json.loads(old.read_text(encoding="utf-8"))
    record = {
        "kind": "routeb_full_fourier_cell_enclosure",
        "status": "PASS_ALL_36_FOURIER_CELL_SUBSET_CANONICAL",
        "evidence_level": "exact-rational-pinned-cell-enclosure",
        "files": [ref(report), ref(checker), ref(result)],
        "canonical_interval_source_sha256": CANONICAL_SHA,
        "matrix_entries_checked": 36,
        "passed_entry_count": 36,
        "blocked_entry_count": 0,
        "max_leaf_count_used": summary["max_leaf_count_used"],
        "deployed_julia_extensional_equivalence_proved": False,
        "global_domain_coverage": False,
        "registry_promoted": False,
        "formal_certificate_allowed": False,
    }
    graph.setdefault("bottleneck_audits", []).append(record)
    graph.setdefault("workflow_hardening", []).append(record)
    graph.setdefault("open_frontier_updates", []).append({
        "node": "B45-1_bind_regularized_mass_entries_to_Fourier_evaluator",
        "status": "pinned_cell_all_36_closed_deployed_binding_open",
        "reason": "all 36 finite Fourier cell enclosures fit the canonical natural interval; source extensionality and global coverage remain open",
        "evidence": ref(result),
    })
    graph.update(schema="routeb-proposed-proof-dag-v275", supersedes=old.name)
    new.write_text(json.dumps(graph, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    checkpoint = ROOT / "artifacts/routeb_storage_checkpoint_20260908/state-before-revision321.json"
    if not checkpoint.exists():
        checkpoint.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(store.path, checkpoint)
    graph_sha = sha(new)
    state.graph_artifacts.append({
        "schema_version": 1,
        "algorithm": "routeb_revision321_fourier_cell_enclosure/v1",
        "graph_sha256": graph_sha, "roots": [], "selected_nodes": [],
        "evidence_sha256": sha(report), "checker_sha256": sha(checker),
        "result_sha256": sha(result), "canonical_interval_source_sha256": CANONICAL_SHA,
        "matrix_entries_checked": 36, "passed_entry_count": 36,
        "blocked_entry_count": 0, "deployed_source_binding_complete": False,
        "registry_promoted": False, "formal_certificate_allowed": False,
    })
    state.event(
        "routeb_revision321_fourier_cell_enclosure_recorded",
        proposed_dag=ref(new), proposed_dag_sha256=graph_sha,
        matrix_entries_checked=36, passed_entry_count=36,
        blocked_entry_count=0, pinned_cell_only=True,
        deployed_source_binding_complete=False, global_domain_coverage=False,
        registry_promoted=False, formal_certificate_allowed=False,
        broad_regression_run=False,
    )
    store.save(state)
    print(json.dumps({"revision": state.revision, "graph": new.name,
                      "registry": len(state.registry),
                      "formal_certificate_allowed": False}))


if __name__ == "__main__":
    main()
