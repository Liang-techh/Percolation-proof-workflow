# P4：relative-plus-additive → 条件式 Schur/PMI absorption

日期：2026-09-07。新增 `NEW_P4_032_SchurPMIAbsorption.lean` 与本 review。
状态是 **UNCOMPILED bounded source-independent proof attempt**。
本轮不运行 Lean/Lake，不修改旧模块、共享脚本、state 或 registry。
未引入 sqrt、具体 source 参数或 source/coverage/admission/registry 结论。

## 输入与严格 gate

直接导入 `NEW_P4_032_RelativeAdditive`，使用其 `Parameters`、`EnvelopesAt`、
`rhoEff`、`biasEff` 及 force/accel 定理，不复制 weighted Cauchy、参数重排或旧 Schur identity。
以下记 `E=energy`、`rho=rhoEff p`、`B=biasEff p`。

`Slack p delta` 保存 `0<delta` 与 `rho+delta≤1`；
`strict_iff_positive_slack` 给出 `rho<1 ↔ ∃delta, Slack p delta`。
`exactSlack` 取 `delta=1-rho`。构造 slack 不含除法。
只有 `rho≤1` 不够：rho=1 没有正 slack，不能进行后面的除法或消元。

上游参数包保留正权重及其 reciprocal gate、tau 的非负性与 tau²，
以及 rhoA/kappaD/kappaB/biasD/biasB 的非负性。
`EnvelopesAt` 保留 E/ED/EB 非负与两条 affine defect envelope。
新标量 `AbsorbedAt` 还显式保留 q≥0；typed 分支中 q 为 `||rB||₂²`。

## Schur/PMI 余量消费者

`absorb_relative_additive` 消费已经提供的

```text
q ≤ rho*E+B,  E≥0, q≥0, delta>0, rho+delta≤1
```

得到 `delta*E-B ≤ E-q`，保留 additive debit。
`SchurPMIBinding` 另要求同一点的归一化标量比较 `E-q≤margin`，
`schur_pmi_margin` 才能输出 `delta*E-B≤margin`。
`schur_pmi_nonnegative` 需要额外的 `B≤delta*E` 才推出 `margin≥0`。
正 slack 本身不使含 B 的余量自动非负，也不使整块矩阵自动 PSD。

这个绑定是待调用者证明的下界，不是本文件证明的 Schur 恒等式。
若实际表达式含未控制的交叉项、其他 residual、非单位能量系数或放大因子，
必须先证明对应比较或统一归一化。例如 residual 被乘以 c≥0 时，
需要控制 c*rho 的吸收 gate 和 c*B 的 additive 项；不能仅检查原 rho<1。

## 最终 affine budget 的额外闭合条件

residual 上界不能单独推出 E 的上界。
`FeedbackBinding` 显式要求 `base≥0` 和 **`E≤base+q`**。
它与 Schur/PMI 下界是两个独立可选消费者；文件没有从一个推导另一个。

`close_affine_budget` 在此闭合条件下给出：

```text
delta*E ≤ base+B
delta*q ≤ rho*base+B
E ≤ base/delta+B/delta
q ≤ (rho/delta)*base+B/delta
```

q 的第二条使用 rho≥0、B≥0 和 rho+delta≤1；不会漏掉 additive 项。
`close_of_strict` 直接从原 relative budget 和 rho<1 取 delta=1-rho，
从而得到 `E≤(base+B)/(1-rho)` 与 `q≤(rho*base+B)/(1-rho)` 的 affine 写法。
所有除法都在明确的 delta>0 后出现，不包含 sqrt。

`residual_allocation` 提供 division-free 的最终 allowance 消费：
若 available≥0 且 `rho*base+B≤delta*available`，则 q≤available。
部分非负字段为语义契约保留，单条代数蕴涵不一定使用所有字段。

## Force/accel typed 路径

`force_absorption` 调用上游 `force_relative_additive`，保留
`DistalForceDefect`、`forceTerm MBD J eD` 与 `ActionBound (MBD*J) tau`。
`accel_absorption` 调用 `accel_relative_additive`，保留
`DistalAccelDefect`、`accelTerm MBD eD` 与 `ActionBound MBD tau`。
两者要求原来的精确 residual identity、port bound、ED/EB 平方预算和 envelopes，
输出 `AbsorbedAt p E (||rB||₂²) delta`，随后可分别接到
`schur_pmi_margin` / `schur_pmi_nonnegative` 或 `close_affine_budget`。
没有添加 convention adapter，也没有把两种 distal 缺陷类型混用。

## 验证与剩余边界

仅进行文件/接口与纸面代数检查，未运行 Lean、Lake、kernel 或 `#print axioms`。
导入链也沿用未编译状态；无 sorry/axiom 占位不代表 elaboration 或 kernel 已通过。
未来仍需核查 Lean elaboration、定理 API 与公理依赖。

实际使用还需在同一状态、域、energy/metric、regularizer/key、归一化下证明
上游预算、严格 slack 与所选择的 downstream 绑定。
点态接口没有域覆盖量词；固定参数的全域有效性需要独立的全域证据。
此 sidecar 不识别部署 source，不证明 continuous-PDE、coverage、admission 或注册结果。
