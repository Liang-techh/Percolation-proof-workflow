---
kind: companion_log
task_id: T-P5-262-RATIONAL-AMGM-METRIC-BRIDGE
source_agent: 古月方源
created_at: 2026-09-10T16:55:00Z
review_commit: 7a684d6d780bc287bd62ffab96d4db3897767851
status: pending
admission_label: pending
---

# 古月方源 — T-P5-262 协作记录

本轮承接狂蛮魔尊 T-P5-261 明确保留的 mixed-metric polarization seam，没有转做 provenance、receipt、admission 或重复验证。

## 当前完成

对两个同 quotient 上的 SPD metric `M,W`，以及 homogeneous quadratic vector map `F` 的 canonical symmetric factor `A_sym`，若真实 radial packet 已经证明

`||F(u)||² <= κ (uᵀMu)(uᵀWu)`，

则对任意 `t>0` 定义

`J_t=t²M+W`，

存在完全无平方根的恒等式

`(uᵀJ_tu)² - 4t²(uᵀMu)(uᵀWu)`

`= [t²(uᵀMu)-(uᵀWu)]² >=0`。

因此可以先把 mixed radial quartic 嵌入单一 matched metric `J_t`，调用 T-P5-261 的 lossless canonical polarization，再把结果送回原始 metric。

若提交 rational `p,q` 满足

`J_t <= pM`, `J_t <= qW`，

则严格得到

`A_sym(u)ᵀA_sym(u) <= κ [pq/(4t²)] (uᵀMu) W`。

所以 actual checker 只需要 rational `(t,p,q,C)`，验证

`pM-J_t >=0`, `qW-J_t >=0`, `pq<=4t²C`。

不需要 matrix square root、geometric mean、SVD、pseudoinverse 或 floating generalized eigensystem。

## 相比旧 budget 的改进

如果当前只知道

`αW <= M <= βW`, `0<α<=β`，

则可以取

`p=t²+1/α`, `q=βt²+1`，

得到 distortion

`C(t)=[βt²+1+β/α+1/(αt²)]/4`。

这条 bridge family 的最优实数 infimum 是

`C_*=[(1+sqrt(β/α))/2]²`，

优化条件为 `t⁴=1/(αβ)`。

只要 `β>α`，就有严格改进

`C_* < β/α`。

因此 T-P5-261 的 `β/α` 可以保留作最便宜 fallback，但预算敏感时应先试本轮 rational bridge。

## Exact rational regression

取 T-P5-261 的 mismatch 例子

`W=I`, `M=diag(1,1/16)`，

则 `α=1/16, β=1`。旧 condition-ratio factor 是 `16`。

本轮取完全 rational 的 `t=2`，得到

`p=20`, `q=5`, `4t²=16`，

因此新 factor 精确为

`C=25/4`。

即 `16 -> 25/4`，而且没有引入任何代数数或数值 eigensolver。

## 需要保留的边界

1. `C_*` 只是在 `J_t=t²M+W` 这一 AM-GM bridge family 内、使用 interval-derived `p,q` 时的最优值；不声称它是特定 `F,M,W` 的 universal sharp constant。
2. 真正比例 metric `M=cW` 应继续优先走 T-P5-261，直接得到 factor `1`；不要为了“全 rational”反而用近似 `t` 损失 reserve。
3. bridge PSD 比较失败只代表这个高维 sufficient lane 太粗，不能标记 physical FAIL；二元/三元 quotient 继续保留 T-P5-258/259 的 realized-direction SOS/Gram escape hatch。
4. arbitrary factor 必须先做 canonical symmetrization；antisymmetric syzygy 不能计入 bridge charge。

## 给其他 Agent 的建议

后续 actual source packet 一旦出现同键 `M,W,F`，建议先做 exact proportionality；不成比例时直接搜索小分母 rational `t`，并用 exact LDL/PSD 找 `pM-J_t>=0`、`qW-J_t>=0`。这通常会比先压成全局 `α,β` 更锐。若 `M(s),W(s)` 在参数 polytope 上仿射，同一 `(t,p,q)` 的两张 Loewner gate 也是 affine matrix family，所以只检查 vertices 就能 lossless 地证明 uniform bridge overhead；可直接和 T-P5-260 的 cell dispatcher 拼接。

下一条真正独立的数学 seam 是：若 actual reserve 连 `C_*` 级别仍不够，研究更一般的 structured auxiliary metric `J`，要求可 exact 证明 `q_J² >= 4q_Mq_W`，再用 `J<=pM,J<=qW` transport；重点应放在 block/eigenspace alignment 能否比 scalar `t` bridge 更锐，而不是再做一遍 condition-ratio audit。

当前仍是 `CONDITIONAL_PASS_MATHEMATICAL_CHILD / pending source binding`。actual P5 metric/factor/source、coverage、Float64/interval、Lean/kernel、封不觉独立验证、registry/admission 与 parent closure 均未升级。