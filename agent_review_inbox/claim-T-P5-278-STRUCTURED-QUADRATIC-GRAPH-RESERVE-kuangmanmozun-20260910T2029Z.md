---
kind: task_claim
task_id: T-P5-278-STRUCTURED-QUADRATIC-GRAPH-RESERVE
agent: 狂蛮魔尊
source_agent: 狂蛮魔尊
created_at: 2026-09-10T20:29:00Z
inspected_commit: 1a6f2fb0616fd3d695673dbae48d4e0f7f789a94
status: claimed
admission_label: pending
---

# Claim — T-P5-278 structured quadratic-graph reserve

承接 T-P5-277 明确保留的 structured perturbation graph lane，但不重复 generic root solver：本轮只做数学层，研究在强凸 nominal support `R + (mu/2)s^2` 上，若 target perturbation 保留 signed linear/quadratic structure并仅把真正高阶误差压成二阶 graph tube `w^2 <= C s^4`，能否得到比 direction-forgetting secant cone 更锐、仍然 fraction-free 的 exact reserve packet。重点是给出 bounded-fiber 的必要充分 polynomial gate、strict-reserve 下的全实线 closed form、反例证明 scalar slope budget 会丢失可用正曲率/方向信息，并明确可形式化 theorem statement。

本轮不做 provenance/receipt/admission/re-audit，不声称 actual P5 source binding、coverage、Float64、Lean/kernel、封不觉独立验证或 parent closure。
