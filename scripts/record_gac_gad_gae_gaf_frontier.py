"""Persist the GAC-GAF frontier results as append-only research evidence."""
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
    assert state.revision == 227 and not state.registry
    old = ROOT / "artifacts/routeb_6dof/block45-obligations-v181.json"
    new = ROOT / "artifacts/routeb_6dof/block45-obligations-v182.json"
    backup = ROOT / "artifacts/routeb_storage_checkpoint_20260907/state-before-revision228.json"
    specs = [
        ("task_GAC_existing_bridge_composition_20260907", ["REPORT.md", "candidates.json", "provenance.md", "compile-evidence.md"], "existing_bridge_composition", "OPEN_FAIL_CLOSED", "The smallest source-mass bridge candidate still lacks FrameRecursion and did not compile."),
        ("task_GAD_schur_matrix_repair_20260907", ["REPORT.md", "GADSchurMatrixRepair.lean", "STATUS.md", "provenance.md", "strict_compile_shared_GA.log", "strict_compile_shared_GA_retry.log"], "matrix_schur_repair", "OPEN_FAIL_CLOSED", "The stronger explicit matrix Schur candidate has no valid olean because the pinned dependency cache/build failed."),
        ("task_GAE_flowpipe_budget_composition_20260907", ["REPORT.md", "theorem_leaves.json", "provenance.md"], "flowpipe_budget_composition", "CURRENT_PIN_STRICT_COMPILE_PASS_CANDIDATE_ONLY", "A conditional FirstExitSafe plus terminal-budget composition compiles, but upstream flowpipe and physical budget premises remain open."),
        ("task_GAF_cell_receipt_replay_20260907", ["REPORT.md", "missing_field_audit.json", "replay_checker.py", "provenance.md"], "cell_receipt_replay", "BLOCKED", "Existing artifacts cannot produce one complete replayable cell receipt; no enumeration or coverage claim."),
    ]
    assert old.is_file() and not new.exists()
    graph = json.loads(old.read_text(encoding="utf-8"))
    audits = []
    for dirname, names, node, status, reason in specs:
        sidecar = ROOT / "artifacts" / dirname
        files = [sidecar / name for name in names]
        assert all(path.is_file() for path in files)
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
            "kind": audit["kind"], "source": "local-routeb-gac-gad-gae-gaf-frontier",
            "sidecar": audit["sidecar"], "files": audit["files"],
            "registry_promoted": False, "formal_certificate_allowed": False,
        })
        graph.setdefault("open_frontier_updates", []).append({
            "node": audit["kind"], "status": status.lower(), "reason": reason,
        })
    graph.update(schema="routeb-proposed-proof-dag-v182", supersedes=old.name)
    new.write_text(json.dumps(graph, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if not backup.exists():
        backup.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(store.path, backup)
    digest = sha(new)
    state.graph_artifacts.append({
        "schema_version": 1, "algorithm": "routeb_gac_gad_gae_gaf_frontier/v1",
        "graph_sha256": digest, "roots": [], "selected_nodes": [],
        "source": "independent-sidecars:GAC,GAD,GAE,GAF",
        "evidence_sha256": sha(ROOT / "artifacts/task_GAE_flowpipe_budget_composition_20260907/theorem_leaves.json"),
        "registry_promoted": False, "formal_certificate_allowed": False,
    })
    state.event(
        "routeb_gac_gad_gae_gaf_frontier_recorded", proposed_dag=ref(new),
        proposed_dag_sha256=digest,
        audits=[{"kind": x["kind"], "status": x["status"]} for x in audits],
        registry_promoted=False, formal_certificate_allowed=False,
        broad_regression_run=False,
    )
    store.save(state)
    print({"revision": state.revision, "graph": new.name, "audits": len(audits), "registry": len(state.registry)})


if __name__ == "__main__":
    main()
