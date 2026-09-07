"""Record the latest O1/O2/force interface reviews without false promotion."""
from __future__ import annotations

import hashlib
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
O1 = ROOT / "agent_review_inbox/review-T-P4-033-O1-source-export-minimal-canonical-receipt-codex-20260907.md"
O2 = ROOT / "agent_review_inbox/review-T-P4-036.2-theta2-real-branch-triple-export-plan-codex-20260907.md"
O2_RUNTIME = ROOT / "agent_review_inbox/review-T-P4-O2-BB-triple-julia-obstruction-codex-20260907.md"
FORCE = ROOT / "agent_review_inbox/review-T-P4-force-github-execution-blocked-codex-20260907.md"
FORCE_BLOCKER = ROOT / "agent_review_inbox/review-T-P4-force-github-execution-blocked-codex-20260907.md"
BRANCH = ROOT.parent / "6dof_sos_optimized" / "6dof_sos_optimized" / "routeB_dense_Mq" / "routeB_interval_branch_bound.jl"
BACKUP = Path(str(BRANCH) + ".bak_20260907_o2_triple")
STATE = ROOT / "artifacts/routeb_6dof/state.json"
sys.path.insert(0, str(ROOT / "src"))
from percolation_workflow.store import StateStore  # noqa: E402


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def find(state, name: str):
    for node in state.nodes.values():
        if node.name == name:
            return node
    raise ValueError(f"missing node: {name}")


def main() -> int:
    for path in (O1, O2, O2_RUNTIME, FORCE, FORCE_BLOCKER, BRANCH, BACKUP, STATE):
        if not path.is_file():
            raise FileNotFoundError(path)
    o1_text = O1.read_text(encoding="utf-8", errors="replace")
    o2_text = O2.read_text(encoding="utf-8", errors="replace")
    o2_runtime_text = O2_RUNTIME.read_text(encoding="utf-8", errors="replace")
    force_text = FORCE.read_text(encoding="utf-8", errors="replace")
    for phrase in (
        "PARTIAL_SOURCE_EXPORT",
        "OPEN_TYPED_SOURCE_INHABITANT",
        "h_source_mass or (h_aggregate and h_body)",
        "M_authoritative = M_fourier + mu * I",
    ):
        if phrase not in o1_text:
            raise ValueError(f"O1 partial export boundary missing: {phrase}")
    for phrase in (
        "no real theta2 triple receipt",
        "PENDING_EXTERNAL_PREMISES",
        "routeb-theta2-canonical-coverage-v1",
        "source interval membership",
        "CoverageJoin2",
    ):
        if phrase not in o2_text:
            raise ValueError(f"O2 triple export boundary missing: {phrase}")
    for phrase in (
        "BLOCKED_NO_JULIA_RUNTIME",
        "JULIA_FOUND=False",
        "P3_BB_TRIPLE_CELL_ID",
        "PENDING / READY",
        "未验证用户所述",
    ):
        if phrase not in o2_runtime_text:
            raise ValueError(f"O2 triple runtime obstruction missing: {phrase}")
    for phrase in (
        "BLOCKED_WORKFLOW_NOT_LANDED",
        "force-general-state-export.yml",
        "workflow list",
        "未生成 CSV/receipt",
    ):
        if phrase not in force_text:
            raise ValueError(f"force GitHub blocker boundary missing: {phrase}")
    current_hash, backup_hash = sha(BRANCH), sha(BACKUP)
    if current_hash == backup_hash:
        raise ValueError("O2 branch exporter patch did not change the source")
    o1node = None
    store = StateStore(STATE)
    state = store.load()
    o1node = find(state, "P4.true_dh_exact_real_coefficient_identity")
    o2node = find(state, "P4.true_dh_float64_evaluator_enclosure")
    forcenode = find(state, "P4.true_dh_force_descriptor_semantics")
    entries = [
        (o1node, "o1_partial_source_export_reviews", {
            "status": "PARTIAL_SOURCE_EXPORT",
            "review_sha256": sha(O1),
            "canonical_typed_inhabitant": False,
            "source_binding_theorem_present": False,
            "required_binding": "h_source_mass or (h_aggregate and h_body)",
            "registry_promoted": False,
        }),
        (o2node, "o2_real_branch_export_plans", {
            "status": "OPEN_REAL_THETA2_TRIPLE_RECEIPT_MISSING",
            "review_sha256": sha(O2),
            "branch_source_before_patch_sha256": sha(BACKUP),
            "branch_source_after_patch_sha256": current_hash,
            "backup_path": str(BACKUP.resolve()),
            "canonical_triple_receipt_present": False,
            "external_premises_present": False,
            "global_coverage": False,
            "registry_promoted": False,
        }),
        (o2node, "o2_triple_export_runtime_obstructions", {
            "status": "BLOCKED_NO_JULIA_RUNTIME",
            "review_sha256": sha(O2_RUNTIME),
            "branch_source_sha256": current_hash,
            "backup_source_sha256": sha(BACKUP),
            "julia_found": False,
            "parse_verified": False,
            "runtime_ready": False,
            "external_premises_present": False,
            "global_coverage": False,
            "registry_promoted": False,
        }),
        (forcenode, "force_github_execution_blockers", {
            "status": "BLOCKED_WORKFLOW_NOT_LANDED",
            "review_sha256": sha(FORCE),
            "workflow_file_landed": False,
            "runtime_receipt_present": False,
            "registry_promoted": False,
        }),
        (forcenode, "force_github_workflow_blockers", {
            "status": "BLOCKED_WORKFLOW_NOT_LANDED",
            "review_sha256": sha(FORCE_BLOCKER),
            "workflow_file_landed": False,
            "runtime_receipt_present": False,
            "registry_promoted": False,
        }),
    ]
    changed = False
    for node, key, entry in entries:
        prior = list(node.metadata.get(key, []))
        if entry not in prior:
            prior.append(entry)
            node.metadata[key] = prior
            changed = True
    desired_o2 = {
        "status": "OPEN_REAL_THETA2_TRIPLE_RECEIPT_MISSING",
        "review_sha256": sha(O2),
        "branch_source_after_patch_sha256": current_hash,
        "canonical_triple_receipt_present": False,
        "external_premises_present": False,
        "global_coverage": False,
        "registry_promoted": False,
    }
    if o2node.metadata.get("o2_real_branch_export_plan") != desired_o2:
        o2node.metadata["o2_real_branch_export_plan"] = desired_o2
        changed = True
    desired_o2_runtime = {
        "status": "BLOCKED_NO_JULIA_RUNTIME",
        "review_sha256": sha(O2_RUNTIME),
        "branch_source_sha256": current_hash,
        "backup_source_sha256": sha(BACKUP),
        "julia_found": False,
        "parse_verified": False,
        "runtime_ready": False,
        "external_premises_present": False,
        "global_coverage": False,
        "registry_promoted": False,
    }
    if o2node.metadata.get("o2_triple_export_runtime_obstruction") != desired_o2_runtime:
        o2node.metadata["o2_triple_export_runtime_obstruction"] = desired_o2_runtime
        changed = True
    if changed:
        state.event(
            "routeb_latest_interface_reviews_recorded",
            o1_status="PARTIAL_SOURCE_EXPORT",
            o2_status="OPEN_REAL_THETA2_TRIPLE_RECEIPT_MISSING",
            o2_runtime_status="BLOCKED_NO_JULIA_RUNTIME",
            force_status="BLOCKED_WORKFLOW_NOT_LANDED",
            registry_promoted=False,
            formal_certificate_allowed=False,
        )
        state.validate()
        store.save(state)
    print({"status": "recorded" if changed else "already_recorded", "state_revision": store.load().revision, "o2_branch_source_sha256": current_hash, "o1_source_binding": False, "force_workflow_landed": False})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
