# P4：relative/additive 参数 → DomainUniformContraction 定向桥接

日期：2026-09-07。新增 `NEW_P4_032_UniformParameterBridge.lean` 与本 review。
**UNCOMPILED bounded source-independent proof attempt**；仅静态及纸面审阅，
不运行 Lean/Lake 或大回归，不修改共享脚本、旧模块或 registry。

## 相同域与参数类型

`ParameterField X` 固定 domain、逐点 Parameters、energy、residual、ED/EB 和 base。
`LocalEvidence f` 与 `UniformParameters f` 都以同一个 f 为索引，
避免在接口中隐式替换域、能量或参数函数。
上游 Parameters 保留正权重、reciprocal gate、非负参数与 tau² 定义，
本轮没有重新计算或展开 rhoEff/biasEff。

`LocalEvidence` 要求对每个域内点提供：

```text
EnvelopesAt (params x) (energy x) (ED x) (EB x)
0 ≤ residual x
residual x ≤ rhoEff(params x)*energy x + biasEff(params x)
FeedbackBinding (energy x) (residual x) (base x)
```

最后一项包含 base≥0、energy≤base+residual，是独立闭合前提。
`ofWeighted` 直接调用旧 `consume_weighted_budget` 生成 relative 证据。
已有 force/accel typed 结果也可填入 `relative` 字段，此时 residual 应明确取对应的
`||rB||₂²`，并使用同一点的原 force/accel 定理和参数；不需要重复证明或约定转换。
该新接口本身仍是标量参数接口，不把任意 residual 自动识别为物理 force/accel。

## 总 additive 项不得丢失 base

`toBudgetField f` 的定义是：

```text
rho(x)  = rhoEff(params x)
bias(x) = base(x) + biasEff(params x)
energy/domain 保持原函数。
```

原因是两条局部输入只能推出
`energy≤base+biasEff+rhoEff*energy`。
除非实际 base 为零，否则只用 B_eff 作为 uniform additive 项会漏预算。

`UniformParameters f` 要求非负 rhoBar/biasBar/cap 以及：

```text
rhoBar < 1
∀x∈domain, rhoEff(params x) ≤ rhoBar
∀x∈domain, base(x)+biasEff(params x) ≤ biasBar
biasBar ≤ (1-rhoBar)*cap
```

`ofSeparateBiasBounds` 可消费分别证明的 base≤baseBar 和 biasEff≤defectBiasBar，
取总 biasBar=baseBar+defectBiasBar；仍要求有效 relative 系数的显式统一上界。
这不是从原始参数样本或各参数非负性自动算出有效常数的优化器。

## 已有定理的消费路径

`toUniformBudget` 将参数包逐字段交给现有 `UniformBudget`。
`toPointwiseClosure` 复用 `effective_coefficients_nonnegative`，由 uniform 界得到点态 strict，
并组合已提供的 relative 与 feedback 两条不等式。
`uniform_parameter_cap` 只调用已有 `DomainUniformContraction.uniform_cap`，输出
`∀x∈domain, energy(x)≤cap`。

没有重复标量除法/消去或 DomainUniform theorem，新增声明与证明无变量除法、倒数或 sqrt。
只有显式完整证据包才能调用这个消费者，没有缺失证据的默认值或自动升级路径。

## 四类 obstruction 与未完成绑定

1. **逐点参数/预算证据缺失**：参数非负或某次采样不能代替 EnvelopesAt、weighted/relative
   上界或 feedback。缺少其中任一项，就不能构造所需 LocalEvidence。
   即使每点有独立的参数界，也仍须证明它们如何给出同域统一的有效系数界。
2. **统一参数证据缺失或失败**：点态 rhoEff<1 不自动给出统一 rhoBar<1；
   前轮 dyadic 反例说明统一 bias 已有也不够。`bad_point_blocks_uniform_parameters`
   进一步记录：若有域内点 rhoEff≥1，则此 UniformParameters 包不可能存在。
   这是本接口的 obstruction，不等价于实际系统无界或不稳定。
3. **true-DH/K-path binding 缺失**：函数类型一致不证明它们确实来自目标 DH 模型、
   K-path、metric、regularizer/key 或 normalization。需要另行给出这些等式与有效性证据；
   本模块不生成 source 身份或物理解释。
4. **coverage 缺失**：结论仅覆盖 f.domain。把目标物理域的每个状态纳入此 domain，
   或通过明确映射提供其域成员资格，仍是外部义务。有限点/样本不替代全域量词，
   空域上的真命题也不证明目标域被覆盖。

这些缺失表示条件式接口尚不能应用，不都表示数学上不存在其他界。
本轮没有 true-DH/source/coverage/admission/registry 成功结论。
新模块与导入链的 elaboration、kernel 和公理检查均未执行，`#print axioms` 仅为未来入口。
