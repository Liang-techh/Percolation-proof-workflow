---
type: review_claim
review_id: RVW-T-P5-162-TANGENT-PD-AFFINE-SUPPORT-CONTINUATION-HLMZ-20260909T1452Z
task_id: T-P5-162-TANGENT-PD-AFFINE-SUPPORT-CONTINUATION
agent: 红莲魔尊
source_agent: 红莲魔尊
claimed_at: '2026-09-09T14:52:00Z'
lease_expires_at: '2026-09-09T15:52:00Z'
unique_valid_claim: true
replacement_for: none
derived_from: '[review-T-P5-159-MONOTONE-SYMBOLIC-FLOOR-BRACKETING-liuguanyi-20260909T1410Z, review-T-P5-160-DEGENERATE-SUPPORT-KERNEL-BRANCH-guyuefangyuan-20260909T1432Z, review-T-P5-161-Z-MATRIX-COPOSITIVITY-EQUALS-PSD-kuangmanmozun-20260909T1442Z]'
---
# Review Claim — tangent-PD affine active-support continuation

## Scope
Advance the symbolic-floor/Lyapunov-reset mathematics without duplicating T-P5-159 bracketing, T-P5-160 degenerate-kernel handling, or T-P5-161 Z-matrix PSD fast path. On a fixed support whose base quadratic has strict positive curvature on the simplex tangent space, derive an exact affine continuation of the support minimizer in the floor parameter D, an exact scalar quadratic value law, and a root-free active-support validity/sharpness interface.

## Route
1. Solve two D-independent bordered linear systems for the affine stationary path `lambda(D)=u+D v`.
2. Prove the exact energy-gap identity `q_D(mu)-phi(D)=(mu-lambda(D))^T M0 (mu-lambda(D))` on the affine support hyperplane.
3. Derive the scalar quadratic `phi(D)=a+bD+cD^2`, with `c=-v^T M0 v<=0` and `phi'(D)=g^T lambda(D)`.
4. Show that while `lambda(D)` remains in the simplex, `phi` is strictly increasing and the support has at most one zero crossing; characterize support-entry/exit by affine coordinate gates.
5. Give exact rational checker packets and a sharp rational example; record the tangent-semidefinite/face-change obstruction explicitly.

No source admission, provenance/receipt audit, runtime/Float64 claim, registry mutation, Lean/kernel validation, or independent re-audit is in scope.