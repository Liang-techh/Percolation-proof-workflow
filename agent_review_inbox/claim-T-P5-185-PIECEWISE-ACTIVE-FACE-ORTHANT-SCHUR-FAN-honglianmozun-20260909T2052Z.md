---
kind: task_claim
task_id: T-P5-185-PIECEWISE-ACTIVE-FACE-ORTHANT-SCHUR-FAN
agent: 红莲魔尊
source_agent: 红莲魔尊
claimed_at: '2026-09-09T20:52:00Z'
lease_expires_at: '2026-09-09T21:52:00Z'
completed_at: '2026-09-09T20:56:00Z'
unique_valid_claim: true
replacement_for: none
derived_from: '[T-P5-183-COMPLEMENTARY-ORTHANT-SCHUR-TRANSPORT, T-P5-182-ORTHANT-FEASIBLE-PSD-BLOCK-SCHUR-DESCENT]'
status: completed
result_path: agent_review_inbox/review-T-P5-185-PIECEWISE-ACTIVE-FACE-ORTHANT-SCHUR-FAN-honglianmozun-20260909T2055Z.md
result_commit: 2cef444f49ae94b85815734cf4376812b76f824a
companion_path: null
companion_commit: null
---
# Review Claim — piecewise active-face orthant Schur fan

## Scope
Close one narrow mathematical gate left explicitly open by T-P5-183: when no single global complementary transport `Y,R` exists for all external nonnegative directions, prove a sound and lossless cone/active-face subdivision theorem. On each external cone permit its own linear transport, derive the exact constrained energy value, and show that a finite cone cover reduces full copositivity to cone-restricted reduced quadratic forms.

## Non-overlap
Do not redo T-P5-183 global complementarity, T-P5-184 Z-matrix positive-part solve, generic support-KKT/copositivity enumeration, source/provenance/admission audit, or Lean compilation. The intended new content is specifically direction-dependent active-face transport and a positive-definite finite active-set fan corollary.

## Intended deliverable
Exact-real/rational theorem; fixed-face polyhedral checker packet; proof that positive-definite inherited energy automatically admits a finite active-face Schur fan; strict rational regression showing global T-P5-183 transport can fail while a two-cone fan is exact; explicit singular/coverage boundaries and remaining obligations.