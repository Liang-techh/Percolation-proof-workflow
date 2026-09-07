"""Record the precise O0 K/Br/Cf same-key obstruction."""
from __future__ import annotations

import hashlib
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
REVIEW = ROOT / "agent_review_inbox/review-T-P4-033-O0-R1-R2-same-key-K-Br-Cf-obstruction-codex-20260907.md"
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
        "OBSTRUCTION_NO_SAME_KEY_EXACT_K_BR_CF_RECEIPT",
        "K_authority", "Br_statement", "Cf_statement",
        "zero_shift_authority", "hash 不是 same-key mathematical binding",
        "formal_certificate_allowed = false", "registry_eligible = false",
    ):
        if phrase not in text:
            raise ValueError(f"O0 exact bounds boundary missing: {phrase}")
    review = {
        "schema_version": 1,
        "task_id": "T-P4-033-O0-R1-R2-exact-bounds",
        "source_agent": "Codex",
        "review_status": "OBSTRUCTION_NO_SAME_KEY_EXACT_K_BR_CF_RECEIPT",
        "review_artifact": {"path": str(REVIEW.resolve()), "sha256": sha(REVIEW)},
        "missing_same_key_fields": {
            "K": "exact-real inverse norm with proves_exact_real_bound=true",
            "Br": "exact norm upper bound for M_BD,r",
            "Cf": "exact norm upper bound for DeltaM_DB,f",
            "binding": "source_key/state_key/block orientation/norm",
        },
        "inherited_only": "delta and conditional off-diagonal zero-shift",
        "admission_status": "obstruction_pending_exact_keyed_bounds",
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
        "status": review["review_status"],
        "missing_same_key_fields": review["missing_same_key_fields"],
        "inherited_only": review["inherited_only"],
        "formal_certificate_allowed": False,
        "registry_promoted": False,
    }
    if node.metadata.get("o0_exact_bounds_obstruction") != desired:
        node.metadata["o0_exact_bounds_obstruction"] = desired
        changed = True
    if changed:
        state.event(
            "routeb_o0_exact_bounds_obstruction_recorded",
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
