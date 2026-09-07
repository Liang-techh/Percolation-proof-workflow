---
kind: companion_log
task_id: T-P4-016
source_agent: 狂蛮魔尊
created_at: 2026-09-07T03:46:00-06:00
related_review: review-T-P4-016-kuangmanmozun-20260907T0344
---

# T-P4-016 协作摘要

- 给 source/IEEE lane：多个 `DeltaM/DeltaC/DeltaG/delta_ctrl/solveDefect` 增量进入同一 P4 通道时，必须先做总预算；`6/25` 是所有 same-coordinate 项共享的总预算，不是每项各有 `6/25`。
- 给 certificate lane：横向正二次储备必须明确“归谁消费”。若不同 remainder 使用互不重叠的 `H_i`，可用 `KAPPA=sum kappa_i`；若多个 remainder 都拿同一个 `H` 做前提，直接相加 `kappa_i` 是错的，最小反例 `H=1,b1=b2=1,kappa1=kappa2=1` 已足够排除该路线。
- 更推荐的 source 接口：先把各 remainder 的横向坐标斜率按坐标聚合成 `Gamma_j=sum_i gamma_ij`，再一次性计算 `KAPPA=sum_j Gamma_j^2/h_j`；如果能在取绝对值之前直接认证总 remainder 的增量区间，还可能保留真实抵消。
- block 4 在同坐标总系数已经花到 `1/4` 时，所有横向项合计只能共享 `583338333333335*KAPPA <= 37503000000001`，不能让每项各自拿满右端预算。
- 给形式化 lane：最小新 theorem 是 finite/two-term reserve Cauchy composition 加 shared-reserve counterexample；随后直接复用现有 `T-P4-014` Schur consumer，不要重写整套 P4。
