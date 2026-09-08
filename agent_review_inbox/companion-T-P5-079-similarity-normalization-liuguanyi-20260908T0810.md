---
kind: companion_log
review_id: companion-T-P5-079-similarity-normalization-liuguanyi-20260908T0810
source_agent: 柳冠一
created_at: 2026-09-08T08:10:00-06:00
related_review: review-T-P5-079-similarity-normalization-liuguanyi-20260908T0806
related_task: T-P5-079-SIMILARITY-NORMALIZATION
integration_status: pending
admission_label: pending
---

# 柳冠一 companion — T-P5-079 坐标归一化桥

本轮补上了 P5 weighted SCC 的一个跨层接口：若物理坐标与归一化坐标满足

`x=c+Sz`,

且 residual 同步满足

`F_x(c+Sz)=S F_z(z)`,

那么正确的新权重必须是

`W_z=S^T W_x S`。

在这个 contract 下，strong-monotonicity、squared-Lipschitz、root-centered Lyapunov level、anchor residual budget 以及 damped corrector 的步长 `h` 都保持完全相同的标量常数。Jacobian 层同时有

`J_x S=S J_z`,

`A_z=S^T A_x S`,

`H_z=S^T H_x S`,

其中 `A=WJ+J^TW`，`H=J^TWJ`。因此 source 若已经在一个 chart 证明了 T-P5-074/076 的 quadratic-form certificate，不需要在另一个 chart 重新做 eigenvalue/operator-norm 计算。

有两个必须 fail-closed 的边界。

第一，anisotropic state scaling 后若继续使用旧 weight，会改变数学问题。精确例子

`J_x=[[1,1],[-1,1]]`, `W_x=I`, `S=diag(3,1)`

在物理坐标有 `mu=1, Lambda=2`；正确 `W_z=diag(9,1)` 后仍精确保持这两个常数。但若错误地在 z 坐标继续用 `I`，则 `J_z+J_z^T` 在 `(1,1)` 方向给出 `-4/3`，连 monotonicity 都失效。

第二，state 和 residual/output 若用不同 scale，不能把导出的 residual 直接送进 corrector。若

`F_x(c+Sz)=D G(z)`,

则真实 normalized consumer field 是

`Phi=R G`, `S R=D`，

而不是 `G`。这个接口可以完全无除法地保存：对 diagonal scale 只需检查 `s_i Phi_i=d_i G_i`。1D 的 `F_x(x)=x, S=2, D=1` 已经能给出错误步长语义反例。

另一个重要实现提醒：theorem-level congruence 是严格 invariant 的，但 T-P5-076 那种 equal-charge Gershgorin row sufficient certificate 本身不是 tensorial。`H_x=[[2,9/10],[9/10,2]]`, `Lambda=29/10` 在 `S=diag(10,1)` 后 exact congruence 仍成立，但直接对 transformed entries 重跑相同 row test 会在第二行错误失败。正确做法是 transport 已证明的 quadratic form，或使用 scaled Young

`2 s_j s_k |v_j v_k| <= s_j^2 v_j^2+s_k^2 v_k^2`

保留原来的 pair charge。

建议后续 Lean 只先做 `quadraticForm_congruence`、`strongMonotone_similarity_iff`、`sqLipschitz_similarity_iff`、`corrector_step_similarity`、`jacobian_sym_congruence`、`jacobian_gram_congruence` 六个小叶；source lane 再单独绑定真实 `S/c`、same-cell domain map 与 residual covariance。不要把独立 output normalization、非线性 chart 或 time-dependent moving frame 静默塞进这个 affine theorem。

当前状态严格为 `pending mathematical/interface child`；未改变 P5/P8/M4、registry、coverage、Lean/kernel 或 admission 状态。
