# Body-6 tail：typed Schur 消元适配器

状态：**UNCOMPILED PROOF ATTEMPT**。未运行 Lean/Lake，未取得内核验证或 registry admission。

新增 `NEW_BODY6_SLICE_TAILSCHUR20260907.lean`（85 行），只直接导入
`NEW_BODY6_SLICE_TAILINVERSE20260907`。本叶消费既有左右逆和求解接口，新增任意外部块的类型对齐、两项有限和展开及证明接口打包；不重新推导逆块、PSD 或主子式。

## 维度、索引与自由外部块

| 对象 | Lean 类型 | 含义 |
| --- | --- | --- |
| `X` | `Fin r → Fin 2 → ℝ` | 任意 `r×2` 外部块 |
| `B,D` | `Fin 2 → Fin 2 → ℝ` | tail 块及显式逆块 |
| `Y` | `Fin 2 → Fin c → ℝ` | 任意 `2×c` 外部块 |
| `solvedRight Y` | `Fin 2 → Fin c → ℝ` | 对 `Y` 的每一列应用显式逆 |
| `schurCorrection X Y` | `Fin r → Fin c → ℝ` | 收缩结果 |

`r,c : ℕ` 独立，未要求相等或正值；外部空索引域按通常有限类型语义处理。
只有内部 `Fin 2` 两个槽位继承真实 tail 顺序 `0 ↦ 3`、`1 ↦ 4`。
这不构造从外部 `Fin r`／`Fin c` 到真实关节索引的映射。

`X/Y` 是任意实数组，不要求转置关系、非负性、对称性或真实 source 来源。
特别是本叶不实例化旧 mixed `3×2` 表，也不宣称当前 `X/Y` 等于任何 source cross block。

## Fin 2 有限和与两项表达

令

\[
d_0=\kappa+mh^2\sin^2z,\quad d_1=\kappa+mh^2,\quad
D=\operatorname{diag}(1/d_0,1/d_1).
\]

`schurCorrection` 定义为

\[
C_{ij}=\sum_{a\in\mathrm{Fin}\,2}\sum_{b\in\mathrm{Fin}\,2}
X_{ia}D_{ab}Y_{bj}.
\]

`correction_expansion_attempt` 尝试给出

\[
C_{ij}=\frac{X_{i0}Y_{0j}}{d_0}+\frac{X_{i1}Y_{1j}}{d_1}.
\]

`solvedRight` 对每列定义 `V[:,j] = inverseApply(Y[:,j])`，所以

\[
V_{0j}=Y_{0j}/d_0,\qquad V_{1j}=Y_{1j}/d_1.
\]

`correction_via_solve_attempt` 尝试证明 `Cij = ∑a Xia Vaj`。
这些只是展开同一显式倒数表的恒等式，不需要取消分母；在 Lean 中即使倒数按零分母全定义，它们也不自动成为有效消元证据。

## 具有前提的适配器

`TailEliminationAdapter ... : Prop` 是证明接口，六个字段分别保存：

1. 两个分母严格为正；
2. `B*D = I₂` 的全部逐项等式；
3. `D*B = I₂` 的全部逐项等式；
4. 对每个外部列 `j`，`B*V[:,j] = Y[:,j]`；
5. 上述两项显式收缩表达；
6. 收缩等于 `X` 作用于已求解列的有限和。

`tail_elimination_adapter_attempt` 显式要求 `kappa > 0`、`m ≥ 0`、`h² ≥ 0`，并直接调用旧
`denominators_positive_attempt`、`inverse_two_sided_attempt` 和 `inverse_solves_attempt` 来填写相关字段。
没有重做这些符号／逆矩阵证明，也没有用纯展开恒等式代替非零分母或求解义务。

## 实际 source seam

`source_tail_elimination_adapter_attempt` 将 `B` 取为真实 `sourceTail q`。
body 是 `(5 : Fin 6)`，即通常编号的 body-6；内部两列仍为有序 `{3,4}`。
`q : Fin 6 → ℝ` 任意，`z = q 4` 使用从 0 开始编号，`h = offset = 7/200`。

该构造器显式保留 `CenterOffsetTarget`、实际 `SourceWeightsTarget m kappa`、
`kappa > 0`、`m ≥ 0` 与 `offset² ≥ 0`。
它直接消费旧 `source_tail_inverse_interface_attempt` 中的两侧逆和任意实右端求解接口。
外部 `X/Y` 即使出现在此 source 构造器中，仍不获得 source 数值绑定。

本叶没有定义完整块矩阵或证明 Schur 补 PSD 等价性，也没有要求 `Y = Xᵀ`。
因此不能仅从这个适配器推出收缩结果半正定、完整 body-6 矩阵性质或消元后的完整系统正确性。

## 有限检查与开放边界

写入 sidecar 前运行一次内联 Python/SymPy 精确代数核对，以非零符号分母和任意单行／单列条目代表任意固定 `i,j`：

- `X*diag(1/p,1/r)*Y` 与两项分式的差为精确零。
- `X` 乘以显式已求解列与同一两项分式的差为精确零。
- 原对角块作用于已求解列后与原列的差为两个精确零。

该检查只核对独立转写的有限有理表达，不验证 Lean 类型检查、实际 source 或具体 cross-block 数值。
静态检查确认直接 import 文件存在，sidecar 未见 `sorry`、`admit`、`axiom` 或 `opaque`。

sidecar 实际字节 SHA-256：
`52226f5edd6f122e133413f469b207d50b625ffa7066b76ca7e69ec5f5841d8b`。

仅新增 sidecar 和本 REVIEW，未修改共享脚本、旧叶或 state/registry。
未运行 Lean/Lake；具体 cross-block source 绑定、完整 Schur PSD、完整 body-6、Fourier、coverage 和 registry admission 均不在本叶结论范围内。
