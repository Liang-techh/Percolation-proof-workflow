---
kind: companion_log
task_id: T-P5-016
review_id: review-T-P5-016-guyuefangyuan-20260907T0538
source_agent: 古月方源
created_at: 2026-09-07T05:40:00-06:00
---

### 2026-09-07 05:40 — 古月方源
- 当前完成：新增 `T-P5-016`，针对 `T-P5-013` 只能得到有限时域 barrier 的根本障碍，构造了 block-(4,5) 的 hypocoercive 交叉项储能。对冻结的 exactized PMI block，可得到完全有理的全状态 coercivity，并在理想无 forcing 情况下得到 `V' <= -(457/800)V`；有加性残差时得到 `V' <= -(457/1600)V + (800/457)||e||^2`，对应无除法 barrier `208849 Vstar > 1280000 Ebar`。
- 发现的问题：`T-P5-013` 的“additive work 只能线性累计”并不是所有 Lyapunov 架构的绝对障碍，而是 kinetic-only storage 缺少配置耗散的结果；只要恢复力块有正 coercivity，就可以用交叉项把位置能转成负 drift。反过来，如果没有恢复力，存在 `v=0,q!=0` 的平衡族，任何 `V'<=-lambda V` 都不可能成立，因此恢复力前提确实是必要的。
- 给其他 Agent 的建议：形式化层若无人认领，可只实现 `block45_hypocoercive_derivative_identity`、`V_lower/V_upper`、`block45_hypocoercive_rate` 与 division-free barrier 四个纯有理 lemma；P4/source lane 不必再强迫所有 remainder 都 velocity-relative，常数型 `l` 也可通过该 ISS 型 consumer 收费，但必须给同域 `||l||^2` 上界。
- 建议的下一步：梁智炜可把本路线作为 P5 的可选 infinite-horizon/ultimate-bound child，不应替代已经编译的 `T-P5-013/015` finite-horizon 主线，除非 exactized block 与真实 source residual 的绑定更容易完成。P8 若继续使用 `w=c t`，还可另开 moving-equilibrium child，用 `h=B^{-1}g=(2340/8699,1520/8699)` 把 `w` 幅值 forcing 换成常数 ramp-rate forcing。
- 关联任务/Review：`T-P5-016`、`review-T-P5-016-guyuefangyuan-20260907T0538.md`、`T-P5-013`、`T-P5-012`、`T-P4-018`、`T-P3-010`。

> 说明：共享 `collaboration_board.md` 当前只能通过“整文件替换”写入，缺少安全的原子 append；仓库历史上已发生过一次追加时截断留言板事故。本轮为避免覆盖并行 Agent 的新留言，没有冒险重写该文件，故先把同样的中文协作信息放入 companion log，供梁智炜下一次收割时安全追加/整合。
