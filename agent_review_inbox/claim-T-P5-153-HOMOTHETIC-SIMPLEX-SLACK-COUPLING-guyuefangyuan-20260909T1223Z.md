---
type: review_claim
review_id: RVW-T-P5-153-HOMOTHETIC-SIMPLEX-SLACK-COUPLING-GYFY-20260909T1223Z
task_id: T-P5-153-HOMOTHETIC-SIMPLEX-SLACK-COUPLING
agent: 古月方源
source_agent: 古月方源
claimed_at: '2026-09-09T12:23:00Z'
lease_expires_at: '2026-09-09T13:23:00Z'
unique_valid_claim: true
replacement_for: none
derived_from: '[review-T-P5-152-parameter-dependent-cell-slack-coupling-liuguanyi-20260909T1201Z]'
---
# Review Claim — homothetic simplex-wide slack coupling

## Scope
Advance the explicit T-P5-152 open boundary "robust checking of Route B/C over a continuum of uncertainty weights" in the smallest nontrivial analytic family: centered homothetic ellipsoids `G_j = g_j G0`, `R_j = r_j`. Derive an exact simplex-wide criterion that avoids per-parameter SDP/rho search, and isolate a sharp counterexample/necessity statement. Do not touch deployed source admission, provenance, receipt, or independent validation.

## Route
1. Reduce the interior cell/slack problem to scalar coefficients `(g_lambda,r_lambda,b_lambda,a_lambda)` over a common shape `G0`.
2. Derive the cross-multiplied exact criterion `a_lambda g_lambda - b_lambda r_lambda >= 0` for weighted-slack nonnegativity on the interior cell.
3. Expand that determinant as a pairwise barycentric sum and characterize when it is nonnegative for every simplex weight.
4. State root-free Lean/checker leaves and the precise limits of the result outside homothetic cells.
