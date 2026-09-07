"""Record O2 GCN parent/sibling candidates as non-authoritative evidence."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
REVIEW = ROOT / "agent_review_inbox/review-T-P4-036.2-parent-sibling-source-bound-candidates-codex-20260907.md"
OBSTRUCTION = ROOT / "artifacts/routeb_theta2_leaf_handoff_20260907/theta2_leaf_1_coverage_join_obstruction.json"
F1 = ROOT / "artifacts/task_routeb_gcn_f1_leaf_current/leaf_witness.json"
F2 = ROOT / "artifacts/task_routeb_gcn_f2_neighbor_current/neighbor_witness.json"
HANDOFF = ROOT / "artifacts/routeb_theta2_leaf_handoff_20260907/theta2_leaf_1_endpoint_handoff.json"
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
    for path in (REVIEW, OBSTRUCTION, F1, F2, HANDOFF, STATE):
        if not path.is_file():
            raise FileNotFoundError(path)
    text = REVIEW.read_text(encoding="utf-8", errors="replace")
    for phrase in (
        "source/hash-bound parent/sibling CANDIDATE：找到",
        "source/hash-bound authoritative O2 parent/sibling：仍未找到",
        "不能",
        "BLOCKED_AUTHORITY_NOT_ADMISSIBLE",
        "不是 O2 handoff 所需的 canonical 13-coordinate `RectBox13`",
        "未进行 Lean/Lake 编译或全域回归",
    ):
        if phrase not in text:
            raise ValueError(f"O2 candidate-authority obstruction missing: {phrase}")
    obstruction = json.loads(OBSTRUCTION.read_text(encoding="utf-8"))
    if obstruction.get("status") != "BLOCKED_AUTHORITY_NOT_ADMISSIBLE":
        raise ValueError("coverage obstruction is not fail-closed")
    actual = {"review": sha(REVIEW), "obstruction": sha(OBSTRUCTION), "f1": sha(F1), "f2": sha(F2), "handoff": sha(HANDOFF)}
    entry = {
        "schema_version": 1,
        "task_id": "T-P4-036.2-GCN-CANDIDATE-AUTHORITY",
        "source_agent": "codex-inbox",
        "review_status": "BLOCKED_AUTHORITY_NOT_ADMISSIBLE",
        "review_artifact": {"path": str(REVIEW.resolve()), "sha256": actual["review"]},
        "obstruction_artifact": {"path": str(OBSTRUCTION.resolve()), "sha256": actual["obstruction"]},
        "candidate_records": [
            {"name": "GCN-F1", "path": str(F1.resolve()), "sha256": actual["f1"], "admissible_for_o2_join": False},
            {"name": "GCN-F2", "path": str(F2.resolve()), "sha256": actual["f2"], "admissible_for_o2_join": False},
        ],
        "o2_leaf_handoff_sha256": actual["handoff"],
        "authority_status": "ENDPOINT_PROVENANCE_ONLY",
        "coverage_join_premise_instantiated": False,
        "global_coverage": False,
        "formal_certificate_allowed": False,
        "registry_promoted": False,
        "missing": [
            "canonical O2 13D parent endpoint",
            "canonical O2 13D sibling endpoint",
            "same-namespace child-parent/sibling linkage",
            "source interval membership and accepted authority status",
            "typed parent coverage join premise",
        ],
    }
    store = StateStore(STATE)
    state = store.load()
    node = find(state, "P4.true_dh_float64_evaluator_enclosure")
    prior = list(node.metadata.get("o2_candidate_authority_obstructions", []))
    changed = entry not in prior
    if changed:
        prior.append(entry)
        node.metadata["o2_candidate_authority_obstructions"] = prior
    desired = {
        "status": entry["review_status"],
        "review_sha256": actual["review"],
        "obstruction_sha256": actual["obstruction"],
        "f1_sha256": actual["f1"],
        "f2_sha256": actual["f2"],
        "authority_status": entry["authority_status"],
        "coverage_join_premise_instantiated": False,
        "global_coverage": False,
        "formal_certificate_allowed": False,
        "registry_promoted": False,
    }
    if node.metadata.get("o2_candidate_authority_obstruction") != desired:
        node.metadata["o2_candidate_authority_obstruction"] = desired
        changed = True
    if changed:
        state.event(
            "routeb_o2_candidate_authority_obstruction_recorded",
            node_id=node.id,
            review_status=entry["review_status"],
            authority_status=entry["authority_status"],
            coverage_join_premise_instantiated=False,
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
        "coverage_join_premise_instantiated": False,
        "global_coverage": False,
        "registry_promoted": False,
    })
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
