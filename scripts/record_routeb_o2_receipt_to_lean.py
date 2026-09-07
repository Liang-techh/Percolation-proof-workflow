"""Record a pinned single-leaf receipt-to-Lean adapter conditionally."""
from __future__ import annotations

import hashlib
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
REVIEW = ROOT / "agent_review_inbox/review-T-P4-036.2-receipt-to-lean-single-leaf-codex-20260907.md"
INPUT = ROOT / "artifacts/routeb_agent_p3_coverage_next_20260906T091543Z/p3_coverage_bridge_audit.json"
GENERATOR = ROOT / "scripts/routeb_theta2_receipt_to_lean.py"
SOURCE = ROOT / "artifacts/routeb_fd8_tensor_christoffel_enclosure_20260906/mathlib/DownstreamTest/Theta2ReceiptAdapterGenerated.lean"
OLEAN = ROOT / "artifacts/routeb_fd8_tensor_christoffel_enclosure_20260906/mathlib/.lake/build/lib/lean/DownstreamTest/Theta2ReceiptAdapterGenerated.olean"
STATE = ROOT / "artifacts/routeb_6dof/state.json"
EXPECTED = {
    "input": "87CF832BF5D9D266A532EEA4DC54B9365FF9E4A5E709031907C8E9A97BDDC7D6",
    "generator": "9675312237FEC4F69EE9B22D53E00B8ED9AFDD3F2C35AF445BD65D0E1ED52C39",
    "source": "5B9AD6A95D2F8C18C5F48A91AA6852724DA36C52060EDFCF3F95300431D56112",
    "olean": "DAE74AD000EC6153D7D03585A686C81915DC0506315AA33FF61A0A3EE996A3E9",
}
sys.path.insert(0, str(ROOT / "src"))

from percolation_workflow.store import StateStore  # noqa: E402


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def ref(path: Path) -> dict[str, str]:
    return {"path": str(path.resolve()), "sha256": sha(path)}


def find(state, name: str):
    for node in state.nodes.values():
        if node.name == name:
            return node
    raise ValueError(f"missing node: {name}")


def main() -> int:
    for path in (REVIEW, INPUT, GENERATOR, SOURCE, OLEAN, STATE):
        if not path.is_file():
            raise FileNotFoundError(path)
    text = REVIEW.read_text(encoding="utf-8", errors="replace")
    for phrase in (
        "Single-leaf receipt-to-Lean adapter",
        "cell_id = \"1\"",
        "receipt_leaf1_theta2_exact_real_interval",
        "exit_code: 0",
        "[propext, Classical.choice, Quot.sound]",
        "InRectBox_actual_witness: OPEN",
        "coverage_completeness: OPEN",
        "formal_certificate_allowed: false",
        "registry_promoted: false",
    ):
        if phrase not in text:
            raise ValueError(f"O2 receipt-to-Lean boundary missing: {phrase}")
    actual = {
        "input": sha(INPUT), "generator": sha(GENERATOR),
        "source": sha(SOURCE), "olean": sha(OLEAN),
    }
    if actual != EXPECTED:
        raise ValueError(f"O2 receipt-to-Lean hash drift: {actual}")
    entry = {
        "schema_version": 1,
        "task_id": "T-P4-036.2",
        "source_agent": "codex-inbox",
        "review_status": "COMPILED_SINGLE_LEAF_RECEIPT_TO_LEAN_CONDITIONAL",
        "review_artifact": ref(REVIEW),
        "input_receipt": ref(INPUT),
        "generator": ref(GENERATOR),
        "generated_source": ref(SOURCE),
        "generated_olean": ref(OLEAN),
        "leaf_id": 1,
        "coordinate_order": ["q1", "q2", "q3", "q4", "q5", "q6", "dq1", "dq2", "dq3", "dq4", "dq5", "dq6", "w"],
        "compiler_exit_code": 0,
        "axioms": ["propext", "Classical.choice", "Quot.sound"],
        "in_rectbox_actual_witness": "OPEN",
        "coverage_completeness": "OPEN",
        "float64_libm_dag": "OUT_OF_SCOPE",
        "formal_certificate_allowed": False,
        "registry_promoted": False,
        "admission_status": "conditional_single_leaf_transport",
    }
    store = StateStore(STATE)
    state = store.load()
    node = find(state, "P4.true_dh_float64_evaluator_enclosure")
    prior = list(node.metadata.get("o2_receipt_to_lean_children", []))
    changed = entry not in prior
    if changed:
        prior.append(entry)
        node.metadata["o2_receipt_to_lean_children"] = prior
    desired = {
        "status": entry["review_status"],
        "task_id": entry["task_id"],
        "leaf_id": 1,
        "input_sha256": EXPECTED["input"],
        "generator_sha256": EXPECTED["generator"],
        "source_sha256": EXPECTED["source"],
        "olean_sha256": EXPECTED["olean"],
        "compiler_exit_code": 0,
        "in_rectbox_actual_witness": "OPEN",
        "coverage_completeness": "OPEN",
        "formal_certificate_allowed": False,
        "registry_promoted": False,
    }
    if node.metadata.get("o2_receipt_to_lean_single_leaf") != desired:
        node.metadata["o2_receipt_to_lean_single_leaf"] = desired
        changed = True
    if changed:
        state.event(
            "routeb_o2_receipt_to_lean_single_leaf_recorded",
            node_id=node.id,
            leaf_id=1,
            compiler_exit_code=0,
            in_rectbox_actual_witness="OPEN",
            coverage_completeness="OPEN",
            registry_promoted=False,
            formal_certificate_allowed=False,
        )
        state.validate()
        store.save(state)
    print({
        "status": "recorded" if changed else "already_recorded",
        "review_status": entry["review_status"],
        "leaf_id": 1,
        "state_revision": store.load().revision,
        "registry_promoted": False,
        "formal_certificate_allowed": False,
    })
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
