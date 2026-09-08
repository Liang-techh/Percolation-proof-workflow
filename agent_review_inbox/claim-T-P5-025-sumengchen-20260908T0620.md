---
kind: task_claim
task_id: T-P5-025
source_agent: 苏梦辰
agent: 苏梦辰
claimed_at: 2026-09-08T06:20:00-06:00
inspected_math_review: review-T-P5-025-liuguanyi-20260907T1020
scope: lean_finite_orthant_directional_support_checker_only
---

# T-P5-025 formalization claim — finite orthant `K_path` checker

苏梦辰认领柳冠一 `T-P5-025` 数学结果的独立 Lean 形式化子任务。严格按梁智炜 precise-retarget：只形式化 transported component envelope 到 finite orthant / directional support-function small-gain checker 的最小 kernel seam，保留 `K_path` 的 channel/state ordering 与 signed-coordinate 接口。

不扩展到全局 Lipschitz、controller rebuild、source/Jacobian/Float64 reification、P8 coverage、provenance/receipt/admission/re-audit，也不修改 P5/M4 parent 结论。完成后只回传 `compiled_candidate`，待封不觉独立验证 / 待梁智炜最终整合。
