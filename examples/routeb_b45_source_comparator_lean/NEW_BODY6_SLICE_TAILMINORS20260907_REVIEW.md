# Body-6 tail 主子式／行列式接口

状态：**UNCOMPILED PROOF ATTEMPT**。未运行 Lean/Lake，不声明编译通过、内核验证或 registry admission。

新增 `NEW_BODY6_SLICE_TAILMINORS20260907.lean`（89 行），直接导入
`NEW_BODY6_SLICE_TAILPSD20260907`，复用既有加权表、实际 source 绑定与显式 `TailPSD` 定义。
本叶只新增三个非空主子式的表达／符号证据及到对角 PSD 判据的连接；不重推此前的 `kappa` 二次型下界或最小对角定理。

## 三个主子式

对于任意实数 `z,h,m,kappa`，令

\[
d_0=\kappa+mh^2\sin^2z,\qquad d_1=\kappa+mh^2,
\qquad B=\operatorname{diag}(d_0,d_1).
\]

| 有序 tail 局部索引集合 | 对应实际关节索引 | 非空主子式 |
| --- | --- | --- |
| `{0}` | `{3}` | `d0 = kappa + m*h²*sin²(z)` |
| `{1}` | `{4}` | `d1 = kappa + m*h²` |
| `{0,1}` | `{3,4}` | `d0*d1` |

`det2 B` 明确定义为 `B00*B11 − B01*B10`。已有两个交叉项均为零，因而

\[
\det_2 B=(\kappa+mh^2\sin^2z)(\kappa+mh^2).
\]

`tail_principal_formulas_attempt` 将两项一阶主子式与上述行列式公式共同给出。
这里使用显式 `2×2` 标量行列式定义，尚未声明 `Matrix.det` API 适配证明。
没有以行列式代替任何完整矩阵或特征值结论。

## 条件式严格正性

`tail_principal_positive_attempt` 明确保留
`hk : 0 < kappa`、`hm : 0 ≤ m`、`hh : 0 ≤ h²`。
由 `m*h² ≥ 0` 及 `sin² z ≥ 0` 得到 `d0 ≥ kappa > 0` 与 `d1 ≥ kappa > 0`，
再由正数乘积得到 `det2 B > 0`。

`StrictPrincipalMinors B` 精确表示两个一阶主子式与行列式均严格为正；
`strict_to_nonnegative_attempt` 将它连接到三个主子式均非负的 `PrincipalMinorCriterion B`。
没有额外假定 `m > 0`、`h ≠ 0` 或 `sin z ≠ 0`；严格正性由 `kappa > 0` 提供。

## PSD 判据连接的边界

`diagonal_minor_criterion_to_psd_attempt` 消费：

- `B01 = 0`；
- `B10 = 0`；
- `PrincipalMinorCriterion B`。

它返回既有 `TailPSD B`，即对称性加所有实向量上的二次型非负。
两个零交叉项给出对称性，并使二次型化为 `B00*x0² + B11*x1²`；
两个一阶主子式的非负性即可使该和非负。
对这个明确限定的对角类，行列式非负条件是冗余的，但作为完整主子式接口保留。

这不是任意非对称矩阵的主子式判据；单有正行列式也没有被当作 PSD 证据。
新连接只做上述有限对角判据的转换，没有重推已有带权平方余项、二次型定量下界或最小对角公式。

`tail_minor_psd_interface_attempt` 将严格主子式、非负主子式判据与 `TailPSD` 合并为一个条件式接口。

## 真实 source seam

`source_tail_minors_attempt` 消费已有 `source_tail_eq_attempt`。
实际 body 为 `(5 : Fin 6)`，即通常编号的 body-6；继承 `tailJoint` 的真实顺序 `0 ↦ 3`、`1 ↦ 4`。
`q : Fin 6 → ℝ` 任意，`z = q 4` 使用从 0 开始编号的第五个关节角。

该 source 接口明确保留 `CenterOffsetTarget`、`SourceWeightsTarget m kappa`、
`kappa > 0`、`m ≥ 0` 与 `offset² ≥ 0`。
权重继续绑定实际 body-6 的质量与已除惯量；中心和权重见证没有被无条件构造。

返回内容为实际 tail 的行列式精确乘积、三个主子式严格正性、非负主子式判据和条件式 PSD。
没有声称其他关节列、完整 body-6 矩阵或其特征值性质。

## 有限检查

在写入 sidecar 前，执行一次内联 Python/SymPy 精确代数核对，令 `a = m*h²`、`u = sin² z`：

1. 对角矩阵的符号行列式与 `(kappa+a*u)*(kappa+a)` 的展开差为精确零。
2. 行列式与 `kappa² + kappa*a*(1+u) + a²*u` 的展开差为精确零。

严格正性的依据是前述实数符号推导；符号展开本身不构成 Lean 不等式证明。
没有重新运行 Gram、二次型下界、最小对角或 Fourier 检查。

静态检查确认直接 import 文件存在，sidecar 未见 `sorry`、`admit`、`axiom` 或 `opaque`。
这不证明 tactic 能通过编译，也不构成依赖闭包或内核公理审计。

sidecar 实际字节 SHA-256：
`90686f7fcd2ac9701ca9e1d32816667d0b106527b61c9022a3788154aa335c8e`。

仅新增 sidecar 与本 REVIEW；没有修改共享脚本、旧数学叶、state 或 registry。
Fourier、coverage、编译与准入边界全部保持开放／fail-closed。
