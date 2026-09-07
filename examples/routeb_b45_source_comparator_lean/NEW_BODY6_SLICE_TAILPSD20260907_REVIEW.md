# Body-6 tail：半正定与最小对角下界 sidecar

状态：**UNCOMPILED PROOF ATTEMPT**。未运行 Lean/Lake，未取得内核验证或 registry admission。

新增 `NEW_BODY6_SLICE_TAILPSD20260907.lean`（92 行），只直接导入已完成的
`NEW_BODY6_SLICE_MASSTAIL_Source20260907`。本叶消费已有精确 tail 表，新增二次型非负与最小对角下界接口；不重做加权 Gram、DH 几何或其他矩阵块。

## 范围与前提

- 实际 body 为 `(5 : Fin 6)`，即从 1 开始编号的第 6 刚体。
- 继承 `tailJoint` 的真实顺序 `0 ↦ 3`、`1 ↦ 4`，两行两列均按此顺序。
- source 配置是任意 `q : Fin 6 → ℝ`；标量角度 `z = q 4` 使用从 0 开始的下标。
- 半正定接口显式要求 `kappa > 0`、`m ≥ 0`、`h² ≥ 0`。
- source 结论还显式要求 `CenterOffsetTarget`、`SourceWeightsTarget m kappa`，并将平方前提特化为 `offset² ≥ 0`。
- `h² ≥ 0` 虽可由实数平方非负推出，仍按请求保留。代数下界与最小对角恒等式本身不需要 `kappa > 0`；PSD 与上层 source 接口保留该前提。

## 新数学内容

令 `a = m h²`、`u = sin² z`。已有表为

\[
B=\begin{pmatrix}\kappa+au&0\\0&\kappa+a\end{pmatrix}.
\]

本叶定义有限实二次型

\[
Q_B(x)=\sum_{i,j\in\mathrm{Fin}\,2}x_iB_{ij}x_j,
\quad N(x)=x_0^2+x_1^2,
\]

并尝试证明以下三个接口。

1. **二次型显式下界**：
   \[
   Q_B(x)=\kappa N(x)+mh^2(\sin^2z\,x_0^2+x_1^2)
   \ \ge\ \kappa N(x).
   \]
   非负余项由 `m ≥ 0`、`h² ≥ 0` 和实数平方非负逐项得到，保留全部 `h²` 修正。

2. **半正定性**：`TailPSD B` 定义为 `B` 对称且对所有实向量 `x` 有 `Q_B(x) ≥ 0`。
   对称性复用原表接口；二次型非负由上述下界和 `kappa > 0` 推出。
   这是明确的有限实矩阵 PSD 定义，没有声称已接到 Mathlib 的 `Matrix.PosSemidef` API。

3. **精确最小对角项及其下界**：
   \[
   \min(B_{00},B_{11})=\kappa+mh^2\sin^2z\ge\kappa.
   \]
   `sin² z ≤ 1` 来自 `sin² z + cos² z = 1` 和 `cos² z ≥ 0`。
   结合 `mh² ≥ 0` 得到第一项不大于第二项，因此最小对角表达式是确定的。
   本叶不把该表达式命名为完整 body-6 矩阵的最小特征值。

对应定理尝试为 `quadratic_decomposition_attempt`、`quadratic_lower_attempt`、
`tail_psd_attempt`、`min_diagonal_exact_attempt` 和 `min_diagonal_lower_attempt`。

## 实际 source seam

`sourceTail q` 定义为
`sourceBodyMass q 5 (tailJoint i) (tailJoint j)`，没有另设候选矩阵替代实际 source。

`source_tail_eq_attempt` 从 `CenterOffsetTarget` 和实际权重绑定消费已有
`source_weighted_tail_attempt`，连接 `sourceTail q` 与 `explicitTail (q 4) offset m kappa`。

`source_tail_psd_bounds_attempt` 在保留中心偏移、权重绑定、`kappa > 0`、`m ≥ 0`、
`offset² ≥ 0` 的同时，返回以下合取：实际 tail 半正定、全部实向量的 `kappa` 二次型下界、最小对角项至少 `kappa`、以及该最小对角项的精确公式。

权重仍绑定实际 `routeBMass 5` 与 `routeBInertiaScalar 5`，即 `3/20` 和已除惯量 `1/60`；没有构造无条件权重或中心偏移见证，没有添加正则项。

## 有限检查与证据限制

写入 sidecar 前执行一次内联 Python/SymPy 精确代数核对：

- `Q − kappa*(x²+y²) − a*(u*x²+y²)` 展开为精确零。
- 两个对角项之差减去 `a*(1−u)` 展开为精确零。

符号核对只验证两条独立转写的代数分解，不是自动不等式证明。
非负条件 `a ≥ 0`、`0 ≤ u ≤ 1` 由上面的数学推导说明，并在 Lean proof attempt 中写明；Python 检查不替代 Lean 证明项。

静态检查确认直接 import 文件存在，sidecar 未见 `sorry`、`admit`、`axiom`、`opaque`。
没有运行 Lean/Lake，没有检查依赖闭包的内核公理，没有重新运行 Gram/Fourier 旧检查或共享脚本。

sidecar 实际字节 SHA-256：
`bb18ff316f6cf0193ccca504577703b6d308638d9430365b5cb7a8e9b0fbf38d`。

## 保持开放

本叶只涉及有序 `{3,4}` 的 `2×2` tail；不能由这个主子块的非负性推出完整 body-6 矩阵半正定。
没有声称完整矩阵、Fourier、coverage、Lean 编译或 registry admission。
仅新增 sidecar 与本 REVIEW，未修改共享脚本、既有叶或准入状态。
