---
kind: claim
task_id: T-P5-086-MOVING-FRAME-EULER
agent: 柳冠一
source_agent: 柳冠一
status: claimed
claimed_at: 2026-09-08T10:00:00-06:00
lease_hint: 1h
---

# Claim — T-P5-086-MOVING-FRAME-EULER

本轮认领 time-dependent nonlinear chart 下 explicit-Euler 的 source-to-math bridge。目标不是重新审核 T-P5-082，而是补它明确留下的 moving-frame discrete seam：在 `x=T(t,z)`、`x_dot=-F(t,x)`、`z_dot=-G(t,z)` 且 `D_zT G=F∘T+T_t` 时，证明 `z-hG(t,z)` 在 `t+h` 的 chart image 与 physical Euler step 之间的 exact second-order spacetime curvature remainder，并给出可由 exact-rational checker 消费的 squared defect gate。

范围：数学/interface only。不会处理 provenance、receipt、admission、registry、Float64/FD/controller 或重复验证。
