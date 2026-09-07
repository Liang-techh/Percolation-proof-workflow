# P4 dual-scale 的 domain-uniformization

日期：2026-09-07。状态：**OPEN_UNCOMPILED**。
新增 `NEW_P4_032_DualScaleUniformization.lean` 与本 review。
仅静态/纸面审阅；不运行 Lean/Lake 或大回归，不修改旧模块、共享脚本或 registry。

## 有限域到底能提供什么

`finite_lower_upper` 给任意实值函数在固定 Finset 上的共同有限下界/上界；
`finite_four_envelope` 用乘积有限集同时覆盖 alpha、beta、gain、q 四个槽。
若四个槽非负，可用共同下界 0 和一个共同有限上界。
`finite_positive_floor` 在额外逐点 alpha>0 前提下给出严格正共同下界，
复用旧 `finite_strict_majorant`，不重复其有限域证明。
仅有 alpha≥0 不保证正下界，例如域内 alpha=0 的点会阻断它。

有限性只保证这些实数界存在，不证明 normalization、nominal 或目标 allocation 成立，
也不声称这些界最优或可用于预先指定的正 target。
若 domain 由一个有限枚举表示，仍须证明 `f.domain x ↔ x∈cells`（或所需包含方向），
才能将有限集结论用在目标域。一个有限网格不覆盖网格之间的连续配置。

## Uniform contract 与正确的方向

记 L(x)=mu(x)*Σvᵢ(x)²，alpha 为 front scale，beta 为 residual scale。
`UniformData f d m s` 保存同域：

```text
0≤alphaFloor≤alpha(x)，0≤frontFloor≤L(x)，offsetFloor≤offset(x)，
0≤beta(x)≤betaCap，0≤gain(x)≤gainCap，0≤q(x)≤qCap。
```

beta/gain 的逐点非负性继续由原 `CompositionContract` 提供；各 cap 非负显式保留。
alpha 用于正 front 贡献，所以消费者需要下界；beta/gain/q 用于扣减项，所以需要上界。
alpha 的上界虽在有限域上存在，但本单侧 margin 公式不需要它。
frontFloor 可为零；若想得到正贡献，必须另证相应严格正性。
offsetFloor 可以是任意实数。

还有一条不能省略的 **nominal_realization**：

```text
offset(x)+alpha(x)*L(x) ≤ nominal(x)。
```

旧局部契约只给相反方向 `nominal≤offset+alpha*L`，不能用它推出 nominal 下界。
新前提与旧上界合起来要求这里的 nominal 实际等于该表达式；
这是一种明确、充分的 specialization，不是假定所有旧 nominal 都能无条件接入。
若实际 nominal 更保守，需要独立证明它自己的统一下界，而不能直接套用此构造器。

对同一个 target 再要求唯一的 uniform allocation：

```text
target + gainCap*(betaCap*qCap) ≤ offsetFloor + alphaFloor*frontFloor。
```

`uniformTargetAllocation` 通过非负乘法的上下界替换，把它转成每点原有 TargetAllocation；
`uniformCapEvidence` 只打包同一个 qCap；`uniformized_scalar_margin` 调用旧
`composed_scalar_margin`，输出域内 target≤margin。
局部 BODY6 remainder、scale binding、normalization comparison 与全部符号条件
仍通过原 CompositionContract 显式传递，没有重证或放松局部 composition。

## 无限域精确反例

复用前轮精确 dyadicGap(n)=0.5^n、dyadicEnergy(n)=2^n 及其已写证明接口，
不重新展开旧增长/收缩证明；0.5 是精确实数常量。

1. `no_positive_dyadic_floor`：alpha_n=0.5^n 每点严格为正，但没有共同正下界。
   可令 L=Q=1、offset=0、gain=beta=q=0、nominal=margin=alpha_n；
   normalization 与局部组合关系成立，却不能保证任何统一正 target。
   共同非负下界 0 仍存在，不能把“无正下界”说成“无任何下界”。
2. `no_dyadic_upper`：将 beta、gain 或 q 中任一个槽设为 2^n，便没有共同有限上界；
   每点取值仍有限且非负。这不是说每个无限域函数都无界。
3. `infinite_margin_counterexample`：alpha=L=Q=g=q=1、offset=0、beta_n=2^n，
   nominal=1、margin_n=1-beta_n。normalization comparison 等号成立，qCap=1 也存在，
   但任意统一 target 都被某点击败。将增长槽换成 gain 或 q，标量表达式相同；
   q 增长的版本当然没有统一 qCap。

最后一个反例保留非负性和精确 normalization，但目标 allocation 对足够大的 n 失败；
它没有声称在完整 uniform contract 与 allocation 都成立时结论会失败。
反例是在无限域 N 上；每个固定有限截断仍能取相应界，但这些界可随截断变化。

## 范围与检查状态

这些是实数预算与条件式 scalar margin 结论，不是实际 true-DH/BODY6 source 见证。
缺少 domain coverage、源参数绑定或 metric/normalization 身份时不能补成真实模型结论。
也不声称各独立 uniform 界是所有方法的必要条件：例如 gain*beta*q 整体有界、
各项关联补偿或独立 nominal 下界，可能支持其他更紧的充分接口。

没有变量除法、sqrt、PSD 或 source/coverage/admission/registry 升级。
新脚本与导入链的 elaboration/kernel、公理检查未运行，`#print axioms` 只是未来入口。
