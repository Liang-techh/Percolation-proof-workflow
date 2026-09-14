---
kind: companion_log
task_id: T-P5-188-RESIDUAL-STRATUM-CANONICAL-COMPRESSION
agent: 狂蛮魔尊
source_agent: 狂蛮魔尊
created_at: '2026-09-09T21:37:00Z'
status: mathematical_closure_written_source_binding_pending
---

# 狂蛮魔尊协作记录 — T-P5-188 residual-stratum canonical compression

本轮已先读取 `README.md`、`task_queue.md`、`collaboration_board.md` 和最新消息。梁智炜此前点名我的 `GH-MATH-P4-BLOCK456-METRIC-CAP` 已有正式结果与 companion，因此没有重复认领；最新 T-P5-185/186/187 也分别由红莲魔尊、柳冠一、古月方源完成，本轮没有抢占。

本轮接 T-P5-187 的 residual uniqueness 往前推进一小步：对固定 external direction，若 `P=P^T>=0` 且已有一个 KKT minimizer `y`，令唯一 residual `r=Py+b`，再分

`I={i:r_i=0}`，`J={j:r_j>0}`。

则全部 orthant minimizer 精确等于

`z_J=0, z_I>=0, P_II z_I=-b_I`。

最关键的新桥是：PSD 下，如果一个只支撑在 `I` 的向量满足 `P_II d_I=0`，那么它的 full quadratic energy 也是 0，因此自动有 `Pd=0`。所以 reduced principal system 的任意两个解虽然可能因 singular kernel 不同，但这种差异绝不会偷偷改变 `J` 上的 residual。由此，一个固定方向上的多个 overlapping active-face representatives 可以压成同一个 zero-residual affine slice，不需要两两 seam 比较。

精确 affine 形式是

`M={(y_I+k,0_J): k in ker(P_II), y_I+k>=0}`。

因此 `P_II>0` 时 minimizer 唯一；`P_II` singular 时全部非唯一性就是这个 kernel gauge 与 orthant 的交。注意 `I` 只是“允许 active”的 canonical zero-residual set，不等于每个 minimizer 的真实 support，不能把两者混写。

失败边界也已钉死：仅有 copositivity 不够。取 `P=[[0,1],[1,0]]`、`b=(0,1)`，整个 orthant 上 `f=2*x2*(x1+1)>=0`，所有 `(t,0)` 都是 global minimizer，但 residual 是 `(0,t+1)`，会随 `t` 变化；同时 principal zero-kernel 也不会 lift 成 full kernel。因此 T-P5-188 必须保留 ordinary PSD 前提。

当前仍是 `CONDITIONAL_PASS_MATHEMATICAL_CHILD / pending source binding`。没有升级 source、external-cone coverage、Float64/interval sign、Lean/kernel、封不觉验证、admission、registry 或 P5/P8/M4 parent closure。

建议下一数学 child 只在需要时做 `residual-stratum stability under varying external direction`：给出 exact cone inequalities，证明一整个 polyhedral cone 内 `r_J(e)>0`、`r_I(e)=0` 的 sign stratum 保持不变，从 pointwise compression 推到 cone-wise compression。