"""Record the directed critical-point interval repair for Route-B trig atoms."""
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
    if state.revision != 294 or state.registry:
        raise ValueError("revision-295 recorder requires revision 294 and empty registry")
    old = ROOT / "artifacts/routeb_6dof/block45-obligations-v248.json"
    new = ROOT / "artifacts/routeb_6dof/block45-obligations-v249.json"
    side = ROOT / "artifacts/task_FLT_trig_rounding_bridge_20260908"
    # Keep the canonical source path explicit to avoid ambiguous globs.
    source = Path(r"C:\Users\z5242\Desktop\重构版\6dof_sos_optimized\6dof_sos_optimized\robot_final\routeB_interval_bounds.jl")
    required = [old, side / "REPORT.md", side / "probe.after_fix.out", side / "check_critical_points.jl", side / "critical.after_fix.out"]
    if not all(path.is_file() for path in required):
        raise ValueError("missing trig rounding evidence")
    if not source.is_file():
        raise ValueError("canonical Route-B source missing")
    probe = (side / "probe.after_fix.out").read_text(encoding="utf-8")
    critical = (side / "critical.after_fix.out").read_text(encoding="utf-8")
    expected_source_sha = "13a8fc73a24a73fd2fb3bc464a3b50a55ec3f8e4d30538726dbcc6c25ba7bf22"
    if sha(source) != expected_source_sha or f"interval_source_sha256={expected_source_sha}" not in probe:
        raise ValueError("canonical source hash is not bound in trig probe")
    for marker in ("critical_sin_max_contains_one", "critical_sin_min_contains_minus_one", "critical_cos_max_contains_one", "critical_cos_min_contains_minus_one"):
        if marker + "=true" not in critical:
            raise ValueError("critical-point checker missing " + marker)
    record = {
        "kind": "routeb_directed_trig_critical_point_bridge",
        "status": "PASS_LOCAL_SOURCE_SEMANTICS_ATOM",
        "evidence_level": "canonical-source-hash-plus-julia-mpfr-probe-plus-critical-point-focused-check",
        "source_sha256": expected_source_sha,
        "files": [ref(side / name) for name in ("REPORT.md", "probe.after_fix.out", "check_critical_points.jl", "critical.after_fix.out")],
        "rounding_precision_bits": 256,
        "julia_version": "1.12.7",
        "mpfr_version": "4.2.2",
        "critical_extrema_checked": ["sin:+1", "sin:-1", "cos:+1", "cos:-1"],
        "source_interval_semantics_formalized": False,
        "domain_coverage_complete": False,
        "registry_promoted": False,
        "formal_certificate_allowed": False,
    }
    graph = json.loads(old.read_text(encoding="utf-8"))
    graph.setdefault("bottleneck_audits", []).append(record)
    graph.setdefault("external_intakes", []).append(record)
    graph.setdefault("open_frontier_updates", []).append({
        "node": "B45.trig_rounding",
        "status": "directed_critical_point_intervalized_source_semantics_atom",
        "reason": "pi and 2*pi extrema are now guarded by outward critical-point intervals; full DH/source binding and coverage remain open.",
    })
    graph.update(schema="routeb-proposed-proof-dag-v249", supersedes=old.name)
    new.write_text(json.dumps(graph, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    backup = ROOT / "artifacts/routeb_storage_checkpoint_20260908/state-before-revision295.json"
    if not backup.exists():
        backup.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(store.path, backup)
    digest = sha(new)
    state.graph_artifacts.append({
        "schema_version": 1,
        "algorithm": "routeb_revision295_trig_rounding_bridge/v1",
        "graph_sha256": digest,
        "roots": [],
        "selected_nodes": [],
        "source": str(side),
        "evidence_sha256": sha(side / "REPORT.md"),
        "canonical_source_sha256": expected_source_sha,
        "focused_probe_pass": True,
        "critical_point_guard_pass": True,
        "source_semantics_open": True,
        "domain_coverage_complete": False,
        "registry_promoted": False,
        "formal_certificate_allowed": False,
    })
    state.event(
        "routeb_revision295_trig_rounding_bridge_recorded",
        proposed_dag=ref(new),
        proposed_dag_sha256=digest,
        canonical_source_sha256=expected_source_sha,
        directed_rounding_precision_bits=256,
        julia_version="1.12.7",
        mpfr_version="4.2.2",
        focused_probe_pass=True,
        critical_point_guard_pass=True,
        source_interval_semantics=False,
        domain_coverage_complete=False,
        registry_promoted=False,
        formal_certificate_allowed=False,
        broad_regression_run=False,
    )
    store.save(state)
    print(json.dumps({"revision": state.revision, "graph": new.name, "registry": len(state.registry)}))


if __name__ == "__main__":
    main()
