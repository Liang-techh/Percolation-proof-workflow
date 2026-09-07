"""Record the fail-closed O1 typed witness generator contract."""
from __future__ import annotations

import hashlib
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
REVIEW = ROOT / "agent_review_inbox/review-T-P4-033-O1-source-binding-witness-generator-codex-20260907.md"
GENERATOR = ROOT / "agent_review_inbox/generate_routeb_o1_mdd_binding_witness.py"
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
    for path in (REVIEW, GENERATOR, STATE):
        if not path.is_file():
            raise FileNotFoundError(path)
    text = REVIEW.read_text(encoding="utf-8", errors="replace")
    for phrase in (
        "fail-closed generator",
        "source_key/state_key",
        "Path A",
        "Path B",
        "READY_TYPED_*_TARGET_NOT_VERIFIED",
        "No O1 status is advanced",
    ):
        if phrase not in text:
            raise ValueError(f"O1 witness-generator boundary missing: {phrase}")
    entry = {
        "schema_version": 1,
        "task_id": "T-P4-033-O1-source-binding-witness-generator",
        "source_agent": "codex-inbox",
        "review_status": "READY_FAIL_CLOSED_TYPED_WITNESS_GENERATOR",
        "review_artifact": {"path": str(REVIEW.resolve()), "sha256": sha(REVIEW)},
        "generator": {"path": str(GENERATOR.resolve()), "sha256": sha(GENERATOR)},
        "accepted_paths": {
            "A": ["h_MDD_def", "h_inv_def", "hdet"],
            "B": ["h_MDD_def", "h_left"],
        },
        "required_equalities": [
            "source_key", "state_key", "mu_ident", "q_ident",
            "block_order_one_based=[1,2,3,6]",
            "didx_zero_based=[0,1,2,5]",
        ],
        "output_boundary": "READY_TYPED_TARGET_NOT_VERIFIED",
        "source_receipt_present": False,
        "formal_certificate_allowed": False,
        "registry_promoted": False,
    }
    store = StateStore(STATE)
    state = store.load()
    node = find(state, "P4.true_dh_exact_real_coefficient_identity")
    prior = list(node.metadata.get("source_binding_witness_generators", []))
    changed = entry not in prior
    if changed:
        prior.append(entry)
        node.metadata["source_binding_witness_generators"] = prior
    desired = {
        "status": entry["review_status"],
        "generator_sha256": entry["generator"]["sha256"],
        "accepted_paths": entry["accepted_paths"],
        "required_equalities": entry["required_equalities"],
        "source_receipt_present": False,
        "formal_certificate_allowed": False,
        "registry_promoted": False,
    }
    if node.metadata.get("source_binding_witness_generator") != desired:
        node.metadata["source_binding_witness_generator"] = desired
        changed = True
    if changed:
        state.event(
            "routeb_o1_source_binding_witness_generator_recorded",
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
        "generator_sha256": entry["generator"]["sha256"],
        "registry_promoted": False,
        "formal_certificate_allowed": False,
    })
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
