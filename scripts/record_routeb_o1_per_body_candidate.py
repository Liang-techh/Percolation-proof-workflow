"""Record the O1 per-body Lean candidate without promoting it."""
from __future__ import annotations

from hashlib import sha256
import json
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
BODY2_CHECK = ROOT / "examples/routeb_b45_source_comparator_lean/O1_BODY_2_TARGET_CHECK.json"
BODY2_RECEIPT = ROOT / "examples/routeb_b45_source_comparator_lean/O1_BODY_2_SOURCE_BRIDGE_RECEIPT.json"
BODY3_RECEIPT = ROOT / "examples/routeb_b45_source_comparator_lean/O1_BODY_3_SOURCE_BRIDGE_RECEIPT.json"
BODY3_CHECK = ROOT / "examples/routeb_b45_source_comparator_lean/O1_BODY_3_TARGET_CHECK.json"
BODY3_DECOMP_RECEIPT = ROOT / "examples/routeb_b45_source_comparator_lean/O1_BODY_3_SOURCE_DECOMPOSITION_RECEIPT.json"
BODY3_DECOMP_REVIEW = ROOT / "agent_review_inbox/review-T-P4-033-O1-body-3-source-decomposition-codex-20260907.md"
BODY4_RECEIPT = ROOT / "examples/routeb_b45_source_comparator_lean/O1_BODY_4_SOURCE_BRIDGE_RECEIPT.json"
BODY4_CHECK = ROOT / "examples/routeb_b45_source_comparator_lean/O1_BODY_4_TARGET_CHECK.json"
BODY4_REVIEW = ROOT / "agent_review_inbox/review-T-P4-033-O1-body-4-source-bridge-codex-20260907.md"
BODY5_RECEIPT = ROOT / "examples/routeb_b45_source_comparator_lean/O1_BODY_5_SOURCE_BRIDGE_RECEIPT.json"
BODY5_CHECK = ROOT / "examples/routeb_b45_source_comparator_lean/O1_BODY_5_TARGET_CHECK.json"
BODY5_REVIEW = ROOT / "agent_review_inbox/review-T-P4-033-O1-body-5-source-bridge-codex-20260907.md"
BODY4_FOLD_TARGET = ROOT / "examples/routeb_b45_source_comparator_lean/RouteBO1Body4TraceFoldTargets.lean"
BODY4_FOLD_RECEIPT = ROOT / "examples/routeb_b45_source_comparator_lean/O1_BODY_4_TRACE_FOLD_TARGETS_RECEIPT.json"
BODY4_FOLD_REVIEW = ROOT / "agent_review_inbox/review-T-P4-033-O1-body-4-tagged-trace-fold-codex-20260907.md"
BODY4_GRAM_TARGET = ROOT / "examples/routeb_b45_source_comparator_lean/RouteBO1Body4SourceGramTargets.lean"
BODY4_GRAM_CHECK = ROOT / "scripts/check_routeb_o1_body4_source_gram.py"
BODY4_GRAM_RECEIPT = ROOT / "examples/routeb_b45_source_comparator_lean/O1_BODY_4_SOURCE_GRAM_TARGETS_RECEIPT.json"
BODY4_GRAM_REVIEW = ROOT / "agent_review_inbox/review-T-P4-033-O1-body-4-source-gram-codex-20260907.md"
BODY5_TRACE_TARGET = ROOT / "examples/routeb_b45_source_comparator_lean/RouteBO1Body5SourceTraceTargets.lean"
BODY5_TRACE_RECEIPT = ROOT / "examples/routeb_b45_source_comparator_lean/O1_BODY_5_SOURCE_TRACE_DECOMPOSITION_RECEIPT_20260907_44fcccf7bd1a.json"
BODY5_TRACE_REVIEW = ROOT / "agent_review_inbox/review-T-P4-033-O1-body-5-source-trace-decomposition-codex-20260907-a977fb4941f1.md"
BODY5_NEW_GRAM = ROOT / "examples/routeb_b45_source_comparator_lean/NEW_BODY5_GramTraceSkeleton20260907.lean"
BODY5_NEW_TRACE = ROOT / "examples/routeb_b45_source_comparator_lean/NEW_BODY5_FiniteTraceSkeleton20260907.lean"
BODY5_NEW_REVIEW = ROOT / "examples/routeb_b45_source_comparator_lean/REVIEW_BODY5_G3_G4_FINITE_TRACE_20260907.md"
O0_BODY3_RECEIPT = ROOT / "agent_review_inbox/receipt-T-P4-033-O0-P-NE-body3-geometry-targets-20260907.json"
O0_BODY4_RECEIPT = ROOT / "agent_review_inbox/receipt-T-P4-033-O0-P-NE-body4-geometry-targets-20260907.json"
O0_BODY5_RECEIPT = ROOT / "agent_review_inbox/receipt-T-P4-033-O0-P-NE-body5-geometry-source-20260907.json"
O0_BODY5_REVIEW = ROOT / "agent_review_inbox/review-T-P4-033-O0-P-NE-body5-geometry-source-20260907.md"
HACC_REVIEW = ROOT / "agent_review_inbox/review-T-P4-033-O0-H-acc-source-semantic-export-20260907.md"
HACC_REFINEMENT_REVIEW = ROOT / "agent_review_inbox/review-T-P4-033-O0-H-acc-evaluator-interval-contract-codex-20260907.md"
HACC_CONTRACT = ROOT / "examples/routeb_o0_h_acc_semantic_export/OPEN_CONTRACT.json"
HACC_RECEIPT = ROOT / "examples/routeb_o0_h_acc_semantic_export/RECEIPT.json"
HACC_REFINEMENT_RECEIPT = ROOT / "examples/routeb_o0_h_acc_source_refinement/RECEIPT.json"
HACC_NEW_SCHEMA = ROOT / "examples/routeb_o0_h_acc_source_refinement/NEW_INTAKE_SCHEMA.json"
HACC_NEW_INTAKE = ROOT / "examples/routeb_o0_h_acc_source_refinement/NEW_INTAKE.json"
HACC_NEW_LAYOUT = ROOT / "examples/routeb_o0_h_acc_source_refinement/NEW_LAYOUT_FIXTURE.json"
HACC_NEW_SOURCE_INTAKE = ROOT / "examples/routeb_o0_h_acc_source_refinement/NEW_source_intake.py"
HACC_NEW_TEST = ROOT / "examples/routeb_o0_h_acc_source_refinement/NEW_test_source_intake.py"
HACC_NEW_REVIEW = ROOT / "examples/routeb_o0_h_acc_source_refinement/NEW_REVIEW.md"
HACC_NEW_RECEIPT = ROOT / "examples/routeb_o0_h_acc_source_refinement/NEW_RECEIPT.json"
HACC_SEAM_SOURCE = ROOT / "examples/routeb_o0_h_acc_source_refinement/NEW_SEAM_source.py"
HACC_SEAM_TEST = ROOT / "examples/routeb_o0_h_acc_source_refinement/NEW_SEAM_test_source.py"
HACC_SEAM_REPORT = ROOT / "examples/routeb_o0_h_acc_source_refinement/NEW_SEAM_REPORT.json"
HACC_SEAM_REVIEW = ROOT / "examples/routeb_o0_h_acc_source_refinement/NEW_SEAM_REVIEW.md"
KEYED_INTERFACE = ROOT / "artifacts/task_routeb_o1_keyed_regrouping_20260907/RouteBO1KeyedRegroupingInterface.lean"
KEYED_RECEIPT = ROOT / "artifacts/task_routeb_o1_keyed_regrouping_20260907/interface_receipt.json"
KEYED_CHECK = ROOT / "artifacts/task_routeb_o1_keyed_regrouping_20260907/interface_check.json"
KEYED_ORIENTATION_REVIEW = ROOT / "agent_review_inbox/review-T-P4-033-O1-orientation-layer-codex-20260907.md"
BODY6_SUPPORT = ROOT / "examples/routeb_b45_source_comparator_lean/O1_BODY_6_SUPPORT_TARGET.json"
BODY6_REVIEW = ROOT / "agent_review_inbox/review-T-P4-033-O1-body-6-support-target-codex-20260907.md"
BODY6_CANONICAL_TARGET = ROOT / "examples/routeb_b45_source_comparator_lean/RouteBO1Body6CanonicalExportTargets.lean"
BODY6_CANONICAL_CONTRACT = ROOT / "examples/routeb_b45_source_comparator_lean/O1_BODY_6_CANONICAL_EXPORT_CONTRACT.json"
BODY6_CANONICAL_RECEIPT = ROOT / "examples/routeb_b45_source_comparator_lean/O1_BODY_6_CANONICAL_EXPORT_RECEIPT.json"
BODY6_CANONICAL_CSV = ROOT / "examples/routeb_b45_source_comparator_lean/O1_BODY_6_CANONICAL_SLICE.csv"
BODY6_CANONICAL_AUDIT = ROOT / "examples/routeb_b45_source_comparator_lean/audit_body6_canonical_export.py"
BODY6_CANONICAL_REVIEW = ROOT / "agent_review_inbox/review-T-P4-033-O1-body-6-canonical-export-codex-20260907.md"
PBUDGET_REVIEW = ROOT / "agent_review_inbox/review-T-P4-033-O0-P-BUDGET-physical-identity-20260907.md"
REVIEW = ROOT / "agent_review_inbox/review-T-P4-033-O1-per-body-candidate-codex-20260907.md"
AGENT_REVIEW = ROOT / "agent_review_inbox/review-T-P4-033-O1-per-body-source-definition-obstruction-codex-20260907.md"


def digest(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest().upper()


def find(state, name: str):
    for node in state.nodes.values():
        if node.name == name:
            return node
    raise ValueError(f"missing node: {name}")


def embedded_adapter_hashes(value):
    if isinstance(value, dict):
        path_text = value.get("path")
        if path_text and "sha256" in value:
            candidate = Path(path_text)
            if not candidate.is_absolute():
                candidate = ROOT / candidate
            if candidate.resolve() == ADAPTER.resolve():
                yield value["sha256"]
        for child in value.values():
            yield from embedded_adapter_hashes(child)
    elif isinstance(value, list):
        for child in value:
            yield from embedded_adapter_hashes(child)


def main() -> None:
    for path in (STATE, LEAN, TRACE, ADAPTER, GENERATOR, BODY_RECEIPT, BODY_CHECK,
                 BODY1_RECEIPT, BODY2_CHECK, BODY2_RECEIPT, BODY3_RECEIPT, BODY3_CHECK,
                 BODY3_DECOMP_RECEIPT, BODY3_DECOMP_REVIEW,
                 BODY4_RECEIPT, BODY4_CHECK, BODY4_REVIEW,
                 BODY5_RECEIPT, BODY5_CHECK, BODY5_REVIEW,
                 BODY4_FOLD_TARGET, BODY4_FOLD_RECEIPT, BODY4_FOLD_REVIEW,
                 BODY4_GRAM_TARGET, BODY4_GRAM_CHECK, BODY4_GRAM_RECEIPT, BODY4_GRAM_REVIEW,
                 BODY5_TRACE_TARGET, BODY5_TRACE_RECEIPT, BODY5_TRACE_REVIEW,
                 BODY5_NEW_GRAM, BODY5_NEW_TRACE, BODY5_NEW_REVIEW,
                 O0_BODY3_RECEIPT, O0_BODY4_RECEIPT, O0_BODY5_RECEIPT, O0_BODY5_REVIEW,
                 HACC_REVIEW, HACC_REFINEMENT_REVIEW, HACC_CONTRACT, HACC_RECEIPT,
                 HACC_REFINEMENT_RECEIPT, HACC_NEW_SCHEMA, HACC_NEW_INTAKE,
                 HACC_NEW_LAYOUT, HACC_NEW_SOURCE_INTAKE, HACC_NEW_TEST,
                 HACC_NEW_REVIEW, HACC_NEW_RECEIPT, HACC_SEAM_SOURCE,
                 HACC_SEAM_TEST, HACC_SEAM_REPORT, HACC_SEAM_REVIEW,
                 KEYED_INTERFACE, KEYED_RECEIPT, KEYED_CHECK,
                 KEYED_ORIENTATION_REVIEW, BODY6_SUPPORT, BODY6_REVIEW,
                 BODY6_CANONICAL_TARGET, BODY6_CANONICAL_CONTRACT, BODY6_CANONICAL_RECEIPT,
                 BODY6_CANONICAL_CSV, BODY6_CANONICAL_AUDIT, BODY6_CANONICAL_REVIEW,
                 PBUDGET_REVIEW,
                 REVIEW, AGENT_REVIEW):
        if not path.is_file():
            raise FileNotFoundError(path)
    adapter_sha256 = digest(ADAPTER)
    for receipt_path in (BODY1_RECEIPT, BODY2_RECEIPT, BODY3_RECEIPT, BODY4_RECEIPT,
                         BODY5_RECEIPT, BODY4_FOLD_RECEIPT, O0_BODY3_RECEIPT,
                         O0_BODY4_RECEIPT, O0_BODY5_RECEIPT, BODY4_GRAM_RECEIPT,
                         BODY5_TRACE_RECEIPT):
        receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
        embedded = list(embedded_adapter_hashes(receipt))
        if embedded and any(str(value).upper() != adapter_sha256 for value in embedded):
            raise ValueError(
                f"stale adapter provenance in {receipt_path}: {embedded!r} != {adapter_sha256}"
            )
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
        "body_trace_adapter_sha256": adapter_sha256,
        "generator_sha256": digest(GENERATOR),
        "body_trace_receipt_sha256": digest(BODY_RECEIPT),
        "body_trace_receipt_status": "OPEN_H_BODY_PROOFS_UNCOMPILED",
        "body_trace_check_sha256": digest(BODY_CHECK),
        "body_trace_check_status": "PASS_GENERATED_TYPED_EVALUATOR_FAIL_CLOSED",
        "body_trace_structure_checked": True,
        "body_1_source_bridge_receipt_sha256": digest(BODY1_RECEIPT),
        "body_1_source_bridge_status": "OPEN_BODY_1_SOURCE_EXPANSION_LEMMAS",
        "body_1_source_bridge_proven": False,
        "body_2_target_check_sha256": digest(BODY2_CHECK),
        "body_2_target_check_status": "PASS_EXACT_BODY2_TARGET_COEFFICIENTS_FAIL_CLOSED",
        "body_2_target_coefficients_proven": False,
        "body_2_source_bridge_receipt_sha256": digest(BODY2_RECEIPT),
        "body_2_source_bridge_status": "OPEN_BODY_2_SOURCE_AND_TRACE_PREMISES",
        "body_2_source_bridge_proven": False,
        "body_3_source_bridge_receipt_sha256": digest(BODY3_RECEIPT),
        "body_3_source_bridge_status": "OPEN_BODY_3_SOURCE_AND_TRACE_PREMISES",
        "body_3_source_bridge_proven": False,
        "body_3_target_check_sha256": digest(BODY3_CHECK),
        "body_3_target_check_status": "PASS_EXACT_BODY3_TARGET_COEFFICIENTS_FAIL_CLOSED",
        "body_3_target_coefficients_proven": False,
        "body_3_source_decomposition_receipt_sha256": digest(BODY3_DECOMP_RECEIPT),
        "body_3_source_decomposition_review_sha256": digest(BODY3_DECOMP_REVIEW),
        "body_3_source_decomposition_status": "OPEN_BODY_3_SOURCE_DECOMPOSITION_TARGETS_ONLY",
        "body_3_source_decomposition_proven": False,
        "body_4_source_bridge_receipt_sha256": digest(BODY4_RECEIPT),
        "body_4_source_bridge_status": "OPEN_BODY_4_SOURCE_AND_TRACE_PREMISES",
        "body_4_source_bridge_proven": False,
        "body_4_target_check_sha256": digest(BODY4_CHECK),
        "body_4_target_check_status": "PASS_EXACT_BODY4_TARGET_COEFFICIENTS_FAIL_CLOSED",
        "body_4_target_coefficients_proven": False,
        "body_4_review_sha256": digest(BODY4_REVIEW),
        "o0_body_4_geometry_receipt_sha256": digest(O0_BODY4_RECEIPT),
        "o0_body_4_geometry_status": "CONDITIONAL_BODY4_GEOMETRY_DERIVATION",
        "o0_body_4_geometry_proven": False,
        "body_5_source_bridge_receipt_sha256": digest(BODY5_RECEIPT),
        "body_5_source_bridge_status": "OPEN_BODY_5_SOURCE_AND_TRACE_PREMISES",
        "body_5_source_bridge_proven": False,
        "body_5_target_check_sha256": digest(BODY5_CHECK),
        "body_5_target_check_status": "PASS_EXACT_BODY5_TARGET_COEFFICIENTS_FAIL_CLOSED",
        "body_5_target_coefficients_proven": False,
        "body_5_review_sha256": digest(BODY5_REVIEW),
        "body_4_trace_fold_target_sha256": digest(BODY4_FOLD_TARGET),
        "body_4_trace_fold_receipt_sha256": digest(BODY4_FOLD_RECEIPT),
        "body_4_trace_fold_review_sha256": digest(BODY4_FOLD_REVIEW),
        "body_4_trace_fold_status": "TARGETS_ONLY_UNPROVEN",
        "body_4_trace_fold_proven": False,
        "body_4_source_gram_target_sha256": digest(BODY4_GRAM_TARGET),
        "body_4_source_gram_checker_sha256": digest(BODY4_GRAM_CHECK),
        "body_4_source_gram_receipt_sha256": digest(BODY4_GRAM_RECEIPT),
        "body_4_source_gram_review_sha256": digest(BODY4_GRAM_REVIEW),
        "body_4_source_gram_status": "OPEN_BODY4_SOURCE_GRAM_CHILD_TARGETS_UNCOMPILED",
        "body_4_source_gram_proven": False,
        "body_5_source_trace_target_sha256": digest(BODY5_TRACE_TARGET),
        "body_5_source_trace_receipt_sha256": digest(BODY5_TRACE_RECEIPT),
        "body_5_source_trace_review_sha256": digest(BODY5_TRACE_REVIEW),
        "body_5_source_trace_status": "OPEN_UNPROVEN_BODY5_SOURCE_TRACE_DECOMPOSITION",
        "body_5_source_trace_proven": False,
        "body_5_g3_g4_skeleton_sha256": digest(BODY5_NEW_GRAM),
        "body_5_finite_trace_skeleton_sha256": digest(BODY5_NEW_TRACE),
        "body_5_g3_g4_finite_trace_review_sha256": digest(BODY5_NEW_REVIEW),
        "body_5_g3_g4_finite_trace_status": "OPEN_UNCOMPILED_PROOF_SKELETON",
        "body_5_g3_g4_finite_trace_proven": False,
        "o0_body_5_geometry_receipt_sha256": digest(O0_BODY5_RECEIPT),
        "o0_body_5_geometry_review_sha256": digest(O0_BODY5_REVIEW),
        "o0_body_5_geometry_status": "CONDITIONAL_BODY5_GEOMETRY_DERIVATION",
        "o0_body_5_geometry_proven": False,
        "h_acc_review_sha256": digest(HACC_REVIEW),
        "h_acc_status": "OPEN_H_ACC_NO_DEPLOYED_SEMANTIC_EXPORT",
        "h_acc_proven": False,
        "h_acc_refinement_review_sha256": digest(HACC_REFINEMENT_REVIEW),
        "h_acc_contract_sha256": digest(HACC_CONTRACT),
        "h_acc_receipt_sha256": digest(HACC_RECEIPT),
        "h_acc_refinement_receipt_sha256": digest(HACC_REFINEMENT_RECEIPT),
        "h_acc_occurrence_intake_schema_sha256": digest(HACC_NEW_SCHEMA),
        "h_acc_occurrence_intake_sha256": digest(HACC_NEW_INTAKE),
        "h_acc_occurrence_layout_fixture_sha256": digest(HACC_NEW_LAYOUT),
        "h_acc_occurrence_intake_checker_sha256": digest(HACC_NEW_SOURCE_INTAKE),
        "h_acc_occurrence_intake_tests_sha256": digest(HACC_NEW_TEST),
        "h_acc_occurrence_intake_review_sha256": digest(HACC_NEW_REVIEW),
        "h_acc_occurrence_intake_receipt_sha256": digest(HACC_NEW_RECEIPT),
        "h_acc_seam_source_sha256": digest(HACC_SEAM_SOURCE),
        "h_acc_seam_test_sha256": digest(HACC_SEAM_TEST),
        "h_acc_seam_report_sha256": digest(HACC_SEAM_REPORT),
        "h_acc_seam_review_sha256": digest(HACC_SEAM_REVIEW),
        "h_acc_seam_status": "PENDING_OPEN_H_ACC_SOURCE_SEAM_ONLY",
        "h_acc_seam_proven": False,
        "h_acc_occurrence_intake_status": "PENDING_OPEN_H_ACC_NO_SOURCE_EXPORT",
        "h_acc_occurrence_intake_proven": False,
        "h_acc_refinement_status": "OPEN_H_ACC_SOURCE_REFINEMENT_AND_INTERVAL_SOUNDNESS",
        "h_acc_refinement_proven": False,
        "o0_body_3_geometry_receipt_sha256": digest(O0_BODY3_RECEIPT),
        "o0_body_3_geometry_status": "CONDITIONAL_BODY3_GEOMETRY_DERIVATION",
        "o0_body_3_geometry_proven": False,
        "keyed_regrouping_interface_sha256": digest(KEYED_INTERFACE),
        "keyed_regrouping_receipt_sha256": digest(KEYED_RECEIPT),
        "keyed_regrouping_status": "INTERFACE_ONLY_UNPROVED",
        "keyed_regrouping_proven": False,
        "keyed_regrouping_check_sha256": digest(KEYED_CHECK),
        "keyed_regrouping_check_status": "PASS_TYPED_KEYED_REGROUPING_INTERFACE_FAIL_CLOSED",
        "keyed_orientation_review_sha256": digest(KEYED_ORIENTATION_REVIEW),
        "keyed_generic_orientation_lemma_proven": True,
        "keyed_source_bound_orientation_proven": False,
        "body_6_support_target_sha256": digest(BODY6_SUPPORT),
        "body_6_support_status": "OPEN_BODY_LABEL_SEMANTIC_MISMATCH",
        "body_6_source_binding_proven": False,
        "body_6_canonical_target_sha256": digest(BODY6_CANONICAL_TARGET),
        "body_6_canonical_contract_sha256": digest(BODY6_CANONICAL_CONTRACT),
        "body_6_canonical_receipt_sha256": digest(BODY6_CANONICAL_RECEIPT),
        "body_6_canonical_slice_sha256": digest(BODY6_CANONICAL_CSV),
        "body_6_canonical_audit_sha256": digest(BODY6_CANONICAL_AUDIT),
        "body_6_canonical_review_sha256": digest(BODY6_CANONICAL_REVIEW),
        "body_6_canonical_export_status": "COEFFICIENT_REPLAY_MATCH_SOURCE_THEOREM_OPEN",
        "body_6_canonical_export_proven": False,
        "p_budget_review_sha256": digest(PBUDGET_REVIEW),
        "p_budget_status": "OPEN_P_BUDGET_PHYSICAL_IDENTITY",
        "p_budget_physical_identity_proven": False,
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
