---
kind: review_result
review_id: review-T-P8-002-EXPLICIT-TIME-13STATE-PARENT-liuchuanafeng-20261026T0814Z
source_agent: 流川枫
created_at: 2026-10-26T08:14:00Z
inspected_commit: dde1fb58d26f76e1fa3a3cf824c32be959f95474
task_id: T-P8-002
admission_label: pending
---

# Review — T-P8-002 explicit-time 13-state parent option

## Question / bottleneck

独立决策审计：比较新的 explicit-time 13-state parent 与现有 14-state ramp parent，包括初始域与终端语句变化。

检查文档 `docs/routeb-p8-next-concrete-child.md` 与 Lean adapter `examples/routeb_p8_contract_adapter/P8ContractAdapter.lean`。

## Evidence inspected

- `docs/routeb-p8-next-concrete-child.md` (SHA f14f362c16ba33583af2545a933fe2b0727c50d9):
  - 当前 source 不能直接实例化 `RouteBP8PicardStep.RampRhsPremise`。
  - 父定理 state = Fin 14 = q1..q6, dq1..dq6, w, c，要求 F z wSlot = z cSlot 且 F z cSlot = 0。
  - 已审计 Julia `full_rhs!` 为 13-state，`du[13]=0`，receipt 将 c 标为 sidecar。
  - zeroTailLift 不满足 ramp（已在 Lean 中证明 zeroTailLift_not_ramp）。
  - timeLift 提供条件性 repair：抽象 G : time → State13 → State13 抬升为 14-state，w' = z cSlot, c' = 0，满足 ramp premise。
  - 但未证明真实 source 前 12 分量等于 G、Float64/FD/solve 语义、interval containment、Picard/flowpipe。
  - Admission: source_binding=OPEN, adapter_contract=COMPILED/conditional_interface_only, flowpipe_coverage=OPEN, formal_certificate_allowed=false, registry unchanged。

- `examples/routeb_p8_contract_adapter/P8ContractAdapter.lean` (SHA 11c8e23a52128e56b65a76024285c45a9070414d):
  - 定义 zeroTailLift 与 timeLift。
  - 定理 zeroTailLift_not_ramp : ¬ RampRhsPremise (zeroTailLift G)。
  - 定理 timeLift_rampPremise : RampRhsPremise (timeLift G t)。
  - 明确声明无 source binding、interval receipt、ODE existence 或 true-DH claim。

## Analysis

explicit-time 13-state option（通过 timeLift）可以在抽象 G 给定时满足现有 14-state ramp parent 的维度/time contract，但：

- 初始域与终端语句仍依赖于父定理的 FullX0 与 ramp前提；未提供新的独立 13-state parent 定理文本。
- source 绑定（前 12 分量 = G）仍 OPEN。
- 无任何 flowpipe coverage、terminal transfer 或 formal certificate 证据。
- 因此不能将此选项作为已验证替代或升级；仅作为 conditional interface scaffold。

## Admission decision

保持 **pending**。不提升 registry、不修改 state、不声称 flowpipe coverage 或 formal proof。

下一跳仍为建立真实 source body 前 12 分量的语义 binding。
