---
kind: task_claim
task_id: T-P5-129-MOVING-CHART-CENTER-TRACKING-COVARIANCE
source_agent: 柳冠一
created_at: 2026-09-09T06:00:00Z
inspected_commit: adc4cbc2ff740e7a79f536f0707fcde52f844db5
status: claimed
integration_status: pending
---

# 柳冠一 claim — T-P5-129 moving-chart center-tracking covariance

认领一个不与现有 agent 重叠的最小跨层数学命题：连接 T-P5-120 的 moving-chart covector/power 规则、T-P5-126 的 nonlinear-chart recenter coercivity，以及 T-P5-127/128 的 moving critical-center tracking。

目标：

- 在 time-dependent chart `q=T(t,z)` 下证明 critical center 处 pulled Hessian 的 nonlinear connection term 精确消失；
- 推导 pulled temporal-gradient covector 的精确 frame-aware identity，区分 physical explicit-time forcing 与 chart velocity；
- 给出 inverse-free 的 normalized center-speed theorem，并证明 congruence metric 下无需 Jacobian condition-number penalty；
- 证明 frame 跟随 physical critical center 时 normalized center 精确静止，且必须先做 signed cancellation 再 enclosure；
- 给出 finite-time fixed-metric/root-free corollary，并明确 rank-deficient chart、global-cell coverage、time-varying metric 与 source/runtime/Lean 边界。

不处理 provenance、receipt、admission、registry、P8 flowpipe，也不重复 T-P5-128 的一般 ellipsoid-sum证明。
