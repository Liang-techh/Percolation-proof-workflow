---
kind: companion_log
task_id: GH-MATH-P4-BLOCK456-METRIC-CAP
agent: 狂蛮魔尊
source_agent: 狂蛮魔尊
created_at: "2026-09-08T19:38:00Z"
status: mathematical_closure_written_source_binding_pending
---

# 狂蛮魔尊 companion — block-(4,5,6) matching-metric cap

本轮只处理梁智炜点名的 `GH-MATH-P4-BLOCK456-METRIC-CAP`，没有转去做 provenance / admission / receipt，也没有抢 source-reification lane。

数学结论已经压成一个很小的 typed bridge：若 block remainder 有精确 source identity

`r_C = R a_C`

且 source 在同一个固定 metric `H=M0_CC^{-1}` 下给出

`rho2_m0_upper * B_up - R^T H R >= 0`，

那么直接有

`r_C^T H r_C <= rho2_m0_upper * (a_C^T B_up a_C)`。

所以 generic consumer 最紧的自然选择就是

`W(x)=rho2_m0_upper * a_C(x)^T B_up a_C(x)`。

这里没有 condition-number tax，也没有额外 metric-conversion 常数，因为 producer 与 consumer 用的是同一个 `H`。另外 `rho2_m0_upper` 已经是 squared operator cap，绝对不能在 consumer 再平方一次。

当前 block metric 还能 exact 化成

`w1*r4^2 + w2*r5^2 + w3*(r6-r4/7)^2`

其中

`w1=375030000000/(7*5000400003)`，
`w2=4000000/200739`，
`w3=350003000000/5000400003`。

因此 Lean/trusted leaf 可以完全避免显式矩阵求逆。

本轮最重要的反例是：不能把 `rho2_upper` 当成 `rho2_m0_upper`。取 `R a = a e6`，Euclidean squared cap 精确等于 `1`，但同一向量的 matching `H`-energy 系数是

`350003000000/5000400003 > 69`。

所以 metric 类型如果丢掉，实际会少算超过 69 倍。`rho2_bchol_upper` 同理，除非 source 把它对应的输出 metric `J` 明确重建出来，再证明 `H <= kappa J`，否则不能替代 matching cap。

建议 source-reification lane 最终不要把 Cholesky/square-root machinery 暴露给 consumer，而是直接输出一个可核验 PSD witness：

`rho2_m0_upper * B_up - R^T H R >= 0`。

这样 consumer 只剩一行 quadratic-form 推理，完全无根式、无除法、无谱计算。

失败边界也已经明确：若实际 remainder 是 `R a + e`，本 cap 只覆盖 `R a`，额外 `e` 必须进入单独 defect/correlation budget；若 block 顺序不是 `(4,5,6)`，必须同步共轭 metric；若只有 Euclidean/bchol cap 而无 metric comparison，只能标记 matching lane 未闭合，不能硬转成 FAIL 或偷偷复用常数。

当前状态：**数学 child 已得到 conditional pass；source binding 仍 pending。** 没有升级 deployed probe、Lean/kernel、P4 总闭合、registry、admission 或 provenance。
