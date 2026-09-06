"""Record the fail-closed angle-domain guard for Route-B trig evaluation."""
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
    if state.revision != 295 or state.registry:
        raise ValueError("revision-296 recorder requires revision 295 and empty registry")
    old = ROOT / "artifacts/routeb_6dof/block45-obligations-v249.json"
    new = ROOT / "artifacts/routeb_6dof/block45-obligations-v250.json"
    side = ROOT / "artifacts/task_FLT_trig_rounding_bridge_20260908"
    source = Path(r"C:\Users\z5242\Desktop\重构版\6dof_sos_optimized\6dof_sos_optimized\robot_final\routeB_interval_bounds.jl")
    report = side / "REPORT_domain_guard.md"
    probe = side / "probe.after_domain_guard.out"
    critical = side / "critical.after_domain_guard.out"
    required = [old, source, report, probe, critical]
    if not all(path.is_file() for path in required):
        raise ValueError("missing trig domain-guard evidence")
    expected_source_sha = "c62c70301f368085f843248efedfee1268b214ad22839a7d51310ecdbb9dd5e2"
    if sha(source) != expected_source_sha:
        raise ValueError("canonical source hash mismatch")
    probe_text = probe.read_text(encoding="utf-8")
    critical_text = critical.read_text(encoding="utf-8")
    if f"interval_source_sha256={expected_source_sha}" not in probe_text:
        raise ValueError("domain-guard probe is not source bound")
    for marker in (
        "critical_sin_max_contains_one=true",
        "critical_sin_min_contains_minus_one=true",
        "critical_cos_max_contains_one=true",
        "critical_cos_min_contains_minus_one=true",
        "out_of_domain_rejected=true",
    ):
        if marker not in critical_text:
            raise ValueError("focused trig check failed: " + marker)
    record = {
        "kind": "routeb_trig_fixed_domain_fail_closed_guard",
        "status": "PASS_LOCAL_SOURCE_SEMANTICS_ATOM",
        "evidence_level": "canonical-source-hash-plus-focused-boundary-and-rejection-receipts",
        "source_sha256": expected_source_sha,
        "files": [ref(side / name) for name in ("REPORT_domain_guard.md", "probe.after_domain_guard.out", "critical.after_domain_guard.out")],
        "certified_angle_domain": "[-100,100]",
        "critical_index_range": "-16:16",
        "critical_extrema_checked": ["sin:+1", "sin:-1", "cos:+1", "cos:-1"],
        "out_of_domain_fail_closed": True,
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
        "status": "conditional_domain_guard_fail_closed",
        "reason": "static critical-index enumeration is now paired with explicit [-100,100] input rejection; full angle-domain and DH binding remain open.",
    })
    graph.update(schema="routeb-proposed-proof-dag-v250", supersedes=old.name)
    new.write_text(json.dumps(graph, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    backup = ROOT / "artifacts/routeb_storage_checkpoint_20260908/state-before-revision296.json"
    if not backup.exists():
        backup.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(store.path, backup)
    digest = sha(new)
    state.graph_artifacts.append({
        "schema_version": 1,
        "algorithm": "routeb_revision296_trig_domain_guard/v1",
        "graph_sha256": digest,
        "roots": [],
        "selected_nodes": [],
        "source": str(side),
        "evidence_sha256": sha(report),
        "canonical_source_sha256": expected_source_sha,
        "certified_angle_domain": "[-100,100]",
        "focused_probe_pass": True,
        "out_of_domain_rejection_pass": True,
        "source_semantics_open": True,
        "domain_coverage_complete": False,
        "registry_promoted": False,
        "formal_certificate_allowed": False,
    })
    state.event(
        "routeb_revision296_trig_domain_guard_recorded",
        proposed_dag=ref(new),
        proposed_dag_sha256=digest,
        canonical_source_sha256=expected_source_sha,
        certified_angle_domain="[-100,100]",
        critical_index_range="-16:16",
        focused_probe_pass=True,
        out_of_domain_rejection_pass=True,
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
