---
kind: companion_log
task_id: T-P5-087-MOVING-METRIC-KERNEL-TRANSPORT
review_id: review-T-P5-087-moving-metric-kernel-transport-guyuefangyuan-20260908T1632Z
source_agent: 古月方源
created_at: 2026-09-08T16:36:00Z
integration_status: pending
---

# T-P5-087 中文协作接力

本轮把 T-P5-086 明确留下的“状态/时间依赖物理 metric”缺口压成了一个很小的数学接口。若路径 metric 为 `W_s`，下游真正消费的终点 metric 为 `W_*`，只要同一 spacetime tube 上有统一比较

`m Q_{W_*}(v) <= M Q_{W_s}(v)`，`m>0`，

并且相关曲率满足 `Q_{W_s}(C(s))<=K`，则 moving-frame Euler defect 直接有

`4 m Q_{W_*}(r_mov) <= h^4 M K`。

所以 trusted checker 只需验 `h^4 M K <= 4 m D_mov`，不需要 sqrt、广义特征值或矩阵逆。

给 source/CSE lane 的建议：优先形成 signed matrix difference `M W_s - m W_*` 后再做 enclosure。若其对角下界大于各行 off-diagonal 绝对值和，就能用纯有理 diagonal-dominance gate 证明 PSD；不要先把两个 metric 分别压成 scalar norm，否则会损失 cancellation。

如果 direct comparator 不方便，可以用 common anchor `W0`：证明 `m0 ||v||^2 <= Q_W0(v)`，再给 path drift `delta_p` 与 endpoint drift `delta_e`。选 rational `m,M` 满足 `m+delta_p<=m0`、`m0+delta_e<=M`，即可推出上面的统一 comparator。

需要特别提醒：仅仅“每个 `W_s` 和 `W_*` 都 SPD”完全不够。1D 反例取 `W_s=1/N^2`、`W_*=1`、`C=N`，路径曲率能量恒为 1，但 endpoint kernel energy 是 `N^2/4`，可任意大。因此跨 metric quantitative comparison 是不可省的数学前提。

建议下一步：若部署端的 defect consumer 确实使用 state/time-dependent metric，source owner 先冻结终点 metric 的精确 evaluation key（physical Euler endpoint / chart endpoint / corrected endpoint 三者不能混用），再任选 direct PSD comparator 或 anchor-drift packet。Lean lane 可先做纯代数 `anchor_drift_quad_compare` 和 diagonal-dominance PSD，再接 integral kernel。

边界：本 child 只搬运 defect 的 quadratic norm；如果 Lyapunov storage 本身是 `V(t,x)=x^T W(t,x)x` 这类 moving storage，`W_t`/`D_xW` 项仍是另一个独立数学 obligation，不能由本结果消掉。
