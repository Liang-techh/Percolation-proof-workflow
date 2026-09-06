"""Persist full-state Lean binding candidate and interval soundness obligations."""
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
    assert state.revision == 267 and not state.registry
    old = ROOT / "artifacts/routeb_6dof/block45-obligations-v221.json"
    new = ROOT / "artifacts/routeb_6dof/block45-obligations-v222.json"
    backup = ROOT / "artifacts/routeb_storage_checkpoint_20260907/state-before-revision268.json"
    gcp = ROOT / "artifacts/task_GCP_lean_fullstate_binding_candidate_20260907"
    gcs = ROOT / "artifacts/task_GCS_interval_soundness_obligations_20260907"
    files = [gcp / "REPORT.md", gcp / "receipt.json", gcp / "FullStateBindingCandidate.lean",
             gcp / "compile_strict.log", gcp / "checker.py", gcs / "REPORT.md",
             gcs / "receipt.json", gcs / "checker.py"]
    assert old.is_file() and not new.exists() and all(path.is_file() for path in files)
    gcp_receipt = json.loads((gcp / "receipt.json").read_text(encoding="utf-8"))
    gcs_receipt = json.loads((gcs / "receipt.json").read_text(encoding="utf-8"))
    graph = json.loads(old.read_text(encoding="utf-8"))
    binding = {
        "kind": "routeb_lean_fullstate_binding_candidate",
        "status": gcp_receipt.get("status"),
        "evidence_level": "pinned-zero-sorry-lean-candidate",
        "sidecar": str(gcp.resolve()), "files": [ref(path) for path in files[:5]],
        "strict_compile": gcp_receipt.get("strict_compile"),
        "contract": ["same source snapshot", "same full-state key", "ell=MBD.mulVec aD"],
        "reported_axioms": gcp_receipt.get("strict_compile", {}).get("reported_axioms", []),
        "physical_source_binding": False, "coverage_complete": False,
        "registry_promoted": False, "formal_certificate_allowed": False,
        "semantic_boundary": "Abstract binding only; no canonical DH runtime, interval containment, coverage, comparator or physical admission.",
    }
    interval = {
        "kind": "routeb_q1_directed_interval_soundness_obligations",
        "status": gcs_receipt.get("status"),
        "evidence_level": "static-proof-obligation-ledger",
        "sidecar": str(gcs.resolve()), "files": [ref(path) for path in files[5:]],
        "open_obligation_count": gcs_receipt.get("open_obligation_count", 7),
        "runtime_executions": gcs_receipt.get("runtime_executions", 0),
        "coverage_complete": False, "registry_promoted": False,
        "formal_certificate_allowed": False,
        "semantic_boundary": "Obligation decomposition only; no interval theorem or global coverage is discharged.",
    }
    graph.setdefault("bottleneck_audits", []).extend([binding, interval])
    graph.setdefault("external_intakes", []).extend([
        {"kind": binding["kind"], "source": "independent-sidecar:GCP-lean-fullstate-binding",
         "sidecar": binding["sidecar"], "files": binding["files"],
         "registry_promoted": False, "formal_certificate_allowed": False},
        {"kind": interval["kind"], "source": "independent-sidecar:GCS-interval-soundness",
         "sidecar": interval["sidecar"], "files": interval["files"],
         "registry_promoted": False, "formal_certificate_allowed": False},
    ])
    graph.setdefault("open_frontier_updates", []).extend([
        {"node": binding["kind"], "status": "abstract_binding_candidate_physical_open",
         "reason": binding["semantic_boundary"]},
        {"node": interval["kind"], "status": "seven_soundness_obligations_open",
         "reason": interval["semantic_boundary"]},
    ])
    graph.update(schema="routeb-proposed-proof-dag-v222", supersedes=old.name)
    new.write_text(json.dumps(graph, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if not backup.exists():
        backup.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(store.path, backup)
    digest = sha(new)
    state.graph_artifacts.append({
        "schema_version": 1, "algorithm": "routeb_revision268_fullstate_interval/v1",
        "graph_sha256": digest, "roots": [], "selected_nodes": [],
        "source": "independent-sidecars:GCP-plus-GCS",
        "evidence_sha256": sha(gcp / "receipt.json"), "strict_compile": True,
        "registry_promoted": False, "formal_certificate_allowed": False,
    })
    state.event("routeb_revision268_fullstate_interval_recorded",
                proposed_dag=ref(new), proposed_dag_sha256=digest,
                fullstate_lean_candidate=True, physical_binding_closed=False,
                interval_obligations_open=interval["open_obligation_count"],
                registry_promoted=False, formal_certificate_allowed=False,
                broad_regression_run=False)
    store.save(state)
    print(json.dumps({"revision": state.revision, "graph": new.name,
                      "interval_obligations_open": interval["open_obligation_count"],
                      "registry": len(state.registry)}))


if __name__ == "__main__":
    main()
