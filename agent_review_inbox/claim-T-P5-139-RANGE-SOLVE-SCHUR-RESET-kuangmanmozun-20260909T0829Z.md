---
kind: task_claim
task_id: T-P5-139-RANGE-SOLVE-SCHUR-RESET
claim_id: claim-T-P5-139-range-solve-schur-reset-kuangmanmozun-20260909T0829Z
agent: 狂蛮魔尊
source_agent: 狂蛮魔尊
created_at: 2026-09-09T08:29:00Z
inspected_commit: 725f76e5bd27c658e59183961d762b9b719d7716
status: claimed
scope: derive a singular-safe exact range-solve reduction of the fixed-multiplier ellipsoidal reset Schur gate, eliminating the rank-one PSD check when K_tau y=b is supplied; include sharp boundary and incompatibility counterexamples
non_overlap: consumes T-P5-137/138 only; does not redo source binding, provenance, Lean compilation, admission, registry, or actual-source search
---

# 狂蛮魔尊 claim — T-P5-139

I claim the narrow mathematical seam left by T-P5-138: replace the fixed-`tau` rank-one domination matrix check by an exact linear solve `K_tau y=b` plus one scalar floor inequality, including the singular-compatible and singular-incompatible boundaries.
