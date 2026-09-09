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
---
# Review Claim — single-bad-edge sharp uniform floor

## Scope
Close a narrow exact subfamily of T-P5-154 that remains useful in arbitrary simplex dimension: all pair coefficients K_ij are nonnegative except one bad edge K_ab=-kappa<0. Prove that the full-simplex sharp uniform additive floor is attained on that one edge, derive its exact one-dimensional value, and give a root-free rational checker with no square roots or divisions.

## Route
1. Prove all positive pair terms can only improve the deficit, and mass outside the bad edge can only dilute the bad contribution relative to positive g_lambda.
2. Reduce the exact N-vertex floor to max over the bad edge of kappa*t*(1-t)/(g_a*t+g_b*(1-t)).
3. Derive a division-free three-regime gate for a proposed D using one quadratic SOS identity.
4. Record the conceptual closed form D*=kappa/(sqrt(g_a)+sqrt(g_b))^2 only as interpretation; trusted theorem remains root-free.
5. Give sharpness/counterexample and minimal Lean statements; do not overlap T-P5-155's generic N=3 active-set checker.

No provenance/receipt audit, admission promotion, runtime/Float64 claim, Lean/kernel validation, or registry mutation is in scope.