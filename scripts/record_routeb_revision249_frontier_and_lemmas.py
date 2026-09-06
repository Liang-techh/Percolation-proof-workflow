"""Persist the narrow mathematical audits and formalizable frontier policy."""
from __future__ import annotations

import hashlib
import json
import shutil
from pathlib import Path

from record_routeb_port_progress import ROOT, ref
from percolation_workflow.store import StateStore


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def files_for(directory: Path, names: list[str]) -> list[Path]:
    paths = [directory / name for name in names]
    assert all(path.is_file() for path in paths), paths
    return paths


def main() -> None:
    store = StateStore(ROOT / "artifacts/routeb_6dof/state.json")
    state = store.load()
    assert state.revision == 248 and not state.registry
    old = ROOT / "artifacts/routeb_6dof/block45-obligations-v202.json"
    new = ROOT / "artifacts/routeb_6dof/block45-obligations-v203.json"
    backup = ROOT / "artifacts/routeb_storage_checkpoint_20260907/state-before-revision249.json"
    gbj = ROOT / "artifacts/task_GBJ_original_formula_lemma_20260907"
    gbk = ROOT / "artifacts/task_GBK_fullstate_closure_audit_20260907"
    gbl = ROOT / "artifacts/task_GBL_frontier_scheduler_audit_20260907"
    sidecars = {
        "GBJ": files_for(gbj, ["REPORT.md", "evidence.json"]),
        "GBK": files_for(gbk, ["REPORT.md", "evidence.json"]),
        "GBL": files_for(gbl, ["REPORT.md", "evidence.json"]),
    }
    source_files = [
        ROOT / "src/percolation_workflow/math_frontier.py",
        ROOT / "src/percolation_workflow/__init__.py",
        ROOT / "tests/test_math_frontier_policy.py",
    ]
    assert old.is_file() and not new.exists() and all(path.is_file() for path in source_files)
    graph = json.loads(old.read_text(encoding="utf-8"))

    gbj_reason = (
        "A sound local interval box with bound_hi-l2_lo<0 is pointwise negative "
        "for h=bound-||l||^2, hence it cannot satisfy h>=0."
    )
    gbk_reason = (
        "The full-state descriptor seam remains open: same-key q/dq/t/w, "
        "physical MBD_aD, remainder reconciliation, Schur margin, coverage, "
        "flowpipe and terminal receipts are missing."
    )
    gbl_reason = (
        "The default scheduler does not consult math_lane; the opt-in "
        "rank_formalizable_frontier filters known numerical blockers while "
        "leaving ordinary scheduling and formal admission unchanged."
    )
    audits = [
        {
            "kind": "routeb_original_formula_local_negative_box_lemma",
            "status": "OPEN_FAIL_CLOSED",
            "evidence_level": "narrow-mathematical-audit",
            "semantic_boundary": gbj_reason,
            "sidecar": str(gbj.resolve()),
            "files": [ref(path) for path in sidecars["GBJ"]],
            "local_lemma": "bound_hi-l2_lo<0 => forall x in box, h(x)<0",
            "registry_promoted": False,
            "formal_certificate_allowed": False,
        },
        {
            "kind": "routeb_fullstate_descriptor_closure_audit",
            "status": "FAIL_CLOSED",
            "evidence_level": "full-state-interface-audit",
            "semantic_boundary": gbk_reason,
            "sidecar": str(gbk.resolve()),
            "files": [ref(path) for path in sidecars["GBK"]],
            "missing_receipts": [
                "N1_full_state_domain", "N2_source_comparator", "N3_remote_action",
                "N4_remainder", "N5_physical_schur", "N6_continuation_and_terminal",
            ],
            "registry_promoted": False,
            "formal_certificate_allowed": False,
        },
        {
            "kind": "routeb_formalizable_frontier_scheduler_policy",
            "status": "ENGINEERING_POLICY_COMPLETE_FORMAL_GATE_UNCHANGED",
            "evidence_level": "workflow-api-focused-tests",
            "semantic_boundary": gbl_reason,
            "sidecar": str(gbl.resolve()),
            "files": [ref(path) for path in sidecars["GBL"] + source_files],
            "api": "rank_formalizable_frontier",
            "mode": "opt_in",
            "filters": ["MathLane.NUMERICAL_BLOCKER"],
            "focused_tests": "19 passed",
            "registry_promoted": False,
            "formal_certificate_allowed": False,
        },
    ]
    graph.setdefault("bottleneck_audits", []).extend(audits)
    graph.setdefault("external_intakes", []).extend({
        "kind": audit["kind"],
        "source": "independent-sidecar:GBJ-GBK-GBL",
        "sidecar": audit["sidecar"],
        "files": audit["files"],
        "registry_promoted": False,
        "formal_certificate_allowed": False,
    } for audit in audits)
    graph.setdefault("open_frontier_updates", []).extend({
        "node": audit["kind"], "status": "open_missing_data",
        "reason": audit["semantic_boundary"],
    } for audit in audits)
    graph.update(schema="routeb-proposed-proof-dag-v203", supersedes=old.name)
    new.write_text(json.dumps(graph, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if not backup.exists():
        backup.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(store.path, backup)
    digest = sha(new)
    state.graph_artifacts.append({
        "schema_version": 1,
        "algorithm": "routeb_revision249_frontier_and_lemmas/v1",
        "graph_sha256": digest,
        "roots": [], "selected_nodes": [],
        "source": "independent-sidecars:GBJ,GBK,GBL",
        "evidence_sha256": {name: sha(paths[1]) for name, paths in sidecars.items()},
        "strict_compile": False,
        "registry_promoted": False,
        "formal_certificate_allowed": False,
    })
    state.event(
        "routeb_revision249_frontier_and_lemmas_recorded",
        proposed_dag=ref(new), proposed_dag_sha256=digest,
        audits=[{"kind": audit["kind"], "status": audit["status"]} for audit in audits],
        scheduler_api="rank_formalizable_frontier",
        registry_promoted=False, formal_certificate_allowed=False,
        broad_regression_run=False,
    )
    store.save(state)
    print({"revision": state.revision, "graph": new.name, "registry": len(state.registry)})


if __name__ == "__main__":
    main()
