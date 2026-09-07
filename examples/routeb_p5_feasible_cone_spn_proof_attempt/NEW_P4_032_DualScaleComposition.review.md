# P4：front quadratic scale 与 residual scalar scale 的 typed composition

日期：2026-09-07。状态：**OPEN_UNCOMPILED**。
新增 `NEW_P4_032_DualScaleComposition.lean` 与本 review。
仅静态/纸面审阅；不运行 Lean/Lake、公理检查或大回归，不修改旧模块或 registry。

## 两个尺度的角色与类型

`FrontQuadraticScale` 与 `ResidualScalarScale` 是两个不同的结构类型，各自显式保存实数 value，
没有自动 coercion、转换或相等证明。`ScaleFields` 分别保存它们的逐点函数。
类型区分防止接口隐式混用，但不替调用者证明填入的实数是正确物理尺度。

记 alpha 为 front scale，beta 为 residual scale，g 为 gain，
L=mu*Σvᵢ²、Q=vᵀRv、q=f.residual。两者的乘法位置明确为：

```text
nominal ≤ offset + alpha*L
offset + alpha*Q - g*(beta*q) ≤ margin
target + g*(beta*qCap) ≤ nominal。
```

BODY6 外部前提提供 L≤Q；alpha≥0 用于该下界的单调缩放。
q≤qCap 和 g≥0、beta≥0 用于 residual 项的上界替换。
有效 residual gain 是 g*beta；alpha 不因参与 front 二次型就自动乘入 residual gain。
若实际模型对整个表达式乘 alpha，则必须另外给出该表达式对应的比较与 gain，不能省略或猜测。

## 组合契约与已有 adapter 的复用

`CompositionContract f d m s` 对同一个 f.domain 显式要求：

- BODY6 中 d.scale(x)=alpha(x) 的绑定等式；
- alpha、beta、g 分别非负；
- `RemainderMargin (d.remainder x) (d.mu x)`；
- 上述 nominal lower relation 与完整 normalization comparison。

`toBodyEvidence` 为已有 BODY6 adapter 填入 quadratic scale=alpha、effective gain=g*beta。
`toScaledComparison` 实际调用旧 BODY6 `toSchurPMIComparison`，然后按乘法结合律
转回 residual adapter 的 gain=g、residualScale=beta 约定。
传给最小 residual consumer 的是原 m 与 beta，没有把已乘 beta 的 gain 再乘一次 beta。

`composed_scalar_margin` 另消费同域 `CapEvidence f qCap` 和
`TargetAllocation f m (residualValues s) qCap target`，只调用旧 `conditional_residual_margin`，
输出域内 target≤margin。qCap 在 cap 与 allocation 中为同一参数。
原 UniformParameterBridge/ResidualMarginConsumer 的证据可经 `capFromAllowance` 导入；
这里不重证其 contraction、rho/bias/feedback 消去或 energy cap。

## 精确反例

前三个定理通过 `ScalarPremises` 记录 offset=0、L≤Q、q≥0、q≤qCap、
nominal/comparison/allocation 全部成立，仅省略被反驳的符号要求：

| 省略条件 | alpha | beta | g | L | Q | q | qCap | nominal | target | margin |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| alpha≥0 | -1 | 1 | 1 | 1 | 2 | 0 | 0 | -1 | -1 | -2 |
| beta≥0 | 1 | -1 | 1 | 1 | 1 | 0 | 1 | 1 | 2 | 1 |
| g≥0 | 1 | 1 | -1 | 1 | 1 | 0 | 1 | 1 | 2 | 1 |

每行都有 margin<target。第一行是 front 下界缩放方向错误，后两行是 residual 上界替换方向错误。
这展示的是“移除某一符号条件、保留其他条件时不能保证结论”；
不声称这些逐项条件是每个退化实例的必要条件。
residual 步骤的最弱乘法符号条件是 g*beta≥0，本契约保留两项分别非负的预算语义。

`false_scale_identification_counterexample` 使用全部正尺度 alpha=1、beta=2、g=1，
L=Q=q=qCap=nominal=1、target=0、margin=-1。
真实 comparison 为 1-2=-1；错误地以 alpha 代 beta 做 allocation，得到 0+1≤1，
看似满足目标。真实 allocation 为 0+2≤1，实际不成立，且 margin<target。
所以不能因两个字段都叫 scale 就将其相等。
若调用者另有同域 alpha=beta 的真实证明，可以显式改写；这里没有禁止这种有证据的等同。

## Normalization 与剩余边界

beta 作用在标量 q 上；若 q=||r||²，向量缩放 c 对应的平方系数是 c²，不能默认 beta=c。
alpha 作用在 BODY6 三维 front 二次型上；它不定义 P4 二维 port 与 front 的维度/metric 映射。
所有这类关系必须由 normalization comparison 和 source 等式明确覆盖。

反例都是精确实数逻辑见证，不是实际 BODY6/true-DH source 反例。
同域类型不产生 coverage；完整矩阵 PSD、真实参数闭合、source/admission/registry 均无新结论。
无变量除法或 sqrt。导入链与新脚本的 elaboration/kernel 检查均未执行；`#print axioms` 仅为未来入口。
