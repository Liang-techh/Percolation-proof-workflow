---
kind: task_claim
task_id: T-P5-076-WEIGHTED-GRAM-LIPSCHITZ
agent: 柳冠一
source_agent: 柳冠一
claimed_at: 2026-09-08T07:04:00-06:00
parent_tasks:
  - T-P5-074-WEIGHTED-STRONG-MONOTONE-SCC
  - T-P5-075-DAMPED-CORRECTOR-ENERGY
scope: mathematics_only_source_to_secant_squared_lipschitz_bridge
---

# T-P5-076 claim — weighted Gram certificate for the missing same-weight squared-Lipschitz packet

柳冠一认领 T-P5-075 明确留下的同一 weighted norm 下 squared-Lipschitz source seam。目标不是重复 strong-monotonicity 或 corrector Lyapunov 证明，而是证明一个 source-to-math bridge：从 `J = D Phi` 的 weighted Gram `J^T W J` 的 signed/correlated cell bounds，生成 exact-rational、无平方根/特征值/矩阵逆的 secant inequality `||Phi(x)-Phi(y)||_W^2 <= Lambda ||x-y||_W^2`。重点保留 Gram cross terms 在求和后的符号抵消，并给 implicit-root Jacobian 的 denominator-cleared contract 与安全但较松的 entrywise fallback。

本轮不做 deployed source binding、Float64/FD/controller/solve、P8/ODE coverage、Lean compile/kernel、receipt/provenance/admission/re-audit，也不改写 T-P5-074/075 的既有 theorem 边界。
