"""Record the current structural obstruction for the O1 exact source export."""
from __future__ import annotations

import hashlib
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
REVIEW = ROOT / "agent_review_inbox/review-T-P4-033-O1-true-dh-exact-MDD-export-obstruction-codex-20260907.md"
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
        "debug_11_dhport.jl",
        "debug_12n_symM.jl",
        "M_DD45_at M mu q",
        "source_key",
        "state_key",
        "block_order",
        "M_DD_left_inverse_witness` remains `OPEN",
    ):
        if phrase not in text:
            raise ValueError(f"O1 exact export obstruction missing: {phrase}")
    entry = {
        "schema_version": 1,
        "task_id": "T-P4-033-O1",
        "source_agent": "codex-inbox",
        "review_status": "OPEN_TRUE_DH_EXACT_MDD_EXPORT_OBSTRUCTION",
        "review_artifact": {"path": str(REVIEW.resolve()), "sha256": sha(REVIEW)},
        "nearest_artifacts": ["debug_11_dhport.jl", "debug_12n_symM.jl", "P3 trig-chain contract"],
        "missing_source_fields": [
            "source_key", "state_key", "mu", "q", "block_order",
            "typed Matrix (Fin 6) (Fin 6) ℝ evaluator",
            "typed M_DD45_at projection", "h_MDD_def",
        ],
        "accepted_paths": {
            "A": ["h_inv_def", "hdet"],
            "B": ["h_left"],
        },
        "structural_obstruction": "current deployed source exposes Float64/runtime or symbolic probes, not same-key exact typed M_DD45",
        "formal_certificate_allowed": False,
        "registry_promoted": False,
    }
    store = StateStore(STATE)
    state = store.load()
    node = find(state, "P4.true_dh_exact_real_coefficient_identity")
    prior = list(node.metadata.get("true_dh_export_obstructions", []))
    changed = entry not in prior
    if changed:
        prior.append(entry)
        node.metadata["true_dh_export_obstructions"] = prior
    desired = {
        "status": entry["review_status"],
        "review_sha256": entry["review_artifact"]["sha256"],
        "missing_source_fields": entry["missing_source_fields"],
        "structural_obstruction": entry["structural_obstruction"],
        "formal_certificate_allowed": False,
        "registry_promoted": False,
    }
    if node.metadata.get("true_dh_export_obstruction") != desired:
        node.metadata["true_dh_export_obstruction"] = desired
        changed = True
    if changed:
        state.event(
            "routeb_o1_true_dh_exact_mdd_export_obstruction_recorded",
            node_id=node.id,
            review_status=entry["review_status"],
            source_receipt_required=True,
            registry_promoted=False,
            formal_certificate_allowed=False,
        )
        state.validate()
        store.save(state)
    print({
        "status": "recorded" if changed else "already_recorded",
        "review_status": entry["review_status"],
        "state_revision": store.load().revision,
        "source_receipt_required": True,
        "registry_promoted": False,
        "formal_certificate_allowed": False,
    })
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
