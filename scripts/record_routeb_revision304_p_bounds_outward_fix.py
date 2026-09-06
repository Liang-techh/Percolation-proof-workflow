"""Record the focused outward p-bound and tightening repair."""
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
    if state.revision != 303 or state.registry:
        raise ValueError("revision-304 recorder requires revision 303 and empty registry")
    old = ROOT / "artifacts/routeb_6dof/block45-obligations-v257.json"
    new = ROOT / "artifacts/routeb_6dof/block45-obligations-v258.json"
    side = ROOT / "artifacts/task_FLT_root_box_audit_20260908"
    source = Path(r"C:\Users\z5242\Desktop\重构版\6dof_sos_optimized\6dof_sos_optimized\robot_final\routeB_interval_branch_bound.jl")
    report = side / "APPLIED_REPORT_p_bounds.md"
    check = side / "check_p_bounds_outward.out"
    root_check = side / "check_root_outward.after_p_fix.out"
    if not all(p.is_file() for p in (old, source, report, check, root_check)):
        raise ValueError("missing p-bound repair evidence")
    source_sha = "25f7bff228ef345159bee202a0c81a428cad57251f40e1bd611660c08813d02f"
    if sha(source) != source_sha:
        raise ValueError("canonical driver hash mismatch")
    if "directed p bounds |    3      3" not in check.read_text(encoding="utf-8") or "P_BOUNDS_OUTWARD_FOCUSED_OK" not in check.read_text(encoding="utf-8"):
        raise ValueError("p-bound focused check failed")
    if "outward global root |    3      3" not in root_check.read_text(encoding="utf-8"):
        raise ValueError("root focused recheck failed")
    record = {
        "kind": "routeb_p_bounds_outward_repair",
        "status": "PASS_P_BOUNDS_FOCUSED_ADAPTIVE_COVERAGE_OPEN",
        "evidence_level": "canonical-driver-hash-plus-no-evaluator-focused-harness",
        "files": [ref(report), ref(side / "check_p_bounds_outward.jl"), ref(check), ref(root_check)],
        "source_sha256": source_sha,
        "repaired": ["square_lower", "square_upper", "p_bounds_weighted_terms", "p_bounds_sum", "tightening_remaining_budget"],
        "focused_test_pass": True,
        "evaluator_nodes_run": 0,
        "adaptive_coverage_open": True,
        "registry_promoted": False,
        "formal_certificate_allowed": False,
    }
    graph = json.loads(old.read_text(encoding="utf-8"))
    graph.setdefault("bottleneck_audits", []).append(record)
    graph.setdefault("external_intakes", []).append(record)
    graph.setdefault("open_frontier_updates", []).append({
        "node": "B45.coverage",
        "status": "p_bounds_outward_repaired_adaptive_coverage_open",
        "reason": "root p-bound and tightening gates now use directed square/term/sum arithmetic; adaptive tree receipt and dynamics coverage remain open.",
    })
    graph.update(schema="routeb-proposed-proof-dag-v258", supersedes=old.name)
    new.write_text(json.dumps(graph, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    backup = ROOT / "artifacts/routeb_storage_checkpoint_20260908/state-before-revision304.json"
    if not backup.exists():
        backup.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(store.path, backup)
    digest = sha(new)
    state.graph_artifacts.append({
        "schema_version": 1,
        "algorithm": "routeb_revision304_p_bounds_outward_fix/v1",
        "graph_sha256": digest,
        "roots": [],
        "selected_nodes": [],
        "source": str(side),
        "evidence_sha256": sha(report),
        "canonical_driver_sha256": source_sha,
        "focused_checks_pass": True,
        "evaluator_nodes_run": 0,
        "adaptive_coverage_open": True,
        "registry_promoted": False,
        "formal_certificate_allowed": False,
    })
    state.event(
        "routeb_revision304_p_bounds_outward_fix_recorded",
        proposed_dag=ref(new),
        proposed_dag_sha256=digest,
        canonical_driver_sha256=source_sha,
        focused_checks_pass=True,
        evaluator_nodes_run=0,
        adaptive_coverage_complete=False,
        registry_promoted=False,
        formal_certificate_allowed=False,
        broad_regression_run=False,
    )
    store.save(state)
    print(json.dumps({"revision": state.revision, "graph": new.name, "registry": len(state.registry)}))


if __name__ == "__main__":
    main()
