"""Record the O1 absence of a source-side typed inhabitant."""
from __future__ import annotations

import hashlib
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
REVIEW = ROOT / "agent_review_inbox/review-T-P4-033-O1-source-inhabitant-search-immutable-codex-20260907.md"
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
        "No inspected deployed-source or exact-artifact file contains",
        "`M_DD45_at` source inhabitant: `NOT FOUND`",
        "`M_DD_left_inverse_witness`: `OPEN`",
        "source_key, state_key",
    ):
        if phrase not in text:
            raise ValueError(f"O1 source-inhabitant obstruction missing: {phrase}")
    if "didx_zero_based: [0,1,2,5]" not in text:
        raise ValueError("O1 canonical zero-based D map missing")
    entry = {
        "status": "OPEN_SOURCE_TYPED_INHABITANT_NOT_FOUND",
        "review_sha256": sha(REVIEW),
        "missing_object": "M_DD45_at M mu q : Matrix (Fin 4) (Fin 4) ℝ",
        "missing_binding": "h_MDD_def : M_DD = M_DD45_at M mu q",
        "required_source_fields": [
            "source_key", "state_key", "exact mu", "exact q or uniform cell",
            "M : Mu → Q → Matrix (Fin 6) (Fin 6) ℝ",
            "block_order_one_based=[1,2,3,6]", "didx_zero_based=[0,1,2,5]",
            "source artifact hash",
        ],
        "canonical_receipt_present": False,
        "left_inverse_witness": "OPEN",
        "formal_certificate_allowed": False,
        "registry_promoted": False,
    }
    store = StateStore(STATE)
    state = store.load()
    node = find(state, "P4.true_dh_exact_real_coefficient_identity")
    prior = list(node.metadata.get("o1_source_inhabitant_obstructions", []))
    changed = entry not in prior
    if changed:
        prior.append(entry)
        node.metadata["o1_source_inhabitant_obstructions"] = prior
    desired = {
        "status": entry["status"],
        "review_sha256": entry["review_sha256"],
        "canonical_receipt_present": False,
        "left_inverse_witness": "OPEN",
        "formal_certificate_allowed": False,
        "registry_promoted": False,
    }
    if node.metadata.get("o1_source_inhabitant_obstruction") != desired:
        node.metadata["o1_source_inhabitant_obstruction"] = desired
        changed = True
    if changed:
        state.event(
            "routeb_o1_source_inhabitant_obstruction_recorded",
            node_id=node.id,
            status=entry["status"],
            canonical_receipt_present=False,
            left_inverse_witness="OPEN",
            formal_certificate_allowed=False,
            registry_promoted=False,
        )
        state.validate()
        store.save(state)
    print({"status": "recorded" if changed else "already_recorded", "state_revision": store.load().revision, "canonical_receipt_present": False, "registry_promoted": False})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
