"""Record the O0-R3 missing weighted baseline/margin obstruction."""
from __future__ import annotations

import hashlib
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
REVIEW = ROOT / "agent_review_inbox/review-T-P4-033-O0-R2-R3-factor2-interface-obstruction-codex-20260907.md"
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
        "The compiled Fin-2 theorem",
        "same-key weighted baseline `rho_r`",
        "strict-margin receipt",
        "epsilon_2_weighted",
        "schur_margin_consumed = false",
        "OPEN_FAIL_CLOSED: same_key_weighted_baseline_and_strict_margin_missing",
    ):
        if phrase not in text:
            raise ValueError(f"O0 factor-2 obstruction missing: {phrase}")
    entry = {
        "schema_version": 1,
        "task_id": "T-P4-033-O0-R2-R3",
        "source_agent": "codex-inbox",
        "review_status": "OPEN_FAIL_CLOSED_SAME_KEY_BASELINE_AND_STRICT_MARGIN_MISSING",
        "review_artifact": {"path": str(REVIEW.resolve()), "sha256": sha(REVIEW)},
        "factor2_join": "COMPOSED_AT_SCALAR_INTERFACE",
        "weighted_perturbation": "AVAILABLE_CONDITIONAL_EXACT_FOURIER_ONE_CELL",
        "missing": [
            "same-key weighted baseline rho_r",
            "same-key positive remaining margin m_r",
            "fixed exact theta",
            "strict positive leftover",
            "physical R_port*a_B=r_B if physical consumer is requested",
        ],
        "safe_weighted_epsilon": "2*epsilon_R_infinity/s",
        "schur_margin_consumed": False,
        "formal_certificate_allowed": False,
        "registry_promoted": False,
    }
    store = StateStore(STATE)
    state = store.load()
    node = find(state, "P4.true_dh_regularizer_semantics_bridge")
    prior = list(node.metadata.get("o0_factor2_interface_obstructions", []))
    changed = entry not in prior
    if changed:
        prior.append(entry)
        node.metadata["o0_factor2_interface_obstructions"] = prior
    desired = {
        "status": entry["review_status"],
        "review_sha256": entry["review_artifact"]["sha256"],
        "factor2_join": entry["factor2_join"],
        "weighted_perturbation": entry["weighted_perturbation"],
        "missing": entry["missing"],
        "schur_margin_consumed": False,
        "formal_certificate_allowed": False,
        "registry_promoted": False,
    }
    if node.metadata.get("o0_factor2_interface_obstruction") != desired:
        node.metadata["o0_factor2_interface_obstruction"] = desired
        changed = True
    if changed:
        state.event(
            "routeb_o0_factor2_interface_obstruction_recorded",
            node_id=node.id,
            review_status=entry["review_status"],
            factor2_join="COMPOSED_AT_SCALAR_INTERFACE",
            schur_margin_consumed=False,
            registry_promoted=False,
            formal_certificate_allowed=False,
        )
        state.validate()
        store.save(state)
    print({
        "status": "recorded" if changed else "already_recorded",
        "review_status": entry["review_status"],
        "state_revision": store.load().revision,
        "factor2_join": entry["factor2_join"],
        "schur_margin_consumed": False,
        "registry_promoted": False,
        "formal_certificate_allowed": False,
    })
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
