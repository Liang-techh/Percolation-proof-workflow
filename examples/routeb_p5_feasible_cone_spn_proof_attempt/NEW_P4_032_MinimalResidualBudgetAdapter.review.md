# P4：最小 residual-budget adapter 定向审阅

日期：2026-09-07。状态：**OPEN_UNCOMPILED**。
新增 `NEW_P4_032_MinimalResidualBudgetAdapter.lean` 与本 review。
本轮仅静态/纸面审阅，不运行 Lean/Lake、公理检查或大回归，不修改旧文件或 registry。

## 拆分后的最小证据边界

`CapEvidence f qCap` 明确保存同一 f.domain 上的 q=f.residual、q≥0、qCap≥0 及 q≤qCap。
它只保留后续 margin 消费需要的 residual 预算，不重新推导 energy cap。

`capFromAllowance` 消费原 `LocalEvidence`、`UniformParameters`、`UniformEnergyCap` 和
`ResidualAllowance`，仅调用旧 `residual_le_allowance`，得到 `CapEvidence f a.qCap`。
因此上游 rho/bias/feedback/envelope 义务集中在构造器中；若直接提供独立 cap 证明，
后续最小核心无须再次接收这一整条推导链。
这并不表示可由一个未证明的数值 qCap 替代 cap 证据。

## Scale、comparison 与 target allocation

新 `residualScale(x)` 明确作用在标量 q 上。要求同域：

```text
gain≥0，residualScale≥0，q≤qCap，
nominal - gain*(residualScale*q) ≤ margin，
target + gain*(residualScale*qCap) ≤ nominal。
```

qCap 在两条预算中是同一个参数，不允许从另一个域或另一个残差的 allowance 偷换。
`effectiveMargin` 把 gain*residualScale 作为原消费者的有效 gain，保留 nominal/margin 原函数。
`toSchurComparison` 返回现有 `SchurPMIComparison`；`toMarginAllocation` 在 qCap=a.qCap
时返回现有 `MarginAllocation`。两个 adapter 只做乘法结合与非负证据传递。

`conditional_residual_margin` 是拆出的最小消费核心，输出同域 `target≤margin`。
它只做一次有效 gain 下的 cap 单调替换并组合比较/分配，不重复 contraction、
uniform parameter bridge、Schur 恒等式或 weighted Cauchy。

若 q=||r||²，residualScale 是这个**平方标量**的系数。
向量变换 r↦c*r 对应的平方缩放为 c²，不能自动将 c 当成此系数。
这里的 residualScale 也不自动等于 BODY6 adapter 中乘在 front 二次型上的 scale；
任何这种身份与 normalization 都须由调用者另行证明。

## 两个精确实数反例

| 反例 | q | qCap | gain | scale | nominal | target | margin |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 缺 q≤qCap | 2 | 1 | 1 | 1 | 1 | 0 | -1 |
| 缺 scale≥0 | 0 | 1 | 1 | -1 | -1 | 0 | -1 |

`missing_qCap_witness` 中所有非负条件、comparison 和 nominal/target allocation 都成立，
但 q>qCap 且 margin<target；仅有 cap 的名字或数值不足以推论目标。

`missing_scale_sign_witness` 中 q≥0、q≤qCap、qCap≥0、gain≥0 都成立，
comparison/allocation 也成立，但负 scale 使上界替换方向失效，margin<target。
负 gain 而 scale 为正也会导致相同的有效系数问题。
单调步骤的最弱代数要求是 gain*scale≥0；接口分别保留 gain/scale 非负以维持预算语义，
不声称两者分别非负是所有可能参数化下的必要条件。

## 剩余边界

全部证据与结论都限定在 f.domain；域外 coverage 不会由接口自动获得。
归一化比较、真实 residual 定义、true-DH/K-path/source 身份仍须外部证明。
`SchurPMIComparison` 是标量比较证据，既不是 solver 状态，也不直接给出矩阵 PSD。
反例仅是精确实数逻辑见证，不声称物理可实现。

新文件无变量除法、倒数或 sqrt；导入链与新脚本未做 elaboration/kernel 检查，
`#print axioms` 未执行。保持 OPEN_UNCOMPILED，无 source/coverage/admission/registry 升级。
