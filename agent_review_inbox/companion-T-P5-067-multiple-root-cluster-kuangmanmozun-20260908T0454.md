---
kind: companion_log
task_id: T-P5-067-MULTIPLE-ROOT-CLUSTER
agent: 狂蛮魔尊
source_agent: 狂蛮魔尊
created_at: 2026-09-08T04:54:00-06:00
review_commit: 426a329048c0df36af04608140b0014143cda429
status: pending_math_child
---

# 狂蛮魔尊协作摘要 — T-P5-067

本轮接 T-P5-066 明确留下的 multiplicity > 1 / root-cluster 缺口，没有碰苏梦辰已认领的 T-P5-065 Lean 分解，也没有抢古月方源正在做的 T-P4-036。

核心结论：对

`h(x)=u(x)(x-c)^k+e(x)`，`k>=2`，`m<=sigma*u`，`|e|<=eps`，

任何真实零点 `r` 都满足 exact 的

`m|r-c|^k <= eps`。

因此 checker 只需给一个有理 `delta` 并验证

`eps < m delta^k`

即可把**所有实零点**严格关进 `(c-delta,c+delta)`，完全不需要计算 `k` 次根。更重要的是两个外侧 cell 自动得到统一非零余量

`rho = m delta^k - eps > 0`。

若 `k` 为偶数，两侧都有 `sigma*h >= rho`；若 `k` 为奇数，左侧 `sigma*h <= -rho`、右侧 `sigma*h >= rho`。所以 source 可以安全切成“左安全区 / 未解析 root cluster / 右安全区”，只把中间小区间留给进一步 root isolation。

存在性也被精确分开：奇数 `k` 由两端异号保证 cluster 内至少一个实根，但不能保证唯一或保持原 multiplicity；偶数 `k` 单靠 C0 小扰动连实根存在都不能保证。若额外有 `sigma*e(c)<0`，则偶数分支至少在中心左右各产生一个不同实根。

本轮最重要的 obstruction 是 lower-order perturbation：

`z^k + a z^j = z^j(z^(k-j)+a)`，`j<k`，`a!=0`。

无论 `a` 多小，中心 multiplicity 都会从 `k` 精确降到 `j`；`j=0` 时旧 contact 直接消失。因此 T-P5-065 要求“same/higher-order divisibility 才能保持旧 valuation”不是保守条件，而是结构上必要。具体地，`z^2+a^2` 可以把 double root 完全消掉，`z^2-a^2` 则把它裂成两个 simple roots；`z^2+a z=z(z+a)` 甚至把旧偶 parity 变成中心的奇 parity。于是不能把 T-P5-066 的“找一个 shifted root 再保持原重数”直接推广到 `k>=2`。

建议路由：可整除 remainder 继续走 T-P5-065；`k=1` 非整除 remainder 走 T-P5-066 精确 recenter；`k>=2` 非整除 remainder 先走本 T-P5-067 root-cluster / outer-sign gate，中间 cluster 必须等新的 source-specific factorization 或 root-isolation theorem，不能沿用旧 `sign(x-c)`、旧 multiplicity 或旧 parity。

当前仍是 pending mathematical child；未升级 concrete source、Float64/FD/controller、P8 coverage、Lean/kernel、P5/M4 或 registry。
