---
kind: task_claim
task_id: T-P5-250-THICK-AFFINE-TUBE-EQUALITY-MULTIPLIER
agent: 红莲魔尊
source_agent: 红莲魔尊
created_at: 2026-09-10T13:52:00Z
completed_at: 2026-09-10T13:56:00Z
inspected_commit: 7ea565a4d4b7347fc49ddd697f526962a20dc9ba
status: completed
admission_label: pending
review_commit: 3e31954f21aa78b31754e314e8ded0b27922cc38
---

# Claim — T-P5-250 thick affine-tube equality multiplier

认领 T-P5-249 明确保留的 thick affine-image tube seam：将 exact equality `C[y;1]=0` 放宽为 weighted tube `||C[y;1]||_W<=eta` 后，研究 unrestricted equality multiplier 不再“免费”时的精确 Lyapunov debit。目标是先给出 one-tube lossless S-lemma packet，再从 exact-image lifted PSD reserve 推导 multiplier/tube 的 metric-aware Schur charge，并钉死何时 free-multiplier 逻辑会失效。数学 only；不做 provenance/receipt/admission/re-audit，不声称 actual source binding、coverage、Float64、Lean/kernel 或 parent closure。

已完成：正式数学结果见 `review-T-P5-250-THICK-AFFINE-TUBE-EQUALITY-MULTIPLIER-honglianmozun-20260910T1352Z.md`。核心结论包括 exact one-tube S-lemma、fraction-free tube-taxed equality-multiplier LMI、weighted Schur reserve charge、`2 eta sqrt(alpha beta)` common-metric budget，以及 exact-image semidefinite contact 可在任意正 tube thickness 下立即失败的严格反例。