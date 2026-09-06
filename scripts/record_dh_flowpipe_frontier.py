"""Record the FY-FZ-GA-GB frontier results as durable, fail-closed evidence."""
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
    assert state.revision == 222 and not state.registry
    old = ROOT / "artifacts/routeb_6dof/block45-obligations-v176.json"
    new = ROOT / "artifacts/routeb_6dof/block45-obligations-v177.json"
    backup = ROOT / "artifacts/routeb_storage_checkpoint_20260907/state-before-revision223.json"
    specs = [
        ("task_FY_true_dh_source_binding_20260907", ["REPORT.md", "obligations.json", "provenance.md"], "source_binding", "OPEN_FAIL_CLOSED", "Exact deployed true-DH RHS and residual source binding remain unclosed."),
        ("task_FZ_single_cell_receipt_probe_20260907", ["REPORT.md", "probe.json", "provenance.md", "check_probe.py"], "single_cell_receipt", "BLOCKED", "Sparse data identifies a cell but cannot produce one replayable exact receipt; no enumeration or coverage claim."),
        ("task_GA_schur_block_lean_20260907", ["SchurBlockLowerBound.lean", "REPORT.md", "provenance.md", "compile_warningAsError.log", "strict_compile_final_20260907.log", "axioms.txt"], "schur_block_lean", "OPEN_FAIL_CLOSED", "Generic Schur sidecar has no valid olean after dependency/binder failures; failure history is retained."),
        ("task_GB_terminal_transfer_lean_20260907", ["TerminalTransferComposition.lean", "PROVENANCE.md", "compile_final.log", "strict_source_check.log", "strict_exit_code.txt"], "terminal_transfer_lean", "CURRENT_PIN_STRICT_COMPILE_PASS_CANDIDATE_ONLY", "Conditional terminal arithmetic compiles under the pinned kernel, but source binding, coverage and physical remainder remain open."),
    ]
    assert old.is_file() and not new.exists()
    graph = json.loads(old.read_text(encoding="utf-8"))
    audits = []
    for dirname, names, node, status, reason in specs:
        sidecar = ROOT / "artifacts" / dirname
        files = [sidecar / name for name in names]
        assert all(path.is_file() for path in files)
        audit = {
            "kind": f"routeb_{node}_audit",
            "status": status,
            "evidence_level": "independent_sidecar_frontier_audit",
            "semantic_boundary": reason,
            "sidecar": str(sidecar.resolve()),
            "files": [ref(path) for path in files],
            "registry_promoted": False,
            "formal_certificate_allowed": False,
        }
        audits.append(audit)
        graph.setdefault("bottleneck_audits", []).append(audit)
        graph.setdefault("external_intakes", []).append({
            "kind": audit["kind"], "source": "local-routeb-dh-flowpipe-frontier",
            "sidecar": audit["sidecar"], "files": audit["files"],
            "registry_promoted": False, "formal_certificate_allowed": False,
        })
        graph.setdefault("open_frontier_updates", []).append({
            "node": audit["kind"], "status": status.lower(), "reason": reason,
        })
    graph.update(schema="routeb-proposed-proof-dag-v177", supersedes=old.name)
    new.write_text(json.dumps(graph, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if not backup.exists():
        backup.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(store.path, backup)
    digest = sha(new)
    state.graph_artifacts.append({
        "schema_version": 1, "algorithm": "routeb_dh_flowpipe_frontier/v1",
        "graph_sha256": digest, "roots": [], "selected_nodes": [],
        "source": "independent-sidecars:FY,FZ,GA,GB",
        "evidence_sha256": sha(ROOT / "artifacts/task_GB_terminal_transfer_lean_20260907/TerminalTransferComposition.lean"),
        "registry_promoted": False, "formal_certificate_allowed": False,
    })
    state.event(
        "routeb_dh_flowpipe_frontier_recorded", proposed_dag=ref(new),
        proposed_dag_sha256=digest,
        audits=[{"kind": x["kind"], "status": x["status"]} for x in audits],
        registry_promoted=False, formal_certificate_allowed=False,
        broad_regression_run=False,
    )
    store.save(state)
    print({"revision": state.revision, "graph": new.name, "audits": len(audits), "registry": len(state.registry)})


if __name__ == "__main__":
    main()
