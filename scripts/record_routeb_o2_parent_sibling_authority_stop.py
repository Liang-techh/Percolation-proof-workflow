"""Record the O2 parent/sibling authority stop without changing O2 status."""
from __future__ import annotations

import hashlib
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
REVIEW = ROOT / "agent_review_inbox/review-T-P4-036.2-leaf1-parent-sibling-authority-stop-codex-20260907.md"
TOPOLOGY = ROOT / "artifacts/task_routeb_math_bottleneck_audit_current/routeB_interval_coverage_receipt_audit_topology.json"
LOCAL_PAYLOAD = ROOT / "artifacts/task_routeb_local_box_replay_current/routeb_p3_source_bound_payload_current.json"
HANDOFF = ROOT / "artifacts/routeb_theta2_leaf_handoff_20260907/theta2_leaf_1_endpoint_handoff.json"
STATE = ROOT / "artifacts/routeb_6dof/state.json"
EXPECTED = {
    "topology": "0D191AD5F86D15F492AE7060E41AE0CBF42BB47E7DBF94AD273FFA32E5F32E5D",
    "local_payload": "028C0E2F1DE5FC0D84BCA8B8F7043073CA02424E5C402889ECE69B94F6F8FF6B",
    "handoff": "9453049983A4F59D0438CE0F51EDD6BC6F6C0E6FDEA91522B524A5828C6709ED",
}
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
    for path in (REVIEW, TOPOLOGY, LOCAL_PAYLOAD, HANDOFF, STATE):
        if not path.is_file():
            raise FileNotFoundError(path)
    text = REVIEW.read_text(encoding="utf-8", errors="replace")
    for phrase in (
        "ENDPOINT_PROVENANCE_ONLY",
        "parent_id、sibling_ids",
        "run_status = INCOMPLETE",
        "coverage_complete = false",
        "不能补出 authoritative parent/sibling",
        "没有修改 leaf-1 adapter",
    ):
        if phrase not in text:
            raise ValueError(f"O2 parent/sibling stop boundary missing: {phrase}")
    actual = {
        "topology": sha(TOPOLOGY),
        "local_payload": sha(LOCAL_PAYLOAD),
        "handoff": sha(HANDOFF),
    }
    if actual != EXPECTED:
        raise ValueError(f"O2 parent/sibling provenance hash mismatch: {actual} != {EXPECTED}")
    entry = {
        "schema_version": 1,
        "task_id": "T-P4-036.2",
        "source_agent": "codex-inbox",
        "review_status": "OPEN_PARENT_SIBLING_AUTHORITY_STOP",
        "review_artifact": {"path": str(REVIEW.resolve()), "sha256": sha(REVIEW)},
        "topology_sha256": actual["topology"],
        "local_payload_sha256": actual["local_payload"],
        "leaf_handoff_sha256": actual["handoff"],
        "parent_sibling_records_present": False,
        "box_subset_premise_instantiated": False,
        "coverage_join_premise_instantiated": False,
        "authority_status": "ENDPOINT_PROVENANCE_ONLY",
        "missing_fields": [
            "parent box/source/hash", "sibling box/source/hash",
            "child-to-parent endpoint inequalities", "same coordinate/leaf linkage",
        ],
        "global_coverage": False,
        "formal_certificate_allowed": False,
        "registry_promoted": False,
    }
    store = StateStore(STATE)
    state = store.load()
    node = find(state, "P4.true_dh_float64_evaluator_enclosure")
    prior = list(node.metadata.get("o2_parent_sibling_authority_stops", []))
    changed = entry not in prior
    if changed:
        prior.append(entry)
        node.metadata["o2_parent_sibling_authority_stops"] = prior
    desired = {
        "status": entry["review_status"],
        "review_sha256": entry["review_artifact"]["sha256"],
        "topology_sha256": actual["topology"],
        "local_payload_sha256": actual["local_payload"],
        "parent_sibling_records_present": False,
        "box_subset_premise_instantiated": False,
        "coverage_join_premise_instantiated": False,
        "authority_status": entry["authority_status"],
        "global_coverage": False,
        "formal_certificate_allowed": False,
        "registry_promoted": False,
    }
    if node.metadata.get("o2_parent_sibling_authority_stop") != desired:
        node.metadata["o2_parent_sibling_authority_stop"] = desired
        changed = True
    if changed:
        state.event(
            "routeb_o2_parent_sibling_authority_stop_recorded",
            node_id=node.id,
            review_status=entry["review_status"],
            parent_sibling_records_present=False,
            global_coverage=False,
            registry_promoted=False,
            formal_certificate_allowed=False,
        )
        state.validate()
        store.save(state)
    print({
        "status": "recorded" if changed else "already_recorded",
        "review_status": entry["review_status"],
        "state_revision": store.load().revision,
        "authority_status": entry["authority_status"],
        "global_coverage": False,
        "registry_promoted": False,
        "formal_certificate_allowed": False,
    })
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
