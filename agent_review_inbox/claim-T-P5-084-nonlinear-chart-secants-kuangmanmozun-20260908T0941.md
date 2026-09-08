---
kind: task_claim
task_id: T-P5-084-NONLINEAR-CHART-SECANT-GEOMETRY
agent: 狂蛮魔尊
source_agent: 狂蛮魔尊
created_at: 2026-09-08T09:41:00-06:00
status: claimed
inspected_head: f481e497dd3ee3c5c007b3e1ea022cb6ae509a8a
---

# Claim — T-P5-084 nonlinear chart secant geometry / injectivity gate

本轮未发现梁智炜对“狂蛮魔尊”的新点名任务。柳冠一的 T-P5-082 已完成 nonlinear differential pullback / finite-step curvature defect，但明确留下 chart injectivity 与 image coverage；古月方源的 T-P5-083 处理 Euler step-segment coverage，并未解决 nonlinear chart 本身的 global secant/co-Lipschitz geometry。

我认领一个窄数学 child：给出 nonlinear chart 在凸 source cell 上从 Jacobian 信息升级到 global secant injectivity/co-Lipschitz 的可检查充分条件，区分 pointwise Jacobian invertibility 与真正 global inverse reserve；构造精确反例证明 `sigma_min(DT) >= mu` 单独不足，并给出与固定 normalized `z`-barrier/physical quadratic contraction 组合时的 division-free gate。

边界：只做数学 closure、反例与 formalizable theorem statements。不会做 provenance、receipt、admission、Lean 编译、deployed source binding、Float64/controller、P8 coverage 或 registry mutation。