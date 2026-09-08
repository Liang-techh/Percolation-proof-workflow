---
kind: companion_log
task_id: T-P5-047
agent: 狂蛮魔尊
source_agent: 狂蛮魔尊
created_at: 2026-09-07T21:50:00-06:00
review_commit: cc2a2f5c10d41891e64adba2f5415c26324678e1
status: handoff
---

# T-P5-047 协作留言 — 狂蛮魔尊

本轮已完成一个新的数学 child：如果最终 P5 bundled certificate 必须让 quarter barrier 与 `Kc=1/12` parameter/incremental gate **共享同一个 Pareto 参数 `r`**，则不能把 T-P5-046 的两个单门优化结果各自 PASS 后直接拼起来；两个严格可行区间可能完全错开。

我利用两个 gate 具有同一个二次曲率 `-d r^2`，把共同可行性压成了一个必要且充分的 **五候选 exact-rational checker**：`r=0`、`r=1`、两个“处在当前 lower-envelope 上”的内部顶点，以及唯一的 affine crossover。所有决定条件都已消去除法与平方根；只有 PASS 后才需要除法构造具体 `r`。

P5 特化里更简单：若

`Fb=(109-r)D(r)-800 Eb(r)`，

`Fg=(109-r)D(r)-2400 Eg(r)`，

则

`Fb-Fg = 800[(3Eg0-Eb0)+(3eg-eb)r]`。

所以哪个 gate 是瓶颈只由两个 bias envelope 决定，determinant 项完全抵消。若这个 affine difference 在 `r=0,1` 同号，一个 gate 全区间支配另一个，直接复用 T-P5-046 的单门 optimizer 即可；若异号，才需要检查 crossover。

反例族也已写入正式 review：

`f1_eps = eps-(r-1/4)^2`，

`f2_eps = eps-(r-3/4)^2`。

每个 gate 单独都在任意 `eps>0` 时 PASS，但共享最优 margin 精确等于 `eps-1/16`。因此 `eps=1/100` 是“两个单门都 PASS、共享 r 却不存在”的严格反例；`eps=1/16` 是 boundary-only；`eps=1/10` 则只有 crossover `r=1/2` 给出最佳共同正 margin `3/80`，说明 crossover 候选不能省。

给梁智炜/形式化侧的关键边界：**先确认最终架构是否真的要求两个 consumer 固定同一个 r。** 如果两个逻辑独立 theorem 可以各自调用 Pareto-family theorem、各用一个 r witness，那么不要强加 T-P5-047；如果 bundled candidate 要冻结单一 r，则应使用本 child，不能使用两个独立 optimizer 的 PASS 代替。

建议最小 Lean 叶：`same_curvature_difference_affine`、`same_curvature_vertex_square`、两个 active-vertex guard、`crossover_inside_of_endpoint_sign_change`、`crossover_value_scaled`、`shared_positive_iff_five_candidates`，再加 P5 的 `Fb-Fg` 消去恒等式和三个 `eps` regression。

当前仍是 pending mathematical child；没有升级 source binding、Float64/controller、flowpipe/P8 coverage、P5/P8/M4 或 registry。