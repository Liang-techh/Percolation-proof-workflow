---
kind: companion_log
task_id: T-P5-095-MOVING-CHART-BASE-LIE-DEFECT
source_agent: 柳冠一
created_at: 2026-09-08T19:06:00Z
review_file: agent_review_inbox/review-T-P5-095-moving-chart-base-lie-defect-liuguanyi-20260908T1905Z.md
admission_label: pending
integration_status: pending
---

# T-P5-095 中文协作说明

本轮补上了 T-P5-093 明确保留的 moving-chart naturality seam。若 `x=T(t,z)`、`J=D_zT`、`M=J^T(W∘T)J`，物理 base perturbation 为 `b`，normalized perturbation `c` 满足正确的向量场变换 `Jc=b∘T`，则其导数满足

`D_zJ[c] + J D_zc = (D_xb∘T)J`。

将它代入 pulled metric 的方向导数后，所有 nonlinear-chart Hessian/connection 项精确抵消，得到

`D_zM[c] + (D_zc)^T M + M D_zc`
`= J^T (D_xW[b] + (D_xb)^T W + W D_xb) J`。

因此 T-P5-093 的 signed base-flow rate debit `rho` 在正确 pulled metric 下原值 transport，不需要额外 Jacobian condition-number 或 chart-curvature 费用。和 T-P5-090 组合后，完整 perturbed contraction tensor 也满足同一 congruence。

关键接口提醒：不要把 `c` 错写成 `b∘T`。一维 `T(z)=2z, W=1, b(x)=x` 时，正确 `c=z` 给 normalized Lie defect `8`；错误 scalar composition `c=2z` 会给 `16`。因此 base perturbation 必须按向量场而不是标量函数变换。

建议下一步由 source lane 只补一个同 tube packet：`T/J`、`W/DW`、`b/Db`、`c/Dc`，以及 exact `Jc=b∘T`/differentiated covariance。若 source 绑定缺失，应保持 pending，不要用 normalized entrywise absolute bounds 代替 signed physical Lie tensor，也不要把 base-flow mismatch 混进普通 variational residual。

关联 review：`review-T-P5-095-moving-chart-base-lie-defect-liuguanyi-20260908T1905Z.md`。