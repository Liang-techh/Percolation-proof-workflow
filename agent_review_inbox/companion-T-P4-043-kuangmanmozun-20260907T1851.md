---
kind: companion_log
task_id: T-P4-043
source_agent: 狂蛮魔尊
created_at: 2026-09-07T18:51:00-06:00
integration_status: pending
related_review: review-T-P4-043-midpoint-reserve-kuangmanmozun-20260907T1848
---

# 狂蛮魔尊协作留言 — T-P4-043

- 当前完成：把 shared-theta 的 strict-intersection 进一步压成“公共有理内区间 → 共享有理 midpoint → 显式正 reserve”的 sharp 定量桥。对每行 `q_i(t)=A_i t²-G_i t+P_i`，若同一 `a<b` 满足两端都 `q_i<=0`，则 `theta0=(a+b)/2` 有精确恒等式 `4q_i(theta0)=2q_i(a)+2q_i(b)-A_i(b-a)²`。若 `A_i>=A_min>0`，统一得到 `q_i(theta0)<=-A_min(b-a)²/4`。
- 新的 sharp 常数：`1/4` 不能改进；极值行 `q=A(t-a)(t-b)` 在两端恰好为零、midpoint 恰好达到 `-A(b-a)²/4`。因此这不是额外 Young 保守性。
- 下游 reserve：若命名 Young reserve 为 `m`，只要 `2(a+b)m <= A_min(b-a)²`，同一个 midpoint 对所有行都满足 `q_i(theta0)+theta0*m<=0`；严格小于时仍有正余量。剩余量的无除法 numerator 是 `A_min(b-a)²-2(a+b)m`。
- 失败边界：`a=b` 时公共宽度为零，不能保证任何正 reserve；若没有 `A_min>0`，`q≡0` 在任意正宽区间上也是反例；逐行 center 或 pairwise midpoint 也不能替代一个由所有行共同端点检查过的 `[a,b]`。
- 给柳冠一/苏梦辰/巨阳仙尊的建议：最终 checker 可以让不受信任的搜索器只负责提出有理 `a<b`，可信层逐行检查两个端点，然后用 midpoint theorem 直接得到 rational shared theta 和 reserve；这样不必把代数根或 `sqrt` 带进最终证书。Lean 最小叶建议为 `quadratic_midpoint_scaled_identity`、`common_midpoint_uniform_reserve`、`common_midpoint_young_reserve_leftover` 和 `(1,1,3)` sharpness witness。
- 给梁智炜的路由提醒：revision 742 的 `task_queue.md` 将狂蛮魔尊 lane 标为 `T-P4-043`；此前 strict-boundary 数学历史已作为 T-P4-041 文件存在并被 Lean lane 消费，本轮不改旧文件，新增 T-P4-043 作为正确 task-id 下的定量 continuation。
- 关联：`T-P4-039/040/041/042/043`。当前仍为 pending mathematical child；未声称 concrete source、Float64 realized lambda、P8 coverage、P4/M4 closure 或 registry admission。