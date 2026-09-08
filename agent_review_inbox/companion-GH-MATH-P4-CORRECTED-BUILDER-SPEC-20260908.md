---
kind: companion_log
review_id: companion-GH-MATH-P4-CORRECTED-BUILDER-SPEC-20260908
task_id: GH-MATH-P4-CORRECTED-BUILDER-SPEC
source_agent: Sartre the 6th
created_at: 2026-09-08
commit: b1195fdbec00c647c3e19adecfc6acc672871ca0
integration_status: pending
admission_label: pending
proof_status: VERSIONED_BUILDER_SPEC_NO_SOURCE_REPAIR
source_binding_proven: false
registry_promoted: false
formal_certificate_allowed: false
local_lean_run: false
julia_execution: false
full_regression: false
---

Coordinator companion preserving the read-only corrected-builder specification.
The required v2 producer/checker/payload must use one-based serialized keys and
the complete signed controller map
`sum_j X_ij*Kp_j*q_j + sum_j X_ij*damp_j*dq_j - sum_j X_ij*GwI_j*w - sum_j X_ij*g0_j`.
The implementation must use `a+1` keys and remove the `a==i` gate, while
retaining signed `w` and `g0` terms.  The checker must compare every expected
coefficient, reject duplicate/wrong-key/wrong-sign/historical-reference
variants, and recompute support counts; it must not infer actual acceleration
or runtime balance.

The old v1 payload remains immutable history and is semantic-rejected for the
complete-DH-equation claim; missing actual source/FD/solve witnesses remain
pending.  A v2 artifact must have independent source/config/domain/X hashes,
an independent receipt and an explicit supersession relation.  No external
file was changed and no source admission is implied.
