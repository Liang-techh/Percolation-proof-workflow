---
kind: task_claim
task_id: T-P5-134-NONLINEAR-KNOT-TANGENT-REMAINDER-ABSORPTION
source_agent: 古月方源
created_at: 2026-09-09T07:22:00Z
inspected_commit: 60275eaef8b3a98cd4eaa28c6ac85d552020e498
status: claimed
integration_status: pending
---

# 古月方源 claim — T-P5-134 nonlinear-knot tangent remainder absorption

认领一个不与现有 agent 重叠的最小数学接口命题：直接承接 T-P5-133 对 nonlinear chart 的 secant-vs-anchor-tangent obstruction，研究在 producer 只能给 anchor tangent `J0*xi` 加一个 certified second-order chart remainder 时，如何仍然安全消费 T-P5-130/131/132 的 sharp physical knot-reset envelope。

目标：

- 从 exact decomposition `x = y + r_T` 推导 knot reset 中 linear mismatch 与 quadratic radius 的完整 remainder bookkeeping；
- 若 chart remainder energy 具有二阶 scaling，给出 root-free / division-free 的相对吸收 gate，把 chart nonlinear correction 压成 curvature-headroom tax，而不是粗暴 additive floor；
- 明确哪些 correction 需要 bounded-cell radius，哪些不需要，并给出 counterexample 证明该 radius obligation 不可删除；
- 从 `D^2T` whole-segment action bound 推导 sharp `1/4` remainder-energy factor；
- 给出可直接接 T-P5-131/132 的 effective-headroom theorem 和最小 Lean theorem statements。

不处理 actual chart/source extraction、provenance、receipt、admission、registry、Float64/controller、P8 flowpipe，也不重复 T-P5-133 的 affine covariance、secant identity或 pullback-Hessian connection identity。
