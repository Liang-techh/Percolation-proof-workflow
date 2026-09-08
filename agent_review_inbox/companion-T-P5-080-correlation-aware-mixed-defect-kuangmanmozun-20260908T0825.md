---
kind: companion_log
task_id: T-P5-080-CORRELATION-AWARE-MIXED-DEFECT
agent: 狂蛮魔尊
source_agent: 狂蛮魔尊
created_at: 2026-09-08T08:25:00-06:00
status: pending_math_child
review_commit: 91b6d1064d8f63a9ce8374006815cb39e07ccc8a
---

# T-P5-080 中文协作说明

本轮补上 T-P5-078 明确留下的 correlation boundary：如果真实 source 能在同一 weighted quadratic form、同一 source cell 上证明 signed inner-product，而不只是三个彼此独立的 norm envelope，那么 corrector 的 evaluator defect 可以得到严格更强、且完全无根式的 closure。

相对误差部分，若 `Q(a)<=qV`、`Q(e_r)<=KV` 且 `<a,e_r>_W>=gamma V`，则 `b=a-h e_r` 精确满足

`Q(b) <= (q-2h gamma+h^2K)V`。

因此有效因子直接是 `kappa_corr=q-2h gamma+h^2K`。例如 `q=K=1/4,h=1` 时，独立 norm envelope 的最坏因子是 1，只能到 boundary；若 source 额外证明 `<a,e_r>>=0`，则因子立刻降到 `1/2`。正交有理 witness `a=(1/2,0), e_r=(0,1/2)` 精确达到 `1/2`。反之，同样的 norm envelope 也允许 `e_r=(-1/2,0)`，此时因子回到 1，所以“采样看起来正交/同向”绝不能替代 cell-uniform signed theorem。

持续 additive defect 也可保留 signed cross 信息。若 `Q(e_0)<=E1 V+E0` 且 `<b,e_0>_W>=-(J1 V+J0)`，则一步更新满足纯 affine energy recurrence

`Q(d_plus) <= A V+B`,

其中 `A=kappa_corr+2hJ1+h^2E1`，`B=2hJ0+h^2E0`。因此 strict invariant level 的 rational gate 只是 `0<=A<1` 与 `B<(1-A)Vstar`；候选 asymptotic floor 也只需检查 `B<=(1-A)Vfloor`，不需要除法或平方根。

若 source 还没显式形成 `b`，可以由 `<a,e_0>` 的下界和 `<e_r,e_0>` 的上界直接得到 `<b,e_0>` 下界。因此建议和 T-P5-076 一样：先形成 signed weighted Gram/cross terms，再做 enclosure；不要过早逐项取绝对值。

当前仍是 pending mathematical child。没有声称 concrete deployed correlation packet、source binding、Float64/FD/controller、P8 coverage、Lean/kernel、admission 或 registry 已闭合。若没有 signed source theorem，下游必须继续使用 T-P5-078/T-P5-075 的 independent-envelope sharp gate，不能擅自升级。