"""Record the exact Fourier/canonical source-membership negative result."""
from __future__ import annotations

import hashlib
import json
import shutil
from pathlib import Path

from record_routeb_port_progress import ROOT, ref
from percolation_workflow.store import StateStore


CANONICAL_INTERVAL_SHA = (
    "03679c7b686842ef9504886614e3498fb9fbf4a6c1466f8e44dcc505d21e3609"
)


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    store = StateStore(ROOT / "artifacts/routeb_6dof/state.json")
    state = store.load()
    if state.revision != 312 or state.registry:
        raise ValueError("revision-313 recorder requires revision 312 and empty registry")

    side = ROOT / "artifacts/task_routeb_mass_source_membership_current"
    report = ROOT / "artifacts/task_routeb_revision313_source_membership_failure/REPORT.md"
    result = side / "CHECK_RESULT.json"
    checker = side / "check_source_membership.py"
    if not all(p.is_file() for p in (report, result, checker)):
        raise ValueError("missing revision-313 evidence")

    check = json.loads(result.read_text(encoding="utf-8"))
    hashes = check.get("source_hashes", {})
    containment = check.get("containment", {})
    if check.get("status") != "FAIL_SIDECAR_OUTER_DOES_NOT_CONTAIN_CANONICAL_MASS_BOX":
        raise ValueError("unexpected source-membership status")
    if check.get("canonical_export", {}).get("entry_count") != 36:
        raise ValueError("source-membership checker did not inspect the full 6x6 matrix")
    if containment.get("failed_entry_count", 0) <= 0:
        raise ValueError("negative source-membership evidence is absent")
    if hashes.get("canonical") != CANONICAL_INTERVAL_SHA:
        raise ValueError("canonical interval source hash drifted")

    old = ROOT / "artifacts/routeb_6dof/block45-obligations-v266.json"
    new = ROOT / "artifacts/routeb_6dof/block45-obligations-v267.json"
    graph = json.loads(old.read_text(encoding="utf-8"))
    record = {
        "kind": "routeb_exact_source_membership_negative",
        "status": check["status"],
        "evidence_level": "exact-pointwise-enclosure-comparison-negative",
        "files": [ref(report), ref(result), ref(checker)],
        "canonical_interval_source_sha256": CANONICAL_INTERVAL_SHA,
        "matrix_entries_checked": check["canonical_export"]["entry_count"],
        "source_membership_failure_count": containment["failed_entry_count"],
        "minimum_lower_margin_decimal": containment["minimum_lower_margin_decimal"],
        "minimum_upper_margin_decimal": containment["minimum_upper_margin_decimal"],
        "exact_sidecar_outer_enclosure_inside_canonical": False,
        "registry_promoted": False,
        "formal_certificate_allowed": False,
    }
    graph.setdefault("bottleneck_audits", []).append(record)
    graph.setdefault("repair_audits", []).append({
        "kind": "source_membership_repair_required",
        "status": "open",
        "blocked_by": "exact Fourier sidecar is not semantically enclosed by canonical interval payload",
        "negative_evidence": ref(result),
        "registry_promoted": False,
        "formal_certificate_allowed": False,
    })
    graph.setdefault("workflow_hardening", []).append(record)
    graph.setdefault("open_frontier_updates", []).append({
        "node": "B45-1_bind_regularized_mass_entries_to_Fourier_evaluator",
        "status": "source_membership_failed",
        "reason": "exact sidecar and canonical interval payload fail both enclosure directions on one pinned box; physical DH identity remains open",
        "evidence": ref(result),
    })
    graph.update(schema="routeb-proposed-proof-dag-v267", supersedes=old.name)
    new.write_text(json.dumps(graph, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    checkpoint = ROOT / "artifacts/routeb_storage_checkpoint_20260908/state-before-revision313.json"
    if not checkpoint.exists():
        checkpoint.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(store.path, checkpoint)

    graph_sha = sha(new)
    state.graph_artifacts.append({
        "schema_version": 1,
        "algorithm": "routeb_revision313_source_membership_failure/v1",
        "graph_sha256": graph_sha,
        "roots": [],
        "selected_nodes": [],
        "evidence_sha256": sha(report),
        "checker_sha256": sha(checker),
        "result_sha256": sha(result),
        "canonical_interval_source_sha256": CANONICAL_INTERVAL_SHA,
        "exact_source_membership_closed": False,
        "registry_promoted": False,
        "formal_certificate_allowed": False,
    })
    state.event(
        "routeb_revision313_source_membership_failure_recorded",
        proposed_dag=ref(new),
        proposed_dag_sha256=graph_sha,
        exact_sidecar_outer_enclosure_inside_canonical=False,
        canonical_interval_inside_exact_sidecar_outer_enclosure=False,
        matrix_entries_checked=check["canonical_export"]["entry_count"],
        source_membership_failure_count=containment["failed_entry_count"],
        registry_promoted=False,
        formal_certificate_allowed=False,
        broad_regression_run=False,
    )
    store.save(state)
    print(json.dumps({
        "revision": state.revision,
        "graph": new.name,
        "registry": len(state.registry),
        "formal_certificate_allowed": False,
    }))


if __name__ == "__main__":
    main()
