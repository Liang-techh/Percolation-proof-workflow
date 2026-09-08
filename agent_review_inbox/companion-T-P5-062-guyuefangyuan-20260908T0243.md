---
kind: companion_log
review_id: companion-T-P5-062-guyuefangyuan-20260908T0243
task_id: T-P5-062-MULTIFACTOR-LIPSCHITZ-STRATA
agent: 古月方源
source_agent: 古月方源
created_at: 2026-09-08T02:43:00-06:00
parent_review: review-T-P5-062-guyuefangyuan-20260908T0240
parent_review_commit: 2482fb59eefbf29adb58b5428fa7898151aacdb3
integration_status: pending
admission_label: pending
---

# T-P5-062 中文协作摘要

本轮补上 T-P5-061 明确留下的“多因子消去以后，怎样得到真正的 cell 级 Lipschitz 余量”问题，并发现一个需要 source/P5 lane 特别注意的结构性陷阱：**在最高余维交点上趋于 0，不代表整个邻域 cell 连续。**

对一个 canonical monomial，把所有 radical channel 的因子数据合并成 excess order `e_a` 和 parity mask `beta_a`。若 cell 能覆盖全部 sign chambers，则整个 monomial 跨所有部分零面可 Lipschitz 延拓，当且仅当每个 `e_a=0` 的因子都满足 `beta_a=0`。也就是所有仍为奇 parity 的 sign 必须落在至少有一次正 excess 的“被阻尼因子”上。通过后可直接给出纯有理 `l1` Lipschitz 常数 `max_a e_a H_a^(e_a-1) prod_{b!=a} H_b^(e_b)`。

最关键的负控是 `A=s^2 t^2, G=s^2 t`，所以 `u=|s| sign(t)`。当 `(s,t)->(0,0)` 时它确实趋于 0，因此只看最深 contact 会判为 removable；但固定任意 `s!=0` 再跨 `t=0`，左右极限是 `±|s|`，整个 box 实际不连续。这说明以后不能把“某个 active factor over-cancelled”直接升级成 whole-cell regularity，必须检查所有 partial strata，或者一次性用本轮的 excess/parity gate。

若 source domain 只允许部分 sign chambers，则可放宽：只要任意两个输出 parity 不同的 reachable chambers，至少有一个正 excess 因子的 sign 也不同，就仍有同一个 Lipschitz bound。若用 T-P5-061 的 chamber-complete subgroup `H` 表示，这个条件等价于 `beta in H^perp + U_P`，其中 `U_P` 是所有正 excess 坐标生成的子空间。balanced 情形 `P=empty` 自动退回 T-P5-061 的 `beta in H^perp`；full box 情形则退回 `supp(beta) subseteq P`。

给 source lane 的建议：在继续做 reduced Jacobian/interval 常数之前，先对每个实际消费 monomial 输出 `(e,beta)`，并按真实 cell 的 reachable chamber/subgroup 跑这个结构 gate。若失败，优先 split 对应零面、证明 sign restriction，或寻找 exact aggregate cancellation；不要先花大量算力收紧数值区间。给 Lean lane 的建议：先形式化一维 `|x|^e` 与 `x|x|^(e-1)` 的 box Lipschitz，再做有限乘积；subgroup 版本最后只需要 XOR/有限 bit-linear arithmetic，不必先引入完整群表示。

当前仍为 pending mathematical child。真实 source factor packet、`Omega/H` reachability、reduced packet bounds、Float64、P8/ODE、Lean/kernel、封不觉验证和 admission 均未关闭。
