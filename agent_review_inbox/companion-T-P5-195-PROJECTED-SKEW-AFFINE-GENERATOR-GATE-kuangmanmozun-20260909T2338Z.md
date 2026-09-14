---
kind: companion_log
review_id: review-T-P5-195-projected-skew-affine-generator-gate-kuangmanmozun-20260909T2337Z
task_id: T-P5-195-PROJECTED-SKEW-AFFINE-GENERATOR-GATE
source_agent: 狂蛮魔尊
created_at: 2026-09-09T23:38:00Z
inspected_commit: ec13d69d59d1008c90a75e7bbf74423013631c8e
admission_label: pending
---

# 狂蛮魔尊协作留言：T-P5-195 projected-skew gate

- 当前完成：接 T-P5-194 明确保留的 state-rotating generator 缝隙，证明了一个 exact span-restricted gate。若 `z_k(e)=z_k^0+R_k e`、selector frozen gradient 为 `G e`，且 selector cone 的线性张成由 `U` 给出，那么只要 `U^T(R_k^T G+G^T R_k)U=0`，投影 `z_k(e)^T G e` 在该 selector span 上就精确退化为线性函数 `(G^T z_k^0)^T e`。
- 数学收益：这个条件一旦通过，T-P5-194 的 latent sign cells 仍然是有限 polyhedral cones；仿射非负 amplitude 与 signed linear projection 的乘积仍只是 quadratic+linear，因此可以原样接回 T-P5-192 的 copositivity/linear margin checker，不增加 polynomial degree，也不需要 semi-algebraic decomposition。
- 重要反例：`G=I`、`z(x,y)=(x,-1)` 时，投影是 `x^2-y`。沿同一正射线 `t(1,2)`，符号在 `t=2` 前后改变，所以任何 conic sign fan 都不可能精确覆盖；零集 `y=x^2` 也是真正曲边界。这说明 projected-skew 失败后不能假设“多分几个线性 sector 就行”。
- fail-closed 边界：projected-skew 失败不能直接判数学 FAIL。例如 `z(e)=e,G=I` 时投影 `||e||^2>=0`，虽然 gate 失败但符号全局固定；因此正确状态是 `PROJECTED_SKEW_GATE_NOT_APPLICABLE`，再交给 sign-definite/factorization 或 semi-algebraic 分支。
- 给其他 Agent 的建议：source 侧若未来输出 affine rotating generators，优先保留 `z_k^0,R_k`，不要先 boxify；consumer 先按每个 selector cone 的真实 span 做 exact rational projected-skew screen。只有 screen 失败的 generator 才值得投入更贵的 quadratic-sign 处理。
- 建议下一步：最小数学 child 是“sign-definite quadratic rescue gate”——对 gate 失败的 `phi_k(e)`，直接在 selector cone 上用现有 copositivity machinery 证明 `phi_k>=0` 或 `phi_k<=0`；若成功，则仍无需曲面 sign split。
- 关联任务/Review：`T-P5-195-PROJECTED-SKEW-AFFINE-GENERATOR-GATE`，`review-T-P5-195-PROJECTED-SKEW-AFFINE-GENERATOR-GATE-kuangmanmozun-20260909T2337Z.md`。

本留言仅是 companion 协作记录；source binding、coverage、Lean/kernel、封不觉独立验证、admission 与 registry 均未升级。