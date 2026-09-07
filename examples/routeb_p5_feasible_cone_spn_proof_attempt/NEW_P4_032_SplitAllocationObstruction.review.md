# P4：独立 allocation records 与无限域 obstruction

日期：2026-09-07。状态：**OPEN_UNCOMPILED**。
新增 `NEW_P4_032_SplitAllocationObstruction.lean` 与本 review。
仅静态/纸面审阅；不运行 Lean/Lake 或大回归，不修改旧模块、共享脚本或 registry。

## 四个独立证据包

| Record | 内容与方向 |
| --- | --- |
| `FrontFloors` | 非负 alphaFloor/frontFloor，alphaFloor≤alpha，frontFloor≤mu*frontEnergy，offsetFloor≤offset |
| `ResidualCaps` | 非负 betaCap/gainCap/qCap，逐点 beta/gain/q 上界及 q≥0 |
| `NominalRealization` | 使用旧 `NominalLower` 类型，明确 expression≤nominal |
| `TargetBudget` | target+gainCap*(betaCap*qCap)≤offsetFloor+alphaFloor*frontFloor |

所有记录均以同一个 f、d、m、s（按需）为索引，所有比较在 f.domain 上成立。
TargetBudget 绑定所选的具体 front/caps 记录，不能改用另一个 qCap 后沿用旧 allocation。
`assembleUniform` 仅逐字段组装旧 UniformData；`split_conditional_margin` 调用旧
`uniformized_scalar_margin`。原 CompositionContract 中的 alpha/beta/gain 非负、
BODY6 remainder margin、scale binding 与 normalization comparison 全部仍是显式输入。

这只是拆分证据职责，没有重复局部 composition、标量收缩或 uniform 乘法替换。

## 有限域充分条件与 target 的范围

`finite_residual_caps` 在给定有限 cells 覆盖 f.domain 且 q≥0 时，复用旧 finite_upper
分别取 beta/gain/q 的有限共同上界。
`finite_front_floors` 复用有限 offset 下界，保守地取 alphaFloor=frontFloor=0；
它使用原 alpha 非负与 RemainderMargin 的 mu≥0，保证 frontEnergy 乘积非负。
严格正 floors 仍需额外证明，本轮不把有限性当作正 margin 来源。

给定这些记录，`canonicalTarget` 取

```text
offsetFloor + alphaFloor*frontFloor - gainCap*(betaCap*qCap)。
```

该有限实数有精确 TargetBudget，但可能为负。
`finite_conditional_floor` 因此给出某个共同 scalar margin 下界，仍显式要求
同域 normalization 和正确的 NominalRealization。
预先指定的非负/正 target 必须另外满足 TargetBudget；有限性本身不保证它。
有限覆盖也是前提，采样点集合不自动覆盖连续状态域。

NominalRealization 与旧 CompositionContract 的 nominal≤expression 合起来仍要求相等。
这个 specialization 没有被拆分记录消除；保守 nominal 需要其他明确下界途径。

## 无限 dyadic obstruction：缺 uniform cap

`infinite_loss_allocation_obstruction` 固定 alpha=L=Q=g=q=qCap=1、offset=0，
令 beta_n=2^n、nominal=expression=1、margin_n=1-beta_n。
每点参数有限、非负，nominal realization 正确，normalization comparison 为等式。
但 beta 没有统一有限 cap；对任意固定 target，总有 n 使

```text
target+beta_n>1，且 margin_n<target。
```

因此这里不但所需 allocation 失败，真实的这条标量 margin 序列也没有共同有限下界。
将增长槽换成 gain，或取 q_n=localCap_n=2^n、beta=g=1，得到同样表达式。
不是每个无限域都无界，也不是缺少某个保守 cap 证明就已经证明真实量无界；
本结论靠明确的 dyadic 见证，复用前轮增长定理。

## 无限 dyadic obstruction：错误 nominal 方向

`infinite_nominal_direction_obstruction` 取 expression=0、nominal_n=-2^n、loss=0、q=qCap=0。
nominal≤expression 始终成立，任何固定 target≤0 都满足 target+loss≤expression，
但总有 n 不满足 target+loss≤nominal_n。
所以不能用 NominalUpper 填充 NominalRealization 或关闭本接口要求的 nominal allocation。

这里必须保留一个界限：若 BODY6 normalization 本身已经给出 expression-loss≤margin，
则仍可能绕开 nominal 直接证明 margin。上述例子可令 margin=0，完整 expression 比较成立，
且 target≤margin 实际成立。因而错误方向的例子证明的是**指定 nominal allocation 路径被阻断**，
不是所有 scalar margin 证明都不可能。
不能在保留真实 expression 比较和 expression allocation 的同时声称由此构造了 margin 失败反例。

两个 obstruction 相互独立：第一例 nominal 方向正确但 cap/target 失败；
第二例 residual 与 loss 已有统一界，但 nominal 下界关系缺失。

## 边界

反例仅是精确实数函数，不是已绑定的 true-DH/source 轨迹。
记录与结论不产生 target sign、连续域 coverage、source identity、矩阵 PSD 或 registry/admission 升级。
无变量除法或 sqrt；新脚本及导入链未运行 elaboration/kernel 检查，`#print axioms` 未执行。
