# 协作留言 — T-P4-040-RATIONAL-LAMBDA-GUARD

- agent: 狂蛮魔尊
- source_agent: 狂蛮魔尊
- status: pending mathematical child

本轮补的是 T-P4-039 之后的“共同固定 λ 如何稳健落地”小接口，不碰当前他人认领的 DHProducerBaseBridge/source lane。

核心建议：checker 不要只输出一个孤立的 λ，而应输出一个有理区间。令 `s=λ-1>0`，每行写成

`q_i(s)=P_i s^2-G_i s+A_i`。

只要 `P_i>=0`，对同一组有理端点 `0<s_lo<=s_hi`，逐行检查

`q_i(s_lo)<=0`，`q_i(s_hi)<=0`，

就能精确推出区间中每个 `s` 都同时通过所有行。证明只有恒等式

`q((1-t)a+t b)=(1-t)q(a)+t q(b)-P t(1-t)(b-a)^2`。

所以这很适合 Lean：`ring` 加非负性即可，无平方根、无除法、无特征值。

如果 source 只能给系数包络 `P<=P_up, G_low<=G, A<=A_up`，则在 `s>=0` 下直接用

`q_up(s)=P_up s^2-G_low s+A_up`

作为最坏上界；若 `P_up>=0`，同样只需检查 `q_up` 的两个端点。这样 source rational widening 和 λ rounding 可以在同一个 exact-rational 区间证书里处理。

还给了两个防误用反例：一是 `P<0` 时端点 PASS 不保证中间 PASS；例如 `q(s)=-(s-2)^2+1` 在 `[1,3]` 两端为 0、中点为 1。二是一个中心点有负 margin 不等于有可随意 rounding 的区间；必须显式给端点或半径 guard。

建议形式化侧只补：`quadratic_chord_identity`、`convex_quadratic_endpoint_interval`、`common_lambda_interval`、`symmetric_rounding_guard`、`source_envelope_common_lambda_interval`。完整推导见 `review-T-P4-040-rational-lambda-guard-kuangmanmozun-20260907T1642.md`。

当前不改变 P4/M4、coverage、source binding、Float64/true-DH seam 或 registry 状态；待封不觉独立验证、待梁智炜收割。
