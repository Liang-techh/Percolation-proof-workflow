---
type: review_claim
review_id: RVW-T-P5-157-SINGLE-BAD-EDGE-SHARP-UNIFORM-FLOOR-GYFY-20260909T1322Z
task_id: T-P5-157-SINGLE-BAD-EDGE-SHARP-UNIFORM-FLOOR
agent: 古月方源
source_agent: 古月方源
claimed_at: '2026-09-09T13:22:00Z'
lease_expires_at: '2026-09-09T14:22:00Z'
unique_valid_claim: true
replacement_for: none
derived_from: '[review-T-P5-153-HOMOTHETIC-SIMPLEX-SLACK-COUPLING-guyuefangyuan-20260909T1223Z, review-T-P5-154-UNIFORM-ADDITIVE-SIMPLEX-FLOOR-kuangmanmozun-20260909T1233Z, review-T-P5-155-three-vertex-exact-copositive-floor-honglianmozun-20260909T1310Z]'
status: completed
result_commit: 4a42f46d6ce6b73b5a72b936e435b22ada5c5e25
---
# Review Claim — single-bad-edge sharp uniform floor

## Scope
Close a narrow exact subfamily of T-P5-154 that remains useful in arbitrary simplex dimension: all pair coefficients K_ij are nonnegative except one bad edge K_ab=-kappa<0. Prove that the full-simplex sharp uniform additive floor is attained on that one edge, derive its exact one-dimensional value, and give a root-free rational checker with no square roots or divisions.

## Route completed
1. Proved all positive pair terms can only improve the deficit, and mass outside the bad edge dilutes the bad contribution relative to positive `g_lambda`.
2. Reduced the exact N-vertex floor to the one bad edge and equivalently reduced full T-P5-154 copositivity to one `2 x 2` principal copositive block.
3. Improved the initially planned three-regime interval test to the smaller exact two-regime root-free gate: with `L=kappa-D(g_a+g_b)`, accept iff `L<=0` or `L^2<=4D^2 g_a g_b`.
4. Recorded the conceptual closed form `D*=kappa/(sqrt(g_a)+sqrt(g_b))^2` only as interpretation; the trusted theorem remains radical-free.
5. Gave an algebraic strict-failure witness, a sharp unequal-scale regression, and minimal Lean theorem statements without overlapping T-P5-155's generic N=3 active-set checker.

No provenance/receipt audit, admission promotion, runtime/Float64 claim, Lean/kernel validation, or registry mutation is performed.