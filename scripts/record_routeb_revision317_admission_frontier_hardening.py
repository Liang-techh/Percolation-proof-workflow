"""Record fail-closed admission and stable frontier normalization."""
from __future__ import annotations

import hashlib
import json
import shutil
from collections import Counter
from pathlib import Path

from record_routeb_port_progress import ROOT, ref
from percolation_workflow.store import StateStore


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    store = StateStore(ROOT / "artifacts/routeb_6dof/state.json")
    state = store.load()
    if state.revision != 316 or state.registry:
        raise ValueError("revision-317 recorder requires revision 316 and empty registry")
    old = ROOT / "artifacts/routeb_6dof/block45-obligations-v270.json"
    new = ROOT / "artifacts/routeb_6dof/block45-obligations-v271.json"
    report = ROOT / "artifacts/task_routeb_revision317_admission_frontier_hardening/REPORT.md"
    audit = ROOT / "artifacts/task_routeb_frontier_binding_current/CHECK_RESULT.json"
    controller = ROOT / "src/percolation_workflow/controller.py"
    tests = ROOT / "tests/test_controller.py"
    if not old.is_file() or not all(
            p.is_file() for p in (report, audit, controller, tests)):
        raise ValueError("missing revision-317 evidence")
    graph = json.loads(old.read_text(encoding="utf-8"))
    frontier = graph.get("next_frontier")
    if not isinstance(frontier, list):
        raise ValueError("DAG frontier is not a list")
    counts = Counter(frontier)
    duplicate_claims = [claim for claim in frontier if counts[claim] > 1]
    if len(frontier) != 52 or len(set(frontier)) != 49:
        raise ValueError("expected the audited 52-to-49 frontier duplicate pattern")
    normalized = list(dict.fromkeys(frontier))
    graph["frontier_normalization"] = {
        "schema": "prove2me-frontier-normalization-v1",
        "policy": "stable_first_occurrence_deduplication",
        "input_count": len(frontier),
        "unique_count": len(normalized),
        "duplicate_claim_count": len(frontier) - len(normalized),
        "duplicate_claims": list(dict.fromkeys(duplicate_claims)),
        "predecessor_graph": old.name,
        "provenance_audit": ref(audit),
    }
    graph["next_frontier_original"] = frontier
    graph["next_frontier"] = normalized
    graph.setdefault("workflow_hardening", []).append({
        "kind": "stable_frontier_normalization",
        "status": "PASS_DUPLICATES_REMOVED_HISTORY_PRESERVED",
        "input_count": 52, "unique_count": 49,
        "duplicate_claims": list(dict.fromkeys(duplicate_claims)),
        "registry_promoted": False, "formal_certificate_allowed": False,
    })
    graph.setdefault("bottleneck_audits", []).append({
        "kind": "routeb_fail_closed_final_admission_gate",
        "status": "PASS_TARGETED_CONTROLLER_GATE",
        "files": [ref(controller), ref(tests), ref(report)],
        "root_registry_and_lean_stage_required": True,
        "explicit_false_formal_certificate_gate_rejected": True,
        "registry_promoted": False, "formal_certificate_allowed": False,
    })
    graph.update(schema="routeb-proposed-proof-dag-v271", supersedes=old.name)
    new.write_text(json.dumps(graph, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    checkpoint = ROOT / "artifacts/routeb_storage_checkpoint_20260908/state-before-revision317.json"
    if not checkpoint.exists():
        checkpoint.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(store.path, checkpoint)
    graph_sha = sha(new)
    state.graph_artifacts.append({
        "schema_version": 1,
        "algorithm": "routeb_revision317_admission_frontier_hardening/v1",
        "graph_sha256": graph_sha, "roots": [], "selected_nodes": [],
        "evidence_sha256": sha(report), "frontier_audit_sha256": sha(audit),
        "controller_sha256": sha(controller), "controller_tests_sha256": sha(tests),
        "frontier_input_count": 52, "frontier_unique_count": 49,
        "admission_gate_hardened": True, "registry_promoted": False,
        "formal_certificate_allowed": False,
    })
    state.event(
        "routeb_revision317_admission_frontier_hardening_recorded",
        proposed_dag=ref(new), proposed_dag_sha256=graph_sha,
        frontier_input_count=52, frontier_unique_count=49,
        duplicate_claim_count=3, history_preserved=True,
        admission_gate_hardened=True, root_registry_and_lean_stage_required=True,
        registry_promoted=False, formal_certificate_allowed=False,
        broad_regression_run=False,
    )
    store.save(state)
    print(json.dumps({"revision": state.revision, "graph": new.name,
                      "registry": len(state.registry),
                      "formal_certificate_allowed": False}))


if __name__ == "__main__":
    main()
