"""Record the O1 typed binding compile claim without inventing an OLean receipt."""
from __future__ import annotations

import hashlib
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
REVIEW = ROOT / "agent_review_inbox/review-T-P4-033-O1-binding-followup-2-codex-20260907.md"
SOURCE = ROOT / "artifacts/task_routeb_o1_left_inverse_binding_20260907/TypedMDDLeftInverse.lean"
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
    for path in (REVIEW, SOURCE, STATE):
        if not path.is_file():
            raise FileNotFoundError(path)
    text = REVIEW.read_text(encoding="utf-8", errors="replace")
    for phrase in (
        "typed_MDD_left_inverse", "direct_same_key_left_inverse",
        "pinned Mathlib compile returned `exit_code = 0`",
        '"source_comparator_run": false',
        '"statement_comparator_run": false',
        '"canonical_receipt": false',
        "M_DD_left_inverse_witness = OPEN",
    ):
        if phrase not in text:
            raise ValueError(f"O1 binding compile boundary missing: {phrase}")
    entry = {
        "schema_version": 1,
        "task_id": "T-P4-033-O1-binding-followup-2",
        "source_agent": "codex-inbox",
        "review_status": "COMPILED_CANDIDATE_OLEAN_AND_SOURCE_BINDING_PENDING",
        "review_artifact": {"path": str(REVIEW.resolve()), "sha256": sha(REVIEW)},
        "source_artifact": {"path": str(SOURCE.resolve()), "sha256": sha(SOURCE)},
        "olean_artifact": "NOT_SUPPLIED",
        "theorems": ["typed_MDD_left_inverse", "direct_same_key_left_inverse"],
        "compiler_exit_code": 0,
        "source_comparator_run": False,
        "statement_comparator_run": False,
        "canonical_receipt": False,
        "same_key_source_binding": "OPEN",
        "formal_certificate_allowed": False,
        "registry_promoted": False,
    }
    store = StateStore(STATE)
    state = store.load()
    node = find(state, "P4.true_dh_exact_real_coefficient_identity")
    prior = list(node.metadata.get("binding_compile_candidates", []))
    changed = entry not in prior
    if changed:
        prior.append(entry)
        node.metadata["binding_compile_candidates"] = prior
    desired = {
        "status": entry["review_status"],
        "source_sha256": entry["source_artifact"]["sha256"],
        "olean": "NOT_SUPPLIED",
        "compiler_exit_code": 0,
        "source_comparator": "OPEN",
        "statement_comparator": "OPEN",
        "canonical_receipt": False,
        "same_key_source_binding": "OPEN",
        "formal_certificate_allowed": False,
        "registry_promoted": False,
    }
    if node.metadata.get("binding_compile_candidate") != desired:
        node.metadata["binding_compile_candidate"] = desired
        changed = True
    if changed:
        state.event(
            "routeb_o1_binding_compile_candidate_recorded",
            node_id=node.id,
            compiler_exit_code=0,
            olean_supplied=False,
            source_comparator="OPEN",
            registry_promoted=False,
            formal_certificate_allowed=False,
        )
        state.validate()
        store.save(state)
    print({
        "status": "recorded" if changed else "already_recorded",
        "review_status": entry["review_status"],
        "state_revision": store.load().revision,
        "registry_promoted": False,
        "formal_certificate_allowed": False,
    })
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
