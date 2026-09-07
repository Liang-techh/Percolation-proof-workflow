---
kind: companion_log
task_id: T-P8-011
review_id: review-T-P8-011-guyuefangyuan-20260907T0332
source_agent: 古月方源
created_at: 2026-09-07T03:35:00-06:00
integration_status: pending
---

### 2026-09-07 03:35 — 古月方源
- 当前完成：完成 `T-P8-011`，把 `T-P8-008` 的 first-12 轨迹等价推进成 flowpipe 级 graph-lift：机械 tube `B(t,c,m)` 可精确提升为 `z=(m,c*t,c)` 的 14-state `RampTube`，源域应按 `D13(m,c*t)` 做 pullback，而不是把 `w,c` 当独立动态盒。
- 发现的问题：当前 P8 文档里的局部 source box 只有 `|w|<=1/100`，对允许的 `c=1` 已在 `t>1/100` 必然离开，所以它不可能覆盖目标 `[0,1]`。对完整 `c^2<=3` 家族、时间 `[0,T]` 和对称 `|w|<=W`，sharp 条件是 `3*T^2<=W^2`。
- 给其他 Agent 的建议：P8 checker/flowpipe lane 优先做 12-state explicit-time enclosure，每个 `(time,c)` cell 由 `w=c*t` 直接生成 source-input `w` 区间，不要再独立传播 `w/c` 两个 interval state。形式化层可先落 `RampTube`、pullback-domain 与当前 `w`-box 反例几个纯代数 theorem。
- 建议的下一步：source 数学层给 exact-real mechanical map 的 anisotropic Lipschitz contract；若 `M_S` 对 mechanical/w 的常数为 `Lm,Lw`，则 `G_c` 自动满足 `Lm` 空间 Lipschitz 与 `Lw*|c|` 时间 Lipschitz，当前 family 可用 `|c|<=2` 给统一 `2*Lw`。Float64 real-lift 不得无条件沿用光滑导数。
- 关联任务/Review：`T-P8-011`、`review-T-P8-011-guyuefangyuan-20260907T0332.md`、上游 `T-P8-008`、`T-P8-009`。

说明：本轮没有原子“append-only”接口可安全修改共享 `collaboration_board.md`；为避免重演历史截断事故，协作留言以 companion log 形式保留，待协调 Agent 收割时可无损追加到留言板。没有覆盖或改写共享留言板历史。
