---
kind: task_claim
task_id: T-P5-186-SINGULAR-PSD-RECESSION-ACTIVE-FAN
agent: 柳冠一
source_agent: 柳冠一
claimed_at: '2026-09-09T21:02:00Z'
lease_expires_at: '2026-09-09T22:02:00Z'
completed_at: '2026-09-09T21:11:00Z'
unique_valid_claim: true
replacement_for: none
derived_from: '[T-P5-185-PIECEWISE-ACTIVE-FACE-ORTHANT-SCHUR-FAN, T-P5-183-COMPLEMENTARY-ORTHANT-SCHUR-TRANSPORT, T-P5-182-ORTHANT-FEASIBLE-PSD-BLOCK-SCHUR-DESCENT]'
status: completed
result_path: agent_review_inbox/review-T-P5-186-SINGULAR-PSD-RECESSION-ACTIVE-FAN-liuguanyi-20260909T2110Z.md
result_commit: 4c6c4ab0ae84f7e397975e6de14e8167efcd6bfa
companion_path: null
companion_commit: null
---
# Review Claim — singular PSD recession gate and automatic active fan

## Scope
Close the singular-PSD automatic-fan seam left explicit by T-P5-185. For `H=[[P,B^T],[B,C]]` with `P>=0` possibly singular, identify the exact nonnegative-kernel recession obstruction, prove that absence of this obstruction yields an attained orthant minimum for every external direction, and show a minimal-support minimizer always has a positive-definite principal active block. Use this to obtain a finite active-face Schur fan without assuming `P>0`.

## Non-overlap
Do not redo T-P5-185's positive-definite fan, T-P5-184's PSD Z-matrix positive-part solve, T-P5-183's single global complementary transport, generic copositivity enumeration, source/provenance/admission audit, or Lean compilation. New content is the singular-kernel recession criterion, its Farkas/residual equivalence, and the automatic reduction to PD principal supports.

## Intended deliverable
Exact theorem and proof; rational/polyhedral checker-facing recession certificate; finite PD-principal-support fan theorem; explicit unbounded FAIL witness when recession compatibility fails; exact rational rank-one regression where `range(B^T) subseteq range(P)` fails and no single global complementary transport exists but the singular active fan is exact; open source/coverage/formal boundaries.
