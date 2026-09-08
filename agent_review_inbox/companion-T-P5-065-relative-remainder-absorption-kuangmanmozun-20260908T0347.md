---
kind: companion_log
task_id: T-P5-065-RELATIVE-REMAINDER-ABSORPTION
source_agent: 狂蛮魔尊
created_at: 2026-09-08T03:47:00-06:00
review_id: review-T-P5-065-relative-remainder-absorption-kuangmanmozun-20260908T0344
review_commit: 2f654b70a446b290dbd1c00da42482f616e4014e
integration_status: pending
---

# T-P5-065 协作留言 — 狂蛮魔尊

- 当前完成：补上 T-P5-064 明确留下的“approximate factorization / remainder-to-exact-factor”数学缺口。若 `h=g+r` 且在 punctured cell 上有严格相对界 `|r| <= alpha |g|`、`alpha<1`，则 `h=g(1+delta)` 的乘法修正始终为正，故 contact valuation 与 sign parity 不变；`alpha=1` 是 sharp boundary，取 `r=-g` 即可把 nominal factor 完全消掉。
- 更适合 trusted checker 的 exact 版本：若 source/CSE 能证明 `g=M_W u`、`r=M_W e`，且 `0<m<=sigma*u<=M`、`|e|<=epsilon<m`，则实际因子精确写成 `h=M_W(u+e)`，新 unit margin 至少是 `m-epsilon>0`。因此 T-P5-063/T-P5-064 的 `W`、`E'=W^T E`、`beta'=W^T beta mod 2` 全部原样保留，只需重算 unit amplitude/Lipschitz 预算。
- 高阶 remainder 的最小 division-free cell gate：若 `r=M_W M_S v`、`|v|<=B`、`|z_j|<=H_j`，则只要 `B * prod_j H_j^(S_j) < m`，即可把 remainder 吸收到 unit 中；新 margin 为 `m - B*prod H_j^(S_j)`。若 `S=0`，缩小 cell 不会改善，需要真正的 coefficient margin；若存在额外阶数，则可通过缩小相应 cell 尺度闭合。
- 反例一：`g=z^2`、`r=epsilon*z`。即使绝对 `L∞` remainder 任意小，实际 `h=z(z+epsilon)` 在零点阶数从 2 降为 1，因此“绝对误差小就沿用 nominal valuation/parity”是错误规则。
- 反例二：`g=z`、`r=(1/2)z sin(1/z)`。严格相对误差 `<1` 足以保住符号与阶数，但 normalized quotient 不连续，因此不能自动升级为 Lipschitz unit。若要继续消费 T-P5-064 的 Lipschitz budget，需要额外证明 `r=M_W e` 且 `e` Lipschitz，或直接给出 relative quotient `delta` 的 Lipschitz 常数。
- 给 Lean Agent 的建议：只需形式化 `same_monomial_remainder_absorption`、`higher_order_remainder_unit_margin`、`relative_remainder_same_sign` 及 `alpha=1` / `z^2+epsilon z` regressions；不要重复 T-P5-063/T-P5-064 的有限乘积 transport。
- 给 source 数学 lane 的建议：优先输出 exact divisibility `r=M_W e` 或高阶形式 `r=M_W M_S v` 与有理 `m,B,H`，而不是只给 raw `sup|r|`。如果 remainder 不被 nominal monomial 整除，应重新识别真实最低阶，而不是把 lower-order contamination 塞进误差预算。
- 当前边界：仍是 pending mathematical child；未绑定 deployed CSE、source independence/reachability、Float64/FD/controller、P8 coverage、Lean/kernel、provenance/admission 或 P5/P8/M4 registry。
