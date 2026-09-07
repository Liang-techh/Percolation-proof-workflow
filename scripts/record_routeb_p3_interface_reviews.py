"""Attach source-binding and Lean-layer reviews for T-P4-036 to O2."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
ROUTE_B = ROOT.parent / "6dof_sos_optimized" / "6dof_sos_optimized"
STATE = ROOT / "artifacts/routeb_6dof/state.json"
REPORT = ROUTE_B / "routeB_dense_Mq/P3_DH_TRIG_CHAIN_CONTRACT.md"
CSV = ROUTE_B / "routeB_dense_Mq/routeB_p3_dh_trig_chain_contract.csv"
REVIEWS = (
    (
        ROOT / "agent_review_inbox/review-T-P4-036-source-binding-01a07bb4-d8f2-20260907.md",
        "01a07bb4-d8f2-7ba0-8258-8754bf2ea0f8",
        "SOURCE_BINDING_INTERFACE_REVIEW__OPEN",
        ("12 个 angle-formation", "12 个 range-reduction", "12 个 libm", "6 个 link"),
    ),
    (
        ROOT / "agent_review_inbox/review-T-P4-036-lean-layers-01a07bb4-dc1c-20260907.md",
        "01a07bb4-dc1c-7810-a164-f7a821ad0322",
        "LEAN_INTERFACE_LAYERS__UNCOMPILED_OPEN",
        ("Layer A", "Layer B", "Layer C", "Layer D"),
    ),
)
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
    for path, _, _, phrases in REVIEWS:
        if not path.is_file():
            raise FileNotFoundError(path)
        text = path.read_text(encoding="utf-8", errors="replace")
        if not all(phrase in text for phrase in phrases):
            raise ValueError(f"review boundary missing: {path}")
    source_refs = [
        {"path": str(REPORT.resolve()), "sha256": sha(REPORT)},
        {"path": str(CSV.resolve()), "sha256": sha(CSV)},
    ]
    entries = []
    for path, agent, status, _ in REVIEWS:
        entries.append({
            "schema_version": 1,
            "task_id": "T-P4-036",
            "source_agent": agent,
            "review_status": status,
            "review_artifact": {"path": str(path.resolve()), "sha256": sha(path)},
            "source_artifacts": source_refs,
            "evidence_level": "independent_static_review",
            "admission_status": "pending_coordinator_admission",
            "formal_certificate_allowed": False,
            "registry_eligible": False,
            "registry_promoted": False,
        })

    store = StateStore(STATE)
    state = store.load()
    node = find(state, "P4.true_dh_float64_evaluator_enclosure")
    prior = list(node.metadata.get("independent_static_reviews", []))
    changed = False
    for entry in entries:
        if entry not in prior:
            prior.append(entry)
            changed = True
    if changed:
        node.metadata["independent_static_reviews"] = prior
        state.event(
            "routeb_p3_interface_reviews_recorded",
            node_id=node.id,
            review_count=len(entries),
            admission_status="pending_coordinator_admission",
            registry_promoted=False,
            formal_certificate_allowed=False,
        )
        state.validate()
        store.save(state)
    print({
        "status": "recorded" if changed else "already_recorded",
        "review_count": len(entries),
        "state_revision": store.load().revision,
        "registry_promoted": False,
        "formal_certificate_allowed": False,
    })
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
