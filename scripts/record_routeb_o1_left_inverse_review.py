"""Record the determinant-to-left-inverse O1 adapter without closing O1."""
from __future__ import annotations

import hashlib
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
REVIEW = ROOT / "agent_review_inbox/review-T-P4-033-O1-det-left-inverse-adapter-codex-20260907.md"
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
        "det_to_canonical_left_inverse", "Matrix.nonsing_inv_mul",
        "det_to_same_named_left_inverse", "h_inv_def",
        "同一 `(mu,q)`", "full `6×6` determinant",
        "不能把", "O1 verified",
    ):
        if phrase not in text:
            raise ValueError(f"O1 left-inverse boundary missing: {phrase}")
    review = {
        "schema_version": 1,
        "task_id": "T-P4-033-O1-det-left-inverse",
        "source_agent": "Codex",
        "review_status": "CONDITIONALLY_COMPILED_DET_TO_LEFT_INVERSE_OPEN_BINDING",
        "review_artifact": {
            "path": str(REVIEW.resolve()), "sha256": sha(REVIEW)
        },
        "api": "Matrix.nonsing_inv_mul",
        "generic_target": "A.det != 0 -> A⁻¹ * A = 1",
        "same_named_target": "h_inv_def: M_DD_inv = (M_DD45 M)⁻¹",
        "required_binding": [
            "same M_DD45 block projection",
            "same exact (mu,q) or cell key",
            "Didx=(1,2,3,6) and source/state hash",
        ],
        "remaining_obstruction": "M_DD_inv definition or exact h_inv_def receipt",
        "reported_temporary_probe": {"exit_code": 0, "canonical_receipt": False},
        "formal_certificate_allowed": False,
        "registry_promoted": False,
        "admission_status": "pending_same_object_inverse_binding",
    }
    store = StateStore(STATE)
    state = store.load()
    node = find(state, "P4.true_dh_exact_real_coefficient_identity")
    prior = list(node.metadata.get("independent_static_reviews", []))
    changed = review not in prior
    if changed:
        prior.append(review)
        node.metadata["independent_static_reviews"] = prior
    desired = {
        "status": "CONDITIONALLY_COMPILED_LEFT_INVERSE_ADAPTER_OPEN_BINDING",
        "api": "Matrix.nonsing_inv_mul",
        "generic_det_target": "A.det != 0 -> A⁻¹ * A = 1",
        "same_named_target": "M_DD_inv = (M_DD45 M)⁻¹",
        "remaining_obstruction": review["remaining_obstruction"],
        "required_binding": review["required_binding"],
        "formal_certificate_allowed": False,
        "registry_promoted": False,
    }
    if node.metadata.get("left_inverse_adapter") != desired:
        node.metadata["left_inverse_adapter"] = desired
        changed = True
    if changed:
        state.event(
            "routeb_o1_left_inverse_review_recorded",
            node_id=node.id,
            review_status=review["review_status"],
            admission_status=review["admission_status"],
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
