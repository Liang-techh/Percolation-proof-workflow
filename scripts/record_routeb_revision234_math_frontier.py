"""Persist the targeted rho, residual-composition, and frontier-cut audits."""
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
    assert state.revision == 233 and not state.registry
    old = ROOT / "artifacts/routeb_6dof/block45-obligations-v187.json"
    new = ROOT / "artifacts/routeb_6dof/block45-obligations-v188.json"
    backup = ROOT / "artifacts/routeb_storage_checkpoint_20260907/state-before-revision234.json"
    assert old.is_file() and not new.exists()

    specs = [
        (
            "task_GAS_rho_shrink_probe_20260907",
            ["rho_shrink_probe.jl", "receipt.json", "REPORT.md"],
            "rho_shrink_probe",
            "OPEN_FAIL_CLOSED",
            "Two targeted q6 contractions leave rho_hi=26.4169425089 unchanged; the sufficient Neumann guard remains unresolved and coverage is false.",
        ),
        (
            "task_GAR_residual_schur_composition_20260907",
            ["ResidualSchurComposition.lean", "B45SchurResidualRepair.lean", "REPORT.md", "verify.sh"],
            "residual_schur_composition",
            "COMPILE_BLOCKED_ENVIRONMENT",
            "The intended exact-real six-term plus remote-Schur composition is staged, but the sidecar lacks a built Mathlib.olean aggregate for a reproducible strict compile.",
        ),
        (
            "task_GAT_frontier_cut_20260907",
            ["REPORT.md"],
            "frontier_cut",
            "OPEN_FAIL_CLOSED",
            "Eight M4 leaves are prioritized source binding -> rho/Schur -> flowpipe -> comparator; M4 remains open and no partial closure is permitted.",
        ),
    ]

    graph = json.loads(old.read_text(encoding="utf-8"))
    audits = []
    for dirname, names, node, status, reason in specs:
        sidecar = ROOT / "artifacts" / dirname
        files = [sidecar / name for name in names]
        assert all(path.is_file() for path in files), (dirname, names)
        audit = {
            "kind": f"routeb_{node}_audit", "status": status,
            "evidence_level": "independent_sidecar_frontier_audit",
            "semantic_boundary": reason, "sidecar": str(sidecar.resolve()),
            "files": [ref(path) for path in files],
            "registry_promoted": False, "formal_certificate_allowed": False,
        }
        audits.append(audit)
        graph.setdefault("bottleneck_audits", []).append(audit)
        graph.setdefault("external_intakes", []).append({
            "kind": audit["kind"], "source": "local-routeb-revision234-math-frontier",
            "sidecar": audit["sidecar"], "files": audit["files"],
            "registry_promoted": False, "formal_certificate_allowed": False,
        })
        graph.setdefault("open_frontier_updates", []).append({
            "node": audit["kind"], "status": status.lower(), "reason": reason,
        })
    graph.update(schema="routeb-proposed-proof-dag-v188", supersedes=old.name)
    new.write_text(json.dumps(graph, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if not backup.exists():
        backup.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(store.path, backup)

    digest = sha(new)
    state.graph_artifacts.append({
        "schema_version": 1, "algorithm": "routeb_revision234_math_frontier/v1",
        "graph_sha256": digest, "roots": [], "selected_nodes": [],
        "source": "independent-sidecars:GAS,GAR,GAT",
        "evidence_sha256": sha(ROOT / "artifacts/task_GAS_rho_shrink_probe_20260907/receipt.json"),
        "strict_compile": False, "registry_promoted": False,
        "formal_certificate_allowed": False,
    })
    state.event(
        "routeb_revision234_math_frontier_recorded", proposed_dag=ref(new),
        proposed_dag_sha256=digest,
        audits=[{"kind": x["kind"], "status": x["status"]} for x in audits],
        registry_promoted=False, formal_certificate_allowed=False,
        broad_regression_run=False,
    )
    store.save(state)
    print({"revision": state.revision, "graph": new.name, "audits": len(audits), "registry": len(state.registry)})


if __name__ == "__main__":
    main()
