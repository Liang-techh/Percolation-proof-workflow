# RemainderMargin：配置域统一化与严格正 margin 反例

状态：**UNCOMPILED PROOF ATTEMPT**。未运行 Lean/Lake，不声明 source margin 自动成立、连续域 coverage 或 registry admission。

新增 `NEW_BODY6_SLICE_MARGINUNIFORM20260907.lean`（138 行）及本定向 review。
唯一直接 import 为 `NEW_BODY6_SLICE_SCHURMARGIN20260907`。
本叶只处理 margin 的量词和配置域范围，未构造任何 body-6 cross-block 数据。

## 统一化契约

`Config := Fin 6 → ℝ`，`D : Set Config`，`R : Config → FrontBlock`。

\[
\operatorname{UniformMargin}(D,R,\mu)
\iff \forall q\in D,\ \operatorname{RemainderMargin}(R(q),\mu).
\]

同一个 `mu` 位于配置量词外。每个 `RemainderMargin` 继续要求对称性、`mu ≥ 0` 和全部 front 向量上的二次型下界。
契约没有把“所有 q”默认为整个配置空间：结论范围恰为声明的 D。

`margin_lowering_attempt` 证明已有 margin `rho` 可以降到任意 `0 ≤ mu ≤ rho`。
证明只将非负平方和乘以下界，再消费已有 `RemainderMargin`，不推导新 source 或几何事实。

`uniform_from_floor_attempt` 的输入是：

1. 每个 `q∈D` 的 margin 证明 `RemainderMargin (R q) (rho q)`；
2. 一条显式共同下界 `∀q∈D, mu ≤ rho q`；
3. `mu ≥ 0`。

它得到同一个 mu 的域内 margin 家族。若要正的共同 margin，还必须提供／取得 `mu > 0`；一般域上逐点 `rho(q)>0` 本身不够。

## 有限配置集

对 `K : Finset Config`，`finite_positive_floor_attempt` 通过有限集归纳构造正共同下界：空集取 1，每插入一点便取当前下界与该点 `rho(q)` 的 `min`。
因此这个下界等价于对 1 和所有给定正 margin 取最小值；不声称是最优下界。

`finite_uniform_attempt` 在所有 `q∈K` 均提供正 `rho(q)` 及其 margin 证明后，得到

\[
\exists\mu>0,\quad\forall q\in K,\ \operatorname{RemainderMargin}(R(q),\mu).
\]

空配置集的结论是空量词下的真命题，不代表验证了某个物理配置。
`UniformMargin (↑K) ...` 只覆盖 K。有限样本通过不能被提升为邻域或连续配置域结论。
`uniform_restrict_attempt` 仅允许沿给定 `D ⊆ E` 证据缩小域；若想把某域 D 作为有限 K 的覆盖对象，必须另给 `D ⊆ ↑K` 的真实证据，不能假设采样点已经覆盖 D。

## 同一 mu 的 source residual consumer

`uniform_source_contract_attempt` 对同一 D、固定实际权重 `m,kappa` 和同一 mu，明确要求：

- `CenterOffsetTarget`、实际权重绑定、`kappa > 0`、`m ≥ 0`、`offset² ≥ 0`；
- 域内每点的 `SourceBlockBinding q (A q) (X q) (Y q)`；
- 域内每点逐项 `R(q)=A(q)−X(q)*inverseTail(q)*Y(q)` 的恒等式；
- 独立外部 `UniformMargin D R mu`。

它逐点调用旧 source margin 构造器，得到一族使用相同 mu 的 `SourceSchurMarginContract`。
`uniform_residual_consumer_attempt` 再逐点消费旧残差定理，给出

\[
\forall q\in D,\ \forall u,\quad
\mu\|u\|^2\le u^T\operatorname{frontResidual}(q,u),
\]

其中 tail 向量仍按旧接口取 `v=-inverseTail(q)*Y(q)*u`。
源侧 body-6、front `{0,1,2}`、有序 tail `{3,4}` 的绑定规则均继承旧接口，没有引入虚构数值。
source block binding 与统一 margin 是分开的必需输入；前者没有自动产生后者。

## 精确反例：逐点严格正不推出统一严格正

定义抽象配置 `q_n`：第 0 坐标为自然数 n，其余五个坐标为 0，`n∈ℕ`；令

\[
D_* = \{q_n:n\in\mathbb N\},\qquad
R_*(q)=\frac{1}{q_0+1}I_3\quad(q\in D_*).
\]

这是独立的实矩阵族，**没有声称它是实际 body-6 的 Schur 余项**。没有为它制造 A/X/Y source 块。

`counter_pointwise_positive_attempt` 给出每点精确正 margin
`rho_n=1/(n+1)>0`，因为二次型恒等于 `rho_n*||u||²`。

`counter_no_uniform_positive_attempt` 尝试证明

\[
\neg\exists\mu>0,\quad\forall q\in D_*,\ \operatorname{RemainderMargin}(R_*(q),\mu).
\]

精确论证：对任意候选 `mu>0`，由 Archimedean 性质选择自然数 `n>1/mu`。
于是 `1/(n+1)<mu`。若这个 mu 是统一 margin，将定义应用于 `q_n` 和基向量 `(1,0,0)` 就要求 `mu≤1/(n+1)`，矛盾。
Lean 代码明确使用 `exists_nat_gt` 和正分母不等式，没有用有限采样或浮点近似代替无限域论证。

需准确区分量词：失败的是“逐点存在正 margin ⇒ 存在统一正 margin”。
并非不存在任何共同 mu；`counter_zero_uniform_attempt` 明确证明 0 仍是共同 PSD margin。
反例不针对添加了紧致性、连续性或正统一下界等额外前提的其他命题。

## 本次定向检查与开放义务

只运行一次小型内联精确检查：标量单位矩阵的二次型展开差为零；
`mu*(n+1)-1 = (mu*n-1)+mu` 的展开差为零，支持上述严格不等式推导；
另用抽象有理 margin `{2/3,1/7,4/5}` 核对有限 `min` 下界为 `1/7`。
这些数值是有限下界规则的说明性检查，不是任何 source 配置或机器人测量，也不验证实际域内 margin。

静态检查确认直接 import 文件存在，新 sidecar 未见 `sorry`、`admit`、`axiom` 或 `opaque`。
该检查不验证 Lean elaboration、依赖闭包或内核证明；未运行 Lean/Lake 或宽回归。

sidecar 实际字节 SHA-256：
`0e48865fd5342acb95c91d6d95b5028868b2a15ffb581071d41b06f6882a34f4`。

本次只新增上述两文件。实际 source 上的逐点 margin 见证、无限域共同下界／统一家族、域覆盖、无条件几何与权重见证、Lean 验证及 registry admission 均仍未提供。
没有修改共享脚本、既有叶或 state/registry，没有声称完整矩阵 PSD 或从有限配置集推出连续域结论。
