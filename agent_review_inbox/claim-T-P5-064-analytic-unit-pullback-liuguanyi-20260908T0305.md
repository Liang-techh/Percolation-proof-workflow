---
kind: claim
task_id: T-P5-064-ANALYTIC-UNIT-PULLBACK
agent: 柳冠一
source_agent: 柳冠一
claimed_at: 2026-09-08T03:05:00-06:00
status: claimed
parent_tasks:
  - T-P5-061
  - T-P5-062-MULTIFACTOR-LIPSCHITZ-STRATA
  - T-P5-063-UNDERCANCELLED-AGGREGATE-GATE
---

# Claim — T-P5-064 analytic-unit pullback bridge

本轮认领 T-P5-063 明确保留的 `nonconstant analytic-unit transport` 数学缺口，不重复 aggregate integer valuation、partial-stratum parity、Lean receipt、source provenance 或 admission。

目标：把 T-P5-063 的纯 monomial source map

`h_a(z)=c_a * prod_j z_j^(W_aj)`

推广到实际更常见的 local normal-crossing / monomial-times-unit 形式

`h_a(z)=u_a(z) * prod_j z_j^(W_aj)`，

其中 `u_a` 是在目标 cell 上严格不消失的连续/Lipschitz unit。优先证明：

1. integer valuation 与 parity 的 exact transport 仍为 `E'=W^T E`、`beta'=W^T beta mod 2`；
2. 非常数 unit 可精确吸收到 reduced packet，而不会改变 contact valuation/parity gate；
3. 给定 exact rational `0<m_a<=|u_a|<=M_a` 与 `Lip(u_a)<=L_a` 时，推出 unit multiplier 的显式 rational sup/lower/Lipschitz budget，并组合 T-P5-062 的 monomial Lipschitz gate；
4. 给出 sharp obstruction：若缺少 uniform nonvanishing margin，所谓 unit 会隐藏额外零阶/极点，纯 exponent transport 不再 sound；
5. 给出最小 Lean-friendly theorem statements 与 source typed contract。

边界：不证明 deployed CSE 已具有该 factorization，不做 Float64/libm、coverage、P8/ODE、receipt/provenance、独立验证、registry/admission，也不抢其他 Agent 已认领的任务。