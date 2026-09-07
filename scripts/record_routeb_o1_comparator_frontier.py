"""Integrate the O1 source-comparator frontier without source promotion."""
from __future__ import annotations

from hashlib import sha256
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from percolation_workflow.store import StateStore  # noqa: E402


STATE = ROOT / "artifacts/routeb_6dof/state.json"
ARTIFACT_DIR = ROOT / "artifacts/task_routeb_o1_true_dh_exact_typed_mdd_source_v2_20260907"
RECEIPT = ARTIFACT_DIR / "SOURCE_COMPARATOR_RECEIPT.json"
LEAN = ARTIFACT_DIR / "RouteBO1SourceComparatorV2.lean"
REVIEW = ROOT / "agent_review_inbox/review-T-P4-033-O1-source-comparator-minimum-gap-codex-20260907.md"


def digest(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest().upper()


def find(state, name: str):
    for node in state.nodes.values():
        if node.name == name:
            return node
    raise ValueError(f"missing node: {name}")


def main() -> None:
    for path in (STATE, RECEIPT, LEAN, REVIEW):
        if not path.is_file():
            raise FileNotFoundError(path)
    store = StateStore(STATE)
    state = store.load()
    node = find(state, "P4.true_dh_exact_real_coefficient_identity")
    entry = {
        "status": "OPEN_H_BODY_SOURCE_COMPARATOR",
        "receipt_sha256": digest(RECEIPT),
        "lean_sha256": digest(LEAN),
        "review_sha256": digest(REVIEW),
        "h_aggregate_data_level_exact": True,
        "h_aggregate_function_lift_proven": False,
        "h_body_proven": False,
        "source_binding_proven": False,
        "lean_compile_status": "UNCOMPILED_CANDIDATE",
        "registry_promoted": False,
        "formal_certificate_allowed": False,
    }
    prior = list(node.metadata.get("o1_source_comparator_frontiers", []))
    changed = entry not in prior
    if changed:
        prior.append(entry)
        node.metadata["o1_source_comparator_frontiers"] = prior
        node.metadata["o1_source_comparator_frontier"] = entry
        state.event(
            "routeb_o1_source_comparator_frontier",
            status=entry["status"],
            h_aggregate_data_level_exact=True,
            h_aggregate_function_lift_proven=False,
            h_body_proven=False,
            source_binding_proven=False,
            registry_promoted=False,
            formal_certificate_allowed=False,
        )
        state.validate()
        store.save(state)
    print({"status": "recorded" if changed else "already_recorded", "revision": store.load().revision})


if __name__ == "__main__":
    main()
