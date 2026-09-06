"""Persist q1 refinement, physical remote-action gap, and FLT adapter audit."""
from __future__ import annotations

import hashlib
import json
import shutil
from pathlib import Path

from record_routeb_port_progress import ROOT, ref
from percolation_workflow.store import StateStore


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def require(paths: list[Path]) -> list[Path]:
    assert all(path.is_file() for path in paths), paths
    return paths


def main() -> None:
    store = StateStore(ROOT / "artifacts/routeb_6dof/state.json")
    state = store.load()
    assert state.revision == 255 and not state.registry
    old = ROOT / "artifacts/routeb_6dof/block45-obligations-v209.json"
    new = ROOT / "artifacts/routeb_6dof/block45-obligations-v210.json"
    backup = ROOT / "artifacts/routeb_storage_checkpoint_20260907/state-before-revision256.json"
    gbx = ROOT / "artifacts/task_GBX_q1_depth_refinement_20260907"
    gby = ROOT / "artifacts/task_GBY_mbd_ad_singlecell_20260907"
    gbz = ROOT / "artifacts/task_GBZ_flt_adapter_admission_audit_20260907"
    local = require([
        ROOT / "src/percolation_workflow/agent_bridge.py",
        ROOT / "src/percolation_workflow/math_frontier.py",
        ROOT / "tests/test_agent_bridge.py",
        ROOT / "tests/test_math_frontier_policy.py",
    ])
    files = {
        "GBX": require([gbx / "REPORT.md", gbx / "receipt.json", gbx / "probe.jl"]),
        "GBY": require([gby / "REPORT.md", gby / "receipt.json", gby / "instrument.jl"]),
        "GBZ": require([gbz / "REPORT.md", gbz / "audit.json", gbz / "checker.py"]),
    }
    assert old.is_file() and not new.exists()
    q1 = json.loads((gbx / "receipt.json").read_text(encoding="utf-8"))
    mbd = json.loads((gby / "receipt.json").read_text(encoding="utf-8"))
    flt = json.loads((gbz / "audit.json").read_text(encoding="utf-8"))
    graph = json.loads(old.read_text(encoding="utf-8"))
    audits = [
        {
            "kind": "routeb_original_q1_depth_refinement",
            "status": q1["status"],
            "evidence_level": "four-targeted-original-source-probes",
            "semantic_boundary": (
                "q1-only contractions 1/2, 1/4, 1/8, 1/16 reduce rho but "
                "remain rho>=1; inverse/Schur, coverage and registry stay open."
            ),
            "sidecar": str(gbx.resolve()),
            "files": [ref(path) for path in files["GBX"]],
            "source_sha256": q1["source_hash"],
            "probe_count": q1["probe_count"],
            "rho_hi_sequence": [
                "13.49713314881121733587418899152642",
                "6.948172442207523464481553946209294",
                "3.674771036555313668268619224207348",
                "2.037624471292355711672895857570591",
            ],
            "registry_promoted": False,
            "formal_certificate_allowed": False,
        },
        {
            "kind": "routeb_original_mbd_ad_singlecell_binding_gap",
            "status": mbd["status"],
            "evidence_level": "one-point-physical-action-instrumentation",
            "semantic_boundary": (
                "The original source exposes a physical point action MBD_aD, "
                "but current interval payload does not contain aD/MBD/MBD_aD; "
                "same-point binding therefore fails closed."
            ),
            "sidecar": str(gby.resolve()),
            "files": [ref(path) for path in files["GBY"]],
            "physical_action_obtained": mbd["physical_action_obtained"],
            "same_point_checks": mbd["same_point_checks"],
            "minimal_patch_seam": mbd["source_gap"]["minimal_patch_seam"],
            "registry_promoted": False,
            "formal_certificate_allowed": False,
        },
        {
            "kind": "anthropic_flt_verified_adapter_boundary_audit",
            "status": "ABSTRACT_ADAPTERS_ONLY_ROUTE_B_PHYSICAL_DENY",
            "evidence_level": "current-pin-axiom-provenance-audit",
            "semantic_boundary": (
                "Four abstract FLT-derived adapters may be maintained in an "
                "independent verified-adapter registry, while three wrappers or "
                "comparators remain candidate-only; none enters the Route-B physical registry."
            ),
            "sidecar": str(gbz.resolve()),
            "files": [ref(path) for path in files["GBZ"]],
            "verified_adapter_count": len(flt["verified_adapters"]),
            "candidate_only_count": len(flt["candidate_only"]),
            "routeb_isolation": flt["routeb_isolation"],
            "source_commit": "aa2d8b34692b16c70f699536de0d8e75b9a3e9ef",
            "registry_promoted": False,
            "formal_certificate_allowed": False,
        },
        {
            "kind": "routeb_formalizable_dispatch_integration",
            "status": "FOCUSED_PATCH_VERIFIED_FORMAL_GATE_UNCHANGED",
            "evidence_level": "opt-in-host-dispatch-policy",
            "semantic_boundary": (
                "prepare_requests now accepts math_lane_policy=formalizable and "
                "filters numerical blockers through rank_formalizable_frontier; "
                "ordinary dispatch remains backward compatible."
            ),
            "files": [ref(path) for path in local],
            "focused_tests": "23 targeted assertions across math frontier, scheduler, reduction, residual and bridge paths",
            "registry_promoted": False,
            "formal_certificate_allowed": False,
        },
    ]
    graph.setdefault("bottleneck_audits", []).extend(audits)
    graph.setdefault("external_intakes", []).extend({
        "kind": audit["kind"], "source": "independent-sidecars:GBX-GBY-GBZ+local-dispatch",
        "sidecar": audit.get("sidecar"), "files": audit["files"],
        "registry_promoted": False, "formal_certificate_allowed": False,
    } for audit in audits)
    graph.setdefault("open_frontier_updates", []).extend({
        "node": audit["kind"], "status": "open_or_advisory_only",
        "reason": audit["semantic_boundary"],
    } for audit in audits)
    graph.update(schema="routeb-proposed-proof-dag-v210", supersedes=old.name)
    new.write_text(json.dumps(graph, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if not backup.exists():
        backup.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(store.path, backup)
    digest = sha(new)
    state.graph_artifacts.append({
        "schema_version": 1,
        "algorithm": "routeb_revision256_q1_mbd_flt/v1",
        "graph_sha256": digest, "roots": [], "selected_nodes": [],
        "source": "independent-sidecars:GBX,GBY,GBZ+local-formalizable-dispatch",
        "evidence_sha256": {
            name: {path.name: sha(path) for path in paths}
            for name, paths in files.items()
        },
        "strict_compile": False,
        "registry_promoted": False,
        "formal_certificate_allowed": False,
    })
    state.event(
        "routeb_revision256_q1_mbd_flt_recorded",
        proposed_dag=ref(new), proposed_dag_sha256=digest,
        audits=[{"kind": audit["kind"], "status": audit["status"]} for audit in audits],
        scheduler_policy="formalizable-opt-in",
        registry_promoted=False, formal_certificate_allowed=False,
        broad_regression_run=False,
    )
    store.save(state)
    print({"revision": state.revision, "graph": new.name, "registry": len(state.registry)})


if __name__ == "__main__":
    main()
