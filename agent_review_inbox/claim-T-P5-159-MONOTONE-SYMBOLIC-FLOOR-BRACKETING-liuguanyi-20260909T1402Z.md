---
type: review_claim
review_id: RVW-T-P5-159-MONOTONE-SYMBOLIC-FLOOR-BRACKETING-LGY-20260909T1402Z
task_id: T-P5-159-MONOTONE-SYMBOLIC-FLOOR-BRACKETING
agent: 柳冠一
source_agent: 柳冠一
claimed_at: '2026-09-09T14:02:00Z'
lease_expires_at: '2026-09-09T15:02:00Z'
unique_valid_claim: true
replacement_for: none
derived_from: '[review-T-P5-154-UNIFORM-ADDITIVE-SIMPLEX-FLOOR-kuangmanmozun-20260909T1233Z, review-T-P5-158-FINITE-SUPPORT-KKT-COPOSITIVITY-DECISION-honglianmozun-20260909T1400Z]'
status: completed
result_path: agent_review_inbox/review-T-P5-159-MONOTONE-SYMBOLIC-FLOOR-BRACKETING-liuguanyi-20260909T1410Z.md
result_commit: 1710eb0b113e44bbe7a4d60367e0bcc8f941ccf9
---
# Review Claim — monotone symbolic-floor bracketing

## Scope
Close the symbolic-`D` seam left explicitly open by T-P5-158 without duplicating its fixed-floor support/KKT decision procedure. Prove the monotonicity and exact generalized-Rayleigh characterization of the least uniform additive floor, show why the sharp floor need not be rational even for rational source data, and derive a fail-closed rational bracketing interface that consumes T-P5-158 fixed-`D` PASS/FAIL witnesses.

## Route
1. Use `q_D(x)=q_0(x)+D(1^T x)(g^T x)` with `g_i>0` to prove upward closure of valid floors and existence of a least floor `D_*`.
2. Identify `D_* = max(0, sup_{x>=0,x!=0} -q_0(x)/((1^T x)(g^T x)))`, equivalently the simplex ratio `max(-Delta_lambda/g_lambda)`.
3. Show a rational fixed-`D` FAIL witness yields a stronger rational lower bound by signed continuation in `D`, while any fixed-`D` PASS yields an upper bound; hence exact rational bisection/support pruning is sound.
4. Give an all-rational two-vertex example with irrational sharp floor, proving that a protocol requiring an exact rational optimizer is mathematically over-constrained.
5. State a root-free two-vertex polynomial threshold gate and a cheap coefficientwise rational upper-floor initialization.

No source admission, provenance/receipt audit, runtime/Float64 claim, registry mutation, Lean/kernel validation, or independent re-audit is in scope.