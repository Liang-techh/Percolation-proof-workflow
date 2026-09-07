"""Record the compiled O2 endpoint witness handoff without widening its claim."""
from __future__ import annotations

import hashlib
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
REVIEW = ROOT / "agent_review_inbox/review-T-P4-036.2-authoritative-leaf-witness-handoff-codex-20260907.md"
SCHEMA = ROOT / "artifacts/routeb_theta2_leaf_handoff_20260907/routeb-theta2-leaf-handoff-v1.schema.json"
HANDOFF = ROOT / "artifacts/routeb_theta2_leaf_handoff_20260907/theta2_leaf_1_endpoint_handoff.json"
SOURCE_RECEIPT = ROOT / "artifacts/routeb_agent_p3_coverage_next_20260906T091543Z/p3_coverage_bridge_audit.json"
LEAN = ROOT / "artifacts/routeb_fd8_tensor_christoffel_enclosure_20260906/mathlib/DownstreamTest/Theta2LeafHandoffAdapterGenerated.lean"
OLEAN = ROOT / "artifacts/routeb_fd8_tensor_christoffel_enclosure_20260906/mathlib/.lake/build/lib/lean/DownstreamTest/Theta2LeafHandoffAdapterGenerated.olean"
STATE = ROOT / "artifacts/routeb_6dof/state.json"
EXPECTED = {
    "schema": "F5191ED71F3A369414803ACCBD4ABE07639F71A3BD1CB3C2BCE03E6C3A77DAB6",
    "handoff": "9453049983A4F59D0438CE0F51EDD6BC6F6C0E6FDEA91522B524A5828C6709ED",
    "source_receipt": "87CF832BF5D9D266A532EEA4DC54B9365FF9E4A5E709031907C8E9A97BDDC7D6",
    "lean": "248DACF3BF0749574477EFAB6DFF71DA0DC4684BB05FC1B5210FF5F7C66D17CB",
    "olean": "45D911A0AB09382793845DE801D21DA10ABBA668BB925ED1DE158F45031A325B",
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
    for path in (REVIEW, SCHEMA, HANDOFF, SOURCE_RECEIPT, LEAN, OLEAN, STATE):
        if not path.is_file():
            raise FileNotFoundError(path)
    text = REVIEW.read_text(encoding="utf-8", errors="replace")
    for phrase in (
        "ENDPOINT_PROVENANCE_ONLY",
        "receipt_leaf1_witness_in_rectbox",
        "coverage_join2_child_or_sibling",
        "source-bound authoritative dynamic leaf",
        "不改变 O2 formal gate",
    ):
        if phrase not in text:
            raise ValueError(f"O2 endpoint witness boundary missing: {phrase}")
    actual = {
        "schema": sha(SCHEMA),
        "handoff": sha(HANDOFF),
        "source_receipt": sha(SOURCE_RECEIPT),
        "lean": sha(LEAN),
        "olean": sha(OLEAN),
    }
    if actual != EXPECTED:
        raise ValueError(f"O2 endpoint witness hash mismatch: {actual} != {EXPECTED}")
    entry = {
        "schema_version": 1,
        "task_id": "T-P4-036.2",
        "source_agent": "codex-inbox",
        "review_status": "COMPILED_ENDPOINT_PROVENANCE_ONLY",
        "review_artifact": {"path": str(REVIEW.resolve()), "sha256": sha(REVIEW)},
        "schema_sha256": actual["schema"],
        "handoff_sha256": actual["handoff"],
        "source_receipt_sha256": actual["source_receipt"],
        "lean_source_sha256": actual["lean"],
        "olean_sha256": actual["olean"],
        "compile_exit_code": 0,
        "axioms": ["propext", "Classical.choice", "Quot.sound"],
        "closed_child": "recorded endpoint -> exact ℚ -> RectBox13 -> lower-corner InRectBox",
        "parent_lift": "conditional BoxSubset premise",
        "coverage_join": "conditional CoverageJoin2 premise only",
        "authority_status": "ENDPOINT_PROVENANCE_ONLY",
        "source_bound_dynamic_leaf": False,
        "trajectory_membership": False,
        "global_coverage": False,
        "formal_certificate_allowed": False,
        "registry_promoted": False,
    }
    store = StateStore(STATE)
    state = store.load()
    node = find(state, "P4.true_dh_float64_evaluator_enclosure")
    prior = list(node.metadata.get("o2_endpoint_witness_handoffs", []))
    changed = entry not in prior
    if changed:
        prior.append(entry)
        node.metadata["o2_endpoint_witness_handoffs"] = prior
    desired = {
        "status": entry["review_status"],
        "handoff_sha256": actual["handoff"],
        "lean_source_sha256": actual["lean"],
        "olean_sha256": actual["olean"],
        "compile_exit_code": 0,
        "authority_status": entry["authority_status"],
        "source_bound_dynamic_leaf": False,
        "trajectory_membership": False,
        "global_coverage": False,
        "formal_certificate_allowed": False,
        "registry_promoted": False,
    }
    if node.metadata.get("o2_endpoint_witness_handoff") != desired:
        node.metadata["o2_endpoint_witness_handoff"] = desired
        changed = True
    if changed:
        state.event(
            "routeb_o2_endpoint_witness_handoff_recorded",
            node_id=node.id,
            review_status=entry["review_status"],
            authority_status=entry["authority_status"],
            source_bound_dynamic_leaf=False,
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
