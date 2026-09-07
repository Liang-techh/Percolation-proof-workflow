"""Persistent proof workflow primitives."""

from .model import EvidenceStage, NodeStatus, ProofNode, WorkflowState, status_is_closed
from .store import StateStore
from .coverage_receipt import (
    CANONICAL_TRIPLE_SCHEMA,
    CoverageReceiptError,
    THETA2_Q2_LO,
    THETA2_Q2_HI,
    EXTERNAL_PREMISES_SCHEMA,
    validate_theta2_external_premises,
    validate_canonical_coverage_triple,
)
from .comparator import CandidateReceiptAudit, build_comparator_manifest, validate_candidate_receipt
from .dry_run_migrator import dry_run_migrate
from .math_frontier import (build_frontier_cut, project_frontier_receipt,
                             project_virtual_frontier,
                             rank_formalizable_frontier)
from .reduction_batch import reduction_closure_batch
from .residual_ledger import audit_full_state_binding, audit_residual_ledger
from .routeb_source_contract import (RouteBP4SourceContract,
                                     audit_routeb_p4_source_contract)
from .routeb_kc_budget import RouteBKcBudget, derive_routeb_kc_budget
from .routeb_mbd_obstruction import (
    RouteBProjectionObstruction,
    audit_routeb_mbd_projection,
)
from .routeb_remote_contract import (
    RouteBRemoteBindingAudit,
    audit_routeb_remote_binding,
    audit_routeb_remote_binding_join,
)
from .routeb_remote_accel_budget import (
    RouteBRemoteAccelerationBudget,
    derive_routeb_remote_acceleration_budget,
)
from .routeb_nominal_distal_contract import (
    RouteBNominalDistalBridgeAudit,
    RouteBPhysicalRationalGramAudit,
    RouteBPhysicalRationalGramReconstructionAudit,
    RouteBPhysicalRationalTailAudit,
    audit_routeb_nominal_distal_bridge,
    audit_routeb_physical_rational_gram,
    audit_routeb_physical_rational_gram_reconstruction,
    audit_routeb_physical_rational_tail,
)
from .routeb_residual_l1_contract import (
    EXPECTED_THEOREMS as RESIDUAL_L1_EXPECTED_THEOREMS,
    RESIDUAL_L1_LEAN_RECEIPT_SCHEMA,
    RouteBResidualL1LeanReceiptAudit,
    audit_routeb_residual_l1_lean_receipt,
)
from .routeb_regularizer_semantics import (
    DEFAULT_BLOCK_COORDS,
    DEFAULT_REMOTE_COORDS,
    EXACT_MU,
    FLOAT64_MU,
    FLOAT64_MU_BITS_HEX,
    MU_DELTA,
    REGULARIZER_SEMANTICS_SCHEMA,
    RouteBExactResolventPremise,
    RouteBGeneralResolventPortPropagation,
    RouteBWeightedPortMetricConversion,
    RouteBInfinityToL2WeightedConversion,
    RouteBAffineBiasGain,
    RouteBPhysicalBaselineFactor,
    RouteBRootWitness,
    RouteBZeroShiftWeightedPerturbation,
    RouteBSchurMarginConsumption,
    RouteBRegularizerDiagonalPropagation,
    RouteBRegularizerFact,
    RouteBRegularizerInclusion,
    RouteBResolventPortPropagation,
    audit_routeb_regularizer_inclusion,
    convert_routeb_port_bound_to_weighted_metric,
    convert_routeb_infinity_port_bound_to_weighted_l2,
    derive_routeb_root_witness,
    derive_routeb_affine_bias_gain,
    derive_routeb_physical_baseline_factor,
    derive_routeb_zero_shift_weighted_perturbation,
    consume_routeb_schur_margin,
    consume_routeb_strict_schur_margin,
    derive_routeb_general_resolvent_port_propagation,
    derive_routeb_resolvent_port_propagation,
    propagate_routeb_regularizer_diagonal,
    routeb_regularizer_fact,
)
from .routeb_o2_receipt import (
    RouteBO2RuntimeReceiptAudit,
    audit_routeb_o2_runtime_receipt,
)
from .routeb_o0_r3_receipt import (
    O0_R3_RECEIPT_SCHEMA,
    O0_R3_CANONICAL_RECEIPT_SCHEMA,
    RouteBO0R3ReceiptAudit,
    RouteBO0R3CanonicalReceiptAudit,
    audit_routeb_o0_r3_receipt,
    audit_routeb_o0_r3_canonical_receipt,
)
from .routeb_o1_source_receipt import (
    O1_SOURCE_RECEIPT_SCHEMA,
    O1_BLOCK_ORDER,
    O1_DIDX,
    O1_BIDX,
    RouteBO1SourceReceiptAudit,
    RouteBO1ArtifactBindingAudit,
    audit_routeb_o1_source_receipt,
    audit_routeb_o1_artifact_bindings,
)
from .disjoint import (audit_do, build_repair_do, canonical_do_schema,
                        classify_manual_review, do_sha256, normalize_do_path)
from .advisory_reuse import (AdvisoryReuseError, SCHEMA_VERSION,
                              project_advisory_reuse)
from .merlean_plan_projection import (cycles as plan_cycles,
                                      export_views as export_plan_views,
                                      forward_cone as plan_forward_cone,
                                      levels as plan_levels,
                                      project as project_plan,
                                      topo_order as plan_topo_order)

__all__ = [
    "EvidenceStage", "NodeStatus", "ProofNode", "WorkflowState", "StateStore",
    "status_is_closed", "CandidateReceiptAudit", "validate_candidate_receipt",
    "CoverageReceiptError", "CANONICAL_TRIPLE_SCHEMA",
    "THETA2_Q2_LO", "THETA2_Q2_HI",
    "EXTERNAL_PREMISES_SCHEMA", "validate_theta2_external_premises",
    "validate_canonical_coverage_triple",
    "build_comparator_manifest", "dry_run_migrate",
    "project_frontier_receipt",
    "project_virtual_frontier",
    "build_frontier_cut",
    "rank_formalizable_frontier",
    "reduction_closure_batch",
    "audit_residual_ledger",
    "audit_full_state_binding",
    "RouteBP4SourceContract", "audit_routeb_p4_source_contract",
    "RouteBKcBudget", "derive_routeb_kc_budget",
    "RouteBProjectionObstruction", "audit_routeb_mbd_projection",
    "RouteBRemoteBindingAudit", "audit_routeb_remote_binding",
    "audit_routeb_remote_binding_join",
    "RouteBRemoteAccelerationBudget", "derive_routeb_remote_acceleration_budget",
    "RouteBNominalDistalBridgeAudit", "audit_routeb_nominal_distal_bridge",
    "RouteBPhysicalRationalGramAudit", "audit_routeb_physical_rational_gram",
    "RouteBPhysicalRationalGramReconstructionAudit",
    "audit_routeb_physical_rational_gram_reconstruction",
    "RouteBPhysicalRationalTailAudit", "audit_routeb_physical_rational_tail",
    "RESIDUAL_L1_EXPECTED_THEOREMS", "RESIDUAL_L1_LEAN_RECEIPT_SCHEMA",
    "RouteBResidualL1LeanReceiptAudit", "audit_routeb_residual_l1_lean_receipt",
    "DEFAULT_BLOCK_COORDS", "DEFAULT_REMOTE_COORDS", "EXACT_MU", "FLOAT64_MU",
    "FLOAT64_MU_BITS_HEX", "MU_DELTA", "REGULARIZER_SEMANTICS_SCHEMA",
    "RouteBExactResolventPremise", "RouteBRegularizerDiagonalPropagation",
    "RouteBGeneralResolventPortPropagation",
    "RouteBWeightedPortMetricConversion",
    "RouteBInfinityToL2WeightedConversion",
    "RouteBRootWitness",
    "RouteBAffineBiasGain",
    "RouteBPhysicalBaselineFactor",
    "RouteBZeroShiftWeightedPerturbation",
    "RouteBSchurMarginConsumption",
    "RouteBRegularizerFact", "RouteBRegularizerInclusion",
    "RouteBResolventPortPropagation", "audit_routeb_regularizer_inclusion",
    "derive_routeb_general_resolvent_port_propagation",
    "convert_routeb_port_bound_to_weighted_metric",
    "convert_routeb_infinity_port_bound_to_weighted_l2",
    "derive_routeb_root_witness",
    "derive_routeb_affine_bias_gain",
    "derive_routeb_physical_baseline_factor",
    "derive_routeb_zero_shift_weighted_perturbation",
    "consume_routeb_schur_margin",
    "consume_routeb_strict_schur_margin",
    "derive_routeb_resolvent_port_propagation",
    "propagate_routeb_regularizer_diagonal", "routeb_regularizer_fact",
    "RouteBO2RuntimeReceiptAudit", "audit_routeb_o2_runtime_receipt",
    "O0_R3_RECEIPT_SCHEMA", "RouteBO0R3ReceiptAudit",
    "audit_routeb_o0_r3_receipt", "O0_R3_CANONICAL_RECEIPT_SCHEMA",
    "RouteBO0R3CanonicalReceiptAudit", "audit_routeb_o0_r3_canonical_receipt",
    "O1_SOURCE_RECEIPT_SCHEMA", "O1_BLOCK_ORDER", "O1_DIDX", "O1_BIDX",
    "RouteBO1SourceReceiptAudit", "audit_routeb_o1_source_receipt",
    "RouteBO1ArtifactBindingAudit", "audit_routeb_o1_artifact_bindings",
    "audit_do", "build_repair_do", "canonical_do_schema", "classify_manual_review", "do_sha256", "normalize_do_path",
    "AdvisoryReuseError", "SCHEMA_VERSION", "project_advisory_reuse",
    "project_plan", "export_plan_views", "plan_topo_order", "plan_levels",
    "plan_forward_cone", "plan_cycles",
]
