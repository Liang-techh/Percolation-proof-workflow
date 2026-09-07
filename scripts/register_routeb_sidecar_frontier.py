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
