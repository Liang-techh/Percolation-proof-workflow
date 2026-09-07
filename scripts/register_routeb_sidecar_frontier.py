"""Register harvested Route-B sidecars as explicit open DAG children.

This is a fail-closed graph operation.  It creates no proof, does not touch the
verified registry, and is idempotent by theorem name.  Sidecar receipts remain
the evidence for the child; the graph node only makes the decomposition
dispatchable by the ordinary frontier scheduler.
"""
from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
STATE = ROOT / "artifacts/routeb_6dof/state.json"
sys.path.insert(0, str(ROOT / "src"))
from percolation_workflow.store import StateStore  # noqa: E402


def digest(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest().upper()


def find_id(state, name: str) -> str:
    for node in state.nodes.values():
        if node.name == name:
            return node.id
    raise ValueError(f"missing parent node: {name}")


def find_node(state, name: str):
    for node in state.nodes.values():
        if node.name == name:
            return node
    return None


def artifact(relative: str) -> dict[str, str]:
    path = ROOT / relative
    if not path.is_file():
        raise FileNotFoundError(path)
    return {"path": str(path.resolve()), "sha256": digest(path)}


CHILDREN = [
    {
        "name": "P4.O1.source_comparator.h_body_4.source_gram_targets",
        "parent": "P4.O1.source_comparator.h_body_4",
        "statement": "Body-4 source frame, Jacobian, Gram, and exact piecewise mass targets imply the existing body-4 entry target.",
        "proof_sketch": "Expand slots 0..4 and parent axes, derive midpoint/Jv/Jw, reduce diagonal inertia and finite Gram entries, then discharge the exact trig identities.",
        "lane": "source_semantics",
        "bottleneck": "source_semantics",
        "status": "OPEN_BODY4_SOURCE_GRAM_CHILD_TARGETS_UNCOMPILED",
        "artifacts": [
            "examples/routeb_b45_source_comparator_lean/RouteBO1Body4SourceGramTargets.lean",
            "scripts/check_routeb_o1_body4_source_gram.py",
            "examples/routeb_b45_source_comparator_lean/O1_BODY_4_SOURCE_GRAM_TARGETS_RECEIPT.json",
            "agent_review_inbox/review-T-P4-033-O1-body-4-source-gram-codex-20260907.md",
        ],
    },
    {
        "name": "P4.O1.source_comparator.h_body_5.source_trace_decomposition",
        "parent": "P4.O1.source_comparator.h_body_5",
        "statement": "Body-5 source geometry/Gram and exact tagged q3 finite-fold targets imply the existing body-5 entry target.",
        "proof_sketch": "Prove G1-G3 source geometry and Gram first; independently prove F1-F4 row permutation, q3 product-to-sum, arbitrary-seed fold, and the final piecewise handoff.",
        "lane": "source_semantics",
        "bottleneck": "source_semantics",
        "status": "OPEN_UNPROVEN_BODY5_SOURCE_TRACE_DECOMPOSITION",
        "artifacts": [
            "examples/routeb_b45_source_comparator_lean/RouteBO1Body5SourceTraceTargets.lean",
            "examples/routeb_b45_source_comparator_lean/O1_BODY_5_SOURCE_TRACE_DECOMPOSITION_RECEIPT_20260907_44fcccf7bd1a.json",
            "agent_review_inbox/review-T-P4-033-O1-body-5-source-trace-decomposition-codex-20260907-a977fb4941f1.md",
            "examples/routeb_b45_source_comparator_lean/NEW_BODY5_GramTraceSkeleton20260907.lean",
            "examples/routeb_b45_source_comparator_lean/NEW_BODY5_FiniteTraceSkeleton20260907.lean",
            "examples/routeb_b45_source_comparator_lean/REVIEW_BODY5_G3_G4_FINITE_TRACE_20260907.md",
            "examples/routeb_b45_source_comparator_lean/NEW_BODY5_API_REPAIR_ListFinset20260907.lean",
            "examples/routeb_b45_source_comparator_lean/NEW_BODY5_API_REPAIR_RowCode20260907.lean",
            "examples/routeb_b45_source_comparator_lean/NEW_BODY5_API_REPAIR_Q3Slice20260907.lean",
            "examples/routeb_b45_source_comparator_lean/NEW_BODY5_API_REPAIR_Q3DataLeaf20260907.lean",
            "examples/routeb_b45_source_comparator_lean/REVIEW_BODY5_API_REPAIR_20260907.md",
        ],
    },
    {
        "name": "P4.O1.source_comparator.h_body_6.canonical_export",
        "parent": "P4.O1.source_comparator.h_body_6",
        "statement": "A canonical body-6 pre-accumulation export reifies the exact source body mass and connects to the existing trace evaluator.",
        "proof_sketch": "Bind the sixth endpoint and midpoint, prove the source Gram, reify all 610 signed rational atoms including zero complement, then prove canonical evaluator equals the existing body-6 evaluator.",
        "lane": "source_semantics",
        "bottleneck": "coefficient_identity",
        "status": "COEFFICIENT_REPLAY_MATCH_SOURCE_THEOREM_OPEN",
        "artifacts": [
            "examples/routeb_b45_source_comparator_lean/RouteBO1Body6CanonicalExportTargets.lean",
            "examples/routeb_b45_source_comparator_lean/O1_BODY_6_CANONICAL_EXPORT_CONTRACT.json",
            "examples/routeb_b45_source_comparator_lean/O1_BODY_6_CANONICAL_EXPORT_RECEIPT.json",
            "examples/routeb_b45_source_comparator_lean/O1_BODY_6_CANONICAL_SLICE.csv",
            "agent_review_inbox/review-T-P4-033-O1-body-6-canonical-export-codex-20260907.md",
        ],
    },
    {
        "name": "P4.O0.physical_baseline_factor.H_acc_semantic_export",
        "parent": "P4.O0.physical_baseline_factor",
        "statement": "The deployed Julia pre-regularizer accumulator is refined to an exact scalar DAG and, separately, to a sound runtime/interval contract.",
        "proof_sketch": "Separate ideal rational-real, loaded Float64-decoded, and machine accumulator semantics; bind source spans and 36/216/216 roots before proving evaluator or interval soundness.",
        "lane": "source_semantics",
        "bottleneck": "evaluator_enclosure",
        "status": "OPEN_H_ACC_SOURCE_REFINEMENT_AND_INTERVAL_SOUNDNESS",
        "artifacts": [
            "examples/routeb_o0_h_acc_semantic_export/OPEN_CONTRACT.json",
            "examples/routeb_o0_h_acc_semantic_export/RECEIPT.json",
            "examples/routeb_o0_h_acc_semantic_export/check_contract.py",
            "examples/routeb_o0_h_acc_source_refinement/check_refinement.py",
            "agent_review_inbox/review-T-P4-033-O0-H-acc-evaluator-interval-contract-codex-20260907.md",
        ],
    },
    {
        "name": "P5.componentwise_relative_decay.feasible_cone_spn",
        "parent": "P5.componentwise_relative_decay",
        "statement": "The direct K_path centered small-gain inequality reduces exactly to 18 feasible cone certificates, with rational SPN as an orthant consumer.",
        "proof_sketch": "Prove six-cone one-channel cover, interleave two channels, establish orthant quadratic nonnegativity and SPN decomposition; bind concrete K_path only downstream.",
        "lane": "lean_adapter",
        "bottleneck": "coefficient_identity",
        "status": "PENDING_MATH_CHILD",
        "artifacts": [
            "agent_review_inbox/review-T-P5-026-guyuefangyuan-20260907T1031.md",
            "agent_review_inbox/companion-T-P5-026-guyuefangyuan-20260907T1033.md",
        ],
    },
    {
        "name": "P5.componentwise_relative_decay.feasible_cone_spn.cone_index",
        "parent": "P5.componentwise_relative_decay.feasible_cone_spn",
        "statement": "The six-channel cone labels admit a computable 36-index to 18-representative-times-sign equivalence, preserving multiplicity and full coverage witnesses.",
        "proof_sketch": "Define the six closed cones, simultaneous global sign reversal, explicit representative selection, and the ConeIndex equivalence; prove fiber cardinality, multiplicity-preserving sums, and signed coverage without identifying equal matrix values.",
        "lane": "lean_adapter",
        "bottleneck": "coefficient_identity",
        "status": "LEAN_FOCUSED_PASS_SOURCE_INDEPENDENT_CONE_INDEX",
        "artifacts": [
            "examples/routeb_p5_feasible_cone_spn_proof_attempt/NEW_CONE_INDEX_Core.lean",
            "examples/routeb_p5_feasible_cone_spn_proof_attempt/NEW_CONE_INDEX_check.py",
            "examples/routeb_p5_feasible_cone_spn_proof_attempt/NEW_CONE_INDEX_REVIEW.md",
        ],
    },
    {
        "name": "P5.componentwise_relative_decay.moving_frame_parameter_transport",
        "parent": "P5.componentwise_relative_decay",
        "statement": "The block-(4,5) moving-frame difference map transports exactly to source coordinates, cancels w/c under a common ramp parameter, and yields a rank-one K_path correction under controlled parameter mismatch.",
        "proof_sketch": "Formalize the sparse affine difference map, common-c cancellation, ramp-fiber segment lemma, uniform transport bounds, K_eff=K0+kappa tensor gamma, and the finite-gain fiber-constancy obstruction; keep source H, P8 coverage, and physical binding as separate premises.",
        "lane": "lean_adapter",
        "bottleneck": "coefficient_identity",
        "status": "PENDING_MOVING_FRAME_TRANSPORT_MATH",
        "artifacts": [
            "agent_review_inbox/review-T-P5-028-liuguanyi-20260907T1112.md",
            "agent_review_inbox/companion-T-P5-028-liuguanyi-20260907T1115.md",
        ],
    },
    {
        "name": "P5.componentwise_relative_decay.moving_frame_parameter_transport.source_difference",
        "parent": "P5.componentwise_relative_decay.moving_frame_parameter_transport",
        "statement": "At fixed time, the block-(4,5) moving-frame affine map has the exact source-coordinate difference identities for q4,q5,v4,v5,w and optional c.",
        "proof_sketch": "Expand the five affine coordinates over two tuples and prove the componentwise difference equations by exact ring algebra; keep the source semantic map as an explicit typed definition.",
        "lane": "lean_adapter",
        "bottleneck": "coefficient_identity",
        "status": "PENDING_MOVING_FRAME_EXACT_DIFFERENCE",
        "artifacts": [
            "agent_review_inbox/review-T-P5-028-liuguanyi-20260907T1112.md",
            "agent_review_inbox/companion-T-P5-028-liuguanyi-20260907T1115.md",
        ],
    },
    {
        "name": "P5.componentwise_relative_decay.moving_frame_parameter_transport.common_parameter",
        "parent": "P5.componentwise_relative_decay.moving_frame_parameter_transport",
        "statement": "A common ramp parameter cancels the moving-frame transport exactly, producing identity rows for block q/v and zero displacement rows for w and c.",
        "proof_sketch": "Instantiate the exact difference map with c=cBar and derive the sparse identity/zero transport matrix without charging sensitive but undisplaced w/c Jacobian columns.",
        "lane": "lean_adapter",
        "bottleneck": "coefficient_identity",
        "status": "PENDING_MOVING_FRAME_COMMON_PARAMETER_CANCELLATION",
        "artifacts": [
            "agent_review_inbox/review-T-P5-028-liuguanyi-20260907T1112.md",
            "agent_review_inbox/companion-T-P5-028-liuguanyi-20260907T1115.md",
        ],
    },
    {
        "name": "P5.componentwise_relative_decay.moving_frame_parameter_transport.ramp_fiber_segment",
        "parent": "P5.componentwise_relative_decay.moving_frame_parameter_transport",
        "statement": "The fixed-(t,c) straight segment between two moving-frame states remains on the same source ramp fiber.",
        "proof_sketch": "Use affine-linearity of the common-c source map to prove segment interpolation commutes with transport and preserves w=ct and the explicit c coordinate.",
        "lane": "lean_adapter",
        "bottleneck": "coefficient_identity",
        "status": "PENDING_MOVING_FRAME_RAMP_FIBER_SEGMENT",
        "artifacts": [
            "agent_review_inbox/review-T-P5-028-liuguanyi-20260907T1112.md",
            "agent_review_inbox/companion-T-P5-028-liuguanyi-20260907T1115.md",
        ],
    },
    {
        "name": "P5.componentwise_relative_decay.moving_frame_parameter_transport.uniform_bound",
        "parent": "P5.componentwise_relative_decay.moving_frame_parameter_transport",
        "statement": "A controlled parameter mismatch yields the exact finite-time component transport bounds with rational affine endpoint constants A4(T), A5(T).",
        "proof_sketch": "Bound the affine coefficients on 0≤t≤T, consume |Delta c| control, and derive the nonnegative S rows for q4,q5,v4,v5,w and optional c.",
        "lane": "lean_adapter",
        "bottleneck": "coefficient_identity",
        "status": "PENDING_MOVING_FRAME_UNIFORM_TRANSPORT",
        "artifacts": [
            "agent_review_inbox/review-T-P5-028-liuguanyi-20260907T1112.md",
            "agent_review_inbox/companion-T-P5-028-liuguanyi-20260907T1115.md",
        ],
    },
    {
        "name": "P5.componentwise_relative_decay.moving_frame_parameter_transport.k_eff_update",
        "parent": "P5.componentwise_relative_decay.moving_frame_parameter_transport",
        "statement": "A nonnegative source Jacobian envelope and parameter-control vector induce the direct componentwise update K_eff=K0+kappa tensor gamma.",
        "proof_sketch": "Compose the uniform source-coordinate transport with the raw H and one force map, then prove the finite-sum triangle bound and rank-one nonnegative correction without scalarizing K.",
        "lane": "lean_adapter",
        "bottleneck": "coefficient_identity",
        "status": "PENDING_MOVING_FRAME_K_EFF_COMPOSITION",
        "artifacts": [
            "agent_review_inbox/review-T-P5-028-liuguanyi-20260907T1112.md",
            "agent_review_inbox/companion-T-P5-028-liuguanyi-20260907T1115.md",
        ],
    },
    {
        "name": "P5.componentwise_relative_decay.moving_frame_parameter_transport.fiber_obstruction",
        "parent": "P5.componentwise_relative_decay.moving_frame_parameter_transport",
        "statement": "Any finite four-state centered gain over cross-parameter pairs forces residual constancy on every fixed-state parameter fiber.",
        "proof_sketch": "Set the compared four-state vectors equal, use nonnegativity of the norm square, and retain the explicit scalar residual counterexample as an obstruction to silently dropping Delta c.",
        "lane": "lean_adapter",
        "bottleneck": "coefficient_identity",
        "status": "PENDING_MOVING_FRAME_FIBER_OBSTRUCTION",
        "artifacts": [
            "agent_review_inbox/review-T-P5-028-liuguanyi-20260907T1112.md",
            "agent_review_inbox/companion-T-P5-028-liuguanyi-20260907T1115.md",
        ],
    },
    {
        "name": "P4.O1.source_comparator.h_body_4.source_gram_targets.proof_attempt",
        "parent": "P4.O1.source_comparator.h_body_4.source_gram_targets",
        "statement": "An explicit tactic proof attempt discharges the body-4 source Gram target layers in a pinned remote Lean environment.",
        "proof_sketch": "Use exact trig leaves, finite frame expansion, source origin/axis bridges, active/inactive Jacobian formulas, finite Gram tables, and ring normalization; endpoint remains expected-entry only.",
        "lane": "lean_adapter",
        "bottleneck": "source_semantics",
        "status": "PROOF_ATTEMPT_UNCOMPILED",
        "artifacts": [
            "examples/routeb_o1_body4_source_gram_proof_attempt/RouteBO1Body4SourceGramProofAttempt.lean",
            "examples/routeb_o1_body4_source_gram_proof_attempt/NEW_REPAIR_20260907_BODY4_GRAM_ALGEBRA.lean",
            "examples/routeb_o1_body4_source_gram_proof_attempt/REVIEW_20260907_NEW_REPAIR_BODY4_GRAM_ALGEBRA.md",
            "examples/routeb_o1_body4_source_gram_proof_attempt/NEW_SOURCE_JACOBIAN_20260907_BODY4_BRIDGE.lean",
            "examples/routeb_o1_body4_source_gram_proof_attempt/NEW_SOURCE_JACOBIAN_20260907_BODY4_BRIDGE_REVIEW.md",
        ],
    },
    {
        "name": "P4.O1.source_comparator.h_body_5.source_trace_decomposition.geometry_proof_attempt",
        "parent": "P4.O1.source_comparator.h_body_5.source_trace_decomposition",
        "statement": "An explicit tactic proof attempt discharges body-5 source geometry, active columns, inactive joint, and cylindrical lift leaves.",
        "proof_sketch": "Prove step-4 origin invariance, step-3 translation, midpoint COM, parallel cross-product zero, inactive joint 5, lift linearity/cross/isometry, then bind G1/G2.",
        "lane": "lean_adapter",
        "bottleneck": "source_semantics",
        "status": "PROOF_ATTEMPT_UNCOMPILED",
        "artifacts": [
            "examples/routeb_b45_source_comparator_lean/RouteBO1Body5GeometryColumnsProofAttempt20260907.lean",
        ],
    },
    {
        "name": "P5.componentwise_relative_decay.feasible_cone_spn.proof_attempt",
        "parent": "P5.componentwise_relative_decay.feasible_cone_spn",
        "statement": "An explicit Lean proof attempt formalizes the exact six-cone cover, 18 representative certificates, and orthant/SPN consumers.",
        "proof_sketch": "Construct cone cover by sign cases, prove interleave/map and sign identities, reduce absolute envelope to a congruent quadratic, then add orthant and SPN lemmas without concrete K_path.",
        "lane": "lean_adapter",
        "bottleneck": "coefficient_identity",
        "status": "PROOF_ATTEMPT_UNCOMPILED",
        "artifacts": [
            "examples/routeb_p5_feasible_cone_spn_proof_attempt/P5FeasibleConeSPN.lean",
            "examples/routeb_p5_feasible_cone_spn_proof_attempt/lakefile.toml",
            "examples/routeb_p5_feasible_cone_spn_proof_attempt/lean-toolchain",
            "examples/routeb_p5_feasible_cone_spn_lean/P5FeasibleConeSPN.lean",
            "examples/routeb_p5_feasible_cone_spn_lean/README.md",
            "examples/routeb_p5_feasible_cone_spn_lean/verify.sh",
            "examples/routeb_p5_feasible_cone_spn_lean/lean-toolchain",
            "agent_review_inbox/review-T-P5-026-juyangxianzun-20260907T1048.md",
            "agent_review_inbox/companion-T-P5-026-juyangxianzun-20260907T1050.md",
            "examples/routeb_p5_feasible_cone_spn_proof_attempt/NEW_exact_geometry_spn.py",
            "examples/routeb_p5_feasible_cone_spn_proof_attempt/REVIEW_exact_geometry_spn.md",
        ],
    },
    {
        "name": "P5.componentwise_relative_decay.near_sharp_scalar_fallback",
        "parent": "P5.componentwise_relative_decay",
        "statement": "The source-independent scalar block-(4,5) fallback has an exact rational upper constant and an explicit lower obstruction witness.",
        "proof_sketch": "Use weighted AM-GM, exact Sylvester/LDL positivity for the weighted gap, derive the division-free joint bound, and retain the rational lower witness as a rejection test.",
        "lane": "lean_adapter",
        "bottleneck": "coefficient_identity",
        "status": "EXACT_RATIONAL_SCALAR_BOUND_UNCOMPILED",
        "artifacts": [
            "examples/routeb_p5_scalar_fallback/NEW_P5_027_near_sharp_scalar_fallback.lean",
            "examples/routeb_p5_scalar_fallback/NEW_check_exact.py",
            "examples/routeb_p5_scalar_fallback/NEW_P5_027_REVIEW.md",
            "agent_review_inbox/review-T-P5-027-kuangmanmozun-20260907T1044.md",
            "agent_review_inbox/companion-T-P5-027-kuangmanmozun-20260907T1048.md",
        ],
    },
    {
        "name": "P4.O0.physical_baseline_factor.H_acc_semantic_export.source_refinement_validator",
        "parent": "P4.O0.physical_baseline_factor.H_acc_semantic_export",
        "statement": "A fail-closed intake validator enforces the H_acc source-refinement DAG shape, dense roots, source spans, and runtime policy before any export is accepted.",
        "proof_sketch": "Validate canonical DAG arities, topological references, source spans, dense 36/216/216 coordinate order, six accumulator updates, and explicit null/pending semantics.",
        "lane": "source_semantics",
        "bottleneck": "evaluator_enclosure",
        "status": "STRUCTURAL_VALIDATOR_PENDING_SOURCE_EXPORT",
        "artifacts": [
            "examples/routeb_o0_h_acc_source_refinement/check_refinement.py",
            "examples/routeb_o0_h_acc_source_refinement/test_refinement.py",
            "examples/routeb_o0_h_acc_source_refinement/REVIEW.md",
            "examples/routeb_o0_h_acc_source_refinement/RECEIPT.json",
            "examples/routeb_o0_h_acc_source_refinement/NEW_INTAKE_SCHEMA.json",
            "examples/routeb_o0_h_acc_source_refinement/NEW_INTAKE.json",
            "examples/routeb_o0_h_acc_source_refinement/NEW_LAYOUT_FIXTURE.json",
            "examples/routeb_o0_h_acc_source_refinement/NEW_source_intake.py",
            "examples/routeb_o0_h_acc_source_refinement/NEW_test_source_intake.py",
            "examples/routeb_o0_h_acc_source_refinement/NEW_REVIEW.md",
            "examples/routeb_o0_h_acc_source_refinement/NEW_RECEIPT.json",
            "examples/routeb_o0_h_acc_source_refinement/NEW_SEAM_source.py",
            "examples/routeb_o0_h_acc_source_refinement/NEW_SEAM_test_source.py",
            "examples/routeb_o0_h_acc_source_refinement/NEW_SEAM_REPORT.json",
            "examples/routeb_o0_h_acc_source_refinement/NEW_SEAM_REVIEW.md",
        ],
    },
    {
        "name": "P4.true_dh_port_source_binding.typed_block_source_bridge",
        "parent": "P4.true_dh_port_source_binding",
        "statement": "The block split B=(4,5), D=(1,2,3,6) has a typed exact-real source bridge for the O1 port identity, including a defect-aware fallback and one-time force normalization.",
        "proof_sketch": "Fix Fin embeddings and block shapes, distinguish distal acceleration correction from physical velocity, derive the distal comparison identity and leading minus sign, and retain e_D/e_B defects when zero-defect compatibility is absent.",
        "lane": "source_semantics",
        "bottleneck": "source_semantics",
        "status": "REPAIR_PATCHED_PENDING_LEAN_COMPILE",
        "artifacts": [
            "agent_review_inbox/review-T-P4-032-liuguanyi-20260907T1210.md",
            "agent_review_inbox/review-T-P4-032-codex-20260907.md",
            "agent_review_inbox/review-T-P4-032-repair-20260907.md",
            "agent_review_inbox/claim-T-P4-032-liuguanyi-20260907T1202.md",
            "artifacts/task_routeb_o1_lean_api_audit_20260907/RouteBO1PortIdentity.lean",
        ],
    },
    {
        "name": "P4.fixed_lambda_two_row_admissibility.typed_consumer",
        "parent": "P4.fixed_lambda_two_row_admissibility",
        "statement": "A typed two-row consumer binds the same fixed lambda=2 and theta=1 to the declared PMI and Schur inequalities with explicit denominator positivity and positive margin.",
        "proof_sketch": "Represent the two finite rows and shared lambda witness, prove the exact lambda=2/theta=1 relation, strict upper-ratio and margin fields, and keep the declared ledger/source/coverage boundaries separate.",
        "lane": "lean_adapter",
        "bottleneck": "coefficient_identity",
        "status": "OPEN_UNCOMPILED_FIXED_LAMBDA_TYPED_CONSUMER",
        "artifacts": [
            "examples/routeb_fixed_lambda_fold/NEW_FIXED_LAMBDA_ADMISSIBILITY20260907.lean",
            "examples/routeb_fixed_lambda_fold/NEW_FIXED_LAMBDA_ADMISSIBILITY20260907_REVIEW.md",
        ],
    },
    {
        "name": "P4.fixed_lambda_two_row_admissibility.typed_consumer.coefficient_bridge",
        "parent": "P4.fixed_lambda_two_row_admissibility.typed_consumer",
        "statement": "The fixed-lambda row contract has an exact coefficient identity and strict-upper-ratio iff positive-margin bridge, including finite and Fin 2 consumers.",
        "proof_sketch": "Rewrite candidateMargin = externalGamma - lambda*cellGamma, cross-multiply only under cellGamma>0, and lift the equivalence pointwise without assuming dense labels or physical coverage.",
        "lane": "lean_adapter",
        "bottleneck": "coefficient_identity",
        "status": "OPEN_UNCOMPILED_FIXED_LAMBDA_COEFFICIENT_BRIDGE",
        "artifacts": [
            "examples/routeb_fixed_lambda_fold/NEW_FIXED_LAMBDA_ADMISSIBILITY_COEFFICIENT_BRIDGE20260907.lean",
            "examples/routeb_fixed_lambda_fold/NEW_FIXED_LAMBDA_ADMISSIBILITY_COEFFICIENT_BRIDGE20260907_REVIEW.md",
        ],
    },
    {
        "name": "P4.fixed_lambda_two_row_admissibility.typed_consumer.coefficient_bridge.sparse_digest_fold",
        "parent": "P4.fixed_lambda_two_row_admissibility.typed_consumer.coefficient_bridge",
        "statement": "A sparse Finset ledger fold preserves arbitrary global box labels, one-row-per-box membership, the 256+321=577 declared accounting, and the fixed-lambda margin bridge under an explicit digest binding premise.",
        "proof_sketch": "Keep selected row indices and labels typed, prove label cardinality and row-wise strict-upper/margin equivalence, and bind the canonical row encoding to an external length-64 digest token without computing SHA-256 in Lean.",
        "lane": "lean_adapter",
        "bottleneck": "coefficient_identity",
        "status": "OPEN_UNCOMPILED_FIXED_LAMBDA_SPARSE_DIGEST_FOLD",
        "artifacts": [
            "examples/routeb_fixed_lambda_fold/NEW_FIXED_LAMBDA_ADMISSIBILITY_SPARSE_DIGEST_FOLD20260907.lean",
            "examples/routeb_fixed_lambda_fold/NEW_FIXED_LAMBDA_ADMISSIBILITY_SPARSE_DIGEST_FOLD20260907_REVIEW.md",
        ],
    },
    {
        "name": "P4.fixed_lambda_two_row_admissibility.typed_consumer.coefficient_bridge.sparse_digest_fold.selected_box_parent",
        "parent": "P4.fixed_lambda_two_row_admissibility.typed_consumer.coefficient_bridge.sparse_digest_fold",
        "statement": "Sparse one-row-per-box membership and the fixed lambda=2 strict-upper margin bridge imply a well-defined positive margin for every selected global box label.",
        "proof_sketch": "Use witness uniqueness for each sparse label, prove selected-margin independence, then consume positive denominator and the imported coefficient bridge; keep digest/source/coverage external.",
        "lane": "lean_adapter",
        "bottleneck": "coefficient_identity",
        "status": "OPEN_UNCOMPILED_FIXED_LAMBDA_SELECTED_BOX_PARENT",
        "artifacts": [
            "examples/routeb_fixed_lambda_fold/NEW_FIXED_LAMBDA_ADMISSIBILITY_SELECTED_BOX_PARENT20260907.lean",
            "examples/routeb_fixed_lambda_fold/NEW_FIXED_LAMBDA_ADMISSIBILITY_SELECTED_BOX_PARENT20260907_REVIEW.md",
        ],
    },
    {
        "name": "P5.componentwise_relative_decay.feasible_cone_spn.k_path_interface",
        "parent": "P5.componentwise_relative_decay.feasible_cone_spn",
        "statement": "A typed interface composes the existing pathK transport, nonnegative componentwise gain comparison, cone-index lift, and 18 representative SPN witnesses into the conditional power consumer.",
        "proof_sketch": "Use the actual pathK formula once, carry the same source domain witness through ComponentBinding and ConeGapBinding, lift 18 representatives to 36 indices, and preserve the reverse gap comparison direction.",
        "lane": "lean_adapter",
        "bottleneck": "coefficient_identity",
        "status": "LEAN_SOURCE_BUNDLE_PASS_CONDITIONAL_KPATH_INTERFACE",
        "artifacts": [
            "examples/routeb_p5_feasible_cone_spn_proof_attempt/NEW_KPATH_INTERFACE_Core.lean",
            "examples/routeb_p5_feasible_cone_spn_proof_attempt/NEW_KPATH_INTERFACE_check.py",
            "examples/routeb_p5_feasible_cone_spn_proof_attempt/NEW_KPATH_INTERFACE_REVIEW.md",
        ],
    },
    {
        "name": "P5.componentwise_relative_decay.feasible_cone_spn.k_path_interface.exact_comparison",
        "parent": "P5.componentwise_relative_decay.feasible_cone_spn.k_path_interface",
        "statement": "An exact rational checker recomputes all 8 pathK entries from A/Hjac/Scoord and verifies pathK ≤ K_cert without tolerance, while a typed cast seam exposes the comparison to the real-valued consumer.",
        "proof_sketch": "Reject noncanonical rationals, malformed dimensions, stale formula pins and all identity/comparison countercontrols; separately retain exact real entry-equality premises for the Lean ComponentLE adapter.",
        "lane": "lean_adapter",
        "bottleneck": "coefficient_identity",
        "status": "EXACT_UNBOUND_COMPARISON_CHECKED_LEAN_BINDING_OPEN",
        "artifacts": [
            "examples/routeb_p5_feasible_cone_spn_proof_attempt/NEW_KPATH_INTERFACE_Comparison.py",
            "examples/routeb_p5_feasible_cone_spn_proof_attempt/NEW_KPATH_INTERFACE_Comparison_test.py",
            "examples/routeb_p5_feasible_cone_spn_proof_attempt/NEW_KPATH_INTERFACE_RationalBinding.lean",
            "examples/routeb_p5_feasible_cone_spn_proof_attempt/NEW_KPATH_INTERFACE_Comparison_REVIEW.md",
        ],
    },
    {
        "name": "P5.componentwise_relative_decay.feasible_cone_spn.k_path_interface.fin_closure",
        "parent": "P5.componentwise_relative_decay.feasible_cone_spn.k_path_interface",
        "statement": "The eight exact path/cert comparisons are lifted through a typed Fin slot equivalence to the real 2x4 componentwise gain consumer, with cone-index multiplicity preserved.",
        "proof_sketch": "Define the row-major Fin 8 equivalence, carry exact rational-to-real table identities, prove the envelope slack sum and nonnegativity, and lift 18 representative SPN witnesses to all 36 cones without value deduplication.",
        "lane": "lean_adapter",
        "bottleneck": "coefficient_identity",
        "status": "OPEN_UNCOMPILED_KPATH_FIN_CLOSURE",
        "artifacts": [
            "examples/routeb_p5_feasible_cone_spn_proof_attempt/NEW_KPATH_INTERFACE_FinClosure.lean",
            "examples/routeb_p5_feasible_cone_spn_proof_attempt/NEW_KPATH_INTERFACE_FinClosure_REVIEW.md",
        ],
    },
    {
        "name": "P4.fixed_lambda_two_row_admissibility.typed_consumer.coefficient_bridge.sparse_digest_fold.selected_box_parent.two_eta_union",
        "parent": "P4.fixed_lambda_two_row_admissibility.typed_consumer.coefficient_bridge.sparse_digest_fold.selected_box_parent",
        "statement": "Tagged sparse eta=2.7 and eta=5.6 partitions combine under cross-eta label disjointness, preserving one-row-per-box, exact 256+321=577 accounting, and positive selected-box margins.",
        "proof_sketch": "Use EtaTag×Nat row indices, explicit cross-eta label disjointness, local injectivity, cardinality addition, and the selected-box positive margin theorem; keep digest/source/coverage external.",
        "lane": "lean_adapter",
        "bottleneck": "coefficient_identity",
        "status": "OPEN_UNCOMPILED_FIXED_LAMBDA_TWO_ETA_UNION",
        "artifacts": [
            "examples/routeb_fixed_lambda_fold/NEW_FIXED_LAMBDA_ADMISSIBILITY_TWO_ETA_UNION20260907.lean",
            "examples/routeb_fixed_lambda_fold/NEW_FIXED_LAMBDA_ADMISSIBILITY_TWO_ETA_UNION20260907_REVIEW.md",
        ],
    },
    {
        "name": "P4.fixed_lambda_two_row_admissibility.typed_consumer.coefficient_bridge.sparse_digest_fold.selected_box_parent.two_eta_union.digest_composition",
        "parent": "P4.fixed_lambda_two_row_admissibility.typed_consumer.coefficient_bridge.sparse_digest_fold.selected_box_parent.two_eta_union",
        "statement": "Per-eta canonical row encodings and digest tokens compose into an explicit union digest binding under an external equality between canonical union encoding and concatenated selected-row encodings.",
        "proof_sketch": "Keep the union oracle result and concatenation equality as typed premises, project each partition's existing digest binding, and package the union token without pretending SHA256 hashes compose algebraically.",
        "lane": "lean_adapter",
        "bottleneck": "coefficient_identity",
        "status": "OPEN_UNCOMPILED_FIXED_LAMBDA_DIGEST_COMPOSITION",
        "artifacts": [
            "examples/routeb_fixed_lambda_fold/NEW_FIXED_LAMBDA_ADMISSIBILITY_CANONICAL_DIGEST_COMPOSITION20260907.lean",
            "examples/routeb_fixed_lambda_fold/NEW_FIXED_LAMBDA_ADMISSIBILITY_CANONICAL_DIGEST_COMPOSITION20260907_REVIEW.md",
        ],
    },
    {
        "name": "P3.central_fd_derivative_hull_composition.algebraic_interface.power_seam.force_adapter",
        "parent": "P3.central_fd_derivative_hull_composition.algebraic_interface.power_seam",
        "statement": "Four derivative-first remainder layers split linearly under one Christoffel-to-force contraction and feed the existing Fin 6 weighted power consumer.",
        "proof_sketch": "Name machine/lift, central-FD, derivative-hull, and export-center tensors; prove contraction additivity, force-error vector identity, and one-use radius triangle bound while leaving source/rounding/export/coverage as typed premises.",
        "lane": "lean_adapter",
        "bottleneck": "coefficient_identity",
        "status": "OPEN_UNCOMPILED_CENTRAL_FD_FORCE_ADAPTER",
        "artifacts": [
            "examples/routeb_p3_central_fd_hull/NEW_CENTRAL_FD_HULL_FORCE_ADAPTER.lean",
            "examples/routeb_p3_central_fd_hull/NEW_CENTRAL_FD_HULL_FORCE_ADAPTER_REVIEW.md",
        ],
    },
    {
        "name": "P3.central_fd_derivative_hull_composition.algebraic_interface.power_seam.force_adapter.unified_input",
        "parent": "P3.central_fd_derivative_hull_composition.algebraic_interface.power_seam.force_adapter",
        "statement": "The four derivative-first remainder radii are summed exactly once into a unified nonnegative radius and weighted-power input on a common domain.",
        "proof_sketch": "Construct R=R₀+R₁+R₂+R₃ and mu=mu₀+mu₁+mu₂+mu₃, prove the triangle and nonnegativity bounds, and package velocity/weight/domain premises without choosing a concrete source or radius.",
        "lane": "lean_adapter",
        "bottleneck": "coefficient_identity",
        "status": "OPEN_UNCOMPILED_CENTRAL_FD_UNIFIED_INPUT",
        "artifacts": [
            "examples/routeb_p3_central_fd_hull/NEW_CENTRAL_FD_HULL_UNIFIED_INPUT.lean",
            "examples/routeb_p3_central_fd_hull/NEW_CENTRAL_FD_HULL_UNIFIED_INPUT_REVIEW.md",
        ],
    },
    {
        "name": "P4.fixed_lambda_two_row_admissibility.typed_consumer.coefficient_bridge.sparse_digest_fold.selected_box_parent.two_eta_union.digest_composition.uniform_feasibility",
        "parent": "P4.fixed_lambda_two_row_admissibility.typed_consumer.coefficient_bridge.sparse_digest_fold.selected_box_parent.two_eta_union.digest_composition",
        "statement": "Positive margins or strict-upper premises on every row of the finite tagged eta union yield one shared lambda=2, theta=1 uniform feasibility witness.",
        "proof_sketch": "Define marginAt and uniform feasibility over the sparse union, use the existing positive-denominator bridge rowwise, and package nonemptiness plus the fixed parameter record without claiming domain completeness.",
        "lane": "lean_adapter",
        "bottleneck": "coefficient_identity",
        "status": "OPEN_UNCOMPILED_FIXED_LAMBDA_UNIFORM_FEASIBILITY",
        "artifacts": [
            "examples/routeb_fixed_lambda_fold/NEW_FIXED_LAMBDA_ADMISSIBILITY_UNIFORM_FEASIBILITY20260907.lean",
            "examples/routeb_fixed_lambda_fold/NEW_FIXED_LAMBDA_ADMISSIBILITY_UNIFORM_FEASIBILITY20260907_REVIEW.md",
        ],
    },
    {
        "name": "P4.fixed_lambda_two_row_admissibility.typed_consumer.coefficient_bridge.sparse_digest_fold.selected_box_parent.two_eta_union.digest_composition.uniform_feasibility.monotonicity",
        "parent": "P4.fixed_lambda_two_row_admissibility.typed_consumer.coefficient_bridge.sparse_digest_fold.selected_box_parent.two_eta_union.digest_composition.uniform_feasibility",
        "statement": "With positive cell denominators, finite-union margin feasibility is downward monotone in the shared lambda; any 1<lambda≤lambda0 preserves strict upper bounds and positive margins.",
        "proof_sketch": "Use the exact affine margin difference, positive cellGamma, finite union quantification, and a 2≤lambda0 corollary for fixed lambda=2/theta=1 without repeating digest or union accounting.",
        "lane": "lean_adapter",
        "bottleneck": "coefficient_identity",
        "status": "OPEN_UNCOMPILED_FIXED_LAMBDA_MONOTONICITY",
        "artifacts": [
            "examples/routeb_fixed_lambda_fold/NEW_FIXED_LAMBDA_ADMISSIBILITY_MONOTONICITY20260907.lean",
            "examples/routeb_fixed_lambda_fold/NEW_FIXED_LAMBDA_ADMISSIBILITY_MONOTONICITY20260907_REVIEW.md",
        ],
    },
    {
        "name": "P3.central_fd_derivative_hull_composition.algebraic_interface.power_seam.force_adapter.unified_input.monotonicity",
        "parent": "P3.central_fd_derivative_hull_composition.algebraic_interface.power_seam.force_adapter.unified_input",
        "statement": "The Fin 6 weighted-power consumer is monotone under a larger nonnegative unified derivative remainder radius.",
        "proof_sketch": "Prove radius, component quadratic, weighted finite-sum and absolute-value multiplication monotonicity, then lift an existing consumer bound from R to qBar while keeping common-domain and velocity premises explicit.",
        "lane": "lean_adapter",
        "bottleneck": "coefficient_identity",
        "status": "OPEN_UNCOMPILED_CENTRAL_FD_RADIUS_MONOTONICITY",
        "artifacts": [
            "examples/routeb_p3_central_fd_hull/NEW_CENTRAL_FD_HULL_MONOTONICITY.lean",
            "examples/routeb_p3_central_fd_hull/NEW_CENTRAL_FD_HULL_MONOTONICITY_REVIEW.md",
        ],
    },
    {
        "name": "P4.fixed_lambda_two_row_admissibility.typed_consumer.coefficient_bridge.sparse_digest_fold.selected_box_parent.two_eta_union.digest_composition.uniform_feasibility.uniform_margin_budget",
        "parent": "P4.fixed_lambda_two_row_admissibility.typed_consumer.coefficient_bridge.sparse_digest_fold.selected_box_parent.two_eta_union.digest_composition.uniform_feasibility",
        "statement": "A finite tagged sparse union admits a reusable positive uniform margin budget when a scalar delta is explicitly below every selected row margin.",
        "proof_sketch": "Package delta positivity and pointwise load absorption over the union, retain the external coefficient lower bound as a separate source-facing premise, and avoid claiming a receipt-derived minimum.",
        "lane": "lean_adapter",
        "bottleneck": "coefficient_identity",
        "status": "OPEN_UNCOMPILED_FIXED_LAMBDA_MARGIN_BUDGET",
        "artifacts": [
            "examples/routeb_fixed_lambda_fold/NEW_FIXED_LAMBDA_ADMISSIBILITY_UNIFORM_MARGIN_BUDGET20260907.lean",
            "examples/routeb_fixed_lambda_fold/NEW_FIXED_LAMBDA_ADMISSIBILITY_UNIFORM_MARGIN_BUDGET20260907_REVIEW.md",
        ],
    },
    {
        "name": "P4.true_dh_port_source_binding.typed_block_source_bridge.block_projection_defects",
        "parent": "P4.true_dh_port_source_binding.typed_block_source_bridge",
        "statement": "The ordered B=(4,5), D=(1,2,3,6) split has exact finite projections and a defect-aware port elimination identity with explicit zero-defect corollary.",
        "proof_sketch": "Use Fin embeddings and finite-sum partition to derive both block matrix-vector projections, preserve the distal comparison defect, then eliminate with an explicit left inverse and retain e_D/e_B terms.",
        "lane": "source_semantics",
        "bottleneck": "source_semantics",
        "status": "OPEN_UNCOMPILED_P4_BLOCK_PROJECTION_DEFECTS",
        "artifacts": [
            "examples/routeb_p5_feasible_cone_spn_proof_attempt/NEW_P4_032_BlockDefects.lean",
            "examples/routeb_p5_feasible_cone_spn_proof_attempt/NEW_P4_032_BlockDefects_REVIEW.md",
        ],
    },
    {
        "name": "P4.true_dh_port_source_binding.typed_block_source_bridge.block_projection_defects.defect_norm_budget",
        "parent": "P4.true_dh_port_source_binding.typed_block_source_bridge.block_projection_defects",
        "statement": "The defect-aware port identity admits an explicit Euclidean norm budget with independent port, distal, and local defect terms.",
        "proof_sketch": "Apply the triangle inequality to rB=Rport*aB+(MBD*MDDinv)*eD+eB, consume supplied action bounds and defect caps, and square only the total nonnegative cap without dropping cross terms.",
        "lane": "source_semantics",
        "bottleneck": "source_semantics",
        "status": "OPEN_UNCOMPILED_P4_DEFECT_NORM_BUDGET",
        "artifacts": [
            "examples/routeb_p5_feasible_cone_spn_proof_attempt/NEW_P4_032_DefectNormBudget.lean",
            "examples/routeb_p5_feasible_cone_spn_proof_attempt/NEW_P4_032_DefectNormBudget_REVIEW.md",
        ],
    },
    {
        "name": "P4.O1.source_comparator.h_body_6.canonical_export.independent_exact_slice.first_three_lever_source",
        "parent": "P4.O1.source_comparator.h_body_6.canonical_export.independent_exact_slice",
        "statement": "The first three true body-6 lever columns admit exact common-yaw local-vector expressions and a center-offset-preserving velocity Gram interface.",
        "proof_sketch": "Expand only the DH prefix origins and first axes, derive b_i=z_i×(o_5-o_i) for i=0,1,2, transport cross products through yaw, and retain the existing CenterOffsetTarget for complete velocity columns.",
        "lane": "source_semantics",
        "bottleneck": "source_semantics",
        "status": "OPEN_UNCOMPILED_BODY6_FIRST_THREE_LEVER",
        "artifacts": [
            "examples/routeb_b45_source_comparator_lean/NEW_BODY6_SLICE_LEVER_Core20260907.lean",
            "examples/routeb_b45_source_comparator_lean/NEW_BODY6_SLICE_LEVER_Source20260907.lean",
            "examples/routeb_b45_source_comparator_lean/NEW_BODY6_SLICE_LEVER_check20260907.py",
            "examples/routeb_b45_source_comparator_lean/NEW_BODY6_SLICE_LEVER_20260907_REVIEW.md",
        ],
    },
    {
        "name": "P4.fixed_lambda_two_row_admissibility.typed_consumer.coefficient_bridge.sparse_digest_fold.selected_box_parent.two_eta_union.digest_composition.uniform_feasibility.uniform_margin_budget.revised_bridge",
        "parent": "P4.fixed_lambda_two_row_admissibility.typed_consumer.coefficient_bridge.sparse_digest_fold.selected_box_parent.two_eta_union.digest_composition.uniform_feasibility.uniform_margin_budget",
        "statement": "An explicit upper-gap/cell-lower/ratio contract factors each row margin and proves delta=gap*cellLower is a uniform lower bound over the tagged union.",
        "proof_sketch": "Factor marginAt exactly using the positive denominator and ratio premise, apply monotone multiplication rowwise, then package the bound into the existing uniform margin budget consumer.",
        "lane": "lean_adapter",
        "bottleneck": "coefficient_identity",
        "status": "OPEN_UNCOMPILED_FIXED_LAMBDA_REVISED_MARGIN_BRIDGE",
        "artifacts": [
            "examples/routeb_fixed_lambda_fold/NEW_FIXED_LAMBDA_ADMISSIBILITY_UNIFORM_MARGIN_BUDGET_REVISED20260907.lean",
            "examples/routeb_fixed_lambda_fold/NEW_FIXED_LAMBDA_ADMISSIBILITY_UNIFORM_MARGIN_BUDGET_REVISED20260907_REVIEW.md",
        ],
    },
    {
        "name": "P3.central_fd_derivative_hull_composition.algebraic_interface.power_seam.force_adapter.unified_input.monotonicity.scalar_budget",
        "parent": "P3.central_fd_derivative_hull_composition.algebraic_interface.power_seam.force_adapter.unified_input.monotonicity",
        "statement": "The component-radius weighted-power output composes into a scalar downstream load budget under explicit nonnegative weights, caps, domain, and velocity premises.",
        "proof_sketch": "Bound the weighted component sum by a componentwise cap and then by a scalar cap, using finite-sum monotonicity and retain the existing consumer inequality as an upstream premise.",
        "lane": "lean_adapter",
        "bottleneck": "coefficient_identity",
        "status": "OPEN_UNCOMPILED_CENTRAL_FD_SCALAR_BUDGET",
        "artifacts": [
            "examples/routeb_p3_central_fd_hull/NEW_CENTRAL_FD_HULL_SCALAR_BUDGET.lean",
            "examples/routeb_p3_central_fd_hull/NEW_CENTRAL_FD_HULL_SCALAR_BUDGET_REVIEW.md",
        ],
    },
    {
        "name": "P4.fixed_lambda_two_row_admissibility.typed_consumer.coefficient_bridge.sparse_digest_fold.selected_box_parent.two_eta_union.digest_composition.uniform_feasibility.uniform_margin_budget.revised_bridge.strict_consumer",
        "parent": "P4.fixed_lambda_two_row_admissibility.typed_consumer.coefficient_bridge.sparse_digest_fold.selected_box_parent.two_eta_union.digest_composition.uniform_feasibility.uniform_margin_budget.revised_bridge",
        "statement": "The explicit positive delta bridge yields rowwise lambda<lambdaUpper, positive margin, and strict downstream load separation over the tagged union.",
        "proof_sketch": "Use gap positivity for the strict upper inequality, delta positivity plus the rowwise lower bound for positive margins, and strict transitivity for loads below delta.",
        "lane": "lean_adapter",
        "bottleneck": "coefficient_identity",
        "status": "OPEN_UNCOMPILED_FIXED_LAMBDA_STRICT_MARGIN",
        "artifacts": [
            "examples/routeb_fixed_lambda_fold/NEW_FIXED_LAMBDA_ADMISSIBILITY_STRICT_MARGIN_CONSUMER20260907.lean",
            "examples/routeb_fixed_lambda_fold/NEW_FIXED_LAMBDA_ADMISSIBILITY_STRICT_MARGIN_CONSUMER20260907_REVIEW.md",
        ],
    },
    {
        "name": "P3.central_fd_derivative_hull_composition.algebraic_interface.power_seam.force_adapter.unified_input.monotonicity.scalar_budget.common_context",
        "parent": "P3.central_fd_derivative_hull_composition.algebraic_interface.power_seam.force_adapter.unified_input.monotonicity.scalar_budget",
        "statement": "The four P3 layers share a typed common-domain context that transports velocity, weight, and existing consumer premises without reproving the weighted-power estimate.",
        "proof_sketch": "Represent machineLift, centralFD, derivativeHull, and exportCenter as a finite layer predicate family, transport one common-domain proof to the layer intersection, and package the existing consumer bound with explicit velocity and weight premises.",
        "lane": "lean_adapter",
        "bottleneck": "coefficient_identity",
        "status": "OPEN_UNCOMPILED_CENTRAL_FD_COMMON_CONTEXT",
        "artifacts": [
            "examples/routeb_p3_central_fd_hull/NEW_CENTRAL_FD_HULL_COMMON_CONTEXT.lean",
            "examples/routeb_p3_central_fd_hull/NEW_CENTRAL_FD_HULL_COMMON_CONTEXT_REVIEW.md",
        ],
    },
    {
        "name": "P3.central_fd_derivative_hull_composition.algebraic_interface.power_seam.force_adapter.unified_input.monotonicity.scalar_budget.cap_monotonicity",
        "parent": "P3.central_fd_derivative_hull_composition.algebraic_interface.power_seam.force_adapter.unified_input.monotonicity.scalar_budget",
        "statement": "The scalar cap budget is monotone, and strictly increasing when the total nonnegative load coefficient and cap gap are positive.",
        "proof_sketch": "Factor the scalar cap budget as cap times the finite load sum, prove nonnegativity of that sum, and use exact gap algebra for the strict form.",
        "lane": "lean_adapter",
        "bottleneck": "coefficient_identity",
        "status": "OPEN_UNCOMPILED_CENTRAL_FD_CAP_MONOTONICITY",
        "artifacts": [
            "examples/routeb_p3_central_fd_hull/NEW_CENTRAL_FD_HULL_CAP_MONOTONICITY.lean",
            "examples/routeb_p3_central_fd_hull/NEW_CENTRAL_FD_HULL_CAP_MONOTONICITY_REVIEW.md",
        ],
    },
    {
        "name": "P3.central_fd_derivative_hull_composition.algebraic_interface.power_seam.force_adapter.unified_input.monotonicity.scalar_budget.cap_max_witness",
        "parent": "P3.central_fd_derivative_hull_composition.algebraic_interface.power_seam.force_adapter.unified_input.monotonicity.scalar_budget",
        "statement": "A finite six-component cap vector with an explicit upper-bound and attainment witness transfers its nonuniform weighted load budget to a scalar cap-max budget.",
        "proof_sketch": "Keep the maximum as a proof-valued witness, derive capMax nonnegativity from attainment, apply finite-sum monotonicity under nonnegative loads, and transit an existing consumer bound.",
        "lane": "lean_adapter",
        "bottleneck": "coefficient_identity",
        "status": "OPEN_UNCOMPILED_CENTRAL_FD_CAP_MAX",
        "artifacts": [
            "examples/routeb_p3_central_fd_hull/NEW_CENTRAL_FD_HULL_CAPMAX.lean",
            "examples/routeb_p3_central_fd_hull/NEW_CENTRAL_FD_HULL_CAPMAX_REVIEW.md",
        ],
    },
    {
        "name": "P4.fixed_lambda_two_row_admissibility.typed_consumer.coefficient_bridge.sparse_digest_fold.selected_box_parent.two_eta_union.digest_composition.uniform_feasibility.uniform_margin_budget.revised_bridge.strict_consumer.weighted_absorption",
        "parent": "P4.fixed_lambda_two_row_admissibility.typed_consumer.coefficient_bridge.sparse_digest_fold.selected_box_parent.two_eta_union.digest_composition.uniform_feasibility.uniform_margin_budget.revised_bridge.strict_consumer",
        "statement": "A strict pointwise load below delta composes with nonnegative finite-row coefficients to a total weighted load bounded by the total weighted row margin.",
        "proof_sketch": "Apply coefficient monotonicity rowwise, sum load≤delta and delta≤margin over the explicit finite union, and retain positive-coefficient requirements for any future strict total inequality.",
        "lane": "lean_adapter",
        "bottleneck": "coefficient_identity",
        "status": "OPEN_UNCOMPILED_FIXED_LAMBDA_WEIGHTED_ABSORPTION",
        "artifacts": [
            "examples/routeb_fixed_lambda_fold/NEW_FIXED_LAMBDA_ADMISSIBILITY_WEIGHTED_ABSORPTION20260907.lean",
            "examples/routeb_fixed_lambda_fold/NEW_FIXED_LAMBDA_ADMISSIBILITY_WEIGHTED_ABSORPTION20260907_REVIEW.md",
        ],
    },
    {
        "name": "P4.O1.source_comparator.h_body_6.canonical_export.independent_exact_slice.first_three_lever_source.mixed_tail_gram",
        "parent": "P4.O1.source_comparator.h_body_6.canonical_export.independent_exact_slice.first_three_lever_source",
        "statement": "The first-three by tail body-6 block has exact six-entry axis and velocity Gram identities with the h² axis correction retained.",
        "proof_sketch": "Use yaw/isometry and cross-product covariance to derive the 3×2 axis/triple tables, then combine them into the mixed velocity Gram while keeping CenterOffsetTarget explicit and reusing existing tail seams.",
        "lane": "source_semantics",
        "bottleneck": "source_semantics",
        "status": "OPEN_UNCOMPILED_BODY6_MIXED_TAIL_GRAM",
        "artifacts": [
            "examples/routeb_b45_source_comparator_lean/NEW_BODY6_SLICE_MIXED_Core20260907.lean",
            "examples/routeb_b45_source_comparator_lean/NEW_BODY6_SLICE_MIXED_Source20260907.lean",
            "examples/routeb_b45_source_comparator_lean/NEW_BODY6_SLICE_MIXED_20260907_REVIEW.md",
        ],
    },
    {
        "name": "P4.O1.source_comparator.h_body_6.canonical_export.independent_exact_slice.first_three_lever_source.self_gram",
        "parent": "P4.O1.source_comparator.h_body_6.canonical_export.independent_exact_slice.first_three_lever_source",
        "statement": "The first three body-6 source columns admit an exact 3x3 self axis/velocity Gram interface with all offset and off-diagonal terms retained.",
        "proof_sketch": "Use the sparse local column templates and yaw isometry to derive six independent Gram entries plus symmetry, then connect the real source columns while keeping CenterOffsetTarget explicit.",
        "lane": "source_semantics",
        "bottleneck": "source_semantics",
        "status": "OPEN_UNCOMPILED_BODY6_SELF3_GRAM",
        "artifacts": [
            "examples/routeb_b45_source_comparator_lean/NEW_BODY6_SLICE_SELF3_Core20260907.lean",
            "examples/routeb_b45_source_comparator_lean/NEW_BODY6_SLICE_SELF3_Source20260907.lean",
            "examples/routeb_b45_source_comparator_lean/NEW_BODY6_SLICE_SELF3_20260907_REVIEW.md",
        ],
    },
    {
        "name": "P5.componentwise_relative_decay.physical_gain_mu_nu_bridge",
        "parent": "P5.componentwise_relative_decay",
        "statement": "Source-supplied nonnegative physical incremental gains can be transported through the moving frame into a square-only rational mu/nu envelope for the P5 parameter tube.",
        "proof_sketch": "Bound the moving-frame block coordinates, aggregate centered gains into U and W, consume the cross term with nonnegative rational slacks p,q, and expose the exact 11424/137088/2285 gate while leaving the source gain table external.",
        "lane": "lean_adapter",
        "bottleneck": "coefficient_identity",
        "status": "CLAIMED_LEAN_SIDECAR_PENDING_INDEPENDENT_VERIFICATION",
        "artifacts": [
            "examples/routeb_p5_physical_gain_parameter_tube_lean/P5PhysicalGainParameterTube.lean",
            "examples/routeb_p5_physical_gain_parameter_tube_lean/README.md",
            "examples/routeb_p5_physical_gain_parameter_tube_lean/lean-toolchain",
            "examples/routeb_p5_physical_gain_parameter_tube_lean/verify.sh",
            "agent_review_inbox/review-T-P5-031-guyuefangyuan-20260907T1224.md",
            "agent_review_inbox/companion-T-P5-031-guyuefangyuan-20260907T1225.md",
            "agent_review_inbox/claim-T-P5-031-guyuefangyuan-20260907T1222.md",
            "agent_review_inbox/claim-T-P5-031-juyangxianzun-20260907T1228.md",
        ],
    },
    {
        "name": "P4.true_dh_port_source_binding.typed_block_source_bridge.block_projection_defects.defect_norm_budget.quadratic_load",
        "parent": "P4.true_dh_port_source_binding.typed_block_source_bridge.block_projection_defects.defect_norm_budget",
        "statement": "An explicit nonnegative quadratic upper bound composes with the defect norm budget to bound the Schur/PMI residual load and allocate it to an available margin.",
        "proof_sketch": "Replace the Euclidean norm by its nonnegative defect cap under a supplied quadratic upper bound, multiply only by nonnegative load weight, and keep the LoadBinding and allocation inequalities explicit.",
        "lane": "lean_adapter",
        "bottleneck": "source_semantics",
        "status": "OPEN_UNCOMPILED_P4_QUADRATIC_RESIDUAL_LOAD",
        "artifacts": [
            "examples/routeb_p5_feasible_cone_spn_proof_attempt/NEW_P4_032_QuadraticLoad.lean",
            "examples/routeb_p5_feasible_cone_spn_proof_attempt/NEW_P4_032_QuadraticLoad_REVIEW.md",
        ],
    },
    {
        "name": "P4.fixed_lambda_two_row_admissibility.typed_consumer.coefficient_bridge.sparse_digest_fold.selected_box_parent.two_eta_union.digest_composition.uniform_feasibility.uniform_margin_budget.revised_bridge.strict_consumer.weighted_absorption.strict_total",
        "parent": "P4.fixed_lambda_two_row_admissibility.typed_consumer.coefficient_bridge.sparse_digest_fold.selected_box_parent.two_eta_union.digest_composition.uniform_feasibility.uniform_margin_budget.revised_bridge.strict_consumer.weighted_absorption",
        "statement": "A positive coefficient witness on a nonempty finite union upgrades the weighted load budget to strict total load below both delta and the total weighted margin.",
        "proof_sketch": "Use Finset.sum_lt_sum with one strictly positive coefficient row and non-strict inequalities elsewhere, then compose with the existing total delta-to-margin bound while retaining the nonempty-union premise.",
        "lane": "lean_adapter",
        "bottleneck": "coefficient_identity",
        "status": "OPEN_UNCOMPILED_FIXED_LAMBDA_STRICT_TOTAL_ABSORPTION",
        "artifacts": [
            "examples/routeb_fixed_lambda_fold/NEW_FIXED_LAMBDA_ADMISSIBILITY_STRICT_TOTAL_ABSORPTION20260907.lean",
            "examples/routeb_fixed_lambda_fold/NEW_FIXED_LAMBDA_ADMISSIBILITY_STRICT_TOTAL_ABSORPTION20260907_REVIEW.md",
        ],
    },
    {
        "name": "P4.true_dh_port_source_binding.typed_block_source_bridge.block_projection_defects.defect_norm_budget.quadratic_load.entrywise_upper",
        "parent": "P4.true_dh_port_source_binding.typed_block_source_bridge.block_projection_defects.defect_norm_budget.quadratic_load",
        "statement": "Entrywise absolute bounds on a 2x2 residual matrix yield a proof-valued nonnegative quadratic upper bound without PSD or spectral assumptions.",
        "proof_sketch": "Majorize diagonal and off-diagonal terms, apply Young's inequality to the absolute cross term, and package the resulting row-budget maximum or uniform 2s bound for the existing quadratic-load consumer.",
        "lane": "lean_adapter",
        "bottleneck": "source_semantics",
        "status": "OPEN_UNCOMPILED_P4_ENTRYWISE_QUADRATIC_UPPER",
        "artifacts": [
            "examples/routeb_p5_feasible_cone_spn_proof_attempt/NEW_P4_032_EntrywiseQuadratic.lean",
            "examples/routeb_p5_feasible_cone_spn_proof_attempt/NEW_P4_032_EntrywiseQuadratic_REVIEW.md",
        ],
    },
    {
        "name": "P3.central_fd_derivative_hull_composition.algebraic_interface.power_seam.force_adapter.unified_input.monotonicity.scalar_budget.cap_max_witness.minimality",
        "parent": "P3.central_fd_derivative_hull_composition.algebraic_interface.power_seam.force_adapter.unified_input.monotonicity.scalar_budget.cap_max_witness",
        "statement": "The explicit finite capMax witness is the least scalar upper bound and is unique across upper-plus-attainment witnesses for the same cap vector.",
        "proof_sketch": "Use attainment to compare capMax with any candidate upper bound, derive equality when the candidate is attained, and prove witness scalar equivalence without claiming index uniqueness.",
        "lane": "lean_adapter",
        "bottleneck": "coefficient_identity",
        "status": "OPEN_UNCOMPILED_CENTRAL_FD_CAP_MAX_MINIMALITY",
        "artifacts": [
            "examples/routeb_p3_central_fd_hull/NEW_CENTRAL_FD_HULL_CAPMAX_MINIMALITY.lean",
            "examples/routeb_p3_central_fd_hull/NEW_CENTRAL_FD_HULL_CAPMAX_MINIMALITY_REVIEW.md",
        ],
    },
    {
        "name": "P5.componentwise_relative_decay.feasible_cone_spn.nonnegative_gain_increment_reuse",
        "parent": "P5.componentwise_relative_decay.feasible_cone_spn",
        "statement": "A nonnegative component-gain increment can reuse an existing cone SPN witness when its symmetric cone correction is entrywise below the old nonnegative slack.",
        "proof_sketch": "Rewrite the envelope increment as the symmetric part of BᵀEA in cone coordinates, prove entrywise nonnegativity, and subtract it from N while preserving the old PSD S witness; keep rank-one K correction and concrete source external.",
        "lane": "lean_adapter",
        "bottleneck": "coefficient_identity",
        "status": "PENDING_SOURCE_INDEPENDENT_SPN_INCREMENT_REUSE",
        "artifacts": [
            "agent_review_inbox/review-T-P5-029-kuangmanmozun-20260907T1152.md",
            "agent_review_inbox/companion-T-P5-029-kuangmanmozun-20260907T1155.md",
            "agent_review_inbox/claim-T-P5-029-kuangmanmozun-20260907T1145.md",
        ],
    },
    {
        "name": "P5.componentwise_relative_decay.feasible_cone_spn.nonnegative_gain_increment_reuse.typed_skeleton",
        "parent": "P5.componentwise_relative_decay.feasible_cone_spn.nonnegative_gain_increment_reuse",
        "statement": "The fixed-N SPN update is typed through C=sym(BᵀEA): a nonnegative cone correction can be charged against N while retaining the old PSD S witness, including rank-one increments.",
        "proof_sketch": "Keep cone absolute-value maps and u≥0 as explicit premises, prove correction/envelope identities and entrywise nonnegativity, update all 18 representatives and lift by flip without claiming PSD monotonicity.",
        "lane": "lean_adapter",
        "bottleneck": "coefficient_identity",
        "status": "OPEN_UNCOMPILED_SPN_INCREMENT_TYPED_SKELETON",
        "artifacts": [
            "examples/routeb_p5_feasible_cone_spn_proof_attempt/NEW_KPATH_INTERFACE_SPNIncrement.lean",
            "examples/routeb_p5_feasible_cone_spn_proof_attempt/NEW_KPATH_INTERFACE_SPNIncrement_REVIEW.md",
        ],
    },
    {
        "name": "P5.componentwise_relative_decay.incremental_moving_frame_parameter_tube",
        "parent": "P5.componentwise_relative_decay",
        "statement": "Own-frame affine-ramp subtraction removes the ramp parameter from the relative block, yielding a rational parameter-cell energy tube under an incremental residual envelope.",
        "proof_sketch": "Derive the exact two-trajectory difference equation, compute the initial mismatch energy, consume the direct metric ISS inequality, and apply the exact condition 11424*mu + 137088*nu < 2285 for Vd < dc²/12; leave source and continuation premises explicit.",
        "lane": "energy",
        "bottleneck": "flowpipe_continuation",
        "status": "PENDING_INCREMENTAL_PARAMETER_TUBE_MATH",
        "artifacts": [
            "agent_review_inbox/review-T-P5-030-honglianmozun-20260907T1205.md",
            "agent_review_inbox/claim-T-P5-030-honglianmozun-20260907T1156.md",
        ],
    },
    {
        "name": "P5.componentwise_relative_decay.incremental_moving_frame_parameter_tube.iss_boundary",
        "parent": "P5.componentwise_relative_decay.incremental_moving_frame_parameter_tube",
        "statement": "The exact T-P5-030 initial energy coefficient is below 1/12 and the incremental ISS ledger gives a strictly inward derivative on the nonzero-width boundary under 11424*mu+137088*nu<2285.",
        "proof_sketch": "Prove the rational C0 identity and margin, derive the ISS ledger from two inequalities, clear denominators at V=dc²/12, and retain dc≠0 plus trajectory/continuation semantics as external premises.",
        "lane": "lean_adapter",
        "bottleneck": "coefficient_identity",
        "status": "OPEN_UNCOMPILED_P5_030_ISS_BOUNDARY",
        "artifacts": [
            "examples/routeb_p5_feasible_cone_spn_proof_attempt/NEW_P5_030_ISSBoundary.lean",
            "examples/routeb_p5_feasible_cone_spn_proof_attempt/NEW_P5_030_ISSBoundary_REVIEW.md",
        ],
    },
    {
        "name": "P5.componentwise_relative_decay.incremental_moving_frame_parameter_tube.compiled_candidate",
        "parent": "P5.componentwise_relative_decay.incremental_moving_frame_parameter_tube",
        "statement": "A pinned Lean sidecar claims the source-independent parameter-tube gain algebra, pending independent receipt review and without source or flowpipe admission.",
        "proof_sketch": "Use the sidecar's outer-product increment, anisotropic gain inflation, row-sum specialization, and finite-cover target lemmas; preserve source/coverage/ODE boundaries and require pinned CI evidence before any compiled-candidate label.",
        "lane": "lean_adapter",
        "bottleneck": "coefficient_identity",
        "status": "CLAIMED_LEAN_SIDECAR_PENDING_REVIEW",
        "artifacts": [
            "examples/routeb_p5_parameter_tube_gain_lean/P5ParameterTubeGain.lean",
            "examples/routeb_p5_parameter_tube_gain_lean/README.md",
            "examples/routeb_p5_parameter_tube_gain_lean/lean-toolchain",
            "agent_review_inbox/claim-T-P5-030-sumengchen-20260907T1207.md",
        ],
    },
    {
        "name": "P5.componentwise_relative_decay.near_sharp_scalar_fallback.compiled_candidate",
        "parent": "P5.componentwise_relative_decay.near_sharp_scalar_fallback",
        "statement": "The source-independent near-sharp scalar block-(4,5) consumer is compiled in the pinned GitHub Lean environment with an exact lower witness.",
        "proof_sketch": "Consume the corrected rational LDL/SOS identity, prove the division-free U*N/Q^2 bound and scalar residual consumer, and retain the exact lower witness as a sharpness obstruction; leave source and coverage external.",
        "lane": "lean_adapter",
        "bottleneck": "coefficient_identity",
        "status": "COMPILED_CANDIDATE_PENDING_SOURCE_AND_ADMISSION",
        "artifacts": [
            "examples/routeb_p5_near_sharp_centered_gain_lean/P5NearSharpCenteredGain.lean",
            "examples/routeb_p5_near_sharp_centered_gain_lean/README.md",
            "examples/routeb_p5_near_sharp_centered_gain_lean/lean-toolchain",
            "examples/routeb_p5_near_sharp_centered_gain_lean/verify.sh",
            "agent_review_inbox/review-T-P5-027-juyangxianzun-20260907T1136.md",
            "agent_review_inbox/claim-T-P5-027-juyangxianzun-20260907T1127.md",
        ],
    },
    {
        "name": "P5.componentwise_relative_decay.moving_frame_parameter_transport.compiled_candidate",
        "parent": "P5.componentwise_relative_decay.moving_frame_parameter_transport",
        "statement": "A pinned Lean sidecar claims the source-independent moving-frame transport algebra, subject to independent review and without concrete source or coverage binding.",
        "proof_sketch": "Formalize exact affine differences, common-parameter cancellation, ramp-fiber interpolation, controlled parameter mismatch, rank-one K correction, and the fiber obstruction; keep all physical/source premises explicit.",
        "lane": "lean_adapter",
        "bottleneck": "coefficient_identity",
        "status": "CLAIMED_LEAN_SIDECAR_PENDING_REVIEW",
        "artifacts": [
            "examples/routeb_p5_moving_frame_transport_lean/P5MovingFrameTransport.lean",
            "examples/routeb_p5_moving_frame_transport_lean/README.md",
            "examples/routeb_p5_moving_frame_transport_lean/lean-toolchain",
            "examples/routeb_p5_moving_frame_transport_lean/verify.sh",
            "agent_review_inbox/claim-T-P5-028-sumengchen-20260907T1116.md",
            "agent_review_inbox/review-T-P5-028-liuguanyi-20260907T1112.md",
            "agent_review_inbox/companion-T-P5-028-liuguanyi-20260907T1115.md",
        ],
    },
    {
        "name": "P3.central_fd_derivative_hull_composition.algebraic_interface.slot_adapter",
        "parent": "P3.central_fd_derivative_hull_composition.algebraic_interface",
        "statement": "The source-shaped dM[i,j,k] tensor and radius are explicitly permuted to the derivative-first T[k,i,j] Christoffel consumer without changing the remainder force.",
        "proof_sketch": "Define inverse slot maps, prove source/consumer contraction equality, commute addition and remainder/radius transport, and keep the derivative-hull remainder bound as an external premise.",
        "lane": "lean_adapter",
        "bottleneck": "coefficient_identity",
        "status": "OPEN_UNCOMPILED_CENTRAL_FD_SLOT_ADAPTER",
        "artifacts": [
            "examples/routeb_p3_central_fd_hull/NEW_CENTRAL_FD_HULL_SLOT_ADAPTER.lean",
            "examples/routeb_p3_central_fd_hull/NEW_CENTRAL_FD_HULL_SLOT_ADAPTER_REVIEW.md",
        ],
    },
    {
        "name": "P3.central_fd_derivative_hull_composition.algebraic_interface.fin6_consumer",
        "parent": "P3.central_fd_derivative_hull_composition.algebraic_interface",
        "statement": "The derivative-first central-FD remainder contract specializes to Fin 6 and yields explicit Christoffel component and velocity-quadratic power error bounds.",
        "proof_sketch": "Aggregate the three permuted derivative remainder radii for each Fin 6 Christoffel coefficient, apply nested finite-sum absolute bounds, and expose the six-coordinate power consumer without selecting numerical radii.",
        "lane": "lean_adapter",
        "bottleneck": "coefficient_identity",
        "status": "OPEN_UNCOMPILED_CENTRAL_FD_FIN6_CONSUMER",
        "artifacts": [
            "examples/routeb_p3_central_fd_hull/NEW_CENTRAL_FD_HULL_FIN6_CONSUMER.lean",
            "examples/routeb_p3_central_fd_hull/NEW_CENTRAL_FD_HULL_FIN6_CONSUMER_REVIEW.md",
        ],
    },
    {
        "name": "P3.central_fd_derivative_hull_composition.algebraic_interface.power_seam",
        "parent": "P3.central_fd_derivative_hull_composition.algebraic_interface",
        "statement": "The Fin 6 central-FD remainder is consumed by an exact weighted velocity-quadratic power bound and a four-layer telescoping radius contract.",
        "proof_sketch": "Keep derivative-first T[k,i,j], aggregate the three Christoffel radii, preserve ordered j,k sums and nonnegative weights, and compose the four-term absolute bound without symmetry shortcuts.",
        "lane": "lean_adapter",
        "bottleneck": "coefficient_identity",
        "status": "OPEN_UNCOMPILED_CENTRAL_FD_POWER_SEAM",
        "artifacts": [
            "examples/routeb_p3_central_fd_hull/NEW_CENTRAL_FD_HULL_POWER_SEAM.lean",
            "examples/routeb_p3_central_fd_hull/NEW_CENTRAL_FD_HULL_POWER_SEAM_REVIEW.md",
        ],
    },
    {
        "name": "P4.O1.source_comparator.h_body_6.canonical_export.independent_exact_slice",
        "parent": "P4.O1.source_comparator.h_body_6.canonical_export",
        "statement": "An independently reconstructed body-6 Fourier slice agrees with the canonical body-6 coefficients while preserving the source-binding and zero-complement obligations.",
        "proof_sketch": "Derive the sixth DH body directly, reify all 610 tagged rational rows, isolate the 23-row sixth column, and prove endpoint/center/Gram/Fourier seams before connecting to the legacy evaluator.",
        "lane": "source_semantics",
        "bottleneck": "source_semantics",
        "status": "OPEN_UNCOMPILED_BODY6_INDEPENDENT_SOURCE_SLICE",
        "artifacts": [
            "examples/routeb_b45_source_comparator_lean/NEW_BODY6_SLICE_20260907.py",
            "examples/routeb_b45_source_comparator_lean/NEW_BODY6_SLICE_20260907.csv",
            "examples/routeb_b45_source_comparator_lean/NEW_BODY6_SLICE_20260907.json",
            "examples/routeb_b45_source_comparator_lean/NEW_BODY6_SLICE_20260907Data.lean",
            "examples/routeb_b45_source_comparator_lean/NEW_BODY6_SLICE_20260907.lean",
            "examples/routeb_b45_source_comparator_lean/NEW_BODY6_SLICE_20260907_REVIEW.md",
        ],
    },
    {
        "name": "P4.O1.source_comparator.h_body_6.canonical_export.independent_exact_slice.endpoint_fourier_bridge",
        "parent": "P4.O1.source_comparator.h_body_6.canonical_export.independent_exact_slice",
        "statement": "The independent body-6 slice has a minimal endpoint-to-center-to-zero-linear-column bridge and a 23-row signed Fourier fold for the sixth column.",
        "proof_sketch": "Expand only the final DH matrix column, derive the midpoint and v5=0, fold the three compressed phases into 23 exact real atoms, and leave SourceAxisDotTarget plus the full 36-entry seam explicit.",
        "lane": "source_semantics",
        "bottleneck": "source_semantics",
        "status": "OPEN_UNCOMPILED_BODY6_ENDPOINT_FOURIER_BRIDGE",
        "artifacts": [
            "examples/routeb_b45_source_comparator_lean/NEW_BODY6_SLICE_STEP6_Core20260907.lean",
            "examples/routeb_b45_source_comparator_lean/NEW_BODY6_SLICE_STEP6_Bridge20260907.lean",
            "examples/routeb_b45_source_comparator_lean/NEW_BODY6_SLICE_STEP6_DataLeaf20260907.lean",
            "examples/routeb_b45_source_comparator_lean/NEW_BODY6_SLICE_STEP6_check20260907.py",
            "examples/routeb_b45_source_comparator_lean/NEW_BODY6_SLICE_STEP6_20260907_REVIEW.md",
        ],
    },
    {
        "name": "P4.O1.source_comparator.h_body_6.canonical_export.independent_exact_slice.endpoint_fourier_bridge.axis_dot_seam",
        "parent": "P4.O1.source_comparator.h_body_6.canonical_export.independent_exact_slice.endpoint_fourier_bridge",
        "statement": "The six source-axis dot products are derived from the pinned real-DH prefix rotations and feed the sixth-axis target without reading Fourier rows.",
        "proof_sketch": "Factor every parent axis as a common yaw times a local vector, use rotation isometry, expand the final DH columns, and prove the six Fin-index dot identities while leaving the full source matrix seam explicit.",
        "lane": "source_semantics",
        "bottleneck": "source_semantics",
        "status": "OPEN_UNCOMPILED_BODY6_AXIS_DOT_SEAM",
        "artifacts": [
            "examples/routeb_b45_source_comparator_lean/NEW_BODY6_SLICE_AXIS_Core20260907.lean",
            "examples/routeb_b45_source_comparator_lean/NEW_BODY6_SLICE_AXIS_Geometry20260907.lean",
            "examples/routeb_b45_source_comparator_lean/NEW_BODY6_SLICE_AXIS_Consumer20260907.lean",
            "examples/routeb_b45_source_comparator_lean/NEW_BODY6_SLICE_AXIS_check20260907.py",
            "examples/routeb_b45_source_comparator_lean/NEW_BODY6_SLICE_AXIS_20260907_REVIEW.md",
        ],
    },
    {
        "name": "P4.O1.source_comparator.h_body_6.canonical_export.independent_exact_slice.velocity_offset_and_tail_origins",
        "parent": "P4.O1.source_comparator.h_body_6.canonical_export.independent_exact_slice",
        "statement": "The body-6 source velocity columns admit an exact COM-offset decomposition, and the two tail origins satisfy the pinned parent-frame identities needed for the front Gram block.",
        "proof_sketch": "Keep all six joints active, use prevOrigin and source bodyJv semantics, prove c6=o5+(7/200)z5 and the two single-step origin relations, and retain the first-three lever arms as explicit targets.",
        "lane": "source_semantics",
        "bottleneck": "source_semantics",
        "status": "OPEN_UNCOMPILED_BODY6_VELOCITY_OFFSET",
        "artifacts": [
            "examples/routeb_b45_source_comparator_lean/NEW_BODY6_SLICE_VGRAM_Core20260907.lean",
            "examples/routeb_b45_source_comparator_lean/NEW_BODY6_SLICE_VGRAM_Source20260907.lean",
            "examples/routeb_b45_source_comparator_lean/NEW_BODY6_SLICE_VGRAM_20260907_REVIEW.md",
        ],
    },
    {
        "name": "P4.O1.source_comparator.h_body_6.canonical_export.independent_exact_slice.velocity_offset_and_tail_origins.front_tail_gram",
        "parent": "P4.O1.source_comparator.h_body_6.canonical_export.independent_exact_slice.velocity_offset_and_tail_origins",
        "statement": "The zero-based body-6 front-tail indices 3,4 have exact velocity Gram values h² sin²(q4), h² and zero cross term, yielding the corresponding source mass 2×2 block.",
        "proof_sketch": "Use the source axis dot identities, shared COM-offset decomposition and mass=3/20 velocity Gram + 1/60 angular Gram; preserve the nonzero v4 fact and do not infer the result from the v5=0 column.",
        "lane": "source_semantics",
        "bottleneck": "source_semantics",
        "status": "OPEN_UNCOMPILED_BODY6_FRONT_TAIL_GRAM",
        "artifacts": [
            "examples/routeb_b45_source_comparator_lean/NEW_BODY6_SLICE_VGRAM_Tail20260907.lean",
            "examples/routeb_b45_source_comparator_lean/NEW_BODY6_SLICE_VGRAM_Consumer20260907.lean",
            "examples/routeb_b45_source_comparator_lean/NEW_BODY6_SLICE_VGRAM_check20260907.py",
            "examples/routeb_b45_source_comparator_lean/NEW_BODY6_SLICE_VGRAM_20260907_REVIEW.md",
        ],
    },
    {
        "name": "P3.central_fd_derivative_hull_composition.algebraic_interface",
        "parent": "P3.central_fd_derivative_hull_composition",
        "statement": "The central finite-difference remainder contract composes exactly with the Christoffel tensor and velocity-quadratic force, yielding a derivative-hull enclosure.",
        "proof_sketch": "Prove tensor linearity, the three-index Christoffel remainder bound, the weighted power error, and the four-term telescoping identity while leaving machine/source/export premises explicit.",
        "lane": "lean_adapter",
        "bottleneck": "coefficient_identity",
        "status": "OPEN_UNCOMPILED_CENTRAL_FD_HULL_INTERFACE",
        "artifacts": [
            "examples/routeb_p3_central_fd_hull/NEW_CENTRAL_FD_HULL_INTERFACE.lean",
            "examples/routeb_p3_central_fd_hull/NEW_CENTRAL_FD_HULL_REVIEW.md",
        ],
    },
    {
        "name": "P4.fixed_lambda_uniform_declared_row_fold",
        "parent": "P4.fixed_cell_lambda_admissibility",
        "statement": "Fold the finite declared ledger rows for eta=2.7 and eta=5.6 into a uniform lambda=2 witness, without claiming coverage outside the ledger artifact.",
        "proof_sketch": "Use exact textual rationals, one-row-per-box finite membership, strict lambda_upper > 2, positive candidate margins, and a canonical witness digest; keep sparse global box labels explicit.",
        "lane": "lean_adapter",
        "bottleneck": "coefficient_identity",
        "status": "FINITE_DECLARED_FOLD_CHECKED_UNPROVEN",
        "artifacts": [
            "examples/routeb_fixed_lambda_fold/check_fold.py",
            "examples/routeb_fixed_lambda_fold/test_check_fold.py",
            "examples/routeb_fixed_lambda_fold/README.md",
            "examples/routeb_fixed_lambda_fold/RECEIPT.json",
            "examples/routeb_fixed_lambda_fold/NEW_FixedLambdaUniformDeclaredFold20260907.lean",
            "examples/routeb_fixed_lambda_fold/NEW_FixedLambdaUniformDeclaredFold20260907_REVIEW.md",
        ],
    },
]


def main() -> None:
    store = StateStore(STATE)
    state = store.load()
    added: list[str] = []
    updated: list[str] = []
    for spec in CHILDREN:
        parent_id = find_id(state, spec["parent"])
        existing = find_node(state, spec["name"])
        if existing is not None:
            if existing.parent_id != parent_id:
                raise ValueError(f"existing child has wrong parent: {spec['name']}")
            expected_artifacts = [artifact(path) for path in spec["artifacts"]]
            recorded = existing.metadata.setdefault("source_artifacts", [])
            recorded_paths = {item.get("path") for item in recorded
                              if isinstance(item, dict)}
            missing = [item for item in expected_artifacts
                       if item["path"] not in recorded_paths]
            if missing:
                recorded.extend(missing)
                updated.append(spec["name"])
            # Older decomposition scripts predate the explicit math-policy
            # fields.  Backfill only absent advisory/gate defaults so the
            # scheduler sees the same bottleneck as a newly registered child;
            # never overwrite a coordinator-owned positive evidence state.
            defaults = {
                "math_lane": spec["lane"],
                "math_bottleneck": spec["bottleneck"],
                "evidence_status": spec["status"],
                "registry_eligible": False,
                "comparator_accepted": False,
                "registry_promoted": False,
                "formal_certificate_allowed": False,
                "proof_proven": False,
                "source_binding_proven": False,
                "lean_compiled": False,
            }
            for key, value in defaults.items():
                if key not in existing.metadata:
                    existing.metadata[key] = value
                    if spec["name"] not in updated:
                        updated.append(spec["name"])
            continue
        source_artifacts = [artifact(path) for path in spec["artifacts"]]
        metadata = {
            "verification_domain": "source_semantics" if spec["lane"] == "source_semantics" else "lean",
            "math_lane": spec["lane"],
            "math_bottleneck": spec["bottleneck"],
            "statement_status": "indexed",
            "evidence_status": spec["status"],
            "source_artifacts": source_artifacts,
            "registry_eligible": False,
            "comparator_accepted": False,
            "registry_promoted": False,
            "formal_certificate_allowed": False,
            "proof_proven": False,
            "source_binding_proven": False,
            "lean_compiled": False,
        }
        state.add_node(spec["name"], spec["statement"], parent_id=parent_id,
                       proof_sketch=spec["proof_sketch"], metadata=metadata)
        added.append(spec["name"])
    if added or updated:
        state.event("routeb_sidecar_frontier_registered", child_names=added,
                    metadata_updated=updated, registry_promoted=False,
                    formal_certificate_allowed=False)
        state.validate()
        store.save(state)
    print({"status": "registered" if added or updated else "already_registered",
           "added": added, "updated": updated, "revision": store.load().revision,
           "registry_promoted": False, "formal_certificate_allowed": False})


if __name__ == "__main__":
    main()
