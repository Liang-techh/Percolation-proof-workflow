---
type: review_claim
review_id: RVW-T-P5-155-THREE-VERTEX-EXACT-COPOSITIVE-FLOOR-HLMZ-20260909T1248Z
task_id: T-P5-155-THREE-VERTEX-EXACT-COPOSITIVE-FLOOR
agent: 红莲魔尊
source_agent: 红莲魔尊
claimed_at: '2026-09-09T12:48:00Z'
lease_expires_at: '2026-09-09T13:48:00Z'
unique_valid_claim: true
replacement_for: none
derived_from: '[review-T-P5-154-UNIFORM-ADDITIVE-SIMPLEX-FLOOR-kuangmanmozun-20260909T1233Z]'
status: completed
result_path: agent_review_inbox/review-T-P5-155-THREE-VERTEX-EXACT-COPOSITIVE-FLOOR-honglianmozun-20260909T1310Z.md
result_commit: b79e57e78e42aeba644b3e030a7e9a93d81eecf0
---
# Review Claim — three-vertex exact copositive floor

Completed. The three-vertex T-P5-154 copositivity target admits an exact finite rational active-set checker, stronger than the generic PSD fast path.

For arbitrary positive vertex scales `g_i`, a proposed floor `D` is reduced to the barycentric triangle quadratic

`F_D=D(sum_i g_i lambda_i)+K_12 lambda_1 lambda_2+K_13 lambda_1 lambda_3+K_23 lambda_2 lambda_3`.

Each of the three edges is decided exactly by endpoint signs plus one division-free univariate discriminant gate. After all edges pass, a hidden interior minimum can exist only when the two-dimensional tangent Hessian is positive definite. Then there is one exact Cramer-numerator barycentric candidate and one polynomial value numerator `I_D`; if the Hessian is singular PSD, every interior stationary value extends along a flat direction to the boundary and creates no new obligation.

For common scale `g`, the interior gate collapses to `g D J+abc>=0`, with `a=K_12,b=K_13,c=K_23` and `J=2(ab+ac+bc)-(a^2+b^2+c^2)`. The T-P5-154 symmetric example `a=b=c=-4,g=1` gives the exact floor `D=4/3`.

A realizable example `tau=(1,2,3)`, `r=(5,1,10)`, `g=1` has `(K_12,K_13,K_23)=(-4,10,9)` and sharp floor `D=1`, while the corresponding `M_D` has determinant `-529/4`; hence PSD fails even though the floor is exactly valid. PSD failure must therefore remain inconclusive in the three-vertex lane.

Actual source binding, same-family uncertainty semantics, coverage, Float64/runtime, Lean/kernel, independent validation by 封不觉, admission and registry remain pending.