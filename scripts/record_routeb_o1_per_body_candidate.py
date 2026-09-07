"""Record the O1 per-body Lean candidate without promoting it."""
from __future__ import annotations

from hashlib import sha256
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from percolation_workflow.store import StateStore  # noqa: E402


STATE = ROOT / "artifacts/routeb_6dof/state.json"
LEAN = ROOT / "examples/routeb_b45_source_comparator_lean/RouteBO1PerBodyExactSource.lean"
TRACE = ROOT / "examples/routeb_b45_source_comparator_lean/BodyTraceEvaluator.lean"
ADAPTER = ROOT / "examples/routeb_b45_source_comparator_lean/RouteBO1PerBodyTraceAdapter.lean"
GENERATOR = ROOT / "examples/routeb_b45_source_comparator_lean/generate_body_trace_evaluator.py"
BODY_RECEIPT = ROOT / "examples/routeb_b45_source_comparator_lean/O1_BODY_TRACE_EVALUATOR_RECEIPT.json"
BODY_CHECK = ROOT / "examples/routeb_b45_source_comparator_lean/O1_BODY_TRACE_EVALUATOR_CHECK.json"
BODY1_RECEIPT = ROOT / "examples/routeb_b45_source_comparator_lean/O1_BODY_1_SOURCE_BRIDGE_RECEIPT.json"
REVIEW = ROOT / "agent_review_inbox/review-T-P4-033-O1-per-body-candidate-codex-20260907.md"
AGENT_REVIEW = ROOT / "agent_review_inbox/review-T-P4-033-O1-per-body-source-definition-obstruction-codex-20260907.md"


def digest(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest().upper()


def find(state, name: str):
    for node in state.nodes.values():
        if node.name == name:
            return node
    raise ValueError(f"missing node: {name}")


def main() -> None:
    for path in (STATE, LEAN, TRACE, ADAPTER, GENERATOR, BODY_RECEIPT, BODY_CHECK,
                 BODY1_RECEIPT, REVIEW, AGENT_REVIEW):
        if not path.is_file():
            raise FileNotFoundError(path)
    store = StateStore(STATE)
    state = store.load()
    leaves = [
        find(state, "P4.O1.source_comparator.h_aggregate_function_lift"),
        *(find(state, f"P4.O1.source_comparator.h_body_{body}")
          for body in range(1, 7)),
    ]
    entry = {
        "status": "UNCOMPILED_TYPED_CANDIDATE",
        "artifact": str(LEAN.resolve()),
        "artifact_sha256": digest(LEAN),
        "body_trace_evaluator": str(TRACE.resolve()),
        "body_trace_evaluator_sha256": digest(TRACE),
        "body_trace_adapter": str(ADAPTER.resolve()),
        "body_trace_adapter_sha256": digest(ADAPTER),
        "generator_sha256": digest(GENERATOR),
        "body_trace_receipt_sha256": digest(BODY_RECEIPT),
        "body_trace_receipt_status": "OPEN_H_BODY_PROOFS_UNCOMPILED",
        "body_trace_check_sha256": digest(BODY_CHECK),
        "body_trace_check_status": "PASS_GENERATED_TYPED_EVALUATOR_FAIL_CLOSED",
        "body_trace_structure_checked": True,
        "body_1_source_bridge_receipt_sha256": digest(BODY1_RECEIPT),
        "body_1_source_bridge_status": "OPEN_BODY_1_SOURCE_EXPANSION_LEMMAS",
        "body_1_source_bridge_proven": False,
        "typed_body_evaluator_present": True,
        "body_trace_row_count": 727,
        "review_sha256": digest(REVIEW),
        "agent_review_sha256": digest(AGENT_REVIEW),
        "h_aggregate_function_lift_proven": False,
        "h_body_proven": False,
        "source_binding_proven": False,
        "registry_promoted": False,
        "formal_certificate_allowed": False,
    }
    changed = False
    for leaf in leaves:
        prior = list(leaf.metadata.get("candidate_artifacts", []))
        if entry not in prior:
            prior.append(entry)
            leaf.metadata["candidate_artifacts"] = prior
            changed = True
    if changed:
        state.event(
            "routeb_o1_per_body_typed_candidate_recorded",
            artifact_sha256=entry["artifact_sha256"],
            leaf_ids=[leaf.id for leaf in leaves],
            h_aggregate_function_lift_proven=False,
            h_body_proven=False,
            registry_promoted=False,
            formal_certificate_allowed=False,
        )
        state.validate()
        store.save(state)
    print({"status": "recorded" if changed else "already_recorded", "revision": store.load().revision})


if __name__ == "__main__":
    main()
