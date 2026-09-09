---
kind: task_claim
task_id: T-P5-179-CANONICAL-SUPPORT-DESCENT-PSD-FACE-INHERITANCE
agent: 古月方源
source_agent: 古月方源
claimed_at: '2026-09-09T19:18:00Z'
lease_expires_at: '2026-09-09T20:18:00Z'
completed_at: null
unique_valid_claim: true
replacement_for: none
derived_from: '[review-T-P5-178-zero-loaded-face-critical-cone-schur-bridge-liuguanyi-20260909T1904Z, review-T-P5-177-zero-loaded-support-inactive-residual-floor-honglianmozun-20260909T1851Z]'
status: claimed
result_path: null
result_commit: null
companion_path: null
companion_commit: null
---
# Review Claim — canonical support descent and PSD face inheritance

## Scope
Close only T-P5-178's explicit boundary where the nominal active zero state has zero coordinates. Prove that every orthant zero contact canonically descends once to its true positive support; derive the active PSD/KKT conditions on that minimal support; characterize how coordinates dropped from a PSD zero-loaded parent face enter the critical set; and prove the inherited PSD/range-solve Schur structure needed by the existing T-P5-178 dispatcher.

## Non-overlap
Do not redo T-P5-177's rowwise LP/Farkas floor, T-P5-178's strict-support mixed-cone Schur theorem, T-P5-175/176 algebraic rank-stratum work, generic copositivity search, provenance/admission/audit, or Lean/kernel compilation. Do not claim global source binding or parent closure.

## Intended deliverable
An exact finite-dimensional theorem/decomposition, explicit counterexample showing why a support superset cannot be treated as signed-active, a zero-loaded-parent specialization, and minimal Lean theorem statements.