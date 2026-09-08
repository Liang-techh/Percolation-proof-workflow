---
kind: task_claim
task_id: T-P5-081-MOVING-AFFINE-CHART
agent: 狂蛮魔尊
source_agent: 狂蛮魔尊
created_at: 2026-09-08T08:30:00-06:00
status: claimed
inspected_head: 786302df585d27a8c212a05528dbaa012f8b269b
---

# Claim — T-P5-081 moving affine chart / connection cancellation

本轮未发现梁智炜对“狂蛮魔尊”的新点名任务。T-P5-079 已完成固定 affine similarity normalization，但明确留下 moving/time-dependent scale `S(t)` 的 derivative/connection term 边界；T-P5-080 正在处理 evaluator defect 的 signed correlation，并未覆盖 moving-chart geometry。

我认领一个窄数学 child：证明 moving affine chart `x=c(t)+S(t)z` 下连续时间与一步 corrector 的 exact transport，区分可由 co-moving congruence metric 精确消掉的 scale/connection term 与不能自动消掉的 moving-center translation term；给出 division-free budget、sharp counterexample，以及可形式化 theorem statement。

边界：只做数学 closure/反例。不会做 provenance、receipt、admission、Lean 编译、deployed source binding、Float64/controller、P8 coverage 或 registry mutation。