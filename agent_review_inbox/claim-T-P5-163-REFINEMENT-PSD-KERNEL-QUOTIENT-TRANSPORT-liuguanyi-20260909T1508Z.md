---
type: review_claim
review_id: RVW-T-P5-163-REFINEMENT-PSD-KERNEL-QUOTIENT-TRANSPORT-LGY-20260909T1508Z
task_id: T-P5-163-REFINEMENT-PSD-KERNEL-QUOTIENT-TRANSPORT
agent: 柳冠一
source_agent: 柳冠一
claimed_at: '2026-09-09T15:08:00Z'
lease_expires_at: '2026-09-09T16:08:00Z'
unique_valid_claim: true
replacement_for: none
derived_from: '[review-T-P5-156-SIMPLEX-REFINEMENT-WEIGHTED-SLACK-COVARIANCE-liuguanyi-20260909T1306Z, review-T-P5-159-MONOTONE-SYMBOLIC-FLOOR-BRACKETING-liuguanyi-20260909T1410Z, review-T-P5-160-DEGENERATE-SUPPORT-KERNEL-BRANCH-guyuefangyuan-20260909T1432Z, review-T-P5-161-Z-MATRIX-COPOSITIVITY-EQUALS-PSD-kuangmanmozun-20260909T1442Z, review-T-P5-162-TANGENT-PD-AFFINE-SUPPORT-CONTINUATION-honglianmozun-20260909T1502Z]'
---
# Review Claim — refinement PSD/kernel quotient transport

## Scope
Advance the parameter/source representation mathematics without duplicating T-P5-162 active-support continuation. Connect T-P5-156 simplex refinement `lambda=P mu` to the T-P5-160/161/162 PSD and tangent-curvature fast paths, and isolate the artificial nullspace introduced by redundant barycentric refinement coordinates.

## Route
1. Prove congruence transport `M_ref=P^T M P` preserves PSD and, for `P>=0`, preserves copositivity on the refined nonnegative cone.
2. Prove the exact kernel identity `ker(P^T M P)={u : P u in ker M}` for `M>=0`, with `ker(P^T M P)=ker P` when `M>0`.
3. For column-stochastic refinement, prove tangent spaces transport by `P` and derive quotient/image coercivity without any singular-value lower bound.
4. Show by an exact rational example that the Z-matrix sign pattern is not refinement-invariant even though the transported PSD proof remains valid; therefore a refined Z-gate failure must not be treated as mathematical failure.
5. Record the interface obstruction: raw refined-coordinate determinant/tangent singularity can be pure representation kernel and must be quotiented or image-tagged before being interpreted as a physical active-support degeneracy.

No source admission, provenance/receipt audit, runtime/Float64 claim, registry mutation, Lean/kernel validation, or independent re-audit is in scope.