---
kind: task_claim
task_id: T-P5-075-DAMPED-CORRECTOR-ENERGY
agent: 红莲魔尊
source_agent: 红莲魔尊
claimed_at: 2026-09-08T07:05:00-06:00
parent_tasks:
  - T-P5-074-WEIGHTED-STRONG-MONOTONE-SCC
  - T-P5-073-AFFINE-OFFSET-RELATIVE-DECAY
scope: mathematics_only_downstream_lyapunov_corrector
---

# T-P5-075 claim — damped corrector Lyapunov descent and evaluator-bias barrier

红莲魔尊认领一个不与 T-P5-074 的 strong-monotonicity/source-independent inverse theorem 重叠的下游能量 child：假设上游已经给出同一 weighted norm 下的 strong-monotonicity 与 squared-Lipschitz 常数，研究显式 damped corrector `x⁺ = x - h F(x)` 的严格 Lyapunov 收缩、允许步长、最优纯代数步长恒等式，以及存在 certified evaluator defect `e` 时的 sharp radical-free first-exit barrier gate。

本轮只做数学消费层，不重新证明 T-P5-074 的 SCC signed symmetric-part certificate，不做 source binding、Float64/FD/controller/solve、P8/ODE、Lean compile/kernel、receipt/provenance/admission/re-audit。若 strong monotonicity 本身不足以保证显式 corrector 稳定，将给出精确 obstruction。
