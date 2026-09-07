"""Record the O0 same-key zero-shift perturbation reduction."""
from __future__ import annotations

import hashlib
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
REVIEW = ROOT / "agent_review_inbox/review-T-P4-033-O0-R1-R2-perturbation-map-obstruction-codex-20260907.md"
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
        "OBSTRUCTION_NO_SAME_KEY_PERTURBATION_RECEIPT",
        "zero off-diagonal regularizer shifts", "U_delta", "epsilon_R", "exact-real `K",
        "source_key", "state_key", "PENDING/OBSTRUCTION",
    ):
        if phrase not in text:
            raise ValueError(f"O0 perturbation boundary missing: {phrase}")
    review = {
        "schema_version": 1,
        "task_id": "T-P4-033-O0-R1-R2-perturbation",
        "source_agent": "Codex",
        "review_status": "OBSTRUCTION_NO_SAME_KEY_PERTURBATION_RECEIPT",
        "review_artifact": {"path": str(REVIEW.resolve()), "sha256": sha(REVIEW)},
        "conditional_reduction": {
            "premise": "same-key authoritative dB=dC=0",
            "unweighted": "Br*Cf*delta*K^2/(1-delta*K)",
            "weighted": "Br*Cf*delta*K^2/((1-delta*K)*s)",
        },
        "missing_receipt_fields": [
            "source_key", "state_key", "exact K with proof flag",
            "Br", "Cf", "delta*K<1", "same-key metric s",
            "authoritative zero off-diagonal shifts", "physical port identity",
        ],
        "admission_status": "obstruction_pending_same_key_receipt",
        "formal_certificate_allowed": False,
        "registry_promoted": False,
    }
    store = StateStore(STATE)
    state = store.load()
    node = find(state, "P4.true_dh_regularizer_semantics_bridge")
    prior = list(node.metadata.get("independent_static_reviews", []))
    changed = review not in prior
    if changed:
        prior.append(review)
        node.metadata["independent_static_reviews"] = prior
    desired = {
        "status": "OBSTRUCTION_NO_SAME_KEY_PERTURBATION_RECEIPT",
        "conditional_reduction": review["conditional_reduction"],
        "missing_receipt_fields": review["missing_receipt_fields"],
        "formal_certificate_allowed": False,
        "registry_promoted": False,
    }
    if node.metadata.get("o0_perturbation_reduction") != desired:
        node.metadata["o0_perturbation_reduction"] = desired
        changed = True
    if changed:
        state.event(
            "routeb_o0_perturbation_review_recorded",
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
