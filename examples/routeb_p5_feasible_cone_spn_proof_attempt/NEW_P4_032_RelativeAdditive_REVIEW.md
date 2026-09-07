# P4：weighted budget → relative-plus-additive 参数接口

日期：2026-09-07。新增 `NEW_P4_032_RelativeAdditive.lean` 与本 review。
**未编译的 bounded source-independent proof attempt**；未运行 Lean/Lake，未修改旧文件、
state 或共享脚本，未引入 sqrt、数值实例、source/coverage/registry/admission 结论。

## 参数与重排

`Parameters` 保存前轮 `Weights`（正权重及倒数和 gate），并明确要求
`rhoA,tau,kappaD,kappaB,biasD,biasB≥0`。
`EnvelopesAt p energy ED EB` 另保存 `energy,ED,EB≥0` 及同一 energy 上的两条前提：

```text
ED ≤ kappaD*energy+biasD，
EB ≤ kappaB*energy+biasB。
```

ED/EB 始终是平方预算。定义的有效系数为：

```text
rho_eff = λu*rhoA + λD*tau²*kappaD + λB*kappaB，
B_eff   = λD*tau²*biasD + λB*biasB。
```

`affine_budget_identity` 是显式参数代入后的环恒等式；
`weighted_budget_le_relative_additive` 使用权重正性及 tau²≥0 代入上述两条不等式，得到：

```text
λu*rhoA*energy + λD*tau²*ED + λB*EB
  ≤ rho_eff*energy + B_eff。
```

tau² 保留在 distal 的 relative 与 additive 两项中，没有遗漏或重复平方。
`effective_coefficients_nonnegative` 与 `relative_additive_budget_nonnegative`
分别给出有效系数和总预算的非负性。energy/ED/EB 的显式非负字段继续保留在契约中，
虽然单纯代入重排不需要每一个符号条件。

`consume_weighted_budget` 将已证明的 `q≤weightedBudget` 接到此结果，q 可取
前轮的 `||rB||₂²`。没有重新证明三项 Cauchy、三角不等式或 convention adapter。

## 两个 typed consumer

`force_relative_additive` 实际调用前轮 `force_defect_budget`，保留
`DistalForceDefect`、`forceTerm=(MBD*J)*eD`、`ActionBound (MBD*J) tau`。

`accel_relative_additive` 实际调用 `accel_defect_budget`，保留
`DistalAccelDefect`、`accelTerm=MBD*eD`、`ActionBound MBD tau`。

两者都要求各自精确的 `rB=u+v+w`、port energy 上界及 ED/EB 平方上界；输出同一形式
`||rB||₂²≤rho_eff*energy+B_eff`。相同公式不使两种 defect 类型或作用界可以互换。
所有范数沿用前轮 Euclidean ℓ₂，所有分量应已在同一 B generalized-force 坐标中。

`zero_bias_corollary` 仅在明确提供 `biasD=biasB=0` 时删掉 B_eff；它不声称这是
B_eff=0 的必要条件，也不因 source-independent 参数化就自动得到纯 relative 结论。

## 精确剩余前提

需要为同一 source 状态、metric/energy、regularizer/key、域和 normalization 提供
实际权重、port coefficient、作用界、两个 defect 平方预算及其 affine envelopes。
本文件没有从某个样本或其他域推断这些前提，也没有识别实际部署 residual 类型。
若要全域使用，需要对同一域内每点提供这些绑定，并证明所选参数对该域统一有效。

新文件及前轮导入链尚需 elaboration/kernel 与公理检查；所有 `#print axioms` 均未执行。
有效预算本身不证明 downstream absorption、source/coverage 或任何注册条件。
