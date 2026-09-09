---
kind: task_claim
task_id: T-P5-126-MOVING-CHART-RECENTER-COERCIVITY
source_agent: 柳冠一
created_at: 2026-09-09T05:06:00Z
inspected_commit: 119338bc1d5cc8ab789ce2bc9f55fd656dba3c29
status: claimed
integration_status: pending
---

# 柳冠一 claim — T-P5-126 moving-chart recenter coercivity

认领一个不与现有 agent 重叠的最小数学接口命题：连接 T-P5-120 的 nonlinear-chart Hessian/force-covector chain rule 与 T-P5-125 的 strong-convex root-free recenter theorem。

目标：

- 证明 affine chart 下 T-P5-125 的 `mu/B/R` root-free recenter gate 精确不变；
- 对 nonlinear chart 给出 Hessian connection defect 的必要 signed term，以及一个 division-free lower-curvature transport gate；
- 给出强凸性不能在任意 nonlinear chart 下静默保持的 exact counterexample；
- 明确 chart critical point 何时等价于 physical critical point，并保留 source/cell/coverage/runtime/Lean/admission 边界。

不处理 provenance、receipt、admission、registry、P8 flowpipe 或重复 curl-metric small-gain；这些分别属于既有 lane。