"""Persist source-ledger, single-cell, composition, and M4 bridge evidence."""
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
    assert state.revision == 230 and not state.registry
    old = ROOT / "artifacts/routeb_6dof/block45-obligations-v184.json"
    new = ROOT / "artifacts/routeb_6dof/block45-obligations-v185.json"
    backup = ROOT / "artifacts/routeb_storage_checkpoint_20260907/state-before-revision231.json"
    specs = [
        ("task_GAK_source_ledger_exporter_20260907", ["exporter.py", "manifest.json", "REPORT.md", "provenance.md"], "source_ledger_exporter", "FAIL_CLOSED", "Rank-0 source manifest records three hashes but 14 numeric receipt fields are missing; exporter exits 2."),
        ("task_GAL_julia_single_cell_probe_20260907", ["receipt_or_missing.json", "REPORT.md", "provenance.md", "checker.py"], "julia_single_cell_probe", "BLOCKED", "Current Julia evaluator has no canonical cell-addressable replay interface; seven fields remain missing and enumeration is zero."),
        ("task_GAM_schur_terminal_composition_20260907", ["SchurTerminalComposition.lean", ".lake/build/lib/lean/SchurTerminalComposition.olean", "compile_strict.log", "axioms.txt", "REPORT.md", "provenance.md"], "schur_terminal_composition", "CURRENT_PIN_STRICT_COMPILE_PASS_CANDIDATE_ONLY", "Generic Schur and terminal-budget interfaces compose under the current pinned Lean kernel; physical premises remain open."),
        ("task_GAN_receipt_to_m4_bridge_audit_20260907", ["REPORT.md", "interface.json", "provenance.md"], "receipt_to_m4_bridge", "OPEN_FAIL_CLOSED", "Advisory m4_context can carry cell/source/domain hashes and six open premises; comparator and registry remain mandatory."),
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
            "kind": audit["kind"], "source": "local-routeb-gak-gal-gam-gan",
            "sidecar": audit["sidecar"], "files": audit["files"],
            "registry_promoted": False, "formal_certificate_allowed": False,
        })
        graph.setdefault("open_frontier_updates", []).append({
            "node": audit["kind"], "status": status.lower(), "reason": reason,
        })
    graph.update(schema="routeb-proposed-proof-dag-v185", supersedes=old.name)
    new.write_text(json.dumps(graph, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if not backup.exists():
        backup.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(store.path, backup)
    digest = sha(new)
    state.graph_artifacts.append({
        "schema_version": 1, "algorithm": "routeb_gak_gal_gam_gan_frontier/v1",
        "graph_sha256": digest, "roots": [], "selected_nodes": [],
        "source": "independent-sidecars:GAK,GAL,GAM,GAN",
        "evidence_sha256": sha(ROOT / "artifacts/task_GAM_schur_terminal_composition_20260907/compile_strict.log"),
        "strict_compile": True, "registry_promoted": False, "formal_certificate_allowed": False,
    })
    state.event(
        "routeb_gak_gal_gam_gan_frontier_recorded", proposed_dag=ref(new),
        proposed_dag_sha256=digest,
        audits=[{"kind": x["kind"], "status": x["status"]} for x in audits],
        registry_promoted=False, formal_certificate_allowed=False,
        broad_regression_run=False,
    )
    store.save(state)
    print({"revision": state.revision, "graph": new.name, "audits": len(audits), "registry": len(state.registry)})


if __name__ == "__main__":
    main()
