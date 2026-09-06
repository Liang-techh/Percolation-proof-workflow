"""Persist residual norm reconciliation and frontier dispatch improvements."""
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
    assert state.revision == 249 and not state.registry
    old = ROOT / "artifacts/routeb_6dof/block45-obligations-v203.json"
    new = ROOT / "artifacts/routeb_6dof/block45-obligations-v204.json"
    backup = ROOT / "artifacts/routeb_storage_checkpoint_20260907/state-before-revision250.json"
    gbn = ROOT / "artifacts/task_GBN_residual_norm_reconciliation_20260907"
    gbo = ROOT / "artifacts/task_GBO_branch_priority_signal_20260907"
    sidecars = {
        "GBN": require([gbn / "REPORT.md", gbn / "schema.json", gbn / "checker.py"]),
        "GBO": require([gbo / "REPORT.md", gbo / "signal.json", gbo / "checker.py"]),
    }
    source_files = require([
        ROOT / "src/percolation_workflow/math_frontier.py",
        ROOT / "src/percolation_workflow/__init__.py",
        ROOT / "tests/test_math_frontier_policy.py",
    ])
    assert old.is_file() and not new.exists()
    graph = json.loads(old.read_text(encoding="utf-8"))
    audits = [
        {
            "kind": "routeb_residual_norm_reconciliation_gate",
            "status": "FAIL_CLOSED",
            "evidence_level": "keyed-ledger-schema-checker",
            "semantic_boundary": (
                "The checker enforces six rho channels, one remainder_total, "
                "same full_state_key/source_snapshot, and rejects induced-2 "
                "versus induced-infinity mixing; no physical values are admitted."
            ),
            "sidecar": str(gbn.resolve()),
            "files": [ref(path) for path in sidecars["GBN"]],
            "formal_admission": "DENY",
            "registry_promoted": False,
            "formal_certificate_allowed": False,
        },
        {
            "kind": "routeb_advisory_q1_branch_priority_signal",
            "status": "ADVISORY_ONLY_DENY",
            "evidence_level": "same-cell-same-source-local-sensitivity",
            "semantic_boundary": (
                "q1 is only a local branch-priority suggestion under matching "
                "source hash, cell and metric; missing authoritative hashes, "
                "coverage and rho_lt_one keep formal admission denied."
            ),
            "sidecar": str(gbo.resolve()),
            "files": [ref(path) for path in sidecars["GBO"]],
            "suggested_coordinate": "q1",
            "formal_admission": "DENY",
            "registry_promoted": False,
            "formal_certificate_allowed": False,
        },
        {
            "kind": "routeb_math_lane_domain_classifier",
            "status": "ENGINEERING_POLICY_COMPLETE_FORMAL_GATE_UNCHANGED",
            "evidence_level": "focused-test-verified-api",
            "semantic_boundary": (
                "Explicit Lean and external-research verification domains now "
                "fill legacy math-lane classification gaps; no theorem status "
                "or evidence stage is changed."
            ),
            "files": [ref(path) for path in source_files],
            "focused_tests": "20 passed",
            "formal_admission": "UNCHANGED",
            "registry_promoted": False,
            "formal_certificate_allowed": False,
        },
    ]
    graph.setdefault("bottleneck_audits", []).extend(audits)
    graph.setdefault("external_intakes", []).extend({
        "kind": audit["kind"], "source": "independent-sidecars:GBN-GBO-local-policy",
        "sidecar": audit["sidecar"] if "sidecar" in audit else None,
        "files": audit["files"], "registry_promoted": False,
        "formal_certificate_allowed": False,
    } for audit in audits)
    graph.setdefault("open_frontier_updates", []).extend({
        "node": audit["kind"], "status": "open_missing_data",
        "reason": audit["semantic_boundary"],
    } for audit in audits)
    graph.update(schema="routeb-proposed-proof-dag-v204", supersedes=old.name)
    new.write_text(json.dumps(graph, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if not backup.exists():
        backup.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(store.path, backup)
    digest = sha(new)
    state.graph_artifacts.append({
        "schema_version": 1,
        "algorithm": "routeb_revision250_norm_and_dispatch/v1",
        "graph_sha256": digest, "roots": [], "selected_nodes": [],
        "source": "independent-sidecars:GBN,GBO+local-math-lane-domain-classifier",
        "evidence_sha256": {
            name: {path.name: sha(path) for path in paths}
            for name, paths in sidecars.items()
        },
        "strict_compile": False, "registry_promoted": False,
        "formal_certificate_allowed": False,
    })
    state.event(
        "routeb_revision250_norm_and_dispatch_recorded",
        proposed_dag=ref(new), proposed_dag_sha256=digest,
        audits=[{"kind": audit["kind"], "status": audit["status"]} for audit in audits],
        formalizable_dispatch_api="rank_formalizable_frontier",
        registry_promoted=False, formal_certificate_allowed=False,
        broad_regression_run=False,
    )
    store.save(state)
    print({"revision": state.revision, "graph": new.name, "registry": len(state.registry)})


if __name__ == "__main__":
    main()
