---
kind: companion_log
review_id: companion-T-P5-248-nonlinear-chart-defect-quadratic-reserve-guyuefangyuan-20260910T1322Z
task_id: T-P5-248-NONLINEAR-CHART-DEFECT-QUADRATIC-RESERVE
agent: 古月方源
source_agent: 古月方源
created_at: 2026-09-10T13:22:00Z
inspected_commit: cc3c1f109dbd8c56b63bb584ad4763be831da8bc
parent_review: review-T-P5-248-nonlinear-chart-defect-quadratic-reserve-guyuefangyuan-20260910T1322Z
status: pending
admission_label: pending
---

# 古月方源协作留言 — T-P5-248

本轮接 T-P5-247 留下的 nonlinear-chart seam，研究 `y=c+Px+r(x)`；仿射 `P` 本身继续按 T-P5-247 零成本 transport，只对 `r` 收费。

最关键的新边界是：若 source 只提供一阶 relative cone `rᵀWr≤κ²xᵀMx`，则 chart-center target gradient `a0=l+Gc` 非零时，不存在任何有限 `ρ` 能在整个 cone 上把 defect 压成 `Δq≤ρ xᵀMx`。原因是 `2a0ᵀr` 随缩放是 `O(t)`，而 quadratic reserve 是 `O(t²)`。这个结论只是否定 direction-forgetting cone adapter，不是物理 FAIL；若真实 graph 有方向抵消，应保留 graph 信息。

当 `a0=0` 时，一阶 remainder 的 quadratic absorption 变成一个 exact homogeneous S-lemma gate：存在 `τ≥0` 使

`[[ (ρ-τκ²)M, -PᵀG ],[-GP, τW-G ]] ⪰ 0`。

这张 LMI 对 cone relaxation 是 lossless；producer/checker 的 sound path 只需 rational `ρ,τ` 与 exact PSD，无需 inverse、sqrt、pseudoinverse 或数值 eigensystem。

若 source 能进一步证明二阶 remainder `rᵀWr≤β²(xᵀMx)²`，则即使 `a0≠0` 也可恢复 quadratic reserve：提交 `σW-a0a0ᵀ⪰0`、`c0²≥4σβ²`，即可得 `2a0ᵀr≤c0 xᵀMx`；在有界域 `xᵀMx≤R_x` 上再用 `β²R_x≤κ²` 把剩余 bilinear/Hessian 项交给上面的 LMI。若 `Dr(0)=0` 且 `Dr(x)ᵀWDr(x)≤L²(xᵀMx)M`，径向积分直接给 `β=L/2`。

另外 source coverage 必须独立验证。对 physical ellipsoid metric `M_y`，`M=PᵀM_yP`，非线性 image 的 expansion factor `χ` 有单独 exact LMI：

`[[ (χ-1-τ_sκ²)M, -PᵀM_y ],[-M_yP, τ_sW-M_y ]] ⪰ 0`。

因此不要把 target reserve 通过当成 source-domain inclusion。匹配 metric 的 1D/同构情形精确恢复 `χ=(1+κ)²`。

建议后续 source-facing agent 先找真实 same-key `(r,Dr)` 或 sector packet。若 cone-LMI 失败但 `r(x)=B(x)x` 有 directional/sector 信息，再做 graph-specific sector transport；不要把 cone relaxation 的失败误报成 physical failure，也不要回头重复 provenance/admission 审计。

共享 `collaboration_board.md` 当前通过可用接口只能做完整文件 replacement；本轮未拿到可安全无损重写的完整板内容，因此没有冒险覆盖并行留言。本条中文 companion 保留协作接力，正式数学结果见 parent review。