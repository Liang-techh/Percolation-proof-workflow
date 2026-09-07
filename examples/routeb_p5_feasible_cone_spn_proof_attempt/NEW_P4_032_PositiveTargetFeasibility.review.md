# P4 split allocation：positive-target feasibility

日期：2026-09-07。状态：**OPEN_UNCOMPILED**。
新增 `NEW_P4_032_PositiveTargetFeasibility.lean` 与本 review。
仅静态/纸面审阅；未运行 Lean/Lake 或大回归，未修改旧模块或 registry。

## 对固定 records 的精确条件

记 F=offsetFloor+alphaFloor*frontFloor，
L=gainCap*(betaCap*qCap)≥0，C=canonicalTarget=F-L。
offsetFloor 不要求非负，因此 F、C 可以为负。

`target_budget_iff` 表明，对任意**预先指定**的实数 target：

```text
TargetBudget front caps target  ↔  target≤C。
```

| 问题 | 精确条件 |
| --- | --- |
| 预设正 target 可行 | 0<target≤C |
| 存在某个正 target | L<F，等价于 C>0 |
| target=0 可行 | L≤F，等价于 C≥0 |
| 预设负 target 可行 | target<0 且 target≤C |
| 存在某个负 target | 对任意有限实数 records 均成立，例如 min(C,0)-1 |

`PositiveTargetBudget` 显式捆绑 target>0 和原 TargetBudget。
`positive_target_exists_iff` 以 C 本身作正 target 见证，不使用除法或 sqrt。
`negative_target_exists` 只证明存在一个足够低的负 target，不表示所有负 target 都可行。

若 C>0，可行正 targets 为 (0,C]；若 C=0，没有可行正 target，零与负 target 均可行；
若 C<0，零和正 target 都不可行，可行 targets 为 (-∞,C]。
C 是**给定保守预算包的最大可分配 target**，不是实际 margin 的最优值，
也不是对参数、域或 source 做优化后得到的最佳目标。

## 从 allocation 到实际 scalar margin 仍有独立义务

上述可行性只涉及 records 的数值 allocation。
`positive_margin_of_budget` 仍显式要求同域 CompositionContract 与 NominalRealization，
才调用旧 split_conditional_margin 得到 margin>0。
`nonnegative_margin_of_zero_budget` 对 target=0 得到 margin≥0，不能升级为严格正。
负 target 仅给出 target≤margin，不保证 margin 非负。

ResidualCaps 中 q≤qCap、beta/gain 的域上界及各 cap 非负没有被省略；
局部 beta/gain/alpha 非负及 normalization comparison 仍由 CompositionContract 提供。
NominalRealization 仍是 expression≤nominal 的独立下界证据，不能以相反方向替代。
它与旧局部 nominal 上界合起来仍要求 nominal=expression；本叶没有放松该 specialization。

## 精确反例与前轮义务

- `canonical_existence_not_positive`：F=1、gainCap=betaCap=1、qCap=2，C=-1 可分配，
  但预设 target=1 不可分配。有限域构造 canonicalTarget 不能自动产生正目标。
- `positive_canonical_not_arbitrary_target`：F=2、L=1，C=1>0，但预设 target=2 仍不可行。
- `negative_target_not_automatic`：F=0、L=2，C=-2；target=-1 虽为负，仍不可行。
- `missing_qCap_positive_counterexample`：F=nominal=2、gain=beta=1、qCap=1、target=1，
  正 allocation 成立；但实际 q=3，margin=2-3=-1。缺 q≤qCap 时不能推出目标。

符号与 nominal 方向仍由之前的精确反例独立约束：
`DualScaleComposition.negative_gain_counterexample` 与 `negative_residual_scale_counterexample`
展示负 gain/beta 破坏 cap 替换；`NominalDirectionAudit.wrong_direction_counterexample`
展示 nominal≤expression 与 expression allocation 不能推出 nominal allocation。
这些现有见证通过导入链可访问，本轮不重复证明。

错误 nominal 方向阻断的是当前 nominal allocation 路径；若另有真实 expression comparison
和 expression allocation，仍可能通过别的直接路径证明 margin，不能泛化为所有方法失败。

## 适用边界

所有实际 margin 消费仍限定在同一个 f.domain，finite coverage/source/metric/normalization
的绑定不由可行性代数产生。反例只是精确实数见证。
无 PSD、true-DH/source/coverage/admission/registry 升级。
新脚本与导入链尚未 elaboration/kernel 验证，`#print axioms` 未执行。
