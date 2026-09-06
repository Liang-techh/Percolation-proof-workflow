"""Persist the GAC-GAF frontier batch and its Lean outcomes."""
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
    assert state.revision == 228 and not state.registry
    old = ROOT / "artifacts/routeb_6dof/block45-obligations-v182.json"
    new = ROOT / "artifacts/routeb_6dof/block45-obligations-v183.json"
    backup = ROOT / "artifacts/routeb_storage_checkpoint_20260907/state-before-revision229.json"
    specs = [
        ("task_GAC_existing_bridge_composition_20260907", ["REPORT.md", "candidates.json", "provenance.md", "compile-evidence.md"], "existing_bridge_composition", "OPEN_FAIL_CLOSED", "Source-mass bridge candidate lacks FrameRecursion and did not compile."),
        ("task_GAH_matrix_schur_repair2_20260907", ["MatrixSchur.lean", "STATUS.md", "compile_strict_lean4331.log", "compile_strict_final.log", "compile_ga_environment.log", "lakefile.toml", "lean-toolchain"], "matrix_schur_repair2", "OPEN_FAIL_CLOSED", "Explicit matrix Schur proof remains unresolved with invalid proof goals and no accepted olean; failure history is preserved."),
        ("task_GAE_flowpipe_budget_composition_20260907", ["REPORT.md", "theorem_leaves.json", "provenance.md"], "flowpipe_budget_composition2", "CURRENT_PIN_STRICT_COMPILE_PASS_CANDIDATE_ONLY", "Conditional FirstExitSafe plus terminal-budget composition compiles; physical flowpipe and budget premises remain open."),
        ("task_GAF_cell_receipt_replay_20260907", ["REPORT.md", "missing_field_audit.json", "replay_checker.py", "provenance.md"], "cell_receipt_replay2", "BLOCKED", "Rank-0 sparse join still lacks six exact receipt field groups; enumeration remains zero."),
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
            "kind": audit["kind"], "source": "local-routeb-gac-gad-gae-gaf",
            "sidecar": audit["sidecar"], "files": audit["files"],
            "registry_promoted": False, "formal_certificate_allowed": False,
        })
        graph.setdefault("open_frontier_updates", []).append({
            "node": audit["kind"], "status": status.lower(), "reason": reason,
        })
    graph.update(schema="routeb-proposed-proof-dag-v183", supersedes=old.name)
    new.write_text(json.dumps(graph, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if not backup.exists():
        backup.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(store.path, backup)
    digest = sha(new)
    state.graph_artifacts.append({
        "schema_version": 1, "algorithm": "routeb_gac_gad_gae_gaf/v1",
        "graph_sha256": digest, "roots": [], "selected_nodes": [],
        "source": "independent-sidecars:GAC,GAH,GAE,GAF",
        "evidence_sha256": sha(ROOT / "artifacts/task_GAE_flowpipe_budget_composition_20260907/theorem_leaves.json"),
        "registry_promoted": False, "formal_certificate_allowed": False,
    })
    state.event(
        "routeb_gac_gad_gae_gaf_recorded", proposed_dag=ref(new),
        proposed_dag_sha256=digest,
        audits=[{"kind": x["kind"], "status": x["status"]} for x in audits],
        registry_promoted=False, formal_certificate_allowed=False,
        broad_regression_run=False,
    )
    store.save(state)
    print({"revision": state.revision, "graph": new.name, "audits": len(audits), "registry": len(state.registry)})


if __name__ == "__main__":
    main()
