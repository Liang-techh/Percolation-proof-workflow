---
type: review_claim
review_id: RVW-T-P5-164-NEGATIVE-STAR-EDGE-DECOMPOSITION-GYFY-20260909T1519Z
task_id: T-P5-164-NEGATIVE-STAR-EDGE-DECOMPOSITION
agent: 古月方源
source_agent: 古月方源
claimed_at: '2026-09-09T15:19:00Z'
lease_expires_at: '2026-09-09T16:19:00Z'
unique_valid_claim: true
replacement_for: none
derived_from: '[review-T-P5-153-HOMOTHETIC-SIMPLEX-SLACK-COUPLING-guyuefangyuan-20260909T1228Z, review-T-P5-154-UNIFORM-ADDITIVE-SIMPLEX-FLOOR-kuangmanmozun-20260909T1237Z, review-T-P5-157-SINGLE-BAD-EDGE-SHARP-UNIFORM-FLOOR-guyuefangyuan-20260909T1337Z, review-T-P5-158-FINITE-SUPPORT-KKT-COPOSITIVITY-DECISION-honglianmozun-20260909T1357Z, review-T-P5-160-DEGENERATE-SUPPORT-KERNEL-BRANCH-guyuefangyuan-20260909T1432Z, review-T-P5-162-TANGENT-PD-AFFINE-SUPPORT-CONTINUATION-honglianmozun-20260909T1502Z]'
---
# Review Claim — negative-star edge decomposition

## Scope
Advance the homothetic-simplex uniform-floor mathematics beyond the single-bad-edge case without duplicating the generic copositivity/KKT or tangent-PD continuation lanes. Treat the exact sign pattern in which every negative pair coefficient is incident to one common hub vertex and all leaf-leaf coefficients are nonnegative.

## Route
1. Prove that for a negative-edge star, global simplex nonnegativity is equivalent to the finite family of two-vertex hub/leaf edge inequalities.
2. Reuse the T-P5-157 root-free two-variable gate to obtain a rational checker with no square roots or continuum optimization.
3. Prove that the sharp global floor is conceptually the maximum of the individual edge sharp floors, so there is no multiway interior tax for a star.
4. Give an exact negative-triangle counterexample showing that edgewise floors cease to suffice once the sign graph contains a negative cycle/triangle.
5. Record the source-facing sign-graph dispatch and small Lean theorem decomposition.

No source admission, provenance/receipt audit, runtime/Float64 claim, registry mutation, Lean/kernel validation, or independent re-audit is in scope.