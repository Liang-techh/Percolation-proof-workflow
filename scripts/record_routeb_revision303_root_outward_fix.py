"""Record the focused outward global-root repair."""
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
    if state.revision != 302 or state.registry:
        raise ValueError("revision-303 recorder requires revision 302 and empty registry")
    old = ROOT / "artifacts/routeb_6dof/block45-obligations-v256.json"
    new = ROOT / "artifacts/routeb_6dof/block45-obligations-v257.json"
    side = ROOT / "artifacts/task_FLT_root_box_audit_20260908"
    source = Path(r"C:\Users\z5242\Desktop\重构版\6dof_sos_optimized\6dof_sos_optimized\robot_final\routeB_interval_branch_bound.jl")
    report, check, output = side / "APPLIED_REPORT.md", side / "check_root_outward.jl", side / "check_root_outward.out"
    if not all(p.is_file() for p in (old, source, report, check, output)):
        raise ValueError("missing root outward evidence")
    source_sha = "c84b16a9dcc10e41af30c1fd312fd73265ac17aa2f1b7db662392570787a0cc5"
    if sha(source) != source_sha:
        raise ValueError("canonical driver hash mismatch")
    text = output.read_text(encoding="utf-8")
    if "outward global root |    3      3" not in text or "ROOT_OUTWARD_FOCUSED_OK" not in text:
        raise ValueError("root focused check failed")
    record = {
        "kind": "routeb_global_root_outward_repair",
        "status": "PASS_ROOT_OUTWARD_FOCUSED_P_BOUNDS_OPEN",
        "evidence_level": "canonical-driver-hash-plus-no-evaluator-root-harness",
        "files": [ref(report), ref(check), ref(output)],
        "source_sha256": source_sha,
        "repaired": ["qrad_roundup", "dqrad_no_float64_narrowing", "pi_joint_limits_outward", "sqrt3_outward"],
        "focused_test_pass": True,
        "evaluator_nodes_run": 0,
        "p_bounds_outward": False,
        "coverage_complete": False,
        "registry_promoted": False,
        "formal_certificate_allowed": False,
    }
    graph = json.loads(old.read_text(encoding="utf-8"))
    graph.setdefault("bottleneck_audits", []).append(record)
    graph.setdefault("external_intakes", []).append(record)
    graph.setdefault("open_frontier_updates", []).append({
        "node": "B45.coverage",
        "status": "root_outward_repaired_p_bounds_open",
        "reason": "global root no longer narrows q/dq/w by nearest or Float64 conversion; p_bounds/tightening and adaptive union receipt remain open.",
    })
    graph.update(schema="routeb-proposed-proof-dag-v257", supersedes=old.name)
    new.write_text(json.dumps(graph, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    backup = ROOT / "artifacts/routeb_storage_checkpoint_20260908/state-before-revision303.json"
    if not backup.exists():
        backup.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(store.path, backup)
    digest = sha(new)
    state.graph_artifacts.append({
        "schema_version": 1,
        "algorithm": "routeb_revision303_root_outward_fix/v1",
        "graph_sha256": digest,
        "roots": [],
        "selected_nodes": [],
        "source": str(side),
        "evidence_sha256": sha(report),
        "canonical_driver_sha256": source_sha,
        "focused_checks_pass": True,
        "evaluator_nodes_run": 0,
        "p_bounds_open": True,
        "coverage_complete": False,
        "registry_promoted": False,
        "formal_certificate_allowed": False,
    })
    state.event(
        "routeb_revision303_root_outward_fix_recorded",
        proposed_dag=ref(new),
        proposed_dag_sha256=digest,
        canonical_driver_sha256=source_sha,
        focused_checks_pass=True,
        evaluator_nodes_run=0,
        p_bounds_outward=False,
        coverage_complete=False,
        registry_promoted=False,
        formal_certificate_allowed=False,
        broad_regression_run=False,
    )
    store.save(state)
    print(json.dumps({"revision": state.revision, "graph": new.name, "registry": len(state.registry)}))


if __name__ == "__main__":
    main()
