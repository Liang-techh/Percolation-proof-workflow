---
kind: task_claim
task_id: T-P5-139-RANGE-SOLVE-SCHUR-RESET
claim_id: claim-T-P5-139-range-solve-schur-reset-kuangmanmozun-20260909T0829Z
agent: 狂蛮魔尊
source_agent: 狂蛮魔尊
created_at: 2026-09-09T08:29:00Z
inspected_commit: 725f76e5bd27c658e59183961d762b9b719d7716
status: completed
completed_at: 2026-09-09T08:37:00Z
result_path: agent_review_inbox/review-T-P5-139-RANGE-SOLVE-SCHUR-RESET-kuangmanmozun-20260909T0834Z.md
result_commit: f0198916eb5fe1783cbeb9055031c9d9bd0dc954
companion_path: agent_review_inbox/companion-T-P5-139-RANGE-SOLVE-SCHUR-RESET-kuangmanmozun-20260909T0836Z.md
companion_commit: a532d5cbdf638050919c922739de77076298871d
scope: derive a singular-safe exact range-solve reduction of the fixed-multiplier ellipsoidal reset Schur gate, eliminating the rank-one PSD check when K_tau y=b is supplied; include sharp boundary and incompatibility counterexamples
non_overlap: consumes T-P5-137/138 only; does not redo source binding, provenance, Lean compilation, admission, registry, or actual-source search
---

# 狂蛮魔尊 claim — T-P5-139

Completed. The result replaces the fixed-`tau` rank-one domination matrix check by an exact solve `K_tau y=b` plus the sharp scalar gate `4(E-C-tau R)-b^T y>=0`, with singular-compatible exactness, singular-incompatible obstruction, rational checker guidance, and minimal Lean leaves.
