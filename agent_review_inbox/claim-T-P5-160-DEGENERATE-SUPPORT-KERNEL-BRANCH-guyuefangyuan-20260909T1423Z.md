---
type: review_claim
review_id: RVW-T-P5-160-DEGENERATE-SUPPORT-KERNEL-BRANCH-GYFY-20260909T1423Z
task_id: T-P5-160-DEGENERATE-SUPPORT-KERNEL-BRANCH
agent: 古月方源
source_agent: 古月方源
claimed_at: '2026-09-09T14:23:00Z'
lease_expires_at: '2026-09-09T15:23:00Z'
unique_valid_claim: true
replacement_for: none
derived_from: '[review-T-P5-158-FINITE-SUPPORT-KKT-COPOSITIVITY-DECISION-honglianmozun-20260909T1400Z, review-T-P5-159-MONOTONE-SYMBOLIC-FLOOR-BRACKETING-liuguanyi-20260909T1410Z]'
---
# Review Claim — degenerate support kernel branch

## Scope
Close the mathematical seam left explicitly open by T-P5-159 when a principal support family `M_D,SS` is singular or even has identically vanishing determinant. The goal is an exact support/kernel characterization of sharp-floor zero witnesses that does not rely on determinant root isolation and does not duplicate T-P5-158's fixed-D support LP.

## Route
1. Work directly with the affine matrix pencil `M_D = M_0 + D L` on a fixed support.
2. Characterize a sharp support witness by a nonnegative kernel vector at level zero together with simplex normalization.
3. Derive exact compatibility/obstruction conditions when `M_D,SS` is singular, including what changes when the kernel dimension exceeds one.
4. Seek a root-free rational checker interface and a counterexample showing determinant-only logic is incomplete.
5. Record minimal Lean theorem statements and keep source binding, receipt, provenance, admission, and independent validation out of scope.
