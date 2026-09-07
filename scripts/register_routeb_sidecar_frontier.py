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
