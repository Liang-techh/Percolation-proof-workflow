---
type: review_claim
review_id: RVW-T-P5-156-SIMPLEX-REFINEMENT-WEIGHTED-SLACK-COVARIANCE-LGY-20260909T1302Z
task_id: T-P5-156-SIMPLEX-REFINEMENT-WEIGHTED-SLACK-COVARIANCE
agent: 柳冠一
source_agent: 柳冠一
claimed_at: '2026-09-09T13:02:00Z'
lease_expires_at: '2026-09-09T14:02:00Z'
unique_valid_claim: true
replacement_for: none
derived_from: '[review-T-P5-152-PARAMETER-DEPENDENT-CELL-SLACK-COUPLING-liuguanyi-20260909T1201Z, review-T-P5-154-UNIFORM-ADDITIVE-SIMPLEX-FLOOR-kuangmanmozun-20260909T1233Z]'
status: completed
result_commit: 6b24af619a6649229803f4b12125a14bcf6e22c0
---
# Review Claim — simplex refinement weighted-slack covariance

## Scope
Close a source-to-math interface seam left by the parameter-dependent-cell robustification: actual uncertainty packets may refine, triangulate, or reparameterize a simplex. Prove when the signed cell slack and the already-weighted multiplier slack transport exactly through a column-stochastic refinement map, and isolate the defect created by incorrectly interpolating `tau` and `c` separately and multiplying afterward.

## Route completed
1. Proved exact pushforward covariance under a nonnegative column-stochastic refinement matrix `P` with induced coarse weights `lambda=P mu`.
2. Proved the robust implication `c_lambda>=0 => h_lambda>=0` and any uniform additive floor transport without refinement tax when `c` and `h=tau*c` are transported as typed signed objects.
3. Derived the exact pairwise covariance defect between pushforward `sum p_i tau_i c_i` and reconstructed `(sum p_i tau_i)(sum p_i c_i)`.
4. Gave sharp safe/unsafe sign conditions, a whole-cell root-free homothetic gate, and an exact rational counterexample where separate interpolation creates a false robust certificate.
5. Proved T-P5-154's homogeneous copositive matrix transports by exact nonnegative congruence `M -> P^T M P`; stated the minimal source/formal interface without entering T-P5-155's three-vertex copositive-floor lane.

No provenance/receipt audit, admission promotion, runtime/Float64 claim, Lean/kernel validation, or registry mutation is performed.
