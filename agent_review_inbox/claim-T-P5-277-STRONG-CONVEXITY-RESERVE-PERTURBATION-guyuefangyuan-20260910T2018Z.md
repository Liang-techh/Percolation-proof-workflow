---
kind: task_claim
task_id: T-P5-277-STRONG-CONVEXITY-RESERVE-PERTURBATION
agent: 古月方源
source_agent: 古月方源
created_at: 2026-09-10T20:18:00Z
inspected_commit: 027071e5a48bbb6ba67788c47479a24681aeca08
status: claimed
admission_label: pending
---

# Claim — T-P5-277 strong-convexity reserve perturbation

承接 T-P5-276 明确保留的下一条数学 seam：在同一 source key / active fiber 上，若原目标满足统一强凸性 `p'' >= mu > 0` 且 interval-selected minimizer `tau` 有严格 reserve `p(tau)-eta >= rho > 0`，本轮只做数学层，推导 coefficient/FD target perturbation 与 moving-bracket perturbation 对 minimizer displacement 和 reserve 的定量影响，并尽量给出 rational/fraction-free checker packet。目标是避免每次小扰动都重建完整 algebraic endpoint / Sturm–Tarski atlas，同时严格区分 target perturbation 与 source/bracket perturbation。

本轮不做 provenance/receipt/admission/re-audit，不声称 actual P5 source binding、coverage、Float64、Lean/kernel、封不觉独立验证或 parent closure。