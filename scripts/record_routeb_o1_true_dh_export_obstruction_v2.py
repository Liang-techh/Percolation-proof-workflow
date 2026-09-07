"""Ingest the refined O1 exact-source export obstruction while preserving history."""
from __future__ import annotations

import hashlib
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
REVIEW = ROOT / "agent_review_inbox/review-T-P4-033-O1-true-dh-exact-MDD-export-obstruction-v2-codex-20260907.md"
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
        "no new true-DH exact `M_DD45` source receipt",
        "mass_matrix(q)",
        "M_DD45_at M mu q : Matrix (Fin 4) (Fin 4) ℝ",
        "h_MDD_def : M_DD = M_DD45_at M mu q",
        "source_key",
        "state_key",
        "projection_shape",
        "M_DD_left_inverse_witness` remains `OPEN",
    ):
        if phrase not in text:
            raise ValueError(f"O1 obstruction v2 boundary missing: {phrase}")
    entry = {
        "schema_version": 1,
        "task_id": "T-P4-033-O1-v2",
        "source_agent": "codex-inbox",
        "review_status": "OPEN_TRUE_DH_EXACT_MDD_EXPORT_OBSTRUCTION_V2",
        "review_artifact": {"path": str(REVIEW.resolve()), "sha256": sha(REVIEW)},
        "missing_object": "M_DD45_at M mu q : Matrix (Fin 4) (Fin 4) ℝ",
        "missing_binding": "h_MDD_def : M_DD = M_DD45_at M mu q",
        "required_fields": [
            "source_key", "state_key", "mu", "q", "block_order",
            "projection_shape", "source_hash", "real_number_semantics",
        ],
        "accepted_paths": {
            "A": ["h_inv_def", "exact non-singular premise"],
            "B": ["h_left"],
        },
        "source_surfaces_rejected": ["runtime Float64 mass_matrix(q)", "symbolic (s,c) polynomial", "q=0 check"],
        "formal_certificate_allowed": False,
        "registry_promoted": False,
    }
    store = StateStore(STATE)
    state = store.load()
    node = find(state, "P4.true_dh_exact_real_coefficient_identity")
    prior = list(node.metadata.get("true_dh_export_obstructions_v2", []))
    changed = entry not in prior
    if changed:
        prior.append(entry)
        node.metadata["true_dh_export_obstructions_v2"] = prior
    desired = {
        "status": entry["review_status"],
        "review_sha256": entry["review_artifact"]["sha256"],
        "missing_object": entry["missing_object"],
        "missing_binding": entry["missing_binding"],
        "required_fields": entry["required_fields"],
        "source_receipt_present": False,
        "formal_certificate_allowed": False,
        "registry_promoted": False,
    }
    if node.metadata.get("true_dh_export_obstruction_v2") != desired:
        node.metadata["true_dh_export_obstruction_v2"] = desired
        changed = True
    if changed:
        state.event(
            "routeb_o1_true_dh_exact_mdd_export_obstruction_v2_recorded",
            node_id=node.id,
            review_status=entry["review_status"],
            source_receipt_present=False,
            registry_promoted=False,
            formal_certificate_allowed=False,
        )
        state.validate()
        store.save(state)
    print({
        "status": "recorded" if changed else "already_recorded",
        "review_status": entry["review_status"],
        "state_revision": store.load().revision,
        "source_receipt_present": False,
        "registry_promoted": False,
        "formal_certificate_allowed": False,
    })
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
