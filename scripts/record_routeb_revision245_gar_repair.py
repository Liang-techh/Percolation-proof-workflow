"""Persist the repaired exact-real residual/Schur Lean candidate."""
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
    assert state.revision == 244 and not state.registry
    old = ROOT / "artifacts/routeb_6dof/block45-obligations-v198.json"
    new = ROOT / "artifacts/routeb_6dof/block45-obligations-v199.json"
    backup = ROOT / "artifacts/routeb_storage_checkpoint_20260907/state-before-revision245.json"
    sidecar = ROOT / "artifacts/task_GAR_residual_schur_composition_20260907"
    files = [
        sidecar / "ResidualSchurComposition.lean",
        sidecar / "B45SchurResidualRepair.lean",
        sidecar / "REPORT.md",
        sidecar / "REPAIR_RECEIPT.md",
        sidecar / "output/repair2/ResidualSchurComposition.olean",
        sidecar / "output/repair2/ResidualSchurComposition.final.log",
    ]
    assert old.is_file() and not new.exists() and all(path.is_file() for path in files)
    graph = json.loads(old.read_text(encoding="utf-8"))
    reason = (
        "GAR exact-real six-residual plus remote-Schur composition now strict-compiles "
        "under the v4.33.1 pin after import-path and Vec2-namespace repairs; it remains "
        "conditional and candidate-only because deployed source binding and physical bounds are open."
    )
    audit = {
        "kind": "routeb_gar_residual_schur_repair_audit",
        "status": "CURRENT_PIN_STRICT_COMPILE_PASS_CANDIDATE_ONLY",
        "evidence_level": "independent_sidecar_repair_receipt",
        "semantic_boundary": reason, "sidecar": str(sidecar.resolve()),
        "files": [ref(path) for path in files], "registry_promoted": False,
        "formal_certificate_allowed": False,
        "olean_sha256": sha(sidecar / "output/repair2/ResidualSchurComposition.olean"),
        "axioms": ["propext", "Classical.choice", "Quot.sound"],
        "source_restrictions": {"sorry": False, "admit": False, "user_axiom": False},
    }
    graph.setdefault("bottleneck_audits", []).append(audit)
    graph.setdefault("external_intakes", []).append({
        "kind": audit["kind"], "source": "local-routeb-revision245-gar-repair",
        "sidecar": audit["sidecar"], "files": audit["files"],
        "registry_promoted": False, "formal_certificate_allowed": False,
    })
    graph.setdefault("open_frontier_updates", []).append({
        "node": audit["kind"], "status": "current_pin_strict_compile_pass_candidate_only", "reason": reason,
    })
    graph.update(schema="routeb-proposed-proof-dag-v199", supersedes=old.name)
    new.write_text(json.dumps(graph, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if not backup.exists():
        backup.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(store.path, backup)
    digest = sha(new)
    state.graph_artifacts.append({
        "schema_version": 1, "algorithm": "routeb_revision245_gar_repair/v1",
        "graph_sha256": digest, "roots": [], "selected_nodes": [],
        "source": "independent-sidecar:GAR-repaired-residual-schur-composition",
        "evidence_sha256": sha(sidecar / "output/repair2/ResidualSchurComposition.final.log"),
        "strict_compile": True, "registry_promoted": False,
        "formal_certificate_allowed": False,
    })
    state.event(
        "routeb_revision245_gar_repair_recorded", proposed_dag=ref(new),
        proposed_dag_sha256=digest, audit={"kind": audit["kind"], "status": audit["status"]},
        registry_promoted=False, formal_certificate_allowed=False, broad_regression_run=False,
    )
    store.save(state)
    print({"revision": state.revision, "graph": new.name, "registry": len(state.registry)})


if __name__ == "__main__":
    main()
