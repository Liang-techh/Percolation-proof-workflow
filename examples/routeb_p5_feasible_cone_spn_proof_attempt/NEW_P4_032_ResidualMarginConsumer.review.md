# P4 true-DH residual → 条件式 Schur/PMI scalar margin

日期：2026-09-07。新增 `NEW_P4_032_ResidualMarginConsumer.lean` 与本 review。
**UNCOMPILED bounded source-independent proof attempt**；仅静态/纸面审阅。
未运行 Lean/Lake、公理检查或大回归，未修改共享脚本、旧模块或 registry。

## 输入与最终结论

最终 `conditional_margin` 显式消费：

| 输入 | 必须提供的证据 |
| --- | --- |
| `LocalEvidence f` | 同域 relative residual bound、非负证据、envelopes，以及 E≤base+q 的反馈闭合 |
| `UniformParameters f` | rhoEff≤rhoBar<1、base+B_eff≤biasBar、biasBar≤(1-rhoBar)*cap，及原非负字段 |
| `UniformEnergyCap f u` | 对所有域内点 E≤u.cap |
| `ResidualAllowance f u` | 非负 qCap 与 rhoEff(x)*cap+B_eff(x)≤qCap |
| `SchurPMIComparison f m` | gain≥0，且 nominal−gain*q≤margin |
| `MarginAllocation f u a m target` | target+gain*qCap≤nominal |

输出仅为 `∀x∈f.domain, target≤margin(x)`。
取 target=0 时只得到指定标量 margin 的非负下界；没有矩阵 PSD、PMI 全局可行性、
solver 验收、source/coverage/admission/registry 结论。

## 已有链路与新消费步骤

`energyCapOfBridge` 只调用上一轮 `uniform_parameter_cap`，生成显式 cap 证据。
没有重复 contraction、参数桥或 domain-uniform theorem。
`residual_le_allowance` 使用 rhoEff≥0，将已知 E 上界代入原 relative residual bound：

```text
q ≤ rhoEff*E+B_eff ≤ rhoEff*cap+B_eff ≤ qCap。
```

由 gain≥0 和提供的 Schur/PMI 比较式，
`conditional_margin` 组合 `target+gain*qCap≤nominal` 得到 target≤margin。
不能将 energy 的上界当作 positive energy 项的下界；这里由独立的 nominal allocation
提供所需下界。比较式若实际含额外交叉项或变换误差，调用者必须先将其计入 nominal/gain
并证明比较，而不能静默删除。

## Residual allowance 的两个显式构造器

`allowanceFromTotalBias` 取 qCap=rhoBar*cap+biasBar。
因为前轮 biasBar 控制的是 base+B_eff，且反馈前提包含 base≥0，故它也控制 B_eff。
这是允许保守性的预算；base 没有从前轮反馈 allocation 中删除，也没有被声称等于零。

若另有同域 B_eff≤defectBiasBar，则 `allowanceFromDefectBias` 可取
qCap=rhoBar*cap+defectBiasBar。缺少这条单独证据时不能自动使用更小的 allowance。

若 q 实例化为 `||rB||₂²`，qCap 也是平方预算，gain 必须对应这个平方 residual。
一个 norm 上界不能直接充当本比较式，solver 返回的数值或成功标志也不是 lower 证明。
本轮保持无变量除法、倒数和 sqrt。

## Obstruction 与精确反例

- **rho 缺失/失效**：原 uniform 参数包仍要求同域 rhoEff≤rhoBar<1；
  点态严格收缩不能自动补全这个包。域内 rhoEff≥1 会阻断此包，沿用前轮结论，未重证。
- **bias/feedback/allocation 缺失**：只有 residual 上界不能产生 energy cap；
  base+B_eff 的总预算不能漏项。即使 cap 和 qCap 已有，没有 nominal allocation 也不能保证
  非负 margin。最终消费者保留全部这些输入，尽管某些上游字段在 cap 已显式给定后
  不参与最后一步代数；这是沿用既定链路的合同，不声称它们是任意 margin 方法的必要条件。
- **coverage 缺失**：结论只覆盖 f.domain。样本、有限点或空域不证明目标物理域已覆盖；
  所有 cap、allowance、comparison 和 allocation 的全域量词都必须实际提供。
- **source 缺失**：同一个 f/m 类型索引并不证明它们来自 true-DH、K-path、目标 residual、
  metric/key 或 normalization；这些来源等式与比较证据仍是外部义务。

`zero_residual_negative_margin` 给出精确标量见证：E=q=0、rho=0.5、base=B=0，
nominal=margin=-1、gain=1。非负能量、零 cap、relative bound、反馈和比较均成立，
但 margin<0；target=0 的 nominal allocation 不成立。
这说明 residual 为零都不能自动证明正 margin，更不能仅凭 residual norm 宣称 PSD。
该见证不声称是物理可实现的 true-DH/source 反例。

新证明脚本与导入链尚待 elaboration/kernel 检查；`#print axioms` 未执行。
