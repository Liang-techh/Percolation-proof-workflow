# Body-6 tail：显式对角逆块与作用接口

状态：**UNCOMPILED PROOF ATTEMPT**。未运行 Lean/Lake，未取得内核验证或 registry admission。

新增 `NEW_BODY6_SLICE_TAILINVERSE20260907.lean`（100 行），仅直接导入
`NEW_BODY6_SLICE_TAILMINORS20260907`。本叶消费已有正主子式，新增显式倒数表、左右逆、逐项非负和求解作用接口；不重新证明 PSD、最小对角或主子式正性。

## 显式逆块与顺序

令

\[
d_0=\kappa+mh^2\sin^2z,\qquad d_1=\kappa+mh^2,
\qquad B=\operatorname{diag}(d_0,d_1).
\]

`inverseTail` 明确写出

\[
D=\begin{pmatrix}1/d_0&0\\0&1/d_1\end{pmatrix}.
\]

source 中 `z = q 4`，`h = offset = 7/200`，继承 `tailJoint` 的顺序 `0 ↦ 3`、`1 ↦ 4`。
实际 body 为 `(5 : Fin 6)`，即通常编号的 body-6。`q : Fin 6 → ℝ` 任意；所有下标均按 Lean 从 0 开始编号。

两个倒数保留完整 `m*h²` 项，特别是第一分母中的 `sin²(q 4)`。没有把两个分母混同或交换列顺序。

## 前提与新接口

`denominators_positive_attempt` 在 `kappa > 0`、`m ≥ 0`、`h² ≥ 0` 下，直接提取已有
`tail_principal_positive_attempt` 的两个一阶主子式正性，得到 `d0 > 0`、`d1 > 0`。
继而取得非零分母，避免把 Lean 对零倒数的全定义约定误当成有效逆矩阵证据。

`product2` 使用两个索引上的有限求和定义矩阵乘法；`identity2` 为 Kronecker 单位表。
`inverse_two_sided_attempt` 尝试逐项证明 `B*D = I₂` 和 `D*B = I₂`。
因此该对象的逆含义由左右乘积恒等式说明，不依赖未建立的 `Matrix.inv` API 适配。

`inverse_entries_nonnegative_attempt` 在同样符号前提下，尝试证明全部四项 `Dij ≥ 0`。
对角项使用正分母，两个非对角项是显式零。
本叶选择给出逐项非负和精确作用接口，没有另行声明算子范数或特征值上界。

对于任意实右端向量 `x : Fin 2 → ℝ`，定义

\[
\operatorname{inverseApply}(x)=(x_0/d_0,\ x_1/d_1).
\]

`inverse_action_formula_attempt` 尝试证明此向量等于 `action2 D x`；
`inverse_solves_attempt` 在上述符号前提下尝试证明

\[
B\,\operatorname{inverseApply}(x)=x.
\]

右端 `x` 不需要逐项非负。逆矩阵逐项非负不意味着它对任意有符号向量的结果逐项非负。
作用表达本身是实数恒等式；它作为有效求解公式的结论仍要求正性前提。

## 实际 source 与 Schur 使用边界

`source_tail_inverse_interface_attempt` 通过已有 `source_tail_eq_attempt` 将两侧矩阵替换为实际
`sourceTail q = sourceBodyMass q 5 (tailJoint i) (tailJoint j)` 的子块。
它完整保留：

- `CenterOffsetTarget`；
- `SourceWeightsTarget m kappa`，绑定实际质量与已除惯量；
- `kappa > 0`、`m ≥ 0`、`offset² ≥ 0`。

返回的合取为左右逆、全部逆元素非负，以及所有实右端向量的求解等式。
没有构造无条件中心或权重见证，也没有加入正则项。

这些接口可供后续 Schur 消元引用 tail 可逆性和求解操作。本叶没有组装其他矩阵块、计算 Schur 补、证明消元等价性或宣称完整 body-6 矩阵可逆。

## 有限检查及其限制

在写入 sidecar 前，运行一次内联 Python/SymPy 精确代数检查，以非零自由分母 `p,r` 构造对角块及倒数块：

1. 左逆乘积减去单位矩阵，四个余项均为精确零。
2. 右逆乘积减去单位矩阵，四个余项均为精确零。
3. 原块作用于 `(x/p,y/r)` 后减去 `(x,y)`，两个余项均为精确零。

这只核对独立转写的有限有理恒等式，分母正性的依据来自继承的主子式前提；不验证实际 source 或 Lean tactic。
未运行旧 PSD、最小对角、主子式或 Fourier 检查，也未修改共享检查脚本。

静态检查确认直接 import 文件存在，sidecar 未见 `sorry`、`admit`、`axiom` 或 `opaque`。
没有运行 Lean/Lake，没有执行依赖闭包或内核公理审计。

sidecar 实际字节 SHA-256：
`bd681202326a1e2d3e33793e578869b9fd32b7c0de259f515cd242fa6dbf0c2c`。

本次只新增 sidecar 和本 REVIEW。完整 body-6、特征值、Fourier、coverage、编译与 registry admission 均不在结论范围内。
