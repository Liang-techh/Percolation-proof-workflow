"""Ingest the O1 source-binding obstruction without closing the theorem."""
from __future__ import annotations

import hashlib
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
REVIEW = ROOT / "agent_review_inbox/review-T-P4-033-O1-source-binding-followup-3-codex-20260907.md"
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
    if not REVIEW.is_file() or not STATE.is_file():
        raise FileNotFoundError(REVIEW if not REVIEW.is_file() else STATE)
    text = REVIEW.read_text(encoding="utf-8", errors="replace")
    for phrase in (
        "M : Mu → Q → Matrix (Fin 6) (Fin 6) ℝ",
        "M_DD45_at M mu q",
        "Path A — canonical inverse",
        "Path B — direct same-object left inverse",
        "same-key exact `M_DD45_at M mu q` binding",
        "M_DD_left_inverse_witness = OPEN",
        "formal_certificate_allowed = false",
    ):
        if phrase not in text:
            raise ValueError(f"O1 follow-up-3 boundary missing: {phrase}")
    review = {
        "schema_version": 1,
        "task_id": "T-P4-033-O1-source-binding-followup-3",
        "source_agent": "codex-inbox",
        "review_status": "OPEN_TYPED_SOURCE_BINDING_PATH_A_OR_B",
        "review_artifact": {"path": str(REVIEW.resolve()), "sha256": sha(REVIEW)},
        "source_object": "M : Mu → Q → Matrix (Fin 6) (Fin 6) ℝ",
        "projected_block": "M_DD45_at M mu q : Matrix (Fin 4) (Fin 4) ℝ",
        "D_order": [1, 2, 3, 6],
        "D_zero_based_Fin_map": [0, 1, 2, 5],
        "consumable_paths": {
            "A": ["h_MDD_def", "h_inv_def", "hdet"],
            "B": ["h_MDD_def", "h_left"],
        },
        "required_source_fields": [
            "source_key", "state_key", "mu", "q", "block_order",
            "matrix_shape", "regularization",
        ],
        "remaining_obstruction": "missing same-key typed receipt for projected M_DD45 and inverse/left-inverse",
        "formal_certificate_allowed": False,
        "registry_promoted": False,
        "admission_status": "pending_authoritative_exact_source_receipt",
    }
    store = StateStore(STATE)
    state = store.load()
    node = find(state, "P4.true_dh_exact_real_coefficient_identity")
    prior = list(node.metadata.get("source_binding_followup3", []))
    changed = review not in prior
    if changed:
        prior.append(review)
        node.metadata["source_binding_followup3"] = prior
    desired = {
        "status": review["review_status"],
        "projected_block": review["projected_block"],
        "D_order": review["D_order"],
        "D_zero_based_Fin_map": review["D_zero_based_Fin_map"],
        "consumable_paths": review["consumable_paths"],
        "remaining_obstruction": review["remaining_obstruction"],
        "formal_certificate_allowed": False,
        "registry_promoted": False,
    }
    if node.metadata.get("source_binding_followup3_gate") != desired:
        node.metadata["source_binding_followup3_gate"] = desired
        changed = True
    if changed:
        state.event(
            "routeb_o1_source_binding_followup3_recorded",
            node_id=node.id,
            review_status=review["review_status"],
            admission_status=review["admission_status"],
            source_receipt_required=True,
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
