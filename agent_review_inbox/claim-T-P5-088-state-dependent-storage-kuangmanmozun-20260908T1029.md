---
kind: task_claim
task_id: T-P5-088-STATE-DEPENDENT-STORAGE-DERIVATIVE
agent: 狂蛮魔尊
source_agent: 狂蛮魔尊
created_at: 2026-09-08T10:29:00-06:00
status: claimed
inspected_head: a1a84c2873d4f1479f79cdc37ac60a8117cec8b5
---

# Claim — T-P5-088 state-dependent storage derivative / material-metric gate

本轮未发现梁智炜对“狂蛮魔尊”的新点名任务。古月方源刚完成 T-P5-087 moving-metric defect transport，并明确留下“若 Lyapunov storage 本身随 state/time 变化，则 `W_t` / `D_x W` 演化项仍 open”的数学边界；T-P5-086/087 处理的是 defect measurement metric，不等价于 moving storage derivative。

我认领一个窄数学 child：对 `V(t,y)=y^T W(t,y)y` 给出沿实际动力学的 exact material-derivative identity、one-sided relative/additive closure、division-free matrix gate；明确 state-dependent metric 下 residual/evaluator defect 还会通过 `D_y W[e]` 进入 storage derivative，构造忽略该项会把增长误判为衰减的精确反例，并给出最小可形式化 theorem statements。

边界：只做数学 closure、sharp/nonsharp 条件、反例与 formalizable theorem statements。不会做 provenance、receipt、admission、Lean 编译、deployed source binding、Float64/controller、P8 coverage 或 registry mutation。