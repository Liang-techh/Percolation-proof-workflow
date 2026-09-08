---
kind: task_claim
task_id: T-P5-089-MECHANICAL-SKEW-ENERGY-CANCELLATION
source_agent: 红莲魔尊
created_at: 2026-09-08T10:50:00-06:00
inspected_commit: c99378fed6897a9802715b32c98717ca6de7df93
status: claimed
admission_label: pending
---

# Claim — T-P5-089 mechanical skew-energy cancellation

红莲魔尊认领一个新的、与现有 T-P5-087/T-P5-088 不重叠的数学 child：研究配置依赖质量矩阵 `M(q)` 的机械 Lyapunov 储能中，`Mdot` 项如何与 Coriolis/Christoffel 项通过 `Mdot-2C` 的 skew 结构精确抵消，并给出当 deployed/FD `C` 只近似满足该结构时的 defect-energy remainder 与 fail-closed obstruction。

边界：只做数学恒等式、能量/耗散 consumer 和候选 theorem statement；不做 source provenance、receipt、admission、Float64 evaluator 或重复 Lean 验证，不抢占 T-P5-088 的 state-dependent-storage derivative 工作。