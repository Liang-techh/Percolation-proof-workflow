"""Attach the latest O0 physical coercivity/bias obstruction fail-closed."""
from __future__ import annotations

from hashlib import sha256
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from percolation_workflow.store import StateStore  # noqa: E402


STATE = ROOT / "artifacts" / "routeb_6dof" / "state.json"
RECEIPT = ROOT / "agent_review_inbox" / "receipt-T-P4-033-O0-physical-coercivity-bias-frontier-obstruction-20260907.json"
REVIEW = ROOT / "agent_review_inbox" / "review-T-P4-033-O0-physical-coercivity-bias-frontier-20260907.md"


def digest(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest().upper()


def find(state, name: str):
    for node in state.nodes.values():
        if node.name == name:
            return node
    raise ValueError(f"missing node: {name}")


def main() -> None:
    for path in (STATE, RECEIPT, REVIEW):
        if not path.is_file():
            raise FileNotFoundError(path)
    store = StateStore(STATE)
    state = store.load()
    node = find(state, "P4.true_dh_exact_real_coefficient_identity")
    entry = {
        "status": "OBSTRUCTION",
        "disposition": "OPEN_FAIL_CLOSED_NO_SAME_KEY_PHYSICAL_COERCIVITY_OR_BIAS_RECEIPT",
        "receipt_sha256": digest(RECEIPT),
        "review_sha256": digest(REVIEW),
        "same_key_baseline_budget": False,
        "same_key_L_base": False,
        "same_key_physical_residual_identity": False,
        "same_key_affine_bias_bound": False,
        "schur_margin_consumed": False,
        "registry_promoted": False,
        "formal_certificate_allowed": False,
    }
    prior = list(node.metadata.get("o0_physical_coercivity_bias_obstructions", []))
    changed = entry not in prior
    if changed:
        prior.append(entry)
        node.metadata["o0_physical_coercivity_bias_obstructions"] = prior
        node.metadata["o0_physical_coercivity_bias_obstruction"] = entry
        state.event(
            "routeb_o0_physical_coercivity_bias_frontier",
            status=entry["status"],
            receipt_sha256=entry["receipt_sha256"],
            missing_contracts=[
                "same_key_physical_baseline_budget",
                "same_key_exact_L_base_or_positive_reserve",
                "same_key_physical_residual_identity",
                "same_key_relative_or_absolute_bias_bound",
            ],
            schur_margin_consumed=False,
            registry_promoted=False,
            formal_certificate_allowed=False,
        )
        state.validate()
        store.save(state)
    print({"status": "recorded" if changed else "already_recorded", "revision": store.load().revision})


if __name__ == "__main__":
    main()
