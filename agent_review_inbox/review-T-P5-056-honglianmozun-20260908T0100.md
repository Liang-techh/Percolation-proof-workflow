# Review Result — T-P5-056

```yaml
review_result:
  task_id: T-P5-056
  source_agent: 红莲魔尊
  status: pending
  created_at: 2026-09-08T01:00:00-06:00
  evidence_sha256: 9d1fc91972de6a11c631a20cd6c3511601110c244e91399d953f06a6866c0c92
  depends_on:
    - T-P5-050
    - coordinator-rev739
    - coordinator-rev742
  scope: >-
    Exact radical-derivative / two-point eta-Lipschitz bridge for source CSE primitives,
    without source monotonicity assumptions, inverse-trig pooling, Float64 reasoning,
    provenance/admission work, or overlap with T-P5-055 experimental lane.
```

## 1. Target obligation

梁智炜在 rev739 明确要求检查 core primitives 的 `∂η`，寻找一个 exact radical-derivative enclosure，使 source evaluator 能输出

`|u(η)-u(η0)| <= Lη |η-η0|`

而不依赖“采样看起来单调”、inverse-trig pooling，或把整段 source range 先粗暴 intervalize。

本 child 给出一个可直接作为 checker contract 的代数 bridge。核心思想是：不要对 radical primitive 做黑盒 interval box，而是对 CSE node 保留

1. radicand 的严格正下界；
2. radicand 的 two-point / derivative variation bound；
3. numerator 的 amplitude + variation bound；
4. 用 exact rationalization 在 radical node 处传播 `Lη`。

这条路线本身不需要 source monotonicity。

---

## 2. Square-root two-point identity

设 `A,A0 >= μ^2 > 0`。利用平方差：

`|sqrt(A)-sqrt(A0)| = |A-A0| / (sqrt(A)+sqrt(A0))`。

因为 `sqrt(A),sqrt(A0) >= μ`，所以

**(Sqrt-Lip)**

`|sqrt(A)-sqrt(A0)| <= |A-A0|/(2μ)`。

若 source 已证明

`|A(η)-A(η0)| <= LA |η-η0|`，

则立刻得到

`|sqrt(A(η))-sqrt(A(η0))| <= LA/(2μ) |η-η0|`。

checker 更适合使用不除法的形式：

**`2 μ |Δ sqrt(A)| <= |ΔA| <= LA |Δη|`.**

注意：这里没有使用 `A` 对 η 的单调性。

---

## 3. Reciprocal square-root identity

同样设 `A,A0 >= μ^2 > 0`。精确恒等式为

`|A^(-1/2)-A0^(-1/2)|`

`= |A-A0| / [sqrt(A)sqrt(A0)(sqrt(A)+sqrt(A0))]`。

分母至少为 `2 μ^3`，所以

**(InvSqrt-Lip)**

`|A^(-1/2)-A0^(-1/2)| <= |A-A0|/(2 μ^3)`。

因此若 `A` 的 eta-Lipschitz 常数是 `LA`，则

**`Lip_eta(A^(-1/2)) <= LA/(2 μ^3)`.**

checker-scaled form：

**`2 μ^3 |Δ(A^(-1/2))| <= |ΔA| <= LA |Δη|`.**

这正是很多 normalized geometry / Newton–Euler primitive 中比直接微分更稳的 two-point algebra。

---

## 4. General inverse half-power family

令整数 `n>=1`，写 `x=sqrt(A)`, `y=sqrt(A0)`，则 `x,y>=μ`。有

`|x^(-n)-y^(-n)|`

`= |x-y| * (sum_{j=0}^{n-1} x^(n-1-j)y^j)/(x^n y^n)`。

逐项用 `x,y>=μ` 可得

`|x^(-n)-y^(-n)| <= n μ^(-(n+1)) |x-y|`。

再用第 2 节的 rationalization：

**`|A^(-n/2)-A0^(-n/2)| <= n/(2 μ^(n+2)) |A-A0|`.**

因此

**`Lip_eta(A^(-n/2)) <= n LA /(2 μ^(n+2))`.**

例如 `A^(-3/2)` 的 exact generic charge 是 `3 LA/(2 μ^5)`。

这个 family 足以覆盖常见 normalized-vector / curvature evaluator 中出现的 `r^(-1)`, `r^(-3)` 等 radical denominator powers。

---

## 5. Normalized radical primitive `u = G/sqrt(A)`

这是更接近 source CSE consumer 的形式。假设在同一个 eta-cell 中：

- `A(η) >= μ^2 > 0`；
- `|A(η)-A(η0)| <= LA |η-η0|`；
- `|G(η)| <= MG`；
- `|G(η)-G(η0)| <= LG |η-η0|`。

把差分拆成

`G/sqrt(A) - G0/sqrt(A0)`

`= (G-G0)/sqrt(A) + G0(A^(-1/2)-A0^(-1/2))`。

于是得到

**(Normalized-radical bridge)**

`|Δu| <= [LG/μ + MG LA/(2 μ^3)] |Δη|`。

等价的 checker-scaled 形式是

**`2 μ^3 |Δu| <= (2 μ^2 LG + MG LA)|Δη|`.**

这条 theorem 不需要微分 API；只要 source side 能提供 four-tuple

`(μ, LA, MG, LG)`

即可直接消费。

如果 source 更方便提供 derivative enclosure：

`|A'(η)| <= DA`, `|G'(η)| <= DG`，

那么用 MVT/FTC 得 `LA=DA`, `LG=DG`，从而

**`Lη(u) = DG/μ + MG DA/(2 μ^3)`**

是一个合法的 exact enclosure。

直接微分也得到同一个结构：

`u' = G'/sqrt(A) - G A'/(2 A^(3/2))`。

这说明 rev739 所要求的“看 core primitive 的 ∂η”可以被压成两个非常局部的 source obligations：radicand margin + derivative magnitude，不需要判定 derivative 的符号。

---

## 6. Radical-free squared variant：更适合现有 P5 residual ledger

如果不希望 checker 中出现一个人为选择的 `μ=sqrt(m)`，可只要求一个 exact rational lower bound

`A,A0 >= m > 0`。

平方第 2、3 节的 rationalization，可得到完全无 radical constant 的 polynomial inequalities：

**`4 m |Δ sqrt(A)|^2 <= |ΔA|^2`**，

**`4 m^3 |Δ(A^(-1/2))|^2 <= |ΔA|^2`**。

更一般地，对 `n>=1`：

**`4 m^(n+2) |Δ(A^(-n/2))|^2 <= n^2 |ΔA|^2`.**

所以若 `|ΔA| <= DA |Δη|`，则例如

`4 m^3 |Δ(A^(-1/2))|^2 <= DA^2 |Δη|^2`。

这和 P5 现有大量 `||residual||^2 <= const * (...)` 的 consumer 更自然匹配，而且 `m,DA` 可以全部保持 exact rational。

### 6.1 `G/sqrt(A)` 的 radical-free squared bridge

令 `u=G/sqrt(A)`，并仍假设

`A>=m>0`, `|ΔA|<=DA|Δη|`, `|G|<=MG`, `|ΔG|<=DG|Δη|`。

差分分成两个项后，对任意 exact rational `θ>0` 使用

`|a+b|^2 <= (1+θ)|a|^2 + (1+1/θ)|b|^2`。

得到

`|Δu|^2 <= [(1+θ) DG^2/m`

` + (1+1/θ) MG^2 DA^2/(4m^3)] |Δη|^2`。

完全乘开后，有一个非常 checker-friendly 的形式：

**`4 θ m^3 |Δu|^2`
` <= (1+θ)(4 θ m^2 DG^2 + MG^2 DA^2)|Δη|^2`.**

这一版只有加、乘、平方和有理参数 `θ`；没有 sqrt、division、eigenvalue 或 monotonicity。

如果 downstream 最终需要 squared residual gain，这一版应优先于先算一个带 radical 的 `Lη` 再平方。

---

## 7. Exact CSE propagation rules

建议 source evaluator 不直接展开整个 curvature expression，而是对每个 CSE node 维护二元 contract

`(|f| <= Mf,  |f(η)-f(η0)| <= Lf |Δη|)`。

那么基本传播规则全部是 exact algebra：

- `f +/- g`：`M <= Mf+Mg`, `L <= Lf+Lg`；
- `c f`：`M <= |c|Mf`, `L <= |c|Lf`；
- `fg`：
  `|fg-f0g0| <= Mf Lg |Δη| + Mg Lf |Δη|`，
  所以 `L <= Mf Lg + Mg Lf`；
- `sqrt(A)`：用第 2 节；
- `A^(-1/2)`：用第 3 或第 6 节；
- `G/sqrt(A)`：最好直接用第 5/6.1 节的 fused node，避免先分别 intervalize 再丢相关性。

这使 source bridge 可以按真实 evaluator DAG 做 local proof，而不要求 whole-expression monotonicity。

---

## 8. Quadratic-radicand corollary：常见 source node 的有限 exact certificate

若某 radicand 在 CSE 后是

`A(η)=a+bη+cη^2`

并且 eta-cell 是 exact rational endpoints `[η-,η+]`，则

`A'(η)=b+2cη`

是 affine。`|A'|` 在闭区间上的最大值一定在 endpoint，因此可以精确取

**`DA = max(|b+2cη-|, |b+2cη+|)`.**

不需要采样，也不需要 `A` 自身单调。

若 numerator 是 affine

`G(η)=g0+g1η`，

则

`DG=|g1|`

且

`MG=max(|G(η-)|,|G(η+)|)`。

因此只剩一个 radicand positive-margin obligation。若已有中心点 `ηc`、halfwidth `h` 和 `A(ηc)=A0`，甚至可以先由

`A(η) >= A0 - DA h`

得到一个 cellwise lower bound。只要选择 exact rational `m>0` 满足

`m <= A0-DA h`，

第 6 节的 radical-free squared bridge 就可以直接使用。

这个 corollary 给出一个真正有限、可程序化的 source-evaluator bridge，而不是“请证明某个神秘 Lipschitz 常数”。

---

## 9. Exact obstructions / failure boundaries

### 9.1 无 positive radicand margin 时，uniform Lipschitz 一般不存在

取完全精确的例子

`A(η)=η`, `η in [0,h]`。

则

`|sqrt(η)-sqrt(0)|/|η-0| = 1/sqrt(η)`，

当 `η -> 0+` 时无界。

所以 `sqrt(A)` 在 touching-zero 的一般情形只有 `1/2`-Holder regularity，不能期待 cellwise finite linear Lipschitz constant。inverse square-root 更直接发散。

因此 generic radical bridge 必须有严格正 margin，除非 source 暴露更强的特殊 algebraic cancellation，例如 radicand 本身可以先 exact factor/simplify 成一个已知固定符号的 square。

### 9.2 只有 interval range、没有 variation information，也不足以构造 `Lη`

知道 `A(η) in [a,b]` 只能限制 amplitude，不能限制 eta-variation。保持相同 range 的高频振荡函数可以有任意大的 Lipschitz constant。

所以 rev739 中“interval box constant 太保守”的问题不能通过继续收紧 amplitude box 从根本上解决；source 必须保留 derivative / two-point variation structure。这正是本 bridge 引入 `DA/LA` 的原因。

### 9.3 sampled trend 不能替代 derivative magnitude theorem

随机点上看见同号趋势不构成 monotonicity 证明。本 child 完全不使用这一假设；只消费绝对 derivative enclosure `|A'|<=DA`, `|G'|<=DG` 或等价的 two-point bounds。

---

## 10. Candidate theorem statements for Lean/checker layer

最小建议 children：

1. `sqrt_two_point_with_margin`
   - assumptions: `0<μ`, `μ^2<=A`, `μ^2<=B`
   - conclusion: `2*μ*|sqrt A-sqrt B| <= |A-B|`.

2. `inv_sqrt_two_point_with_margin`
   - same assumptions
   - conclusion: `2*μ^3*|A^(-1/2)-B^(-1/2)| <= |A-B|`.

3. `inv_half_power_two_point_with_margin`
   - integer `n>=1`
   - conclusion: `2*μ^(n+2)*|A^(-n/2)-B^(-n/2)| <= n*|A-B|`.

4. `normalized_radical_eta_lipschitz`
   - consumes `(μ,LA,MG,LG)`
   - concludes
     `2 μ^3 |Δ(G/sqrt A)| <= (2 μ^2 LG + MG LA)|Δη|`.

5. `normalized_radical_eta_lipschitz_sq`
   - consumes rational lower margin `m`, `DA,DG,MG`, rational `θ>0`
   - concludes
     `4 θ m^3 |Δu|^2 <= (1+θ)(4 θ m^2 DG^2 + MG^2 DA^2)|Δη|^2`.

Theorem 5 is the most directly compatible with current P5 squared-residual consumers.

---

## 11. Downstream source contract

A source-side implementation should now expose, per active eta-cell and per radical CSE node:

- exact lower radicand margin `m_j>0`;
- exact derivative/two-point gain `DA_j`;
- where needed numerator amplitude `MG_j` and derivative gain `DG_j`;
- chosen exact rational Young parameter `θ_j` only if the squared fused bridge is used.

Then the evaluator can propagate an exact `Lη` or `Lη^2` certificate to the final curvature / residual primitive and feed the existing P5 energy consumer.

This is strictly more informative than an interval box and strictly weaker than proving monotonicity.

---

## 12. What remains unclosed

1. I have **not** claimed the deployed `forceError` / DH / FD / controller evaluator actually has the required radicand margins or derivative bounds. Those must be read from the real source CSE and certified separately.
2. I have **not** used T-P5-055 experimental samples to infer monotonicity.
3. I have **not** supplied Float64 semantics, source-parser equivalence, provenance, admission, or receipt claims.
4. If a real source radicand approaches zero inside the deployed eta-cell, this generic linear-Lipschitz route is blocked; the next mathematical move would be to look for source-specific exact cancellation/factorization or shrink/subdivide the cell.
5. If the source CSE contains inverse-trig nodes after the radical stage, they still need their own local derivative enclosure; this child deliberately does not pool or hide them.

## 13. Result

`T-P5-056` establishes a new source-facing mathematical interface:

> **positive radicand margin + absolute eta-derivative/two-point variation bounds are sufficient to turn core radical CSE nodes into exact checker-friendly eta-Lipschitz or squared-Lipschitz certificates, with no monotonicity assumption.**

The strongest downstream-ready form for the current energy ledger is the radical-free squared fused certificate

**`4 θ m^3 |Δ(G/sqrt A)|^2 <= (1+θ)(4 θ m^2 DG^2 + MG^2 DA^2)|Δη|^2`.**

Status remains `pending` until the actual source evaluator supplies the per-node exact constants.
