# Body-6 tail：A − X·inverseTail·Y 系数与求值接口

状态：**UNCOMPILED PROOF ATTEMPT**。未运行 Lean/Lake，不声明内核验证或 registry admission。

新增唯一命名的 `NEW_BODY6_SLICE_SCHURREMAINDER20260907.lean`（92 行）及本同名 `.review.md`。
直接依赖 `NEW_BODY6_SLICE_TAILSCHUR20260907`，由其继承 `TAILINVERSE` 接口。
本叶在已有收缩量上明确加入外部块 `A` 和减法，不重新推导逆矩阵或做大回归。

## 类型与逐项系数

`A : Fin r → Fin c → ℝ`，`X : Fin r → Fin 2 → ℝ`，`Y : Fin 2 → Fin c → ℝ`。
外部 `r,c : ℕ` 独立；结果为 `r×c`。没有要求外部块方阵、对称、转置配对或非负。
内部 `Fin 2` 槽位继承真实 tail 顺序 `0 ↦ 3`、`1 ↦ 4`，没有给外部索引建立关节编号映射。

令

\[
d_0=\kappa+mh^2\sin^2z,\qquad d_1=\kappa+mh^2,\qquad
D=\operatorname{diag}(1/d_0,1/d_1).
\]

`schurRemainder` 明确定义

\[
R_{ij}=A_{ij}-\sum_{a\in\mathrm{Fin}\,2}\sum_{b\in\mathrm{Fin}\,2}X_{ia}D_{ab}Y_{bj}.
\]

`remainder_coefficient_attempt` 消费旧两项收缩展开，尝试证明

\[
R_{ij}=A_{ij}
-\frac{X_{i0}Y_{0j}}{\kappa+mh^2\sin^2z}
-\frac{X_{i1}Y_{1j}}{\kappa+mh^2}.
\]

这里的“系数”是矩阵条目表达，不是 Fourier 系数或覆盖凭据。
两个负号及两列各自分母均显式保留。

## 求解列与矩阵乘法一致性

`solved_column_product_attempt` 直接消费已有 `inverse_action_formula_attempt`，得到

\[
V[:,j]=\operatorname{solvedRight}(Y)[:,j]=D\,Y[:,j].
\]

新定义 `remainderViaSolve` 为 `Aij − ∑a Xia Vaj`，
`remainderViaProduct` 为 `Aij − ∑a Xia (action2 D Y[:,j])a`。
后者的 `action2` 是旧叶定义的实际 `Fin 2` 矩阵乘向量有限和。

`remainder_paths_attempt` 尝试证明 `schurRemainder` 逐项同时等于这两种表达。
因此双重有限和、两项分式、先求解每列再收缩、先计算矩阵乘向量再收缩四种写法在本表达接口中对齐。

上述纯代数恒等式没有取消分母，故不需要正性前提；不能由此直接宣称某个零分母情况下仍有合法的逆或消元。

## 保留消元前提的契约

`SchurRemainderContract ... : Prop` 保存三部分：

1. 完整的已有 `TailEliminationAdapter`，包含两个分母正性、左右逆和 `B*V[:,j]=Y[:,j]`；
2. 每个结果条目的两项分式系数；
3. 每个结果条目的 solve-column 与 matrix-action 两种求值等式。

`remainder_from_adapter_attempt` 消费一个真实证明项 `ha` 来构造此契约；不以纯代数展开或 Python 检查代替逆矩阵／列求解前提。
一般参数 `h,m,kappa` 的合法适配器可由旧 `tail_elimination_adapter_attempt` 在
`kappa > 0`、`m ≥ 0`、`h² ≥ 0` 下提供。本叶没有重新证明这些条件下的 tail 性质。

## 实际 source 的范围

`source_remainder_contract_attempt` 消费旧 `source_tail_elimination_adapter_attempt`。
它明确保留 `CenterOffsetTarget`、实际 `SourceWeightsTarget m kappa`、
`kappa > 0`、`m ≥ 0`、`offset² ≥ 0`。

只有内部 `B = sourceTail q` 接到实际 body-6：body 索引为 `5`，真实关节列顺序为 `{3,4}`。
`q : Fin 6 → ℝ` 任意，`z = q 4` 使用从 0 开始编号，`h = offset = 7/200`。

**未闭合的 source 边界**：`A/X/Y` 仍是任意外部输入，不具备实际完整矩阵块的 source 绑定。
没有实例化具体 mixed 块，也没有构造中心偏移或权重绑定的无条件见证。
没有声称完整 Schur PSD、全系统消元等价性、完整 body-6 矩阵或特征值性质。

## 本次检查

写入 sidecar 前只执行一次小型内联 Python/SymPy 精确有理恒等式检查：

- `A − X*diag(1/p,1/r)*Y` 与 `A − X0*Y0/p − X1*Y1/r` 的差为精确零；
- 同一表达与先构造已求解列再相减的结果之差为精确零。

分母以非零自由符号建模，外部条目为任意实符号。该检查不验证 source 数值、Lean 编译或不等式前提。
没有运行旧逆矩阵、PSD、主子式或 Fourier 检查，也没有做大回归。

静态检查确认直接 import 文件存在，新 sidecar 未见 `sorry`、`admit`、`axiom` 或 `opaque`；这不构成内核或依赖闭包验证。

sidecar 实际字节 SHA-256：
`f16fe297a105dc5373dc102a62cbf040bbf9da92ef6fb2b0890034619901dd5b`。

仅新增上述两文件，未修改旧数学叶、共享脚本、state 或 registry。
Fourier、coverage、完整 source 绑定、Lean 编译及 registry admission 均保持开放／fail-closed。
