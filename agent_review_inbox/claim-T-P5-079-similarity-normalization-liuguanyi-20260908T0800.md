---
kind: task_claim
task_id: T-P5-079-SIMILARITY-NORMALIZATION
agent: 柳冠一
source_agent: 柳冠一
claimed_at: 2026-09-08T08:00:00-06:00
parent_tasks:
  - T-P5-074-WEIGHTED-STRONG-MONOTONE-SCC
  - T-P5-076-WEIGHTED-GRAM-LIPSCHITZ
  - T-P5-077-ANCHOR-LOCALIZED-INVARIANT-BALL
scope: mathematics_only_same-scaling_coordinate_normalization_and_weight_transport_bridge
---

# T-P5-079 claim — similarity normalization bridge for weighted SCC certificates

柳冠一认领一个新的数学接口 child：证明 source 坐标做正对角 affine normalization `x=c+Sz` 时，若 residual/vector field 同步按 `F~(z)=S^{-1}F(c+Sz)` 变换，则 T-P5-074 的 weighted strong-monotonicity、T-P5-076 的 weighted Gram squared-Lipschitz、T-P5-077 的 anchor/root Lyapunov localization 可以通过 transported weight `W~=S^TWS` 精确保持同一 `mu/Lambda/B0/Vstar` 常数；同时给出错误地保持旧 weight 或独立缩放 residual codomain 的 obstruction。只做数学/接口正确性，不进入 Lean receipt、provenance、admission、source execution 或 P8 coverage。
