---
type: review_claim
review_id: RVW-T-P5-165-NEGATIVE-GRAPH-COMPONENT-FACTORIZATION-KMMZ-20260909T1533Z
task_id: T-P5-165-NEGATIVE-GRAPH-COMPONENT-FACTORIZATION
agent: 狂蛮魔尊
source_agent: 狂蛮魔尊
claimed_at: '2026-09-09T15:33:00Z'
lease_expires_at: '2026-09-09T16:33:00Z'
unique_valid_claim: true
replacement_for: none
derived_from: '[review-T-P5-154-UNIFORM-ADDITIVE-SIMPLEX-FLOOR-kuangmanmozun-20260909T1233Z, review-T-P5-158-FINITE-SUPPORT-KKT-COPOSITIVITY-DECISION-honglianmozun-20260909T1357Z, review-T-P5-159-MONOTONE-SYMBOLIC-FLOOR-BRACKETING-liuguanyi-20260909T1405Z, review-T-P5-161-Z-MATRIX-COPOSITIVITY-EQUALS-PSD-kuangmanmozun-20260909T1437Z, review-T-P5-164-NEGATIVE-STAR-EDGE-DECOMPOSITION-guyuefangyuan-20260909T1521Z]'
status: completed
result_path: agent_review_inbox/review-T-P5-165-NEGATIVE-GRAPH-COMPONENT-FACTORIZATION-kuangmanmozun-20260909T1540Z.md
result_commit: f1c26726dcc54201ced3886d51fe0d5f40102ad4
---
# Review Claim — negative-graph component factorization

## Scope
Attack the mixed-sign copositivity bottleneck left after the Z-matrix fast path and the negative-star special family. For a fixed floor candidate `D`, factor the exact copositivity problem by connected components of the graph formed by strictly negative off-diagonal entries of the floor matrix `M_D`.

## Route
1. Prove the exact equivalence: a symmetric matrix is copositive iff every principal block indexed by a connected component of its negative-edge graph is copositive.
2. Prove any support-minimal negative witness lies entirely inside one negative-edge component, eliminating cross-component support enumeration.
3. Specialize to `M_D` from T-P5-154 and prove the negative-edge partition can only refine as `D` increases, giving a monotone structural accelerator for T-P5-159 bracketing.
4. Give an exact rational mixed-sign example that is copositive but indefinite, where the factorization certifies safety while the T-P5-161 PSD path fails.
5. Record a root-free checker dispatch by component size, with generic KKT only inside unresolved components.

No source admission, provenance/receipt audit, runtime/Float64 claim, registry mutation, Lean/kernel validation, or independent re-audit is in scope.