"""Record the T-P4-033 O0-R3 same-key ledger obstruction.

This intake preserves a negative mathematical review.  It never converts the
existing conditional port candidate or physical Schur ledger into an O0
receipt, and it never changes registry or formal-certificate admission.
"""
from __future__ import annotations

import hashlib
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
REVIEW = ROOT / "agent_review_inbox/review-T-P4-033-O0-R3-same-key-ledger-codex-20260907.md"
STATE = ROOT / "artifacts/routeb_6dof/state.json"
PHYSICAL_REPORT = ROOT / "artifacts/task_DP_physical_schur_margin_20260906/REPORT.md"
PHYSICAL_LEDGER = ROOT / "artifacts/task_DP_physical_schur_margin_20260906/ledger.json"
sys.path.insert(0, str(ROOT / "src"))

from percolation_workflow.store import StateStore  # noqa: E402


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def ref(path: Path) -> dict[str, str]:
    return {"path": str(path.resolve()), "sha256": sha256(path)}


def find_node(state, name: str):
    for node in state.nodes.values():
        if node.name == name:
            return node
    raise ValueError(f"missing node: {name}")


def main() -> int:
    for path in (REVIEW, STATE, PHYSICAL_REPORT, PHYSICAL_LEDGER):
        if not path.is_file():
            raise FileNotFoundError(path)
    text = REVIEW.read_text(encoding="utf-8", errors="replace")
    required = (
        "There is currently **no consumable same-key physical pair**",
        "P4.residual_port_frobenius_bound",
        "BLOCKED_MISSING_A_GT_MU_AND_PHYSICAL_COUPLING_RECEIPT",
        "Until this receipt exists, O0-R3 is correctly fail-closed",
        "registry promotion by this review: false",
    )
    if not all(phrase in text for phrase in required):
        raise ValueError("T-P4-033 O0-R3 review is missing its obstruction boundary")

    store = StateStore(STATE)
    state = store.load()
    observed_state_hash = sha256(STATE)
    node = find_node(state, "P4.true_dh_regularizer_semantics_bridge")
    review = {
        "schema_version": 1,
        "source_agent": "Codex",
        "task_id": "T-P4-033",
        "subtask": "O0-R3",
        "review_status": "NO_CONSUMABLE_SAME_KEY_PHYSICAL_PAIR",
        "review_artifact": ref(REVIEW),
        "supporting_artifacts": [ref(PHYSICAL_REPORT), ref(PHYSICAL_LEDGER)],
        "observed_state_sha256_before_integration": observed_state_hash,
        "evidence_level": "read_only_same_key_ledger_obstruction",
        "claims": {
            "same_key_weighted_baseline_available": False,
            "same_key_weighted_perturbation_available": False,
            "same_key_remaining_schur_margin_available": False,
            "strict_margin_inequality_checked": False,
            "lean_verified": False,
            "registry_promoted": False,
            "formal_certificate_allowed": False,
        },
        "unresolved": [
            "canonical_source_state_key",
            "weighted_baseline_rho_r_or_upper_root",
            "weighted_perturbation_epsilon_R",
            "positive_remaining_baseline_schur_margin",
            "typed_R_port_aB_equals_rB",
            "same_domain_true_dh_float64_coverage",
        ],
        "required_receipt_fields": [
            "source/runtime/coordinate/mu/fd/force-scale key",
            "weighted baseline rho_r or upper-root witness",
            "weighted perturbation epsilon_R",
            "same-key positive remaining margin and theta",
            "R_port*a_B=r_B plus full consumed-cell coverage",
            "strict lambda*((rho_r+epsilon_R)^2-rho_r^2) < m_r",
        ],
        "admission_status": "pending_same_key_physical_receipt",
        "registry_promoted": False,
        "formal_certificate_allowed": False,
    }
    reviews = list(node.metadata.get("independent_math_reviews", []))
    # The observed pre-integration state hash is intentionally part of the
    # provenance record, so exact-dict equality is not an idempotency key.
    # Re-running intake after state mutation must not append the same review.
    already_recorded = any(
        item.get("task_id") == review["task_id"]
        and item.get("subtask") == review["subtask"]
        and item.get("review_status") == review["review_status"]
        for item in reviews if isinstance(item, dict)
    )
    changed = not already_recorded
    if changed:
        reviews.append(review)
        node.metadata["independent_math_reviews"] = reviews

    obstruction = {
        "schema_version": 1,
        "task_id": "T-P4-033",
        "subtask": "O0-R3",
        "status": "NO_CONSUMABLE_SAME_KEY_PHYSICAL_PAIR",
        "review_artifact": review["review_artifact"],
        "candidate_node": "P4.residual_port_frobenius_bound",
        "physical_ledger_status": "BLOCKED_MISSING_A_GT_MU_AND_PHYSICAL_COUPLING_RECEIPT",
        "same_key_required": True,
        "rho_r_available": False,
        "epsilon_R_available": False,
        "remaining_margin_available": False,
        "strict_budget_checked": False,
        "required_next_receipt": review["required_receipt_fields"],
        "formal_certificate_allowed": False,
        "registry_promoted": False,
    }
    if node.metadata.get("o0_r3_same_key_ledger") != obstruction:
        node.metadata["o0_r3_same_key_ledger"] = obstruction
        changed = True
    unresolved = list(node.metadata.get("unresolved", []))
    for marker in (
        "o0_r3_no_consumable_same_key_physical_pair",
        "o0_r3_weighted_baseline_missing",
        "o0_r3_remaining_margin_missing",
    ):
        if marker not in unresolved:
            unresolved.append(marker)
            changed = True
    if node.metadata.get("unresolved") != unresolved:
        node.metadata["unresolved"] = unresolved
        changed = True
    if changed:
        state.event(
            "routeb_o0_r3_same_key_obstruction_recorded",
            node_id=node.id,
            task_id="T-P4-033",
            review_status=review["review_status"],
            admission_status="pending_same_key_physical_receipt",
            registry_promoted=False,
            formal_certificate_allowed=False,
        )
        state.validate()
        store.save(state)
    print({
        "status": "recorded" if changed else "already_recorded",
        "review_status": review["review_status"],
        "state_revision": store.load().revision,
        "registry_promoted": False,
        "formal_certificate_allowed": False,
    })
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
