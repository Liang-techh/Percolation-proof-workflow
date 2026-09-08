---
kind: companion_log
task_id: T-P5-063-UNDERCANCELLED-AGGREGATE-GATE
agent: 狂蛮魔尊
source_agent: 狂蛮魔尊
created_at: 2026-09-08T02:55:00-06:00
integration_status: pending
---

# T-P5-063 中文协作留言

本轮补了 T-P5-061 明确保留、且 T-P5-062 因逐通道假设 `q>=m` 没有覆盖的 under-cancelled 数学缺口。

核心结论：对一个已经做完 exact CSE 的 consumer monomial，不应该逐通道检查 `q_i-m_i>=0`，而应该先聚合成整数净阶

`E_a=sum_i n_i(q_{i,a}-m_{i,a})`

和总 parity

`beta_a=sum_i n_i q_{i,a} mod 2`。

如果 active factors 在 source cell 里可以独立趋零，那么 universal boundedness 的 exact gate 就是所有 `E_a>=0`；连续/Lipschitz 还要对每个 `E_a=0` 的坐标要求偶 parity（或接 T-P5-061 的 reachable-sign 版本）。负净阶是真 pole，parity 再好也救不了。

但“某一个 channel under-cancelled 就整项 FAIL”是错误规则。精确反例：

`A1=A2=h^4, G1=h, G2=h^3`，

于是 `u1=1/h`、`u2=h`，单看 `u1` 发散，但 exact nonlinear consumer `u1*u2=1`，净阶 `E=0`、总 parity 偶，完全可移除且 Lipschitz 常数为 0。

另外给了 correlated-source rescue 的 exact 接口。若 source 能证明局部 monomial map

`h_a=c_a prod_j z_j^(W_aj)`，

则 trusted math 只需把 valuation/parity 拉回独立 source coordinates：

`E'=W^T E`，`beta'=W^T beta mod 2`。

之后在 `z` 坐标重新应用同一 gate。例子 `h1=z,h2=z^2` 下，factor-space 的 `E=(-1,1)` 虽有负分量，但 `E'=1`，所以实际沿 source domain 是 `|z|` 而不是 pole。反过来，若找到一条 certified rate path `|h_a|=c_a t^(w_a)` 且 `E·w<0`、reduced packet 极限非零，就得到硬无界反例，不必再做数值 enclosure。

需要注意 polynomial sum 仍可能有 exact symbolic cancellation，例如两个 `1/h` 项做差恒为 0；因此 negative-order fail-fast 应作用在 exact CSE/已消费恒等式之后的 canonical monomial 上，不能从采样猜 cancellation，也不能把可证明的 cancellation 强行禁止。

正式数学推导、sharp 反例、pullback theorem、Lean-friendly child statements 已写入：

`agent_review_inbox/review-T-P5-063-undercancelled-aggregate-kuangmanmozun-20260908T0252.md`

当前只标记 pending mathematical child；未声称 concrete source factorization/independence、Float64/controller、P8 coverage、Lean/kernel、P5/M4 或 registry 已闭合。