"""Record the focused scalar outward-rounding repair."""
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
    if state.revision != 301 or state.registry:
        raise ValueError("revision-302 recorder requires revision 301 and empty registry")
    old = ROOT / "artifacts/routeb_6dof/block45-obligations-v255.json"
    new = ROOT / "artifacts/routeb_6dof/block45-obligations-v256.json"
    side = ROOT / "artifacts/task_FLT_rounding_patch_design_20260908"
    source = Path(r"C:\Users\z5242\Desktop\重构版\6dof_sos_optimized\6dof_sos_optimized\robot_final\routeB_interval_bounds.jl")
    required = [old, source, side / "APPLIED_REPORT.md", side / "focused_rounding_checks_canonical.out", ROOT / "artifacts/task_FLT_trig_rounding_bridge_20260908/probe.after_scalar_rounding_fix.out", ROOT / "artifacts/task_FLT_trig_rounding_bridge_20260908/critical.after_scalar_rounding_fix.out"]
    if not all(p.is_file() for p in required):
        raise ValueError("missing scalar rounding repair evidence")
    source_sha = "58fa9d1038a83d0ff02c96d53a86d40da909d55f7f9b26a709dfac2701558297"
    if sha(source) != source_sha:
        raise ValueError("canonical source hash mismatch")
    focused = (side / "focused_rounding_checks_canonical.out").read_text(encoding="utf-8")
    if "canonical rounding helpers |   10     10" not in focused or "canonical qext expansion |    8      8" not in focused:
        raise ValueError("focused scalar rounding tests did not pass")
    critical = (ROOT / "artifacts/task_FLT_trig_rounding_bridge_20260908/critical.after_scalar_rounding_fix.out").read_text(encoding="utf-8")
    for marker in ("critical_sin_max_contains_one=true", "critical_sin_min_contains_minus_one=true", "critical_cos_max_contains_one=true", "critical_cos_min_contains_minus_one=true", "out_of_domain_rejected=true"):
        if marker not in critical:
            raise ValueError("trig regression marker missing: " + marker)
    record = {
        "kind": "routeb_scalar_outward_rounding_repair",
        "status": "PASS_FOCUSED_CANONICAL_CHECKS_SCALAR_AGGREGATION_OPEN",
        "evidence_level": "canonical-source-hash-plus-focused-julia-tests",
        "files": [ref(side / name) for name in ("APPLIED_REPORT.md", "focused_rounding_checks_canonical.jl", "focused_rounding_checks_canonical.out")],
        "source_sha256": source_sha,
        "repaired": ["square_bounds", "midpoint", "radius", "qext"],
        "focused_test_counts": {"rounding_helpers": 10, "qext_guards": 8},
        "scalar_aggregation_open": True,
        "registry_promoted": False,
        "formal_certificate_allowed": False,
    }
    graph = json.loads(old.read_text(encoding="utf-8"))
    graph.setdefault("bottleneck_audits", []).append(record)
    graph.setdefault("external_intakes", []).append(record)
    graph.setdefault("open_frontier_updates", []).append({
        "node": "B45.rounding",
        "status": "endpoint_seams_repaired_scalar_aggregation_open",
        "reason": "square/radius/qext endpoint contractions are repaired and focused-tested; scalar sums and proof-facing kappa/h endpoints remain open.",
    })
    graph.update(schema="routeb-proposed-proof-dag-v256", supersedes=old.name)
    new.write_text(json.dumps(graph, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    backup = ROOT / "artifacts/routeb_storage_checkpoint_20260908/state-before-revision302.json"
    if not backup.exists():
        backup.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(store.path, backup)
    digest = sha(new)
    state.graph_artifacts.append({
        "schema_version": 1,
        "algorithm": "routeb_revision302_scalar_rounding_fix/v1",
        "graph_sha256": digest,
        "roots": [],
        "selected_nodes": [],
        "source": str(side),
        "evidence_sha256": sha(side / "APPLIED_REPORT.md"),
        "canonical_source_sha256": source_sha,
        "focused_checks_pass": True,
        "scalar_aggregation_open": True,
        "registry_promoted": False,
        "formal_certificate_allowed": False,
    })
    state.event(
        "routeb_revision302_scalar_rounding_fix_recorded",
        proposed_dag=ref(new),
        proposed_dag_sha256=digest,
        canonical_source_sha256=source_sha,
        focused_checks_pass=True,
        repaired_endpoints=["square_bounds", "midpoint", "radius", "qext"],
        scalar_aggregation_open=True,
        registry_promoted=False,
        formal_certificate_allowed=False,
        broad_regression_run=False,
    )
    store.save(state)
    print(json.dumps({"revision": state.revision, "graph": new.name, "registry": len(state.registry)}))


if __name__ == "__main__":
    main()
