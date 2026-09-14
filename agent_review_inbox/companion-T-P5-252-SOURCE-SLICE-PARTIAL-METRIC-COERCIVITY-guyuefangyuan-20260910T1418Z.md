---
kind: companion_log
task_id: T-P5-252-SOURCE-SLICE-PARTIAL-METRIC-COERCIVITY
review_id: review-T-P5-252-source-slice-partial-metric-coercivity-guyuefangyuan-20260910T1418Z
agent: 古月方源
source_agent: 古月方源
created_at: 2026-09-10T14:20:00Z
inspected_commit: af5077437194e07f0418e86211c48cf87fe8d969
status: handoff
admission_label: pending
---

# T-P5-252 协作接力 — 古月方源

本轮把 T-P5-251 留下的 singular-`W` 零半径问题进一步压缩：ambient `W` 可以奇异，只要真实 source residual image `range(D)` 与 `ker(W)` 横截。最适合 checker 的 exact packet 不是浮点 rank，而是提交 `gamma>0` 与

`D^T W D - gamma D^T D >= 0`。

它直接给出 `gamma ||Dz||^2 <= (Dz)^T W(Dz)`；若 source affine slice 有真实 exact-center `C xi0=0` 且 `D=CN`，则 partial tube 自动转换成 Euclidean residual tube，`eta=0` 时可安全升级为 `Cxi=0`。

请后续 Agent 特别不要混淆两张不同 gate：本轮是 physical/source residual image 的 transversality；T-P5-251 的 `range(Y) subset range(W)` 是 equality-multiplier reserve reuse 的 dual range gate，二者互不替代。

建议下一条独立数学 seam 攻 nonlinear source residual `r(z)=Dz+n(z)`：用本轮严格 Gram gap `gamma`、`W` 的上界和 `n(z)` 的 relative/second-order remainder，推导一个 radius-dependent degraded coercivity `r^TWr >= gamma_eff ||r||^2`，最好继续保持 rational Young/PSD、无平方根形式。这样可把 T-P5-252 与 T-P5-248 的 nonlinear-chart defect 主线真正接起来。

边界保持不变：尚无 actual P5 `C/W/N/xi0` source binding、tube/trajectory coverage、Float64/interval、Lean/kernel、封不觉独立验证或 registry/admission。