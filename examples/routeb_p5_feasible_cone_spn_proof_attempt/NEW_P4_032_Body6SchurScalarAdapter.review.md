# P4：BODY6 Schur margin → scalar comparison 最小 adapter

日期：2026-09-07。新增 `NEW_P4_032_Body6SchurScalarAdapter.lean` 与本 review。
**UNCOMPILED bounded proof attempt**；仅静态/纸面审阅，未运行 Lean/Lake 或大回归。
未修改原 BODY6/P4 模块或共享脚本。

## 已核对的真实输入类型

直接导入 `NEW_BODY6_SLICE_SCHURMARGIN20260907`，其文件位于
`examples/routeb_b45_source_comparator_lean/`；同时导入现有 `ResidualMarginConsumer`。
未来编译必须同时解析这两个目录及各自导入链；本轮未配置或验证模块搜索路径。

BODY6 的 `RemainderMargin R mu` 实际是：

```text
R 对称，mu≥0，
∀v : Fin 3 → ℝ, mu*Σᵢvᵢ² ≤ Σᵢvᵢ*(frontAction R v)ᵢ。
```

它本身含外部提供的二次型下界证据。adapter 只消费这一证据，
不从 source 块恒等式、residual norm 或 solver 状态构造它。
原字段允许 mu=0，不自动提供正 mu。

BODY6 front 是三维，既不等于 P4 二维 port，也不等于 source 配置向量。
新接口把 front 向量与 P4 的标量 residual 分别保留，未构造隐式维度映射。
这里的 residual q 指 `f.residual x`，不是 BODY6 source API 中的六维配置参数 q。

## 明确的 residual、normalization、nominal 与 target 关系

`RemainderField` 保存逐点 R、mu、front 向量 v、scale 与 offset。
记 N=Σᵢvᵢ²、Q=vᵀRv；`ScalarBridgeEvidence f d m` 显式要求同域：

```text
RemainderMargin R mu
scale≥0，gain≥0
nominal ≤ offset + scale*(mu*N)
offset + scale*Q - gain*q ≤ margin。
```

nominal 可以保守；若调用者想取 nominal=offset+scale*mu*N，可用该等式证明对应前提，
但接口不自动认定任何现有 nominal 采用这种定义。
最后一行是**外部 normalization/comparison premise**，不是从 RemainderMargin 推出的恒等式。
它必须真正连接所选 BODY6 二次型、同一个 P4 residual 和目标 scalar margin，
计入所有坐标、度量、单位、变换与交叉项；不提供该证明就不能构造 adapter 证据包。

`toSchurPMIComparison` 直接调用 `(remainder_margin x hx).2.2 (front x)`，
将 mu*N≤Q 按非负 scale 缩放，再组合两条外部比较，输出旧类型要求的
`nominal-gain*q≤margin`。
没有重证 Schur identity、矩阵 PSD、contraction 或参数桥。

最终 `conditional_body6_scalar_margin` 另外接收原 `LocalEvidence`、`UniformParameters`、
`UniformEnergyCap`、`ResidualAllowance` 和 `MarginAllocation`。
target 的关系仍明确要求 `target+gain*qCap≤nominal`，随后只调用旧 `conditional_margin`，
输出 `∀x∈domain, target≤margin(x)`。
target 不自动等于 mu；标量 margin 也不自动等于矩阵最小特征值。

## Comparison 与 normalization obstruction

- **缺 comparison**：RemainderMargin 只约束 Q，不能约束一个未连接的目标 scalar margin。
  `missing_comparison_witness` 取 lower=quadratic=1、q=0、gain=1、targetMargin=-1，
  quadratic lower bound 仍成立，但目标比较失败。它是精确标量逻辑反例，不是物理 source 实例。
- **缺 scale 符号**：`negative_scale_witness` 取 lower=1、quadratic=2、scale=-1，
  缩放后 -2<-1，不能维持 lower-bound 方向。scale=0 虽允许代数传递，却不保留正二次型贡献；
  若声称可逆物理归一化或正贡献，需要额外正性/可逆证据。
- **缺 metric/normalization 身份**：非负 scale 不等于证明归一化正确。
  非标量变换、不同 energy metric 或 Fin 3 与 Fin 2 的关系，必须由外部比较覆盖，不能默认相同。
- **缺 nominal/target allocation**：即使 comparison 成立，仍不能自动把 mu 提升为目标 margin。
  rho/bias/feedback/cap 缺口继续由原消费者的显式前提阻断。
- **缺 source/coverage**：R 可以是抽象矩阵；此 adapter 不证明它就是实际 Schur remainder，
  也不提供 true-DH、K-path 或域覆盖。结论只对提供全部证据的 f.domain 成立。

这些 obstruction 表示条件尚未满足，不等价于原矩阵非 PSD、模型不稳定或其他方法不可用。
外部 RemainderMargin 的二次型正性不会被包装成新的无条件完整矩阵 PSD 声明。
无真实参数闭合、source/coverage/admission/registry 成功结论。
新声明与证明无变量除法或 sqrt；导入链和新脚本的 elaboration/kernel 检查均未执行。
