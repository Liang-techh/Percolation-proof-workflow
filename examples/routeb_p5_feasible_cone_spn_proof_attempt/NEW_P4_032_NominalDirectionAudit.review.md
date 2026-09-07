# P4 uniformTargetAllocation：nominal 方向与 target sign 定向审查

日期：2026-09-07。状态：**OPEN_UNCOMPILED**。
新增 `NEW_P4_032_NominalDirectionAudit.lean` 与本 review。
仅静态/纸面审阅；未运行 Lean/Lake 或大回归，未修改旧 contract、共享脚本或 registry。

## 审查结果：原方向正确，但合并前提要求 nominal 精确实现

旧 `uniformTargetAllocation` 的传递链是：

```text
uniformFloor ≤ offset(x)+alpha(x)*L(x) ≤ nominal(x)。
```

最后一步实际使用 `UniformData.nominal_realization`，方向为 expression≤nominal，正确。
它没有从 `CompositionContract.nominal_bound` 的相反方向推导 nominal 下界。
不过这两个 contract 同时存在时，由反对称性必有 **nominal=expression**。
`current_uniform_nominal_is_exact` 将此事实记录为条件式引理。
这是比“nominal 为保守下预算”更强的 specialization；不能无条件接入严格小于 expression 的 nominal。
本轮没有修改或放松旧接口。

## 三种命题的不同证明类型

| 类型 | 命题 | 用途 |
| --- | --- | --- |
| `NominalUpper` | nominal≤expression | 已有 nominal allocation 可转成 expression allocation 的必要条件 |
| `NominalLower` | expression≤nominal | expression allocation 可转成 nominal allocation 的充分条件 |
| 原 `TargetAllocation` | target+loss≤nominal | 最终 margin 消费器真正要求的 allocation |

另设 `ExpressionAllocation` 表示 target+loss≤expression，避免将 RHS 混为一谈。
`allocation_via_lower` 仅接受 NominalLower；
`expression_allocation_necessary` 只证明相反的必要性路径，不提供逆向转换。
`upperFromComposition`、`lowerFromUniform` 显式接到实际旧字段。

这里 loss(x)=gain(x)*(scale(x)*qCap)。
`margin_via_nominal_lower` 同时要求同一个 f/domain 上的 CapEvidence 和 ScaledComparison，
保留 q≥0、qCap≥0、q≤qCap、gain/scale≥0 与 normalization comparison，
然后复用旧 `conditional_residual_margin`。
纯粹的 order-transitivity 引理不需要这些符号条件；它们没有从 margin 消费接口中删除。
若接入 BODY6，front alpha 的非负、remainder margin 与 normalization 仍由原 composition 前提负责。

## Target sign

allocation 和 target≤margin 对任意实数 target 都有意义，不能擅自增加或推断 target≥0。
`NonnegativeTarget` 显式保存非负证明，`nonnegative_margin` 才将结果转为 margin≥0。
`positive_margin` 另要求 target>0；target=0 只保证非负，不能保证严格正。
这些仍是 scalar margin 结论，不是矩阵 PSD 的判据。

## 精确实数反例

1. **方向错误**：nominal=0、expression=1、loss=0、target=1、margin=0。
   nominal≤expression、target+loss≤expression 和 nominal-loss≤margin 全部成立，
   但 target+loss≤nominal 不成立，且 margin<target。
   可取 q=qCap=0、gain=scale=1，符号与 cap 都没有问题。
2. **缺 qCap 关系**：nominal=expression=1、q=2、qCap=1、target=0、margin=-1，gain=scale=1。
   target+qCap≤nominal 与真实 comparison nominal-q≤margin 都成立，但 q>qCap，margin<target。
   nominal 双向关系正确也不能替代 residual cap 证据。
3. **负 target**：nominal=expression=0、q=qCap=1、target=margin=-1，gain=scale=1。
   cap、allocation、comparison 和 target≤margin 全部成立，margin 仍为负。
   这不是原定理失败，而是说明不能把任意 target 的下界结论升级为非负 margin。

三个反例均为精确实数，未声称物理 source 可实现。
表达式、残差或比较若属于另一个域/metric/normalization，不可通过这些类型自动搬运。
没有 source/coverage/admission/registry 或 PSD 升级；导入链与新脚本的 elaboration/kernel 检查未执行。
