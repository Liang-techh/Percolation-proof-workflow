---
kind: companion_log
review_id: companion-T-P5-064-analytic-unit-pullback-liuguanyi-20260908T0324
task_id: T-P5-064-ANALYTIC-UNIT-PULLBACK
agent: 柳冠一
source_agent: 柳冠一
created_at: 2026-09-08T03:24:00-06:00
parent_review: review-T-P5-064-analytic-unit-pullback-liuguanyi-20260908T0321
parent_review_commit: cfe49413a024e86c3b282af469797327d095799e
integration_status: pending
admission_label: pending
---

# T-P5-064 中文协作摘要

本轮补上 T-P5-063 明确留下的 `nonconstant analytic-unit transport`：把纯 monomial source map

`h_a=c_a prod_j z_j^(W_aj)`

推广到真正更常见的

`h_a=u_a(z) prod_j z_j^(W_aj)`。

核心结论是：只要 `u_a` 在同一 cell 上有显式固定符号和严格正的 nonvanishing margin，变量 unit **不会改变** aggregate valuation/parity。仍然精确有

`E'=W^T E`，`beta'=W^T beta mod 2`。

所有 unit 的影响都可以吸收到一个正 multiplier `U_E(z)` 中。若 source 给出 exact rational

`0<m_a<=sigma_a u_a(z)<=M_a`

以及 `Lip_1(u_a)<=L_a`，则对任意整数 `E_a`（包括负数）可以机械地产生 exact rational 的 unit 上界、正下界和 Lipschitz 预算。之后直接与 T-P5-062 的 contact monomial budget 组合：valuation/parity gate 不变，只多收一次 unit amplitude/Lipschitz charge。

这条 bridge 的一个重要简化是：trusted theorem 本身不需要 analytic API。analytic factorization 只负责上游证明 exact identity；真正的数学 consumer 只需 same-cell identity、sign bit、`m/M/L` 和整数 exponent matrix。

本轮还给出 sharp obstruction：如果只知道所谓 unit 在 punctured set 上“点点非零”，但没有 uniform lower margin，那么 exponent transport 可以完全失真。最简单例子是把 `u(z)=z` 错当 unit、取 `W=0,E=-1`；形式 transport 会给 `E'=0`，但真实 factor 是 `1/|z|`，直接发散。`E=0,beta=1` 时则会漏掉 `sign(z)` jump。因此任何 unit 的零或换号都必须提升成显式 factor/exponent，不能藏在 `u_a` 里面。

另一个边界是 disconnected source domain：即便 `|u_a|` 有正下界，两个连通分量上的 unit sign 也可能不同。此时要么分 cell，要么把 component sign 作为离散 reachable key 送回 T-P5-061 sign-action 层，不能静默选一个全局 `sigma_a`。

给 source lane 的最小建议：每个 factor 输出 `W_aj`、exact factor identity、`sigma_a`、rational `m_a/M_a/L_a`；每个 consumer 只需输出 aggregate `E,beta` 与 reduced-packet `M_R/L_R`。math adapter 自动算 `E',beta'`、unit budgets 与最终 Lipschitz cap。若只能给 `h=u*z^W+remainder`，暂时不能走本轮 theorem，必须另补 zero-location/domination bridge。

当前仍是 pending mathematical/interface child。deployed CSE factorization、source 坐标独立性、真实 `m/M/L` enclosure、Float64、P8/ODE、Lean/kernel、封不觉独立验证、comparator/admission/registry 均未关闭。