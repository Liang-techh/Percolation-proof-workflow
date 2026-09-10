---
kind: companion_log
task_id: T-P5-261-MATCHED-METRIC-POLARIZATION-LOSSLESS-GRAM
source_agent: 狂蛮魔尊
created_at: 2026-09-10T16:44:00Z
review_commit: f17933375d1275a5ad9ecff9bf810d0678e5c113
status: pending
admission_label: pending
---

# 狂蛮魔尊 — T-P5-261 协作记录

本轮继续数学 closure，没有转做 provenance、receipt、admission 或重复验证。T-P5-258/259/260 已分别覆盖二元 quartic、三元 quartic 与参数 cell Gram selector，因此本轮没有抢占这些 lane，而是处理一个跨任意 quotient 维数的结构性正分支。

## 当前完成

对 homogeneous quadratic vector map `F(u)` 和 SPD metric `Q(u)=u^T W u`，取唯一 symmetric polarization `S`，定义 canonical factor `A_sym(u)v=S(u,v)`。已经证明三件事完全等价：

`||F(u)||^2 <= kappa Q(u)^2`；

`||S(u,v)||^2 <= kappa Q(u)Q(v)`；

`A_sym(u)^T A_sym(u) <= kappa Q(u)W`。

因此在 source/storage 两个 radial metric 相同或成正比例时，canonical matrix gate **没有任何常数损失**；scalar、bilinear、matrix 三个 sharp constant 完全相同。这个结论不依赖 quotient 维数，也不依赖 binary/ternary quartic 的 Hilbert 特例。

## Fraction-free gate

若 producer 给出任意线性 factor `A(u)`，先在两个输入 tensor slot 上做对称化。用 doubled coefficients

`Chat_{aij}=C_{aij}+C_{aji}`

构造 `Ahat_sym=2A_sym`，则可以完全有理地检查

`Ahat_sym(u)^T Ahat_sym(u) <= 4 kappa Q(u)W`。

这一步会自动丢掉所有满足 `N(u)u=0` 的 antisymmetric/syzygy gauge；这些 gauge 对真实 radial vector 完全不可见，不应消耗 reserve。

## 关键反例

取 `F=(x^2,xy)`、`Q=x^2+y^2`。真实 scalar sharp 常数为 `1`。若选 gauge-equivalent factor

`A=[[x-y,x],[0,x]]`，

在 `(1,0)` 有 `det(I-A^T A)=-1`，matrix gate 失败；但 canonical symmetrization 后同一个 `kappa=1` 精确通过。因此 arbitrary-factor matrix failure 不能报 radial FAIL。

另一个边界反例证明 metric matching 不能删：保持同一个 `F` 与 `Q`，取 `q=x^2+y^2/16`。scalar 仍有 `||F||^2<=qQ`，但 canonical factor 在 `(0,1)` 给出 `diag(1/4,0)`，而 `qI=(1/16)I`，所以 same-constant matrix gate 失败。

## 非匹配 metric 的安全预算

若 `alpha W <= M <= beta W`，则 scalar mixed packet

`||F||^2 <= kappa (u^T M u)(u^T W u)`

至少能推出 canonical matrix packet，常数损失至多 `beta/alpha`。比例 metric 时 `alpha=beta`，损失严格回到 `1`。

## 给其他 Agent 的建议

若实际 source lane 后续给出同一 quotient 上的两个 quadratic metric，先 exact 检查是否成比例；若是，应优先走本 child 的 canonical symmetrization，而不是继续做低维 quartic Gram search。若只得到 Loewner sandwich，则可以用 `beta/alpha` 做安全 nonsharp budget。若 metric 真正不匹配且预算敏感，再回到 T-P5-258/259 的 realized-direction quartic lane。

下一条独立数学 seam 是 mixed-metric polarization：寻找比 `beta/alpha` 更锐、最好同常数的两 metric bilinear/tensor packet，或证明 proportionality 之外不存在某类 universal same-constant matrix representation。

当前仍是 `CONDITIONAL_PASS_MATHEMATICAL_CHILD / pending source binding`。actual P5 factor/metric、coverage、Float64/interval、Lean/kernel、封不觉独立验证、registry/admission 与 parent closure 均未升级。
