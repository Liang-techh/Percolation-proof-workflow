"""Record the O0 missing coercivity/additive-reserve obstruction."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
RECEIPT = ROOT / "agent_review_inbox/receipt-T-P4-033-O0-coercivity-bias-interface-obstruction-20260907.json"
REVIEW = ROOT / "agent_review_inbox/review-T-P4-033-O0-coercivity-or-bias-interface-codex-20260907.md"
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
    for path in (RECEIPT, REVIEW, STATE):
        if not path.is_file():
            raise FileNotFoundError(path)
    doc = json.loads(RECEIPT.read_text(encoding="utf-8"))
    if doc.get("status") != "OPEN_FAIL_CLOSED_BASELINE_RESERVE_MISSING":
        raise ValueError("O0 coercivity obstruction status drift")
    if doc.get("schur_margin_consumed") is not False or doc.get("registry_promoted") is not False:
        raise ValueError("O0 coercivity obstruction crossed a gate")
    text = REVIEW.read_text(encoding="utf-8", errors="replace")
    for phrase in (
        "energy-side baseline coefficient",
        "L_base > lambda*(rho_r+epsilon_R)^2",
        "same_key_baseline_coercivity_or_additive_reserve_missing",
        "A nonzero fixed bias",
        "main_state_modified = false",
    ):
        if phrase not in text:
            raise ValueError(f"O0 coercivity/bias boundary missing: {phrase}")
    entry = {
        "status": doc["status"],
        "receipt_sha256": sha(RECEIPT),
        "review_sha256": sha(REVIEW),
        "source_key": doc["key"]["source_key"],
        "state_key": doc["key"]["state_key"],
        "missing": [
            "same-key L_base/coercivity theorem or direct m_r",
            "strict m_f > 0 proof",
            "physical R_port*a_B=r_B identity",
        ],
        "affine_bias_alternatives": [
            "beta_bias plus exact root witness",
            "beta_abs plus positive additive reserve",
        ],
        "schur_margin_consumed": False,
        "formal_certificate_allowed": False,
        "registry_promoted": False,
    }
    store = StateStore(STATE)
    state = store.load()
    node = find(state, "P4.true_dh_regularizer_semantics_bridge")
    prior = list(node.metadata.get("o0_coercivity_bias_obstructions", []))
    changed = entry not in prior
    if changed:
        prior.append(entry)
        node.metadata["o0_coercivity_bias_obstructions"] = prior
    desired = {
        "status": entry["status"],
        "receipt_sha256": entry["receipt_sha256"],
        "review_sha256": entry["review_sha256"],
        "missing": entry["missing"],
        "affine_bias_alternatives": entry["affine_bias_alternatives"],
        "schur_margin_consumed": False,
        "formal_certificate_allowed": False,
        "registry_promoted": False,
    }
    if node.metadata.get("o0_coercivity_bias_obstruction") != desired:
        node.metadata["o0_coercivity_bias_obstruction"] = desired
        changed = True
    if changed:
        state.event(
            "routeb_o0_coercivity_bias_obstruction_recorded",
            node_id=node.id,
            status=entry["status"],
            schur_margin_consumed=False,
            formal_certificate_allowed=False,
            registry_promoted=False,
        )
        state.validate()
        store.save(state)
    print({"status": "recorded" if changed else "already_recorded", "state_revision": store.load().revision, "schur_margin_consumed": False, "registry_promoted": False})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
