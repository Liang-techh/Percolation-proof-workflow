"""Record the fail-closed SOS/Gram export contract."""
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
    assert state.revision == 184 and not state.registry
    old_graph = ROOT / "artifacts/routeb_6dof/block45-obligations-v138.json"
    new_graph = ROOT / "artifacts/routeb_6dof/block45-obligations-v139.json"
    backup = ROOT / "artifacts/routeb_storage_checkpoint_20260906/state-before-revision185.json"
    assert old_graph.is_file() and not new_graph.exists()
    base = ROOT / "artifacts/routeb_agent_AM_export_contract_20260906"
    files = {name: base / name for name in ("README.md", "routeB_pmi_export_v2.patch")}
    ap = ROOT / "artifacts/task_AP_l0_l6_rebase_20260906"
    ap_files = {name: ap / name for name in (
        "rebased_proposal_revision184.json", "report.json", "REPORT.md", "SUMMARY.json",
        "stale_snapshot_rejection.json", "run_dry_run.py")}
    aq = ROOT / "artifacts/routeb_agent_p3_source_trig_dh_contract_20260906T180000Z"
    aq_files = {name: aq / name for name in ("REPORT.md", "contract.json", "contract.py")}
    for path in (*files.values(), *ap_files.values(), *aq_files.values()):
        assert path.is_file(), path
    graph = json.loads(old_graph.read_text(encoding="utf-8"))
    graph.setdefault("bottleneck_audits", []).append({
        "kind": "routeb_pmi_export_v2_contract",
        "status": "EXPORT_CONTRACT_READY_EXACT_WITNESS_MISSING",
        "evidence_level": "static_fail_closed_export_audit",
        "semantic_boundary": "current Float64 Gram/polynomial snapshots are not exact coefficients or exact Gram witnesses",
        "exact_coefficients": False, "exact_gram": False, "promotion_allowed": False,
        "registry_promoted": False, "formal_certificate_allowed": False,
        "files": {key: {"path": ref(path), "sha256": sha(path)} for key, path in files.items()},
    })
    graph.setdefault("open_frontier_updates", []).append({
        "node": "RouteBP4.SOS_Gram_exact_export",
        "status": "contract_ready_witness_open",
        "reason": "stable PMI names, variable basis, source roles and exactness flags are required before coefficient/Gram promotion",
    })
    graph.setdefault("bottleneck_audits", []).append({
        "kind": "routeb_l0_l6_revision184_rebase",
        "status": "DRY_RUN_REBASE_PASS_NO_INSTALL",
        "evidence_level": "snapshot_bound_dag_migration_audit",
        "semantic_boundary": "proposal is not installed and registry remains unchanged",
        "registry_promoted": False, "formal_certificate_allowed": False,
        "files": {key: {"path": ref(path), "sha256": sha(path)} for key, path in ap_files.items()},
    })
    graph.setdefault("open_frontier_updates", []).append({
        "node": "Workflow.DAG.L0_L6_revision184_rebase",
        "status": "fresh_dry_run_parent_open",
        "reason": "64 checks and acyclic combined DAG pass; actual child installation and proof evidence remain open",
    })
    graph.setdefault("bottleneck_audits", []).append({
        "kind": "routeb_p3_trig_dh_chain_contract",
        "status": "ATOMIC_TO_DH_CHAIN_CONTRACTIONAL_SOURCE_OPEN",
        "evidence_level": "conditional_exact_rational_taylor_chain",
        "semantic_boundary": "deployed Float64 trig binding, pi semantics, central-FD third derivative and rounding remain open",
        "registry_promoted": False, "formal_certificate_allowed": False,
        "files": {key: {"path": ref(path), "sha256": sha(path)} for key, path in aq_files.items()},
    })
    graph.setdefault("open_frontier_updates", []).append({
        "node": "RouteBP3.DH_trig_chain_source_binding",
        "status": "conditional_interval_parent_open",
        "reason": "one DH trig chain interval closes conditionally; center sin/cos source binding and FD semantics remain unresolved",
    })
    graph.update(schema="routeb-proposed-proof-dag-v139", supersedes=old_graph.name)
    new_graph.write_text(json.dumps(graph, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if not backup.exists():
        backup.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(store.path, backup)
    digest = sha(new_graph)
    state.graph_artifacts.append({
        "schema_version": 1, "algorithm": "routeb_pmi_export_v2_contract/v1",
        "graph_sha256": digest, "roots": [], "selected_nodes": [],
        "source": "fail-closed SOS/Gram export contract",
        "contract_sha256": sha(files["routeB_pmi_export_v2.patch"]),
        "exact_coefficients": False, "exact_gram": False,
        "registry_promoted": False, "formal_certificate_allowed": False,
    })
    state.graph_artifacts.append({
        "schema_version": 1, "algorithm": "routeb_l0_l6_revision184_rebase/v1",
        "graph_sha256": digest, "roots": [], "selected_nodes": [],
        "source": "revision-184 snapshot-bound L0-L6 dry-run rebase",
        "proposal_sha256": sha(ap_files["rebased_proposal_revision184.json"]),
        "registry_promoted": False, "formal_certificate_allowed": False,
    })
    state.graph_artifacts.append({
        "schema_version": 1, "algorithm": "routeb_p3_trig_dh_chain_contract/v1",
        "graph_sha256": digest, "roots": [], "selected_nodes": [],
        "source": "conditional DH trig chain exact-rational Taylor contract",
        "contract_sha256": sha(aq_files["contract.json"]),
        "registry_promoted": False, "formal_certificate_allowed": False,
    })
    state.event(
        "routeb_pmi_export_contract_recorded", proposed_dag=ref(new_graph),
        proposed_dag_sha256=digest, contract=ref(files["routeB_pmi_export_v2.patch"]),
        contract_sha256=sha(files["routeB_pmi_export_v2.patch"]),
        status="EXPORT_CONTRACT_READY_EXACT_WITNESS_MISSING", exact_coefficients=False,
        exact_gram=False, promotion_allowed=False, registry_promoted=False,
        formal_certificate_allowed=False, broad_regression_run=False,
    )
    store.save(state)
    print({"revision": state.revision, "graph": new_graph.name, "registry": len(state.registry)})


if __name__ == "__main__":
    main()
