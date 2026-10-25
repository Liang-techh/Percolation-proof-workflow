---
kind: review_result
review_id: T-P8-002-EXPLICIT-TIME-13STATE-PARENT-20261025
source_agent: 流川枫
created_at: 2026-10-25T10:10:00Z
inspected_commit: 553a4535b518f3452727fb7a79424639ed3fa72c
task_id: T-P8-002
admission_label: pending
---

# Review Result — T-P8-002 explicit-time 13-state parent option

## Inspected question

比较新的 explicit-time 13-state parent 与现有 14-state ramp parent，包括初始域与终端语句变化；交付决策备忘与最小定理签名，不修改 source，不声称 flowpipe coverage。

## Evidence inspected

- `docs/routeb-p8-next-concrete-child.md` (SHA f14f362c16ba33583af2545a933fe2b0727c50d9)
- `examples/routeb_p8_contract_adapter/P8ContractAdapter.lean` (SHA 11c8e23a52128e56b65a76024285c45a9070414d)
- 现有 parent 定理 `RouteBP8PicardStep.RampRhsPremise` 要求 Fin 14 = q1..q6, dq1..dq6, w, c，且 `F z wSlot = z cSlot`、`F z cSlot = 0`
- 已审计 Julia `full_rhs!` 为 13-state（输入 u[1:13]，du[13]=0），receipt 将 c 标记为 sidecar

## Findings

1. **维度与 ramp contract mismatch 已确认**：当前 deployed source 不能直接实例化 14-state `RampRhsPremise`。若将 13-state 自然补成 14-state 且令 w'/c'=0，则在合法状态 z（cSlot=1）上 `F z wSlot = 0 ≠ z cSlot`，故 `zeroTailLift_not_ramp` 成立（负事实 CLOSED）。

2. **条件 adapter 已编译**：`timeLift G t` 将抽象 TimeVectorField13 提升为满足 ramp premise 的 14-state field（w' = z cSlot，c' = 0），`timeLift_rampPremise` 为 exact-real 定理。但仅为 conditional_interface_only，不绑定真实 Julia DH `full_rhs!` 前 12 分量，也不涵盖 Float64/FD/区间/Picard/flowpipe。

3. **初始域与终端语句**：任何新 explicit-time 13-state parent 必须明确改写初始域（排除 c 非零的退化）与终端语句；当前文档未提供已验证的完整替代 parent，仅提供接口修复形状。

4. **最小定理签名（建议，非证明）**：
   ```text
   theorem explicit_time_13state_parent_option
     (G : TimeVectorField13)
     (source_binding : ∀ t z, first12 (deployed_full_rhs t z) = G t (forgetTail z))
     : RampRhsPremise (timeLift G t) ∧ 初始域排除 c≠0 退化
   ```
   实际 source_binding 仍 OPEN。

## Admission boundary

- source_binding = OPEN
- ramp_binding for deployed 13-state = OPEN
- adapter_contract = compiled / conditional_interface_only
- flowpipe_coverage = OPEN
- formal_certificate_allowed = false
- registry = unchanged

**admission_label: pending**

本审计不修改任何正式证明、registry 或 state；不声称 flowpipe coverage或 parent 替换已完成。下一步仍为 source-to-G 前 12 分量语义绑定。
