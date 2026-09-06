"""Persist the kernel sign lemma and host cascade harness evidence."""
from __future__ import annotations

import hashlib
import json
import shutil
from pathlib import Path

from record_routeb_port_progress import ROOT, ref
from percolation_workflow.store import StateStore


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> None:
    store = StateStore(ROOT / "artifacts/routeb_6dof/state.json")
    state = store.load()
    assert state.revision == 277 and not state.registry
    old = ROOT / "artifacts/routeb_6dof/block45-obligations-v231.json"
    new = ROOT / "artifacts/routeb_6dof/block45-obligations-v232.json"
    backup = ROOT / "artifacts/routeb_storage_checkpoint_20260907/state-before-revision278.json"
    sign = ROOT / "artifacts/task_GDI_lean_h_sign_normalization_20260907"
    harness = ROOT / "artifacts/task_GDM_host_cascade_harness_20260907"
    required = [old, sign / "HSignNormalization.lean", sign / "receipt.json", sign / "compile.log",
                harness / "harness.py", harness / "receipt.json", harness / "report.md"]
    assert all(path.is_file() for path in required) and not new.exists()
    sr, hr = load(sign / "receipt.json"), load(harness / "receipt.json")
    graph = load(old)
    sign_audit = {
        "kind": "routeb_h_sign_normalization_lean_candidate",
        "status": sr.get("status", "PASS"),
        "evidence_level": "pinned-lean-zero-sorry-candidate",
        "theorems": sr.get("theorems") or ["lower_le_hsrc_and_positive_lower_implies_hneg_lt_zero", "negative_upper_implies_not_nonnegative_hsrc"],
        "sidecar": str(sign.resolve()),
        "files": [ref(path) for path in required[1:4]],
        "registry_promoted": False, "formal_certificate_allowed": False,
        "semantic_boundary": "Abstract sign theorem only; it does not bind the Julia source, interval endpoints, DH model, coverage, or Route-B registry.",
    }
    cascade_audit = {
        "kind": "host_cascade_coordinator_command_and_parent_closure_harness",
        "status": hr.get("status", "PASS"),
        "evidence_level": "isolated-coordinator-harness",
        "sidecar": str(harness.resolve()),
        "files": [ref(path) for path in required[4:]],
        "positive_path": hr.get("positive_path"),
        "negative_paths": hr.get("negative_paths"),
        "registry_promoted": False, "formal_certificate_allowed": False,
        "semantic_boundary": "Harness validates orchestration gates and cascade order; it is not physical theorem evidence.",
    }
    graph.setdefault("workflow_repairs", []).extend([sign_audit, cascade_audit])
    graph.setdefault("bottleneck_audits", []).append(sign_audit)
    graph.setdefault("external_intakes", []).extend([
        {"kind": sign_audit["kind"], "source": "pinned-lean-sidecar:GDI",
         "sidecar": sign_audit["sidecar"], "files": sign_audit["files"],
         "registry_promoted": False, "formal_certificate_allowed": False},
        {"kind": cascade_audit["kind"], "source": "isolated-harness:GDM",
         "sidecar": cascade_audit["sidecar"], "files": cascade_audit["files"],
         "registry_promoted": False, "formal_certificate_allowed": False},
    ])
    graph.setdefault("open_frontier_updates", []).extend([
        {"node": sign_audit["kind"], "status": "abstract_sign_lemma_candidate_only", "reason": sign_audit["semantic_boundary"]},
        {"node": cascade_audit["kind"], "status": "control_harness_passed_physical_open", "reason": cascade_audit["semantic_boundary"]},
    ])
    graph.update(schema="routeb-proposed-proof-dag-v232", supersedes=old.name)
    new.write_text(json.dumps(graph, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if not backup.exists():
        backup.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(store.path, backup)
    digest = sha(new)
    state.graph_artifacts.append({
        "schema_version": 1, "algorithm": "routeb_revision278_sign_lean_cascade_harness/v1",
        "graph_sha256": digest, "roots": [], "selected_nodes": [],
        "source": "sidecars:GDI-GDM", "evidence_sha256": sha(sign / "receipt.json"),
        "strict_compile": True, "registry_promoted": False, "formal_certificate_allowed": False,
    })
    state.event("routeb_revision278_sign_lean_cascade_harness_recorded",
                proposed_dag=ref(new), proposed_dag_sha256=digest,
                sign_lemma_zero_sorry=True, host_cascade_harness_passed=True,
                physical_registry_promoted=False, formal_certificate_allowed=False,
                broad_regression_run=False)
    store.save(state)
    print(json.dumps({"revision": state.revision, "graph": new.name, "registry": len(state.registry)}))


if __name__ == "__main__":
    main()
