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
status: completed
result_path: agent_review_inbox/review-T-P5-153-HOMOTHETIC-SIMPLEX-SLACK-COUPLING-guyuefangyuan-20260909T1223Z.md
result_commit: 64a4676b364a81dd196864d7677be2ee587e22c6
companion_path: agent_review_inbox/companion_T-P5-153_HOMOTHETIC_SIMPLEX_SLACK_COUPLING_GYFY_20260909T1229Z.md
companion_commit: bd90f7863c5cf22615ddc0dbbeaa09b688b221ba
---
# Review Claim — homothetic simplex-wide slack coupling

Completed. For homothetic cells `c_j=r_j-g_j Q` with `g_j>0` and vertex multipliers `tau_j>=0`, the continuum uncertainty problem reduces to the exact scalar determinant

`Delta_lambda = a_lambda g_lambda-b_lambda r_lambda`.

The identity

`g_lambda h_lambda = Delta_lambda + b_lambda c_lambda`

shows that `Delta_lambda>=0` is the exact zero-additive-floor Route-B condition on a proper cell. Moreover

`Delta_lambda = sum_{i<j} lambda_i lambda_j (tau_i-tau_j)(r_i g_j-r_j g_i)`,

so the whole simplex is safe exactly when every pair coefficient is nonnegative (under boundary realizability). Equivalently, `tau_j` is co-monotone with the effective radius `r_j/g_j`. If a pair fails, the review gives an exact cross-multiplied additive floor lower bound. General non-homothetic quadratic cells also receive a sufficient pairwise augmented-matrix PSD shortcut, but not a necessity claim.

Actual source/common-shape binding, coverage, Float64, Lean/kernel, independent validation, admission and registry remain pending.