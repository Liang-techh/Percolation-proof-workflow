---
kind: companion_log
task_id: T-P5-091-VARIATIONAL-DEFECT-ROBUST-CONTRACTION
review_id: review-T-P5-091-variational-defect-robust-contraction-guyuefangyuan-20260908T1730Z
source_agent: 古月方源
created_at: 2026-09-08T17:33:00Z
integration_status: pending
---

# T-P5-091 中文协作接力

本轮接 T-P5-090 明确留下的“variational dynamics 含 defect/noise”数学缺口，完成的是连续微分 contraction 的鲁棒层，不重复 T-P5-087 的 Euler curvature defect，也不重复 T-P5-088/089 的 state-storage / mechanical-energy 路线。

核心结论：若 nominal moving-metric contraction 给出 `C >= 2 mu W`，变分方程为 `xidot=-A xi+e`，则精确有

`Vdot <= -2 mu V + 2 <xi,e>_W`，其中 `V=xi^T W xi`。

若 relative defect 满足 `Q_W(r)<=rho^2 V`，则无需开方即可推出 `<xi,r>_W<=rho V`，contraction rate 精确损失为 `mu-rho`。若 relative defect 是 `r=Rxi`，更建议 source 直接证明 signed symmetric power

`xi^T(WR+R^TW)xi <= 2 rho V`，

不要先对 `R` 做 operator norm/逐项绝对值；纯 skew defect 在能量里可以完全零收费，即使 `||R||` 任意大。

更实用的是 mixed defect `e=r+d`。令 `nu=mu-rho>0`，若 `Q_W(d)<=Ebar`，由 `Q_W(nu xi-d)>=0` 可完全无除法地得到

`nu Vdot <= -nu^2 V + Ebar`。

所以候选能量边界只需 exact 检查

`Ebar <= nu^2 Vstar`

即可推出 `V=Vstar` 上 `Vdot<=0`。真正的 forward invariance 只差标准 first-exit/barrier + same-tube coverage，不需要 sqrt 或求 `Ebar/nu^2`。一维 aligned 模型会精确达到 `Vstar=Ebar/nu^2`，因此这个阈值在该信息层上是 sharp 的。

本轮还给出 moving-chart 的无损 defect transport：若 T-P5-090 的 chart 满足 `M=J^T W J`，物理/归一化 defect 只需有 forward covariance `J e_z=e_x`，则 defect energy 和 cross power 都精确保持：`Q_M(e_z)=Q_W(e_x)`、`<eta,e_z>_M=<xi,e_x>_W`。因此 `mu/rho/Ebar/Vstar` 无需乘 Jacobian condition number，也不需要写 `J^{-1}`。operator route 若有 `J R_z=R_x J`，signed symmetric defect 同样精确 congruence。

硬 obstruction 也已记录：bounded additive defect 不能推出向零严格 contraction。标量 `xidot=-mu xi+epsilon` 已有非零平衡点 `epsilon/mu`，而且小正 `xi` 区域 `Vdot>0`。所以 additive lane 的正确结论必须是 invariant/ultimate tube，除非 defect 随 `xi` 消失。

给 Lean lane 的建议：优先做 `scaled_cross_young_sq`（`2*lambda*cross <= lambda^2*V+E`）和 `robust_contraction_mixed_defect_sq`，这两条纯代数、square-only，之后再补 `defect_power_pullback` / `defect_energy_pullback`。给 source/CSE lane 的建议：relative operator defect 先形成 signed `WR+R^TW` 再 enclosure；additive defect 直接输出同 metric 的 squared budget `Ebar`。

当前仍 open：真实 deployed variational defect split、same-tube `(mu,rho,Ebar,Vstar)`、metric coercivity、first-exit/coverage、base-flow perturbation、stochastic noise、finite-separation/secant contraction、Float64/FD/controller、P8/ODE、Lean/kernel、封不觉独立验证与 admission/registry。

共享 `collaboration_board.md` 目前通过可用 GitHub contents 写接口只能整文件替换，且读取结果会被截断；为避免覆盖其他并行 Agent 的历史留言，本轮没有冒险重写留言板。上述中文协作建议已完整持久化在本 companion，供梁智炜安全收割后追加。
