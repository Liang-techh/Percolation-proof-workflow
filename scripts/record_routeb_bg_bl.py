"""Record the next bounded Route-B bottleneck audits without promotion."""
from __future__ import annotations

import hashlib
import json
import shutil
from pathlib import Path

from record_routeb_port_progress import ROOT, ref
from percolation_workflow.store import StateStore


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def files(*names: str) -> dict[str, Path]:
    result = {}
    for name in names:
        path = ROOT / name
        assert path.is_file(), path
        result[name] = path
    return result


def main() -> None:
    store = StateStore(ROOT / "artifacts/routeb_6dof/state.json")
    state = store.load()
    assert state.revision == 192 and not state.registry
    old_graph = ROOT / "artifacts/routeb_6dof/block45-obligations-v146.json"
    new_graph = ROOT / "artifacts/routeb_6dof/block45-obligations-v147.json"
    backup = ROOT / "artifacts/routeb_storage_checkpoint_20260906/state-before-revision193.json"
    assert old_graph.is_file() and not new_graph.exists()
    audits = [
        ("routeb_p3_float64_source_semantics", "FAIL_CLOSED_SOURCE_SEMANTICS_OPEN", "P3 source binding remains open", files("artifacts/task_BG_p3_float64_source_bound_20260906/REPORT.md", "artifacts/task_BG_p3_float64_source_bound_20260906/replay.json")),
        ("routeb_full_x0_produced_rhs_receipt", "CHECKER_STRENGTHENED_PAYLOAD_OPEN", "strict produced receipt checker exists; no authenticated RHS values", files("artifacts/task_BH_full_x0_rhs_receipt_20260906/REPORT.md", "artifacts/task_BH_full_x0_rhs_receipt_20260906/checker/check_produced_rhs_receipt.py", "artifacts/task_BH_full_x0_rhs_receipt_20260906/fixtures/produced_receipt_schema.json")),
        ("routeb_p4_delim_gram_witness", "CONDITIONAL_WITNESS_OPEN", "runtime SOS coefficients and exact Gram witness absent", files("artifacts/task_BI_p4_delim_gram_witness_20260906/REPORT.md", "artifacts/task_BI_p4_delim_gram_witness_20260906/replay.json")),
        ("routeb_schur_finite_cell_coverage", "ONE_CELL_PLUS_GAPS", "one-cell rho<1 guard replayed; coverage gaps explicit", files("artifacts/task_BJ_schur_cell_cover_20260906/REPORT.md", "artifacts/task_BJ_schur_cell_cover_20260906/schur_cell_cover_ledger.json", "artifacts/task_BJ_schur_cell_cover_20260906/check_schur_cell_cover.py")),
        ("routeb_s_d_payload_binding", "FAIL_CLOSED_PAYLOAD_OPEN", "same-state payload/hash/COMMIT checker exists; manifest and payload absent", files("artifacts/task_BK_sd_payload_binding_20260906/check_sd_payload_binding.py")),
        ("routeb_registry_parent_closure", "SAFE_TO_MUTATE_FALSE", "revision 192 registry empty; conditional and kernel metadata remain open", files("artifacts/task_BL_registry_parent_closure_20260906/REPORT.md", "artifacts/task_BL_registry_parent_closure_20260906/report.json", "artifacts/task_BL_registry_parent_closure_20260906/check_registry_closure.py")),
    ]
    graph = json.loads(old_graph.read_text(encoding="utf-8"))
    for kind, status, reason, evidence in audits:
        graph.setdefault("bottleneck_audits", []).append({
            "kind": kind, "status": status, "evidence_level": "bounded_sidecar_audit",
            "semantic_boundary": reason, "registry_promoted": False,
            "formal_certificate_allowed": False,
            "files": {k: {"path": ref(v), "sha256": sha(v)} for k, v in evidence.items()},
        })
        graph.setdefault("open_frontier_updates", []).append({
            "node": kind, "status": status.lower(), "reason": reason,
        })
    graph.update(schema="routeb-proposed-proof-dag-v147", supersedes=old_graph.name)
    new_graph.write_text(json.dumps(graph, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if not backup.exists():
        backup.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(store.path, backup)
    digest = sha(new_graph)
    for kind, _status, _reason, evidence in audits:
        first = next(iter(evidence.values()))
        state.graph_artifacts.append({
            "schema_version": 1, "algorithm": kind + "/v1", "graph_sha256": digest,
            "roots": [], "selected_nodes": [], "source": str(first),
            "evidence_sha256": sha(first), "registry_promoted": False,
            "formal_certificate_allowed": False,
        })
    state.event(
        "routeb_bg_bl_recorded", proposed_dag=ref(new_graph), proposed_dag_sha256=digest,
        audits=[kind for kind, _status, _reason, _evidence in audits],
        registry_promoted=False, formal_certificate_allowed=False,
        broad_regression_run=False,
    )
    store.save(state)
    print({"revision": state.revision, "graph": new_graph.name, "registry": len(state.registry)})


if __name__ == "__main__":
    main()
