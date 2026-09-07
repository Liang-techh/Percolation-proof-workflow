"""Record the O0-R3 strict-positive-leftover obstruction fail-closed."""
from __future__ import annotations

import hashlib
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
REVIEW = ROOT / "agent_review_inbox/review-T-P4-033-O0-R3-strict-leftover-obstruction-codex-20260907.md"
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
        "No consumable same-key receipt exists",
        "weighted_baseline.rho_r",
        "schur_baseline.remaining_margin_m_r",
        "a fixed exact `theta`",
        "strict_positive_leftover_undetermined",
        "main_state_modified = false",
        "schur_margin_consumed = false",
    ):
        if phrase not in text:
            raise ValueError(f"O0 strict-leftover obstruction missing: {phrase}")
    entry = {
        "schema_version": 1,
        "task_id": "T-P4-033-O0-R3",
        "source_agent": "codex-inbox",
        "review_status": "OPEN_FAIL_CLOSED_STRICT_LEFTOVER_REQUIRED",
        "review_artifact": {"path": str(REVIEW.resolve()), "sha256": sha(REVIEW)},
        "scope": "same-key exact-Fourier one-cell R3",
        "source_key": "routeb-exact-fourier-mass:a986a208b62f585c6ca1b9c81b958710d2043e5bf786ddc930a6fa29f7a232b8|mu=1/1000000|contract=exp(i*nu*q)",
        "state_key": "routeb-qcell:center=(0,0,0,0,0,0)|radius=1/1000|B=(4,5)|D=(1,2,3,6)|orientation=M_BD[B,D],DeltaM_DB[D,B]|norm=induced_infinity",
        "available": ["factor-2 weighted perturbation epsilon"],
        "missing": [
            "same-key weighted baseline rho_r",
            "same-key positive remaining margin m_r",
            "fixed exact theta",
            "strict positive leftover m_f",
            "physical R_port*a_B=r_B if physical consumer is requested",
        ],
        "strict_formula": "m_f = m_r - (1+1/theta)*((rho_r+epsilon)^2-rho_r^2)",
        "rejected_candidates": [
            "unkeyed Frobenius CSV candidates",
            "unkeyed theta/charge/margin columns",
            "arithmetic-only rational roots",
        ],
        "schur_margin_consumed": False,
        "formal_certificate_allowed": False,
        "registry_promoted": False,
    }
    store = StateStore(STATE)
    state = store.load()
    node = find(state, "P4.true_dh_regularizer_semantics_bridge")
    prior = list(node.metadata.get("o0_strict_leftover_obstructions", []))
    changed = entry not in prior
    if changed:
        prior.append(entry)
        node.metadata["o0_strict_leftover_obstructions"] = prior
    desired = {
        "status": entry["review_status"],
        "review_sha256": entry["review_artifact"]["sha256"],
        "scope": entry["scope"],
        "missing": entry["missing"],
        "strict_formula": entry["strict_formula"],
        "schur_margin_consumed": False,
        "formal_certificate_allowed": False,
        "registry_promoted": False,
    }
    if node.metadata.get("o0_strict_leftover_obstruction") != desired:
        node.metadata["o0_strict_leftover_obstruction"] = desired
        changed = True
    if changed:
        state.event(
            "routeb_o0_strict_leftover_obstruction_recorded",
            node_id=node.id,
            review_status=entry["review_status"],
            strict_positive_leftover=False,
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
        "strict_positive_leftover": False,
        "schur_margin_consumed": False,
        "registry_promoted": False,
        "formal_certificate_allowed": False,
    })
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
