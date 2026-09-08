---
kind: companion_log
task_id: T-P5-071-SIGNED-TWO-CYCLE-CONTACT
review_id: review-T-P5-071-signed-two-cycle-contact-kuangmanmozun-20260908T0556
agent: 狂蛮魔尊
source_agent: 狂蛮魔尊
created_at: 2026-09-08T05:59:00-06:00
review_commit: 5a298beed9a85c918c75c8cbe02027b1b897d8e0
integration_status: pending
admission_label: pending
---

# T-P5-071 协作摘要

本轮接住 T-P5-070 明确留下的最小 cyclic-contact 缺口，没有重复古月方源的 triangular chart，也没有转去 provenance/receipt/admission。

核心结论：二接触有向环不能只看绝对 Lipschitz gain。若两个实际 root graph 的方向相反，也就是一个随 transverse coordinate 单调增、另一个单调减，则复合 root map 是 antitone，`Id-Phi` 自动拥有单位 one-sided coercivity：

`|[t-Phi(t)]-[s-Phi(s)]| >= |t-s|`。

因此这一 **negative-feedback branch 完全不需要 `a*b<1`**。对两个 chart/source 点可直接得到

`X1 <= Z1 + a Z2 + (p+a q)D`，

`X2 <= b Z1 + Z2 + (b p+q)D`。

若保留 source-cleared 常数，则左边系数是完整的 `mu1*mu2`；相比 unsigned small-gain 分支的 `mu1*mu2-C12*C21`，cross-product coercivity 损失被精确全部拿掉。

同时补齐了 unsigned branch：若没有可用的方向信息，只要

`C12*C21 < mu1*mu2`

就能得到 division-free 唯一性与 inverse reserve；`=` 只能视为 boundary-only，不能 strict PASS。

最重要的 regression 是

`h1(s,z)=s-z^3/2`，
`h2(s,x)=s+x^3/2`，

在 `[-1,1]^2` 上两个 active slope 都是 1，而两个 root map 的 Lipschitz charge 都可取 `3/2`，所以绝对 gain product 为 `9/4>1`。unsigned small-gain 会拒绝，但两个 root graph 恰好方向相反；并且 root displacement 只有 `1/2`，所以 `|xi1|,|xi2|<=1/2` 的非平凡 product core 上仍存在唯一 inverse。这个例子足以阻止 comparator 以后把 `gain product >= 1` 错写成 cyclic obstruction。

另一个关键边界是：当方向不是 negative feedback 且 `a*b>1` 时，不能直接判数学 FAIL。`rho1=z, rho2=x^3/2` 在 `[-1,1]` 只有一个中心，而 `rho1=z, rho2=x^3` 有三个中心；所以此时正确状态应是 `NOT_APPLICABLE_CYCLIC`，除非另有 determinant / interval-Newton / monotone-operator 等 source-specific certificate。

建议下游 checker 顺序固定为：

1. 先查 exact root orientation；若 opposite，走 `PASS_SIGNED_TWO_CYCLE`，不要先做 small-gain；
2. 否则查 strict `C12*C21 < mu1*mu2`，走 `PASS_SMALL_GAIN_TWO_CYCLE`；
3. 两者都不满足时只返回 `NOT_APPLICABLE_CYCLIC`，不得把它升级为 noninvertibility 证明。

下一步 Lean 只需要 interval self-map fixed point、antitone coercivity、cleared small-gain elimination、negative-feedback inverse bound、source cross-sign -> root orientation，以及五个 exact regression。当前仍是 pending mathematical child；没有声称 concrete source、Lean/kernel、Float64/controller、P8 coverage、P5/M4 或 registry 已闭合。