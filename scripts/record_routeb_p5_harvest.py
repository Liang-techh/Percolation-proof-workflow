"""Attach the latest P5 mathematical harvest without theorem admission."""
from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
STATE = ROOT / "artifacts/routeb_6dof/state.json"
NODE_NAME = "P5.componentwise_relative_decay"
P5_NODE = ROOT / "examples/routeb_p5_joint_centered_gain_lean"
P5_024_REVIEW = ROOT / "agent_review_inbox/review-T-P5-024-kuangmanmozun-20260907T0945.md"
P5_025_REVIEW = ROOT / "agent_review_inbox/review-T-P5-025-liuguanyi-20260907T1020.md"

sys.path.insert(0, str(ROOT / "src"))
from percolation_workflow.store import StateStore  # noqa: E402


def digest(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest().upper()


def find(state, name: str):
    for node in state.nodes.values():
        if node.name == name:
            return node
    raise ValueError(f"missing node: {name}")


def artifact(path: Path) -> dict[str, str]:
    return {"path": str(path.resolve()), "sha256": digest(path)}


def main() -> None:
    files = [P5_024_REVIEW, P5_025_REVIEW, P5_NODE / "P5JointCenteredGain.lean",
             P5_NODE / "README.md", P5_NODE / "lean-toolchain", P5_NODE / "verify.sh"]
    for path in files:
        if not path.is_file():
            raise FileNotFoundError(path)
    p5_024 = {
        "child_id": "T-P5-024",
        "statement": "25 * U * N <= 144 * Q^2 and 144 * ell2 <= 25 * mu^2 implies centered coupling <= mu * Q",
        "status": "compiled_candidate",
        "integration_status": "pending_coordinator_admission",
        "admission_label": "compiled_candidate",
        "review_artifact": artifact(P5_024_REVIEW),
        "sidecar_artifacts": [artifact(P5_NODE / name) for name in
                              ("P5JointCenteredGain.lean", "README.md", "lean-toolchain", "verify.sh")],
        "source_independent": True,
        "physical_source_binding": False,
        "path_or_coverage_binding": False,
        "registry_promoted": False,
        "formal_certificate_allowed": False,
        "evidence_boundary": "review reports focused Lean CI, but coordinator has not independently rerun it",
        "required_followups": [
            "independent final-agent audit",
            "statement comparator receipt",
            "source/path/coverage binding before any Route-B admission",
        ],
    }
    p5_025 = {
        "child_id": "T-P5-025",
        "statement": "finite orthant PSD certificates consume a nonnegative K_path table directly",
        "status": "pending_math_child",
        "integration_status": "pending_coordinator_admission",
        "admission_label": "pending",
        "review_artifact": artifact(P5_025_REVIEW),
        "source_independent": True,
        "physical_source_binding": False,
        "path_or_coverage_binding": False,
        "registry_promoted": False,
        "formal_certificate_allowed": False,
        "evidence_boundary": "mathematical interface only; no compiled sidecar or source-bound K_path receipt",
        "required_followups": [
            "formalize finite orthant sign reduction",
            "preserve K_path as a typed component matrix",
            "independent final-agent audit",
        ],
    }
    store = StateStore(STATE)
    state = store.load()
    node = find(state, NODE_NAME)
    children = list(node.metadata.get("conditional_children", []))
    by_id = {entry.get("child_id"): entry for entry in children if isinstance(entry, dict)}
    changed = False
    for entry in (p5_024, p5_025):
        if by_id.get(entry["child_id"]) != entry:
            by_id[entry["child_id"]] = entry
            changed = True
    if changed:
        node.metadata["conditional_children"] = list(by_id.values())
        node.metadata["p5_harvest_boundary"] = "compiled candidates and pending mathematics do not close P5"
        state.event(
            "routeb_p5_mathematical_harvest_recorded",
            node_id=node.id,
            child_ids=["T-P5-024", "T-P5-025"],
            p5_024_status=p5_024["status"],
            p5_025_status=p5_025["status"],
            registry_promoted=False,
            formal_certificate_allowed=False,
        )
        state.validate()
        store.save(state)
    print({"status": "recorded" if changed else "already_recorded",
           "node": node.id, "revision": store.load().revision,
           "registry_promoted": False, "formal_certificate_allowed": False})


if __name__ == "__main__":
    main()
