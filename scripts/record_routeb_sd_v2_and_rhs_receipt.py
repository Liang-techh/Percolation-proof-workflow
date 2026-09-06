"""Record the corrected S-D export contract and RHS receipt boundary."""
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
    assert state.revision == 187 and not state.registry
    old_graph = ROOT / "artifacts/routeb_6dof/block45-obligations-v141.json"
    new_graph = ROOT / "artifacts/routeb_6dof/block45-obligations-v142.json"
    backup = ROOT / "artifacts/routeb_storage_checkpoint_20260906/state-before-revision188.json"
    assert old_graph.is_file() and not new_graph.exists()
    at = ROOT / "artifacts/task_AT_sd_export_patch_20260906"
    at_files = {name: at / name for name in (
        "README.md", "routeB_export_traj_sd_source_patch_v2.unified.diff",
        "sd_source_witness_manifest.schema.json")}
    rhs = ROOT / "artifacts/routeb_agent_AS_rhs_lipschitz_receipt_20260906"
    rhs_files = {name: rhs / name for name in (
        "rhs_local_lipschitz_receipt.json", "check_rhs_local_lipschitz_receipt.py", "README.md")}
    au = ROOT / "artifacts/task_AU_routeb_pmi_export_v2"
    au_files = {name: au / name for name in ("contract.json", "check_routeb_pmi_export_v2.py", "REPORT.md")}
    for path in (*at_files.values(), *rhs_files.values(), *au_files.values()):
        assert path.is_file(), path
    graph = json.loads(old_graph.read_text(encoding="utf-8"))
    graph.setdefault("bottleneck_audits", []).append({
        "kind": "routeb_s_d_export_patch_v2",
        "status": "SELF_CONSISTENT_PATCH_NOT_APPLIED",
        "evidence_level": "reviewable_fail_closed_source_patch",
        "semantic_boundary": "Julia was not executed and no CSV witness or coverage certificate exists",
        "registry_promoted": False, "formal_certificate_allowed": False,
        "files": {key: {"path": ref(path), "sha256": sha(path)} for key, path in at_files.items()},
    })
    graph.setdefault("open_frontier_updates", []).append({
        "node": "RouteBSchur.s_D_export_patch_v2",
        "status": "patch_review_ready_runtime_open",
        "reason": "same-k state, regularized/physical split, column order, residuals and atomic manifest are specified; patch remains unapplied",
    })
    graph.setdefault("bottleneck_audits", []).append({
        "kind": "routeb_rhs_local_lipschitz_receipt",
        "status": "FAIL_CLOSED_INVERSE_AND_FLOAT64_GAP",
        "evidence_level": "source_bound_receipt_schema",
        "semantic_boundary": "no inverse guard or deployed Float64/regularization RHS binding is supplied",
        "registry_promoted": False, "formal_certificate_allowed": False,
        "files": {key: {"path": ref(path), "sha256": sha(path)} for key, path in rhs_files.items()},
    })
    graph["open_frontier_updates"].append({
        "node": "RouteBFlowpipe.RHS_local_Lipschitz_receipt",
        "status": "receipt_schema_guard_open",
        "reason": "source fields and hashes are checked; M inverse guard and Float64/regularized exact semantics remain missing",
    })
    graph.setdefault("bottleneck_audits", []).append({
        "kind": "routeb_pmi_export_v2_gram_contract",
        "status": "FAIL_CLOSED_EXACT_GRAM_MISSING",
        "evidence_level": "independent_gram_checker_contract",
        "semantic_boundary": "no exact coefficient or exact Gram witness has been exported",
        "exact_coefficients": False, "exact_gram": False, "promotion_allowed": False,
        "registry_promoted": False, "formal_certificate_allowed": False,
        "files": {key: {"path": ref(path), "sha256": sha(path)} for key, path in au_files.items()},
    })
    graph["open_frontier_updates"].append({
        "node": "RouteBP4.independent_gram_checker",
        "status": "contract_ready_exact_export_open",
        "reason": "stable names, basis and reconstruction checks are specified; source export and exact Gram witness are absent",
    })
    graph.update(schema="routeb-proposed-proof-dag-v142", supersedes=old_graph.name)
    new_graph.write_text(json.dumps(graph, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if not backup.exists():
        backup.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(store.path, backup)
    digest = sha(new_graph)
    for algorithm, source, extra in (
        ("routeb_s_d_export_patch_v2/v1", at_files["sd_source_witness_manifest.schema.json"], {"schema_sha256": sha(at_files["sd_source_witness_manifest.schema.json"])}),
        ("routeb_rhs_local_lipschitz_receipt/v1", rhs_files["rhs_local_lipschitz_receipt.json"], {"receipt_sha256": sha(rhs_files["rhs_local_lipschitz_receipt.json"])}),
        ("routeb_pmi_export_v2_gram_contract/v1", au_files["contract.json"], {"contract_sha256": sha(au_files["contract.json"])}),
    ):
        state.graph_artifacts.append({
            "schema_version": 1, "algorithm": algorithm, "graph_sha256": digest,
            "roots": [], "selected_nodes": [], "source": str(source), **extra,
            "registry_promoted": False, "formal_certificate_allowed": False,
        })
    state.event(
        "routeb_sd_v2_and_rhs_receipt_recorded", proposed_dag=ref(new_graph),
        proposed_dag_sha256=digest, sd_patch=ref(at_files["routeB_export_traj_sd_source_patch_v2.unified.diff"]),
        sd_patch_sha256=sha(at_files["routeB_export_traj_sd_source_patch_v2.unified.diff"]),
        rhs_receipt=ref(rhs_files["rhs_local_lipschitz_receipt.json"]),
        rhs_receipt_sha256=sha(rhs_files["rhs_local_lipschitz_receipt.json"]),
        registry_promoted=False, formal_certificate_allowed=False, broad_regression_run=False,
    )
    store.save(state)
    print({"revision": state.revision, "graph": new_graph.name, "registry": len(state.registry)})


if __name__ == "__main__":
    main()
