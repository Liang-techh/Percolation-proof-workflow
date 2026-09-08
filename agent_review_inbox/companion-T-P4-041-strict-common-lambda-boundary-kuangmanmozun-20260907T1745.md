---
kind: companion_log
review_id: review-T-P4-041-strict-common-lambda-boundary-kuangmanmozun-20260907T1742
task_id: T-P4-041-STRICT-COMMON-LAMBDA-BOUNDARY
agent: 狂蛮魔尊
source_agent: 狂蛮魔尊
created_at: 2026-09-07T17:45:00-06:00
status: pending
---

# 协作摘要（中文）

### 2026-09-07 17:45 — 狂蛮魔尊
- 当前完成：按梁智炜 revision-742 点名，补齐 shared `theta/lambda` 的严格交集层。有限多行存在共同严格 witness，当且仅当每行 `delta_i>0`，且所有 pair 都通过 square-root-free strict gate：`C<U+V` 或 `(C-U-V)^2<4UV`。
- 发现的问题：弱可行与严格可行不能混用。若弱 gate 通过但严格 gate 失败，则在全族 weak-feasible 前提下，必然要么某行 `delta=0`，要么存在一对行满足 exact boundary-touch：`C>=U+V` 且 `(C-U-V)^2=4UV`。此时全族共同可行集只能是单点，任何正 shared reserve、非零 rounding interval、generic source widening tolerance 都不存在。
- 反例：`q1=(t-1)(t-2)` 与 `q2=(t-2)(t-3)` 各自行都有严格可行区间，但共同 weak set 只有 `{2}`；对应直接 lambda 形式的唯一共同点是 `lambda=3/2`，两行同时饱和。pair 数据 `C=4,U=V=1`，弱 gate 以等号通过、严格 gate 精确失败。
- 闭包边界：把第二行改成 `q2_e=(t-(2-e))(t-3)`，则 `e>0` 有正宽交集、`e=0` 单点接触、`e<0` 完全断开；精确判别量 `4UV-(C-U-V)^2=32e(1-e)`。`e=1/10` 时取 `t=39/20`，两行 margin 分别为 `19/400` 与 `21/400`，最小正 reserve `19/400`；当 `e→0+` 时 reserve 收缩到 0。
- 给其他 Agent 的建议：Lean lane 可直接形式化 `sqrt_sum_lt_iff_poly`、boundary equality、finite strict interval Helly、finite strict witness ↔ positive common reserve 和 touching counterexample。source/checker lane 若只得到 weak equality witness，不应送入 T-P4-040 的非零 interval/rounding consumer；先过 strict gate。
- 建议的下一步：梁智炜可把链条固定为“weak gate 只判存在/不存在 → strict gate 判 positive-reserve eligibility → T-P4-040 endpoint interval 负责 rational robustness”。不要用 weak PASS 偷渡 strict Schur margin。
- 关联任务/Review：`T-P4-039`、`T-P4-040-RATIONAL-LAMBDA-GUARD`、`review-T-P4-041-strict-common-lambda-boundary-kuangmanmozun-20260907T1742.md`。

说明：本轮已读取 `collaboration_board.md`。GitHub connector 当前只提供整文件 replace，不提供安全 append；为避免覆盖并发 Agent 的历史留言，本中文协作内容写入 companion log，未修改共享留言板。
