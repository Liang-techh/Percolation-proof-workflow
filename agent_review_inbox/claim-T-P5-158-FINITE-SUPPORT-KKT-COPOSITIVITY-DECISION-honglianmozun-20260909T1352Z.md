---
type: review_claim
review_id: RVW-T-P5-158-FINITE-SUPPORT-KKT-COPOSITIVITY-DECISION-HLMZ-20260909T1352Z
task_id: T-P5-158-FINITE-SUPPORT-KKT-COPOSITIVITY-DECISION
agent: 红莲魔尊
source_agent: 红莲魔尊
claimed_at: '2026-09-09T13:52:00Z'
lease_expires_at: '2026-09-09T14:52:00Z'
unique_valid_claim: true
replacement_for: none
derived_from: '[review-T-P5-154-UNIFORM-ADDITIVE-SIMPLEX-FLOOR-kuangmanmozun-20260909T1233Z, review-T-P5-155-THREE-VERTEX-EXACT-COPOSITIVE-FLOOR-honglianmozun-20260909T1255Z, review-T-P5-157-FOUR-VERTEX-FACE-KKT-COPOSITIVITY-CLOSURE-kuangmanmozun-20260909T1332Z]'
status: completed
result_path: agent_review_inbox/review-T-P5-158-FINITE-SUPPORT-KKT-COPOSITIVITY-DECISION-honglianmozun-20260909T1400Z.md
result_commit: fce11e2368dfd33d225a49adfbeb4a880a7c01ae
---
# Review Claim — finite-support KKT copositivity decision

## Scope
Close the fixed-floor finite-dimensional copositivity seam left after T-P5-154/155/157 without duplicating the three-vertex analytic checker or the four-vertex face-specific closure. Prove a dimension-independent exact support/KKT characterization for a rational symmetric matrix on the nonnegative simplex, together with a finite rational decision procedure.

## Route
1. Show every negative copositive counterexample has a support face on which a negative relative-interior stationary point exists.
2. Express that stationary point by the bordered linear system `M_SS lambda = alpha 1`, `1^T lambda=1`, with `lambda>0`, `alpha<0`.
3. Prove the converse and exact rational-witness property for rational `M`.
4. Convert strict sign feasibility into a bounded rational LP margin gate for every nonempty support.
5. Show T-P5-157 is the face-pruned four-vertex special case, while T-P5-155 remains the useful closed-form three-vertex fast path.

No source admission, provenance/receipt audit, runtime/Float64 claim, registry mutation, Lean/kernel validation, or independent re-audit is in scope.