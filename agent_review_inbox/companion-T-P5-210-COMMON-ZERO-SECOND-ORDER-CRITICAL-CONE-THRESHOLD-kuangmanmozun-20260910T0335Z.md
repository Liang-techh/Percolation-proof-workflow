---
kind: companion_log
task_id: T-P5-210-COMMON-ZERO-SECOND-ORDER-CRITICAL-CONE-THRESHOLD
agent: 狂蛮魔尊
source_agent: 狂蛮魔尊
created_at: 2026-09-10T03:35:00Z
claim_commit: 3474a1b3c2c60adcf1c2bae64b4651f0855ff4f3
review_commit: 8cba2b2fa9bb7fc26803b26833df2c44e6cdc0b3
language: zh-CN
---

# 狂蛮魔尊协作留言 — T-P5-210

本轮接 T-P5-209 明确保留的二阶 critical/tangent 分支，没有重复一阶 residual-contact，也没有转去做 provenance / receipt / admission。

新结论：在候选端点 `H=M(t*)` 与 debit `Q` 都 copositive、同一个 `z>=0` 满足 `z^T H z=z^TQz=0` 时，应定义“双临界锥”

`K={v in T_+(z): (Hz)^Tv=0, (Qz)^Tv=0}`。

在这个锥上，`H` 与 `Q` 的一次项都严格消失，所以自动有 `v^THv>=0`、`v^TQv>=0`。如果能找到

`v^THv=0 < v^TQv`，

那么 `t*` 就是 exact ray endpoint：任意 `s>t*` 下，对足够小的 `eps>0`，`z+eps v>=0` 且其能量精确等于 `-eps^2(s-t*) v^TQv<0`。

这比只要求 `Qz=0` 更一般：即使 `Qz` 在部分 inactive row 上为正，只要二阶方向同时避开 `Hz` 与 `Qz` 的正 residual row，仍然可以走该证书。T-P5-209 负责一阶 residual saturation；本结果负责一阶全部消失后的二阶 saturation。

特别提醒：不能只看 `v^THv=0<v^TQv`。我给了反例 `H=[[0,1],[1,1]]`、`Q=diag(0,1)`、`z=e1`、`v=(-1/2,1)`：两个二次条件成立，但 `(Hz)^Tv=1>0`，候选 `t=0` 实际还能安全延伸到 `t=1`。因此 endpoint-residual criticality 是硬 gate，不是装饰。

在 `Qz=0` 的 T-P5-209 原始 open branch 中，critical cone 固定为 `T_+(z) intersect (Cz)^perp`；每个 `q(v)>0` 的方向给出局部上界 `t<=c(v)/q(v)`。其 block 形式正好就是 T-P5-178/T-P5-180 已有的 signed-active / one-sided-inactive mixed quadratic，不需要新造 cone solver。

建议后续数学路线：若 actual pipeline 真落到该分支，优先做 corank-one critical-block scalarization，把 T-P5-180 的 anchor Schur 与 `(H,Q)` 成对使用，将二阶 contact 压成 bordered determinant / Schur remainder signs。当前 source binding、global copositivity、coverage、Float64、Lean、封不觉验证与 registry 均未升级。