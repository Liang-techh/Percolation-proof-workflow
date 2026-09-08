---
kind: companion_log
task_id: T-P5-068-RECENTERED-UNIT-C11
agent: 柳冠一
source_agent: 柳冠一
created_at: 2026-09-08T05:23:00-06:00
review_commit: 6b4685d7e8952aa50de8f284247f96076987cb37
status: pending
---

# 柳冠一协作留言：T-P5-068 已补齐 simple-root recentering 后的 unit 正则性

本轮没有发现梁智炜新的“柳冠一”点名，因此只接 T-P5-066 明确保留的数学缺口，没有抢 T-P5-067 multiple-root/Lean lane。

核心 bridge：T-P5-066 得到真实唯一根 `r` 后，不要在执行层直接计算接近奇点的 `h(x)/(x-r)`。若实际 shifted factor `h` 在同一 cell 上是 `C1,1`，并且

`|h'(x)-h'(y)| <= L2 |x-y|`，

则 canonical recentered unit

`v_r(r)=h'(r)`，`v_r(x)=h(x)/(x-r)` (`x!=r`)

严格满足平均导数恒等式

`v_r(x)=∫_0^1 h'(r+t(x-r)) dt`。

因此 T-P5-066 的 derivative/secant sign bounds 无损传给 `v_r`，而且有 sharp bound

`2 |v_r(x)-v_r(y)| <= L2 |x-y|`，

即 `Lip(v_r)<=L2/2`。这个 `1/2` 在二次函数上达到等号，不能统一改进。

重要 obstruction：仅有 `C1 + unique simple root + transversality` 不足以给 Lipschitz unit。例子 `h(x)=x(1+sqrt(|x|))` 的 root 唯一且导数在小邻域严格为正，但 recentered unit `1+sqrt(|x|)` 在 0 不 Lipschitz。因此后续 source packet 必须真正提供 derivative modulus / C1,1 信息，不能从“根唯一且 unit 非零”自动填写 `unit_lipschitz`。

参数化版本也已经给出：若 `g_y=∂_x h_y` 满足 joint bound

`|g_y(x)-g_y'(x')| <= Lx|x-x'| + Ly d(y,y')`

且 root graph `r(y)` 的 Lipschitz 常数为 `Lr`，那么 triangular chart `xi=x-r(y)` 中的 unit 满足

`|V(y,xi)-V(y',xi')| <= (Lx Lr+Ly)d(y,y') + (Lx/2)|xi-xi'|`。

建议 Lean 最先只做三个 source-independent leaf：segment-average identity、derivative bounds → unit bounds、derivative Lipschitz → `2*|Δv|<=L2|Δx|`。当前仍是 pending mathematical/interface child；deployed source binding、真实 `L2`、FD/Float64、P8 coverage、Lean/kernel、封不觉验证与 admission 均未宣称闭合。