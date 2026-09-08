"""Idempotently integrate pending inbox records as fail-closed metadata.

The inbox is intentionally append-only.  This command never promotes a node,
changes the registry, or edits an input record.  It records provenance on a
matching Route-B node or, for external-library scans, an event-only catalog
record, then writes a small processed marker so a periodic runner can safely
invoke it repeatedly.  In addition to review results, the collector accepts
typed ``handoff`` and ``companion_log`` records so useful agent output is not
lost merely because it was emitted under a different filename.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from percolation_workflow.store import StateStore
from percolation_workflow.routeb_residual_l1_contract import (
    audit_routeb_residual_l1_lean_receipt,
)


TASK_TARGETS = {
    "T-P0-001": ("P0.reproducibility_baseline", "reproducibility_baseline_blocked"),
    "T-DAG-002": ("M4.block45_full_certificate", "child_dag_refinement_proposal"),
    "T-P3-003": ("P3.strict_true_dh_bounds", "pending_source_manifest_binding"),
    "T-P4-003": ("P4.residual_schur_pmi", "conditional_typed_normalization"),
    "T-P4-004": ("P4.residual_schur_pmi", "conditional_typed_normalization_sidecar"),
    "T-P8-003": ("P8.independent_reachability", "explicit_time_contract_recommended"),
    "T-P8-004": ("P8.independent_reachability", "explicit_time_typed_sidecar"),
    "T-P8-002": ("P8.independent_reachability", "pending_explicit_time_parent_option"),
    "T-P5-001": ("P5.sparse_disjunctive_sos", "energy_syzygy_reuse_audit"),
    "T-P3-004": ("P3.strict_true_dh_bounds", "pending_source_semantic_adapter"),
    "T-P3-005": ("P3.strict_true_dh_bounds", "pending_semantic_binding_child"),
    "T-P5-002": ("P5.sparse_disjunctive_sos", "pending_energy_child"),
    "T-P3-006": ("P3.strict_true_dh_bounds", "pending_semantic_binding_sidecar"),
    "T-P5-003": ("P5.sparse_disjunctive_sos", "pending_christoffel_power_sidecar"),
    "T-P5-004": ("P5.sparse_disjunctive_sos", "pending_dissipative_residual_power_child"),
    "T-P5-005": ("P5.sparse_disjunctive_sos", "pending_relative_residual_strict_decay"),
    "T-P5-006": ("P5.componentwise_relative_decay", "pending_component_relative_decay_sidecar"),
    "T-P5-007": ("P5.sparse_disjunctive_sos", "pending_weighted_dual_decay_obstruction"),
    "T-P5-008": ("P5.sparse_disjunctive_sos", "pending_force_error_bias_split"),
    "T-P5-009": ("P5.sparse_disjunctive_sos", "pending_fd_relative_scaling_obstruction"),
    "T-P5-026": ("P5.componentwise_relative_decay.feasible_cone_spn.proof_attempt",
                 "compiled_candidate_source_independent_feasible_cone_spn"),
    "T-P5-027": ("P5.componentwise_relative_decay",
                 "near_sharp_exact_rational_scalar_fallback"),
    "T-P5-028": ("P5.componentwise_relative_decay.moving_frame_parameter_transport",
                 "exact_moving_frame_transport_and_parameter_cancellation"),
    "T-P5-029": ("P5.componentwise_relative_decay.feasible_cone_spn",
                 "pending_spn_nonnegative_gain_increment_reuse"),
    "T-P5-030": ("P5.componentwise_relative_decay",
                  "pending_incremental_moving_frame_parameter_tube"),
    "T-P5-031": ("P5.componentwise_relative_decay",
                  "pending_physical_gain_mu_nu_bridge"),
    "T-P4-032": ("P4.true_dh_port_source_binding",
                 "pending_typed_block_source_bridge"),
    "T-P4-030": ("P4.true_dh_port_source_binding",
                 "pending_port_sign_propagation"),
    "T-P4-031": ("P4.true_dh_port_source_binding",
                 "pending_controller_damping_source_decision"),
    "T-P4-033": ("P4.true_dh_regularizer_semantics_bridge",
                 "pending_regularizer_or_correlated_metric_source_bridge"),
    "T-P4-036.2": ("P4.fixed_lambda_two_row_admissibility",
                   "pending_authoritative_endpoint_witness"),
    "T-P4-037": ("P4.true_dh_port_source_binding",
                 "pending_weighted_scalar_budget_transport"),
    "T-P4-038": ("P4.scalar_young_square",
                 "pending_young_feasibility_discriminant_formalization"),
    "T-P4-039": ("P4.fixed_lambda_two_row_admissibility",
                 "pending_common_lambda_feasibility_formalization"),
    "T-P4-040": ("P4.fixed_lambda_two_row_admissibility",
                 "pending_common_rational_lambda_guard"),
    "T-P4-COMPILED-LEDGER-BINDING": ("P4.fixed_lambda_two_row_admissibility",
                                      "pending_compiled_ledger_binding"),
    "T-P5-034": ("P5.componentwise_relative_decay.feasible_cone_spn",
                 "pending_block45_fifteen_sixteen_sos_sidecar"),
    "T-P5-035": ("P5.componentwise_relative_decay.feasible_cone_spn",
                 "pending_block45_ninety_three_sos_sidecar"),
    "T-P0-FLT-CLASSIFICATION-MATRIX": (None,
                                       "flt_classification_matrix_scan"),
    "T-P4-033-O1-body6-slice": ("P4.O1.source_comparator.h_body_6.canonical_export",
                                "pending_independent_body6_source_slice"),
    "T-P4-fixed-lambda-admissibility": ("P4.fixed_lambda_two_row_admissibility",
                                        "pending_fixed_lambda_admissibility_formalization"),
    "T-P5-026-Kpath-interface": ("P5.componentwise_relative_decay.feasible_cone_spn",
                                 "pending_concrete_k_path_comparison_interface"),
    "T-P3-central-FD-hull": ("P3.central_fd_derivative_hull_composition",
                             "pending_exact_central_fd_derivative_hull_bridge"),
    "GH-MATH-P3-FD-REMAINDER": ("P3.central_fd_derivative_hull_composition",
                                 "pending_exact_central_fd_remainder_interface"),
    "GH-MATH-P4-ADJUGATE-ACCEL": ("P4.true_dh_port_source_binding",
                                   "pending_adjugate_acceleration_bridge"),
    "GH-MATH-P4-DESCRIPTOR-PUPPER": ("P4.true_dh_port_source_binding",
                                      "pending_descriptor_pupper_source_binding"),
    "GH-LEAN-BODY6-ALIGNED-CONSUMER": (
        "P4.O1.source_comparator.h_body_6.canonical_export",
        "pending_aligned_path_cap_consumer_receipt"),
    "GH-MATH-P4-TARGET-CAPS": ("P4.true_dh_port_source_binding",
                                "pending_target_cell_coordinate_caps"),
    "GH-MIXED-FLOWCHUANFENG-ADJUGATE": (
        "P4.true_dh_port_source_binding",
        "pending_adjugate_contract_review"),
    # Reassigned lanes after 流川枫 retirement.  Keep the historical aliases
    # above for late receipts, while routing all new envelopes to the same
    # fail-closed DAG parents under their replacement task IDs.
    "GH-MIXED-schur-absorption-reassigned": (
        "P4.residual_schur_pmi",
        "pending_reassigned_schur_absorption_review"),
    "GH-MIXED-BODY6-PATH-REASSIGNED": (
        "P4.O1.source_comparator.h_body_6.canonical_export",
        "pending_reassigned_body6_path_review"),
    "GH-MIXED-ADJUGATE-REASSIGNED": (
        "P4.true_dh_port_source_binding",
        "pending_reassigned_adjugate_review"),
    "GH-MATH-P4-ACTIVE-ENERGY-NORMALIZATION": (
        "P4.true_dh_port_source_binding",
        "pending_active_energy_normalization"),
    "GH-LEAN-BODY6-PATHCONTRACT-RECEIPT": (
        "P4.O1.source_comparator.h_body_6.canonical_export",
        "pending_body6_pathcontract_receipt"),
    "GH-MATH-P4-SOURCE-ELLIPSOID-BINDING": (
        "P4.true_dh_port_source_binding",
        "pending_source_ellipsoid_binding"),
    "GH-MATH-P4-SCHUR-BUDGET-CLOSURE": (
        "P4.residual_schur_pmi",
        "pending_schur_budget_closure"),
    "GH-MATH-P4-SCHUR-SIGNED-AFFINE-CHART": (
        "P4.residual_schur_pmi",
        "pending_signed_affine_defect_chart"),
    "GH-MATH-P4-VANIS2-RUNTIME-REFINEMENT": (
        "P4.true_dh_port_source_binding",
        "pending_vanis2_runtime_refinement"),
    "T-P4-ACTUAL-ROW-MISSING-BASE": (
        "P4.true_dh_port_source_binding",
        "pending_actual_row_missing_base_takeover"),
    "T-P4-ACTIVE-ENERGY-ORIGIN": (
        "P4.true_dh_port_source_binding",
        "pending_active_energy_origin_normalization"),
    "GH-LEAN-BODY6-PATHREASSIGNED-COMPILE": (
        "P4.O1.source_comparator.h_body_6.canonical_export",
        "pending_reassigned_body6_compile"),
    "GH-MATH-P4-ADJUGATE-PROJECTION-PACKET": (
        "P4.true_dh_port_source_binding",
        "pending_adjugate_projection_packet"),
    "GH-LEAN-P4-SCHUR-CLOSURE-RECEIPT": (
        "P4.residual_schur_pmi",
        "pending_schur_closure_receipt"),
    "GH-MATH-P4-SCHUR-SOURCE-BINDING": (
        "P4.residual_schur_pmi",
        "pending_schur_source_binding"),
    "GH-MATH-P4-ADJUGATE-SOURCE-WITNESS": (
        "P4.true_dh_port_source_binding",
        "pending_adjugate_source_witness"),
    "GH-MATH-P3-FD-STENCIL-BINDING": (
        "P3.central_fd_derivative_hull_composition",
        "pending_fd_stencil_source_binding"),
    "GH-LEAN-BODY6-SEAM-ADAPTER-ONLY": (
        "P4.O1.source_comparator.h_body_6.canonical_export",
        "pending_body6_seam_adapter_receipt"),
    "GH-LEAN-P4-GENERIC-SCHUR-ALLOCATION": (
        "P4.residual_schur_pmi",
        "pending_generic_finite_dimensional_schur_allocation_receipt"),
    "GH-LEAN-P4-GENERIC-SCHUR-ALLOCATION-REPAIR": (
        "P4.residual_schur_pmi",
        "pending_generic_schur_allocation_repair_receipt"),
    "GH-MATH-P4-DIRECT-BLOCK456-METRIC-TRANSPORT": (
        "P4.true_dh_port_source_binding",
        "pending_direct_block456_metric_transport"),
    "GH-MATH-P4-DIRECT-BLOCK456-BETA-DESIGN": (
        "P4.residual_schur_pmi",
        "pending_direct_block456_beta_design"),
    "GH-MATH-P4-DIRECT-BLOCK456-BETA-DESIGN-PROVENANCE": (
        "P4.residual_schur_pmi",
        "pending_direct_block456_beta_design_provenance_correction"),
    "GH-MATH-P4-BLOCK456-SOURCE-REIFICATION": (
        "P4.true_dh_port_source_binding",
        "pending_block456_metric_source_reification"),
    "GH-MATH-P4-BLOCK456-METRIC-CAP": (
        "P4.true_dh_port_source_binding",
        "pending_block456_matching_metric_cap"),
    "GH-MATH-P4-BLOCK456-MATCHING-METRIC-BUDGET": (
        "P4.true_dh_port_source_binding",
        "pending_block456_matching_metric_budget"),
    "GH-MATH-P4-BLOCK456-MATCHING-METRIC-BUDGET-PROVENANCE": (
        "P4.true_dh_port_source_binding",
        "pending_block456_matching_metric_budget_provenance_correction"),
    "GH-MATH-P4-DIRECT-BLOCK456-Q6-RAY-GRAPH-EXCLUSION": (
        "P4.true_dh_port_source_binding",
        "pending_direct_block456_q6_ray_graph_exclusion"),
    "GH-MATH-P4-BLOCK456-METRIC-PRODUCER-PROVENANCE": (
        "P4.true_dh_port_source_binding",
        "pending_block456_metric_producer_provenance"),
    "GH-MATH-P4-DIRECT-BLOCK456-Q6-RAY-SOURCE-BINDING": (
        "P4.true_dh_port_source_binding",
        "pending_direct_block456_q6_ray_source_binding"),
    "GH-LEAN-P4-Q6-GRAPH-EXCLUSION": (
        "P4.true_dh_port_source_binding",
        "pending_q6_graph_exclusion_generic_lean"),
    "GH-LEAN-P4-Q6-GRAPH-EXCLUSION-REPAIR": (
        "P4.true_dh_port_source_binding",
        "pending_q6_graph_exclusion_generic_lean_repair"),
    "GH-MATH-P4-H-ACC-SOURCE-SEAM-LOCAL": (
        "P4.O0.physical_baseline_factor.H_acc_semantic_export",
        "pending_h_acc_source_semantic_seam"),
    "GH-LEAN-BODY5-API-REPAIR-LOCAL": (
        "P4.O1.source_comparator.h_body_5.source_trace_decomposition",
        "pending_body5_api_repair_receipt"),
    "GH-LEAN-BODY5-API-REPAIR": (
        "P4.O1.source_comparator.h_body_5.source_trace_decomposition",
        "pending_body5_api_repair_receipt"),
    "GH-LEAN-P4-SCHUR-JOINT-THRESHOLD": (
        "P4.residual_schur_pmi",
        "pending_schur_joint_threshold_receipt"),
    "GH-MATH-P4-ACTUAL-CELL-PACKET": (
        "P4.true_dh_port_source_binding",
        "pending_actual_cell_source_packet"),
    "GH-MATH-P4-O1-BODY4-FRAME-HANDOFF": (
        "P4.O1.source_comparator.h_body_4.source_gram_targets",
        "pending_body4_frame_source_jacobian_handoff"),
    "GH-MATH-P4-3D-TO-2D-RESTRICTION": (
        "P4.true_dh_port_source_binding",
        "pending_3d_to_2d_restriction_interface"),
    "GH-MATH-P4-ACTUAL-THREE-ROW-WITNESS": (
        "P4.true_dh_port_source_binding",
        "pending_actual_three_row_source_witness"),
    "GH-MATH-P4-SOURCE-SEMANTICS-HALF-ACTIVE": (
        "P4.true_dh_port_source_binding",
        "pending_half_active_source_semantics"),
    "GH-MIXED-flowchuanfeng-schur-absorption": (
        "P4.residual_schur_pmi",
        "pending_reassigned_schur_absorption_review"),
    "GH-MIXED-FLOWCHUANFENG-BODY6-PATH": (
        "P4.O1.source_comparator.h_body_6.canonical_export",
        "pending_reassigned_body6_path_review"),
    "GH-MATH-P4-ROWSPACE-RECOVERY-MINIMAL": (
        "P4.true_dh_port_source_binding",
        "pending_minimal_rowspace_recovery"),
    "GH-LEAN-P4-ROWSPACE-RECOVERY": (
        "P4.true_dh_port_source_binding",
        "pending_rowspace_recovery_lean_receipt"),
    "GH-MATH-P4-ACTIVE-V-TARGET-DEFINITION": (
        "P4.true_dh_port_source_binding",
        "pending_active_target_storage_definition"),
    "GH-MATH-P4-JOINT6-DEFECT-ELIMINATION": (
        "P4.true_dh_port_source_binding",
        "pending_joint6_defect_elimination"),
    "GH-MATH-P4-ALL6-SOURCE-ROWS": (
        "P4.true_dh_port_source_binding",
        "pending_all6_source_rows"),
    "GH-LEAN-P4-ROWSPACE-MINIMAL-CONSUMER": (
        "P4.true_dh_port_source_binding",
        "pending_rowspace_minimal_consumer"),
    "GH-MATH-P4-ACTIVE-V-BINDING-CONTRACT": (
        "P4.true_dh_port_source_binding",
        "pending_active_v_binding_contract"),
    "GH-MATH-P4-JOINT6-WEIGHTED-CONSTRAINTS": (
        "P4.true_dh_port_source_binding",
        "pending_joint6_weighted_constraints"),
    "GH-MATH-P4-DH-CONTROLLER-SOURCE-CORRECTION": (
        "P4.true_dh_port_source_binding",
        "pending_dh_controller_source_correction"),
    "GH-LEAN-FLT-QUOTIENT-CLM-PINNED-HANDOFF": (
        None,
        "flt_quotient_clm_pinned_handoff"),
    "GH-MATH-P4-ACTIVE-INITIAL-BOUND-BINDING": (
        "P4.true_dh_port_source_binding",
        "pending_active_initial_bound_binding"),
    "GH-MATH-P4-SOURCE-ROWS-WEIGHTED-PACKET": (
        "P4.true_dh_port_source_binding",
        "pending_source_rows_weighted_packet"),
    "GH-MATH-P4-CORRECTED-BUILDER-SPEC": (
        "P4.true_dh_port_source_binding",
        "pending_corrected_builder_spec"),
    "GH-LEAN-FLT-QUOTIENT-CLM-API-REPAIR": (
        None,
        "flt_quotient_clm_api_repair"),
    "GH-MATH-P4-VFULL-DH-ANCHOR": (
        "P4.true_dh_port_source_binding",
        "pending_vfull_dh_value_anchor"),
    "GH-MATH-P4-CORRECTED-ACTUAL-ROWS": (
        "P4.true_dh_port_source_binding",
        "pending_corrected_actual_rows"),
    "GH-MATH-P4-O1-BODY4-FINITE-SUM-WITNESS": (
        "P4.O1.source_comparator.h_body_4.source_gram_targets",
        "pending_body4_finite_sum_source_witness"),
    "GH-LEAN-BODY4-FINITE-SUM-RECEIPT-HANDOFF": (
        "P4.O1.source_comparator.h_body_4.source_gram_targets",
        "pending_body4_finite_sum_compile_handoff"),
    "GH-MATH-P4-ACTIVE-V-FUNCTION-ENVELOPE": (
        "P4.true_dh_port_source_binding",
        "pending_active_v_function_envelope"),
    "GH-MATH-P4-ACTIVE-V-FUNCTION-IDENTITY": (
        "P4.true_dh_port_source_binding",
        "pending_active_v_function_identity"),
    "GH-ACTIVE-V-FUNCTION-IDENTITY": (
        "P4.true_dh_port_source_binding",
        "pending_active_v_function_identity"),
    "GH-MATH-P4-JOINT6-PHYSICAL-RECOVERY": (
        "P4.true_dh_port_source_binding",
        "pending_joint6_physical_recovery"),
    "GH-LEAN-FLT-QUOTIENT-CLM-COMPARATOR-HANDOFF": (
        None,
        "flt_quotient_clm_comparator_handoff"),
    # New GitHub proof lanes use descriptive uppercase suffixes.  Route them
    # to existing DAG parents as pending metadata only; no admission path is
    # implied by these aliases.
    "T-P4-020E-ENERGY-BETA": ("P4.residual_schur_pmi",
                               "pending_energy_beta_consumer"),
    "T-P4-DESCRIPTOR-ACCEL-BRIDGE": ("P4.true_dh_port_source_binding",
                                      "pending_descriptor_accel_bridge"),
    "T-P4-034": ("P4.true_dh_port_source_binding",
                  "pending_o2_energy_consumer"),
    "T-P5-071": ("P5.componentwise_relative_decay.feasible_cone_spn",
                  "pending_signed_two_cycle_contact"),
    "T-P5-072-SIGNED-SIMPLE-CYCLE-CONTACT": (
        "P5.componentwise_relative_decay.feasible_cone_spn",
        "pending_signed_simple_cycle_contact"),
    "T-P5-073-AFFINE-OFFSET-RELATIVE-DECAY": (
        "P5.componentwise_relative_decay", "pending_affine_offset_decay"),
    "T-P5-074-WEIGHTED-STRONG-MONOTONE-SCC": (
        "P5.componentwise_relative_decay", "pending_weighted_monotone_scc"),
    "T-P5-075-DAMPED-CORRECTOR-ENERGY": (
        "P5.componentwise_relative_decay", "pending_damped_corrector_energy"),
    "T-P5-076-WEIGHTED-GRAM-LIPSCHITZ": (
        "P5.componentwise_relative_decay", "pending_weighted_gram_lipschitz"),
    "T-P5-077-ANCHOR-LOCALIZED-INVARIANT-BALL": (
        "P5.componentwise_relative_decay", "pending_anchor_invariant_ball"),
    "T-P5-078-MIXED-RELATIVE-ADDITIVE-CORRECTOR": (
        "P5.componentwise_relative_decay", "pending_mixed_additive_corrector"),
    "T-P5-079-SIMILARITY-NORMALIZATION": (
        "P5.componentwise_relative_decay", "pending_similarity_normalization"),
    "T-P5-080-CORRELATION-AWARE-MIXED-DEFECT": (
        "P5.componentwise_relative_decay", "pending_correlated_mixed_defect"),
    "T-P5-081-MOVING-AFFINE-CHART": (
        "P5.componentwise_relative_decay", "pending_moving_affine_chart"),
    "T-P5-082-NONLINEAR-CHART-PULLBACK": (
        "P5.componentwise_relative_decay", "pending_nonlinear_chart_pullback"),
    "T-P5-083-NONLINEAR-STEP-SEGMENT-COVERAGE": (
        "P5.componentwise_relative_decay", "pending_nonlinear_step_segment_coverage"),
    "T-P5-084-NONLINEAR-CHART-SECANT-GEOMETRY": (
        "P5.componentwise_relative_decay", "pending_nonlinear_chart_secant_geometry"),
    "T-P5-085-DESCRIPTOR-RELATIVE-RATE": (
        "P5.componentwise_relative_decay", "pending_descriptor_relative_rate"),
    "T-P5-086-MOVING-FRAME-EULER": (
        "P5.componentwise_relative_decay", "pending_moving_frame_euler"),
    "T-P5-087-MOVING-METRIC-KERNEL-TRANSPORT": (
        "P5.componentwise_relative_decay", "pending_moving_metric_kernel_transport"),
    "T-P5-088-STATE-DEPENDENT-STORAGE-DERIVATIVE": (
        "P5.componentwise_relative_decay", "pending_state_dependent_storage_derivative"),
    "T-P5-089-MECHANICAL-SKEW-ENERGY-CANCELLATION": (
        "P5.componentwise_relative_decay", "pending_mechanical_skew_energy_cancellation"),
    "T-P5-090-MOVING-METRIC-CONTRACTION-CONGRUENCE": (
        "P5.componentwise_relative_decay", "pending_moving_metric_contraction_congruence"),
    "T-P5-091-VARIATIONAL-DEFECT-ROBUST-CONTRACTION": (
        "P5.componentwise_relative_decay", "pending_variational_defect_robust_contraction"),
    "T-P5-092-FINITE-STEP-STORAGE-TAYLOR-CLOSURE": (
        "P5.componentwise_relative_decay", "pending_finite_step_storage_taylor_closure"),
    "T-P5-093-BASE-FLOW-LIE-DEFECT": (
        "P5.componentwise_relative_decay",
        "pending_base_flow_lie_defect_same_tube_binding"),
    "T-P5-026-SIGNED-COVER-CONSUMER": (
        "P5.componentwise_relative_decay",
        "architecture_only_signed_cover_consumer"),
    "GH-LEAN-BODY5-API-REPAIR-SLICE-PENDING": (
        "P4.O1.source_comparator.h_body_5.source_trace_decomposition",
        "pending_body5_q3_slice_api_repair"),
    "SARTRE-P5-SAME-TUBE-SOURCE-PACKET": (
        "P5.componentwise_relative_decay",
        "pending_same_tube_source_packet_obstruction"),
    "SARTRE-P5-EXTERNAL-SOURCE-FIELDS-REV829": (
        "P5.componentwise_relative_decay",
        "pending_external_source_jet_packet_obstruction"),
    # External FLT scans are deliberately event-only: they are advisory
    # catalog evidence, not Route-B theorem nodes or registry entries.
    "T-FLT-DERIV-CALC": (None, "flt_derivation_calculus_scan"),
    "T-FLT-TOPOLOGY-QUOTIENT-CLM": (None, "flt_topology_quotient_scan"),
    "T-FLT-SPECTRAL-LINEAR": (None, "flt_spectral_linear_scan"),
    "T-FLT-TRANSPORT-ADAPTER": (None, "flt_transport_adapter_scan"),
    "T-FLT-INFRA-REGISTRY": (None, "flt_registry_graph_scan"),
    "T-FLT-SPECTRAL-SIDECAR": (None, "flt_spectral_sidecar"),
    "T-FLT-SPECTRAL-PREDICATE": (None, "flt_spectral_predicate_sidecar"),
    "T-FLT-QUOTIENT-SIDECAR": (None, "flt_quotient_transport_sidecar"),
    "T-FLT-P2M-QUOTIENT-MINIMAL-CONTRACT": (
        None,
        "flt_p2m_quotient_minimal_contract"),
    "T-P4-KC-COORDINATE-ADAPTER": ("P4.residual_schur_pmi", "pending_kc_coordinate_adapter"),
    "T-P4-MBD-PROJECTION": ("P4.residual_schur_pmi", "pending_mbd_projection_obstruction"),
    "T-P4-012": ("P4.residual_schur_pmi", "pending_typed_remote_binding_contract"),
    "T-P4-013": ("P4.residual_schur_pmi", "pending_remote_budget_pmi_composition"),
    "T-P4-014": ("P4.residual_schur_pmi", "pending_vector_remote_pmi_composition"),
    "T-P4-015": ("P4.residual_schur_pmi", "pending_nominal_distal_descriptor_bridge"),
    "T-P4-016": ("P4.residual_schur_pmi", "pending_nominal_distal_tail_pmi"),
    "T-P4-017": ("P4.residual_schur_pmi", "pending_tail_gram_reconstruction"),
    "T-P4-018": ("P4.nominal_distal_residual_l1_lean_seam",
                 "pending_residual_l1_lean_seam"),
    "T-P3-007": ("P3.strict_true_dh_bounds", "pending_concrete_mass_entry_bridge"),
    "T-P4-005": ("P4.residual_schur_pmi", "pending_one_channel_source_binding"),
    "T-P4-006": ("P4.residual_schur_pmi", "pending_sharp_schur_formalization"),
    "T-P4-007": ("P4.residual_schur_pmi", "pending_actual_block45_residual_decomposition"),
    "T-P4-008": ("P4.residual_schur_pmi", "pending_kc_mbd_obstruction_formalization"),
    "T-P4-011": ("P4.residual_schur_pmi", "pending_canonical_kc_budget"),
    "T-P3-008": ("P3.strict_true_dh_bounds", "pending_central_fd_christoffel_binding"),
    "T-P3-009": ("P3.strict_true_dh_bounds", "pending_block45_positive_inverse_bounds"),
    "T-P3-010": ("P3.strict_true_dh_bounds", "pending_block45_mass_interval_derivation"),
    "T-P3-011": ("P3.strict_true_dh_bounds", "pending_link_jacobian_block_lower_bound"),
    "T-P3-012": ("P3.true_dh_derivative_hull_leaf", "pending_flt_derivative_leaf_review"),
    "T-P3-013": ("P3.strict_true_dh_bounds", "pending_concrete_true_dh_derivative_hull_instance"),
    "T-P3-014": ("P3.trig_endpoint_enclosure_leaf", "pending_concrete_trig_source_binding"),
    "T-P3-015": ("P3.m33_exact_fourier_source_leaf", "pending_m33_fourier_leaf_lift"),
    "T-P3-016": ("P3.m33_exact_lower_bound", "pending_m33_exact_lower_bound_compile"),
    "T-P3-017": ("P3.rotational_prefix_mass_lower_bound", "pending_rotational_mass_lower_bound_lift"),
    "T-P4-019": ("P4.block45_global_mass_geometry_schur", "pending_block45_global_geometry_schur_lift"),
    "T-P4-020": ("P4.residual_schur_pmi", "pending_one_cell_residual_remainder_absorption"),
    "T-P4-021": ("P4.residual_port_frobenius_bound", "pending_resolved_cell_frobenius_port_lift"),
    "T-P4-022": ("P4.frobenius_operator_norm_bridge", "pending_frobenius_operator_bridge_compile"),
    "T-P4-023": ("P4.weighted_frobenius_port_energy_bridge", "pending_weighted_frobenius_port_energy_adapter"),
    "T-P4-024": ("P4.combined_schur_port_energy_adapter", "pending_combined_schur_port_energy_adapter"),
    "T-P4-025": ("P4.real_norm_square_expansion", "pending_real_norm_square_expansion"),
    "T-P4-026": ("P4.young_cross_term_bound", "pending_young_cross_term_bound"),
    "T-P4-027": ("P4.fixed_cell_lambda_admissibility", "pending_fixed_cell_lambda_contract"),
    "T-M4-008": ("M4.energy_to_schur_budget_bridge", "pending_conditional_energy_schur_bridge"),
    "T-P8-005": ("P8.independent_reachability", "pending_terminal_transfer_interface"),
    "T-P8-006": ("P8.ramp_reconstruction_compiled_candidate", "pending_ramp_reconstruction_child"),
    "T-P8-007": ("P8.independent_reachability", "pending_ramp_sidecar_validation"),
    "T-P8-009": ("P8.independent_reachability", "pending_interval_local_ramp_calculus"),
    "T-P8-010": ("P8.ramp_reconstruction_compiled_candidate", "pending_compiled_candidate_gate_review"),
    "T-P8-011": ("P8.interval_local_endpoint_adapter", "pending_interval_local_ramp_endpoint_adapter"),
    "T-P8-008": ("P8.independent_reachability", "pending_first12_explicit_time_adapter"),
    "T-P0-002": ("P0.reproducibility_baseline", "pending_fresh_receipt_reaudit"),
    "T-M4-002": ("M4.block45_full_certificate", "pending_dependency_cone_reaudit"),
    "T-M4-003": ("M4.block45_full_certificate", "pending_weighted_terminal_split"),
    "T-M4-004": ("M4.block45_full_certificate", "pending_generic_weighted_qpoly_sidecar"),
    "T-M4-005": ("M4.block45_full_certificate", "pending_eta81_terminal_corollary"),
    "T-M4-006": ("M4.block45_full_certificate", "pending_cross_branch_budget_transfer"),
    "T-M4-007": ("M4.cross_branch_budget_transfer", "pending_pure_budget_transfer_formalization"),
    "T-P7-001": ("P7.strict_tail_fallback", "pending_tail_obligation_audit"),
    "T-P7-002": ("P7.tail_schur_completion_2x2", "pending_typed_tail_schur_completion"),
    "T-DAG-003": ("M4.block45_full_certificate", "pending_shared_lemma_projection"),
    "T-REPAIR-001": ("P3.strict_true_dh_bounds", "pending_repair_loop_audit"),
}

REVIEW_ID_ALIASES = {
    "review-FLT-topology-quotient-clm": "T-FLT-TOPOLOGY-QUOTIENT-CLM",
}

RECORD_GLOBS = (
    "review-*.md", "handoff-*.md", "handoff-*.json",
    "companion-*.md", "companion-*.json",
)
RECORD_KINDS = {"review_result", "handoff", "companion_log"}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def front_matter(path: Path) -> dict[str, str]:
    lines = path.read_text(encoding="utf-8").splitlines()
    if len(lines) < 2:
        return {}
    # Accept the legacy inbox shape without an opening delimiter, but expose
    # the repair as metadata so malformed handoffs never look fully clean.
    legacy = lines[0].strip() != "---"
    start = 1 if not legacy else 0
    try:
        end = lines.index("---", start)
    except ValueError:
        if legacy:
            # A few periodic workers emit a key/value header without either
            # YAML delimiter.  Recover only the contiguous pre-heading
            # metadata; never scan the mathematical body for task fields.
            recovered: dict[str, str] = {}
            for line in lines:
                if line.lstrip().startswith("#"):
                    break
                match = re.fullmatch(r"([A-Za-z_][A-Za-z0-9_-]*):\s*(.*)", line)
                if match:
                    recovered[match.group(1)] = match.group(2).strip().strip("'\"")
            if recovered.get("kind"):
                recovered["_format_warning"] = "missing_yaml_delimiters"
                return recovered
        return {}
    result: dict[str, str] = {}
    for line in lines[start:end]:
        match = re.fullmatch(r"([A-Za-z_][A-Za-z0-9_-]*):\s*(.*)", line)
        if match:
            result[match.group(1)] = match.group(2).strip().strip("'\"")
    if legacy:
        result["_format_warning"] = "missing_opening_yaml_delimiter"
    return result


def record_header(path: Path) -> dict[str, str]:
    """Read the bounded metadata envelope for an inbox record."""
    if path.suffix.lower() == ".json":
        try:
            value = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, UnicodeDecodeError, json.JSONDecodeError):
            return {}
        if not isinstance(value, dict):
            return {}
        return {str(key): str(item) if item is not None else ""
                for key, item in value.items()}
    return front_matter(path)


def record_kind(path: Path, header: dict[str, str]) -> str | None:
    """Return the accepted record kind, or ``None`` for planning/noise files."""
    kind = header.get("kind", "")
    if kind in RECORD_KINDS:
        return kind
    if kind:
        return None
    # Some agents use a descriptive ``NEW_REVIEW_*`` filename and omit the
    # kind field.  A bounded task envelope with review-specific status fields
    # is still a review record; do not infer from arbitrary prose or from a
    # bare task_id, so planning/claim documents remain excluded.
    if (header.get("task_id") and
            (header.get("review_id") or header.get("proof_status") or
             header.get("admission_label") or
             path.name.lower().startswith("new_review"))):
        return "review_result"
    # A filename convention is a narrow compatibility fallback for old agent
    # envelopes that omitted ``kind``; it does not scan the mathematical body.
    name = path.name.lower()
    if name.startswith("review-"):
        return "review_result"
    if name.startswith("handoff-"):
        return "handoff"
    if name.startswith("companion-"):
        return "companion_log"
    return None


def inbox_records(inbox: Path) -> list[Path]:
    """Return envelope-recognized root-level records in deterministic order.

    Filename globs remain a compatibility fast path, while all root-level
    Markdown/JSON envelopes are inspected so descriptive ``NEW_REVIEW_*``
    records cannot be silently missed.  ``record_kind`` remains the sole
    admission to this list, keeping planning and claim files out.
    """
    paths = {path for pattern in RECORD_GLOBS for path in inbox.glob(pattern)}
    paths.update(inbox.glob("*.md"))
    paths.update(inbox.glob("*.json"))
    return sorted(path for path in paths
                  if record_kind(path, record_header(path)) is not None)


def reconcile_inferred_claim_records(state, inbox: Path) -> list[str]:
    """Reclassify claims admitted by the pre-fix broad envelope inference.

    The historical integration events and processed markers are retained.  We
    only repair the attached reference, and append an explicit no-admission
    correction event, so the state remains auditable and the repair is
    idempotent.
    """
    repaired: list[str] = []
    for node in state.nodes.values():
        refs = node.metadata.get("agent_review_refs", [])
        if not isinstance(refs, list):
            continue
        for ref in refs:
            if not isinstance(ref, dict) or ref.get("record_kind") != "review_result":
                continue
            record_file = str(ref.get("record_file", ""))
            if not record_file.startswith("agent_review_inbox/claim-"):
                continue
            path = (ROOT / Path(record_file)).resolve()
            try:
                path.relative_to(inbox)
            except ValueError:
                continue
            if not path.is_file():
                continue
            header = record_header(path)
            if header.get("kind") or header.get("status") != "claimed":
                continue
            task_id = str(ref.get("task_id", ""))
            ref.update({
                "record_kind": "claim",
                "integration_status": "reclassified_not_record",
                "classification": "claim_not_review",
                "invalidated_reason": "bounded-envelope-inference-repair",
                "admission_label": "ignored",
            })
            state.event(
                "agent_record_reclassified",
                record_file=record_file,
                record_kind="claim",
                previous_record_kind="review_result",
                reason="bounded inference incorrectly accepted status=claimed",
                task_id=task_id,
                admission_effect="none",
                registry_promoted=False,
                formal_certificate_allowed=False,
                node_id=node.id,
            )
            repaired.append(record_file)
    return repaired


def resolve_task_id(path: Path, header: dict[str, str]) -> str:
    """Resolve an omitted task id from a bounded record-id prefix.

    Periodic agents historically emitted ``review_id`` values such as
    ``review-T-P4-038-agent-20260907T1558`` without a separate ``task_id``.
    Recover only from the known TASK_TARGETS keys and choose the longest
    boundary-aligned prefix; never inspect the mathematical body for routing
    hints.  An explicit task_id remains authoritative, including an unknown
    value which must stay in the inbox for manual triage.
    """
    explicit = str(header.get("task_id", "")).strip()
    if explicit:
        return explicit
    candidates: list[str] = []
    for raw in (header.get("review_id", ""), path.stem):
        token = str(raw).strip()
        token = re.sub(r"^(?:review|handoff|companion)-", "", token,
                       flags=re.IGNORECASE)
        for task_id in TASK_TARGETS:
            if token == task_id or token.startswith(task_id + "-"):
                candidates.append(task_id)
    return max(candidates, key=len) if candidates else ""


def source_commit(path: Path, header: dict[str, str]) -> str:
    """Recover an explicitly printed Git commit when agents put it in prose."""
    declared = str(header.get("commit", "")).strip()
    if declared:
        return declared
    text = path.read_text(encoding="utf-8")
    match = re.search(r"(?<![0-9a-f])[0-9a-f]{40}(?![0-9a-f])", text, re.IGNORECASE)
    return match.group(0) if match else "unknown"


def artifact_binding_audit(header: dict[str, str], root: Path = ROOT) -> dict[str, str] | None:
    """Audit an explicitly declared candidate/artifact path and SHA.

    This is provenance-only.  A matching hash does not mean that the artifact
    compiled or is admissible; missing evidence remains pending and a mismatch
    is rejected without deleting or rewriting the inbox record.
    """
    raw_path = str(header.get("candidate_path", "") or
                  header.get("artifact_path", "")).strip()
    declared = str(header.get("candidate_sha256", "") or
                   header.get("artifact_sha256", "")).strip().upper()
    if not raw_path and not declared:
        return None
    if not raw_path:
        return {"status": "PENDING", "reason": "missing_artifact_path"}
    if not declared:
        return {"status": "PENDING", "reason": "missing_artifact_sha256",
                "path": raw_path}

    candidate = Path(raw_path)
    if not candidate.is_absolute():
        candidate = root / candidate
    try:
        resolved = candidate.resolve(strict=False)
        resolved.relative_to(root.resolve())
    except (OSError, ValueError):
        return {"status": "PENDING", "reason": "artifact_outside_workspace",
                "path": raw_path}
    if not resolved.is_file():
        return {"status": "PENDING", "reason": "artifact_missing",
                "path": raw_path}

    actual = sha256(resolved)
    result = {"status": "BOUND" if actual == declared else "REJECTED",
              "path": str(resolved), "declared_sha256": declared,
              "actual_sha256": actual}
    if actual != declared:
        result["reason"] = "artifact_sha256_mismatch"
    return result


def node_by_name(state, name: str):
    for node in state.nodes.values():
        if node.name == name:
            return node
    raise ValueError(f"no Route-B node named {name!r}")


def routeb_residual_l1_receipt_audit(state, node, path: Path) -> dict | None:
    """Audit only a structured T-P4-018 JSON handoff, never prose claims."""
    if path.suffix.lower() != ".json":
        return None
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError):
        return {"status": "REJECTED", "errors": ["handoff_json_malformed"],
                "pending": []}
    if not isinstance(payload, dict):
        return {"status": "REJECTED", "errors": ["handoff_json_not_object"],
                "pending": []}
    receipt = payload.get("receipt", payload.get("lean_receipt"))
    if not isinstance(receipt, dict):
        return {"status": "PENDING", "errors": [],
                "pending": ["missing_structured_residual_l1_receipt"]}

    source_hash = None
    for artifact in node.metadata.get("source_artifacts", []):
        if (isinstance(artifact, dict) and
                str(artifact.get("path", "")).replace("\\", "/").endswith(
                    "examples/routeb_gram_residual_lean/GramResidual.lean")):
            source_hash = artifact.get("sha256")
            break
    candidate = None
    if node.parent_id and node.parent_id in state.nodes:
        candidate = state.nodes[node.parent_id].metadata.get(
            "candidate_reconstruction_receipt")
    audit = audit_routeb_residual_l1_lean_receipt(
        receipt,
        expected_source_sha256=source_hash,
        expected_coefficient_artifact_sha256=(
            candidate.get("artifact_sha256") if isinstance(candidate, dict) else None),
        candidate_receipt=candidate if isinstance(candidate, dict) else None,
    )
    return {
        "status": audit.status,
        "source_sha256": audit.source_sha256,
        "coefficient_artifact_sha256": audit.coefficient_artifact_sha256,
        "theorem_names": list(audit.theorem_names),
        "axioms": {name: list(values) for name, values in audit.axioms.items()},
        "errors": list(audit.errors),
        "pending": list(audit.pending),
        "formal_certificate_allowed": audit.formal_certificate_allowed,
        "registry_eligible": audit.registry_eligible,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--state", type=Path,
                        default=ROOT / "artifacts/routeb_6dof/state.json")
    parser.add_argument("--inbox", type=Path,
                        default=ROOT / "agent_review_inbox")
    args = parser.parse_args()
    state_path = args.state.resolve(strict=True)
    inbox = args.inbox.resolve(strict=True)
    processed = inbox / "processed"
    processed.mkdir(parents=True, exist_ok=True)

    store = StateStore(state_path)
    state = store.load()
    if state.project != "routeb-6dof-external":
        raise ValueError(f"unexpected project: {state.project!r}")
    repaired_claims = reconcile_inferred_claim_records(state, inbox)
    if repaired_claims:
        store.save(state)

    candidates = []
    for path in inbox_records(inbox):
        header = record_header(path)
        kind = record_kind(path, header)
        if kind is None:
            continue
        if header.get("integration_status") == "integrated":
            continue
        task_id = resolve_task_id(path, header) or REVIEW_ID_ALIASES.get(
            header.get("review_id", ""), "")
        if task_id not in TASK_TARGETS:
            continue
        digest = sha256(path)
        marker = processed / path.with_suffix(".json").name
        previous = None
        if marker.exists():
            try:
                old = json.loads(marker.read_text(encoding="utf-8"))
            except json.JSONDecodeError as exc:
                raise ValueError(f"malformed processed marker: {marker}") from exc
            if old.get("review_sha256", "").upper() == digest:
                continue
            # A changed same-name file is a correction/revision, not an excuse
            # to overwrite history.  Keep the old hash in the new provenance
            # record and require a second, explicit integration event.
            previous = old
        candidates.append((path, header, kind, digest, marker, previous))

    if not candidates:
        print(json.dumps({"integrated": [], "reclassified_claims": repaired_claims,
                          "state_revision": store.load().revision}))
        return 0

    if any(node.status.value == "in_progress" for node in state.nodes.values()):
        raise ValueError("refuse inbox integration while a node is in progress")

    integrated = []
    for path, header, kind, digest, marker, previous in candidates:
        task_id = resolve_task_id(path, header) or REVIEW_ID_ALIASES.get(
            header.get("review_id", ""), "")
        target_name, classification = TASK_TARGETS[task_id]
        record_file = str(path.relative_to(ROOT)).replace("\\", "/")
        ref = {
            "record_file": record_file,
            "record_kind": kind,
            "review_sha256": digest,
            "task_id": task_id,
            "source_agent": header.get("source_agent", "unknown"),
            "created_at": header.get("created_at", "unknown"),
            "integration_status": "integrated_as_pending_metadata",
            "classification": classification,
            "admission_effect": "none",
            "target_scope": "routeb_node" if target_name else "external_reuse_catalog",
            "source_commit": source_commit(path, header),
        }
        artifact_audit = artifact_binding_audit(header)
        if artifact_audit is not None:
            ref["artifact_binding_audit"] = artifact_audit
            if (artifact_audit["status"] == "REJECTED" and
                    "admission_label" not in ref):
                ref["admission_label"] = "rejected"
        if kind == "review_result":
            # Keep the legacy field stable for downstream reports and old
            # processed markers while exposing the generic record envelope.
            ref["review_file"] = record_file
        if header.get("admission_label"):
            ref["admission_label"] = header["admission_label"]
        if previous is not None:
            ref["correction_of_sha256"] = previous.get("review_sha256")
            ref["classification"] = f"{classification}_revision"
        if header.get("_format_warning"):
            ref["format_warning"] = header["_format_warning"]
        if target_name:
            node = node_by_name(state, target_name)
            if task_id == "T-P4-018":
                receipt_audit = routeb_residual_l1_receipt_audit(state, node, path)
                if receipt_audit is not None:
                    ref["residual_l1_receipt_audit"] = receipt_audit
                    node.metadata.setdefault("residual_l1_receipt_audits", []).append({
                        "record_file": record_file,
                        "review_sha256": digest,
                        **receipt_audit,
                    })
            node.metadata.setdefault("agent_review_refs", []).append(ref)
        event_kind = {
            "review_result": "agent_review_integrated",
            "handoff": "agent_handoff_integrated",
            "companion_log": "agent_companion_integrated",
        }[kind]
        state.event(
            event_kind if target_name else f"external_reuse_{event_kind}",
            record_file=record_file,
            record_kind=kind,
            review_sha256=digest,
            task_id=task_id,
            classification=ref["classification"],
            admission_effect="none",
            registry_promoted=False,
            formal_certificate_allowed=False,
            **({"residual_l1_receipt_status": ref["residual_l1_receipt_audit"]["status"]}
               if "residual_l1_receipt_audit" in ref else {}),
            **({"artifact_binding_status": ref["artifact_binding_audit"]["status"]}
               if "artifact_binding_audit" in ref else {}),
            **({"node_id": node.id} if target_name else {
                "catalog": "anthropic-fermats-last-theorem",
            }),
        )
        integrated.append((path, marker, ref, state.events[-1]["at"]))

    # StateStore performs the optimistic revision check and checksum update.
    store.save(state)
    for path, marker, ref, event_at in integrated:
        marker.write_text(json.dumps({**ref, "integrated_at": event_at},
                                     ensure_ascii=False, indent=2) + "\n",
                          encoding="utf-8")
    print(json.dumps({"integrated": [ref["task_id"] for _, _, ref, _ in integrated],
                      "state_revision": state.revision,
                      "registry_size": len(state.registry),
                      "formal_certificate_allowed": False}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
