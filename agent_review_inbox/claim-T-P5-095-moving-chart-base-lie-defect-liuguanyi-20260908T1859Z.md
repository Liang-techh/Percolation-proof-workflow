---
kind: task_claim
task_id: T-P5-095-MOVING-CHART-BASE-LIE-DEFECT
agent: 柳冠一
source_agent: 柳冠一
created_at: 2026-09-08T18:59:00Z
inspected_commit: 8a19cda00777b8abe6c02cc382df74b3f5ad279d
upstream_reviews:
  - agent_review_inbox/review-T-P5-090-moving-metric-contraction-congruence-liuguanyi-20260908T1710Z.md
  - agent_review_inbox/review-T-P5-093-base-flow-lie-defect-honglianmozun-20260908T1758Z.md
  - agent_review_inbox/review-T-P5-094-variational-to-secant-path-energy-guyuefangyuan-20260908T1832Z.md
status: claimed
---

# Claim — T-P5-095 moving-chart base Lie-defect naturality

梁智炜在当前 frontier 中明确将 `T-P5-093-BASE-FLOW-LIE-DEFECT` 的下一步同源 packet 路由给柳冠一或红莲魔尊。红莲魔尊当前已进入 active-V source identity lane，因此本轮认领一个不重叠的最小数学 child：证明 base-flow Lie-defect tensor 在时间依赖/非线性坐标变换下的精确 pullback congruence，并把正确的 vector-field covariance 写成可供 source adapter 消费的 typed mathematical contract。

目标是证明：若 `x=T(t,z)`、`J=D_zT`、pulled metric `M=J^T(W∘T)J`，且 normalized base perturbation `c` 满足 `J c=b∘T`，则 normalized Lie defect

`D_z M[c] + (D_z c)^T M + M D_z c`

精确等于

`J^T (D_xW[b] + (D_xb)^T W + W D_xb) J`。

同时给出错误把 `c` 当成 `b∘T`（忘记 vector-field push/pull factor）时的 exact counterexample，以及 source/checker 所需的最小 same-tube covariance packet。

Out of scope: deployed source binding 本身、Float64/FD/controller/P8、Lean 编译/receipt、provenance/admission/registry 与重复审计。