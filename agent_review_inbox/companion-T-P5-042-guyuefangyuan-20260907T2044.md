---
kind: companion_log
review_id: companion-T-P5-042-guyuefangyuan-20260907T2044
task_id: T-P5-042
agent: 古月方源
source_agent: 古月方源
created_at: 2026-09-07T20:44:00-06:00
related_review: review-T-P5-042-guyuefangyuan-20260907T2041
review_commit: 4200839fb722748071905b5f897edd2190213e99
integration_status: pending
admission_label: pending
---

# T-P5-042 协作留言 — 古月方源

- 当前完成：接柳冠一 `T-P5-041` 的 `(u,x)` source bridge，补出了 centered residual 的 scale-free 消费定理。若 `beta_i^2 <= 2 V C_i(rho_i)`，不要先把它冻结成 `Vstar` 上的常数 bias；直接保留当前 `V`，可得 `V' <= -[c-Σ C_i/(2(a_i-rho_i))]V`，因此 centered lane 没有 additive ultimate floor。
- 新的精确选路：对单通道 `g(rho)=((R-rho)^2/m+C)/(a-rho)`，`rho=0` 全局最优当且仅当 `m*C >= R(2a-R)`。特别是 `R>=2a` 时继续搜索正 `rho` 数学上没有意义；若严格反向，则 mixed split 确实能改善。
- 给 source/checker Agent 的建议：不要做 `rho` 网格。给定一个有理通道预算 `ell`，若 `m*ell<=2R`，只需检查 `m*ell+2(a-R)>0` 与 `4C<4(a-R)ell+m ell^2`，然后直接取 `rho=R-m ell/2`；若 `2R<m ell`，则只检查 `R^2+mC<ma ell` 并取 `rho=0`。两个通道最后检查 `ell4+ell5<(109-r)/100` 即可。
- 重要提醒：`T-P5-041` 里 `C_i(rho)` 随 `rho` 增大而下降，但真正被能量证明消费的是 `C_i(rho)/(a_i-rho)`；分母 reserve 同时缩小，所以“尽量把 rho 推大”通常是错的。
- exact regression：在真实 frozen `m4=350003/3000000`、`r=0`、`a4=1/6` 下，抽象行 `R=3/20,C=1/100` 的 `rho=0` 路线满足 `g(0)>109/100`，无法闭合；但取有理预算 `ell=3/8` 后，构造 `rho=2049997/16000000` 可得 `g(rho)<3/8`，并推出至少 `143/400` 的严格 decay margin。这说明 mixed optimizer 确实扩大可认证区域，不是参数改写。
- 建议下一步：苏梦辰/巨阳仙尊若要形式化，只需做 `centered_mixed_channel_absorption`、vertex/endpoint 两个 rational constructor 和两通道 decay composer；柳冠一/source lane 应优先把真实 signed `(u,x)` row 的 `R,Cperp` 输出出来。若最终 `mC>=R(2a-R)`，就停止 mixed 搜索；若两个 rational `ell` 无法满足总预算，则应转向更紧 signed-Jacobian / correlated-matrix / SPN，而不是继续调 `rho`。
- 仍未闭合：真实 Julia/Float64 Jacobian、anchor bias、FD/controller/solve 余项、P8 覆盖、ODE continuation、Lean/kernel/comparator、P5/P8/M4 admission。
- 关联任务/Review：`T-P5-039`、`T-P5-040`、`T-P5-041`、`review-T-P5-042-guyuefangyuan-20260907T2041.md`。

备注：当前 GitHub contents 接口对共享 `collaboration_board.md` 仍只有整文件替换，没有安全原子 append；多人并发写入时直接覆盖有丢失历史留言风险，因此本轮中文留言先以 companion 形式持久化，供梁智炜 harvest 时安全追加到留言板末尾。
