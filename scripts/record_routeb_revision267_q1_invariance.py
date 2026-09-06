"""Persist the exact-real q1/base-yaw mass-matrix invariance audit."""
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
    assert state.revision == 266 and not state.registry
    old = ROOT / "artifacts/routeb_6dof/block45-obligations-v220.json"
    new = ROOT / "artifacts/routeb_6dof/block45-obligations-v221.json"
    backup = ROOT / "artifacts/routeb_storage_checkpoint_20260907/state-before-revision267.json"
    sidecar = ROOT / "artifacts/task_GCO_q1_invariance_audit_20260907"
    files = [sidecar / "REPORT.md", sidecar / "receipt.json", sidecar / "checker.py"]
    assert old.is_file() and not new.exists() and all(path.is_file() for path in files)
    receipt = json.loads((sidecar / "receipt.json").read_text(encoding="utf-8"))
    graph = json.loads(old.read_text(encoding="utf-8"))
    audit = {
        "kind": "routeb_exact_real_q1_mass_matrix_invariance",
        "status": receipt.get("status"),
        "evidence_level": "source-level-exact-real-structural-audit",
        "sidecar": str(sidecar.resolve()), "files": [ref(path) for path in files],
        "invariant": "M(q1+alpha,q2,...,q6)=M(q1,q2,...,q6) in exact-real DH semantics",
        "invariant_blocks": ["M_BB", "M_BD", "M_DB", "M_DD"],
        "not_implied": ["Float64 bitwise equality", "natural interval enclosure", "rhs", "aD", "MBD*aD", "box_metrics h"],
        "next_frontier": "prove q1-gauge-fixed M_DD/M_BD directed-interval evaluator soundness",
        "coverage_complete": False, "registry_promoted": False,
        "formal_certificate_allowed": False,
        "semantic_boundary": "Exact mass-matrix invariance does not close residual, coverage, flowpipe, terminal transfer or comparator gates.",
    }
    graph.setdefault("bottleneck_audits", []).append(audit)
    graph.setdefault("external_intakes", []).append({
        "kind": audit["kind"], "source": "independent-sidecar:GCO-q1-invariance",
        "sidecar": audit["sidecar"], "files": audit["files"],
        "registry_promoted": False, "formal_certificate_allowed": False,
    })
    graph.setdefault("open_frontier_updates", []).append({
        "node": audit["kind"], "status": "exact_invariance_closed_interval_soundness_open",
        "reason": audit["next_frontier"],
    })
    graph.update(schema="routeb-proposed-proof-dag-v221", supersedes=old.name)
    new.write_text(json.dumps(graph, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if not backup.exists():
        backup.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(store.path, backup)
    digest = sha(new)
    state.graph_artifacts.append({
        "schema_version": 1, "algorithm": "routeb_revision267_q1_invariance/v1",
        "graph_sha256": digest, "roots": [], "selected_nodes": [],
        "source": "independent-sidecar:GCO-q1-invariance",
        "evidence_sha256": sha(sidecar / "receipt.json"), "strict_compile": False,
        "registry_promoted": False, "formal_certificate_allowed": False,
    })
    state.event("routeb_revision267_q1_invariance_recorded",
                proposed_dag=ref(new), proposed_dag_sha256=digest,
                exact_real_mass_matrix_invariance=True, interval_soundness_closed=False,
                rhs_invariance=False, residual_closed=False, registry_promoted=False,
                formal_certificate_allowed=False, broad_regression_run=False)
    store.save(state)
    print(json.dumps({"revision": state.revision, "graph": new.name,
                      "registry": len(state.registry), "formal_certificate_allowed": False}))


if __name__ == "__main__":
    main()
