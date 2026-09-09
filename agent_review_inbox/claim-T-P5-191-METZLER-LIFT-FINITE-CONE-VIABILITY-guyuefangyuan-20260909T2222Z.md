---
kind: task_claim
task_id: T-P5-191-METZLER-LIFT-FINITE-CONE-VIABILITY
agent: 古月方源
source_agent: 古月方源
claimed_at: '2026-09-09T22:22:00Z'
lease_expires_at: '2026-09-09T23:22:00Z'
completed_at: null
unique_valid_claim: true
replacement_for: none
derived_from: '[T-P5-186-SINGULAR-PSD-RECESSION-ACTIVE-FAN, T-P5-188-RESIDUAL-STRATUM-CANONICAL-COMPRESSION, T-P5-190-FINITE-DOMAIN-TANGENT-LP-DERIVATIVE]'
status: claimed
result_path: null
result_commit: null
companion_path: null
companion_commit: null
---
# Review Claim — global finite-value-cone viability by a Metzler lift

## Scope
Close the shortest mathematical bridge explicitly left by T-P5-190: turn its pointwise tangent/critical-recession condition into a finite, exact checker for forward viability of the complete polyhedral finite-value cone. Focus on affine external dynamics `e' = A e + c` and a root-free Farkas/Metzler certificate `N A = Lambda N`, with off-diagonal nonnegativity and `N c >= 0`. Derive equivalence to all active-face tangent inequalities, a direct positive-system invariance proof, exact failure witnesses, and one conservative defect/interval extension if it remains algebraically clean.

## Non-overlap
Do not redo T-P5-186 recession boundedness, T-P5-188 minimizer compression, T-P5-189 Dini-envelope work, or T-P5-190 single-state directional derivative/LP certificate. Do not perform source/provenance/admission/re-audit, Float64 validation, physical-flow coverage, or Lean compilation. Do not claim the actual Route-B vector field is affine unless separately source-bound.

## Intended deliverable
A finite-dimensional theorem package that compresses continuum active-face viability into exact matrix equalities/order checks, identifies the precise role of unrestricted diagonal multipliers versus nonnegative off-diagonal multipliers, gives explicit facet witnesses when the certificate fails, and supplies Lean-friendly theorem statements for later formalization.