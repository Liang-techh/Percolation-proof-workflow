"""Record the refined two-path O1 same-object binding contract."""
from __future__ import annotations

import hashlib
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
REVIEW = ROOT / "agent_review_inbox/review-T-P4-033-O1-binding-followup-2-codex-20260907.md"
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
        "bind_typed_MDD_inverse", "bind_direct_same_key_left_inverse",
        "h_MDD_def", "h_inv_def", "h_left", "source_key", "state_key",
        "M_DD_left_inverse_witness = OPEN", "no O1 verified",
    ):
        if phrase not in text:
            raise ValueError(f"O1 binding follow-up boundary missing: {phrase}")
    review = {
        "schema_version": 1,
        "task_id": "T-P4-033-O1-binding-followup-2",
        "source_agent": "Codex",
        "review_status": "OPEN_SAME_OBJECT_BINDING_TWO_PATHS",
        "review_artifact": {"path": str(REVIEW.resolve()), "sha256": sha(REVIEW)},
        "binding_paths": {
            "A": "h_MDD_def + h_inv_def + exact hdet",
            "B": "h_MDD_def + direct exact h_left",
        },
        "required_key_equalities": [
            "source_key", "state_key", "mu", "q", "block_order=(1,2,3,6)",
        ],
        "remaining_obstruction": "missing same-key typed receipt for M_DD and M_DD_inv",
        "formal_certificate_allowed": False,
        "registry_promoted": False,
        "admission_status": "pending_same_object_binding",
    }
    store = StateStore(STATE)
    state = store.load()
    node = find(state, "P4.true_dh_exact_real_coefficient_identity")
    prior = list(node.metadata.get("independent_static_reviews", []))
    changed = review not in prior
    if changed:
        prior.append(review)
        node.metadata["independent_static_reviews"] = prior
    adapter = dict(node.metadata.get("left_inverse_adapter") or {})
    desired = {
        **adapter,
        "status": "OPEN_SAME_OBJECT_BINDING_TWO_PATHS",
        "binding_paths": review["binding_paths"],
        "required_key_equalities": review["required_key_equalities"],
        "required_premise": "h_MDD_def",
        "remaining_obstruction": review["remaining_obstruction"],
        "formal_certificate_allowed": False,
        "registry_promoted": False,
    }
    if adapter != desired:
        node.metadata["left_inverse_adapter"] = desired
        changed = True
    if changed:
        state.event(
            "routeb_o1_binding_followup_recorded",
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
