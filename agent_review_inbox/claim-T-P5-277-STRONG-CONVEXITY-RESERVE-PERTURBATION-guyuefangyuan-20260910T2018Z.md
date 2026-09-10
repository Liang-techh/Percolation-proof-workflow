---
kind: task_claim
task_id: T-P5-277-STRONG-CONVEXITY-RESERVE-PERTURBATION
agent: 古月方源
source_agent: 古月方源
created_at: 2026-09-10T20:18:00Z
inspected_commit: 027071e5a48bbb6ba67788c47479a24681aeca08
status: completed
admission_label: pending
review_commit: 1a6f2fb0616fd3d695673dbae48d4e0f7f789a94
companion_commit: 42626c0d56ed112b63c77273c6e575ea99eb58cd
---

# Claim — T-P5-277 strong-convexity reserve perturbation

承接 T-P5-276 明确保留的下一条数学 seam：在同一 source key / active fiber 上，若原目标满足统一强凸性 `p'' >= mu > 0` 且 interval-selected minimizer `tau` 有严格 reserve `p(tau)-eta >= rho > 0`，本轮只做数学层，推导 coefficient/FD target perturbation 与 moving-bracket perturbation 对 minimizer displacement 和 reserve 的定量影响，并尽量给出 rational/fraction-free checker packet。目标是避免每次小扰动都重建完整 algebraic endpoint / Sturm–Tarski atlas，同时严格区分 target perturbation 与 source/bracket perturbation。

本轮不做 provenance/receipt/admission/re-audit，不声称 actual P5 source binding、coverage、Float64、Lean/kernel、封不觉独立验证或 parent closure。

已完成：正式数学结果写入 `review-T-P5-277-STRONG-CONVEXITY-RESERVE-PERTURBATION-guyuefangyuan-20260910T2019Z.md`，中文协作摘要写入对应 companion log。核心结论是共同 strong-convexity collar 内 bracket movement 本身零 debit，而 anchored target perturbation 可由完全 fraction-free gate `D <= mu*(2(rho-eps)+mu*S)` 消费；并得到 constrained minimizer 的平方位移界 `mu^2(x-y)^2<=D`。