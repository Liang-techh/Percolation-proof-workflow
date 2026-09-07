# Body-6：source Schur-margin 与 typed residual consumer

状态：**UNCOMPILED PROOF ATTEMPT**。未运行 Lean/Lake，不声明完整 `5×5`／6DOF PSD、coverage 或 registry admission。

新增 `NEW_BODY6_SLICE_SCHURMARGIN20260907.lean`（114 行）及本定向 review。
直接导入 `SELF3MASSBIND`，消费其继承的 `SOURCEBLOCKBIND`、`SCHURREMAINDER` 与 tail inverse 接口。
本叶新增的是带外部 margin 前提的残差消费者，不求解或认证具体 margin。

## Typed 对象及外部 margin

| 对象 | 类型／定义 |
| --- | --- |
| `A,R` | `Fin 3 → Fin 3 → ℝ` |
| `X` | `Fin 3 → Fin 2 → ℝ` |
| `Y,S` | `Fin 2 → Fin 3 → ℝ` |
| `B` | `Fin 2 → Fin 2 → ℝ`，source 构造时为 `sourceTail q` |
| `D` | 已有显式 `inverseTail (q 4) offset m kappa` |
| `S` | `solvedRight ... Y`，已有接口提供 `S = D*Y` 与 `B*S[:,j]=Y[:,j]` |
| `R` | 外部给定的候选余项，另需逐项证明 `R = A − X*D*Y` |

front 对应实际关节 `{0,1,2}`，内部 tail 顺序严格为 `{3,4}`；body 索引为 `5`，即通常编号的 body-6。
参数 `q : Fin 6 → ℝ` 任意但契约针对给定 q；`q 4` 使用从 0 开始编号。

`RemainderMargin R mu` 明确要求：

\[
R_{ij}=R_{ji},\quad \mu\ge0,\quad
\forall u\in\mathbb R^3,\quad
\mu\sum_i u_i^2\le\sum_i u_i(Ru)_i.
\]

`mu=0` 允许一个显式 PSD 前提；正的 `mu` 对应调用者额外提供的严格余量。
本叶没有构造任何 `mu` 的值或这个谓词的无条件见证。
不需要独立 A-PSD 前提来做残差代数；A 自身的 PSD 也不能替代 R 的上述 margin 前提。

## SourceSchurMarginContract

契约保存四个独立部分：

1. `SourceBlockBinding q A X Y`：实际 body-6 A/X/Y 条目绑定；
2. `SchurRemainderContract`：实际 tail 逆块的分母正性、两侧逆和列求解接口；
3. `remainderFormula`：指定 R 逐项等于 `schurRemainder ... A X Y`；
4. `margin`：外部 `RemainderMargin R mu` 证明。

`source_margin_contract_attempt` 明确要求 `CenterOffsetTarget`、实际权重绑定、
`kappa > 0`、`m ≥ 0`、`offset² ≥ 0`，以及上述 source 绑定、R 恒等式和 margin 见证。
它调用旧余项构造器填入 tail 证明包；不会从 A/X/Y 绑定推导 margin。

`canonical_margin_contract_attempt` 取 `A = explicitWeightedA`、`X = mixedX`、`Y = mixedY`，
直接消费 SELF3MASSBIND 的条件式规范 source 绑定，并将 R 定义为其 Schur 余项表达。
该构造器仍必须接收外部 `RemainderMargin`；规范表的存在没有消除这个义务。

## 新残差结论

对任意 `u : Fin 3 → ℝ` 定义消去后的 tail 向量

\[
v=-Su=-DYu.
\]

定义 front 残差 `Au + Xv` 和 tail 残差 `Yu + Bv`。
两条有界代数引理仅使用：

- `Rij = Aij − ∑a Xia Saj`；
- 每列 `B*S[:,j] = Y[:,j]`。

它们分别给出

\[
Au+Xv=Ru,\qquad Yu+Bv=0.
\]

`source_residual_consumer_attempt` 消费 source margin 契约，返回：

1. 全部两个 tail 残差条目为零；
2. 全部三个 front 残差条目等于 `Ru`；
3. `mu*∑i ui² ≤ ∑i ui*(frontResidual)i`，由外部 R-margin 直接转移。

这个结论只针对选定消去向量 `v=-DYu`，没有断言任意 front/tail 向量上的完整块矩阵 PSD，也没有组装完整质量矩阵。

## 本轮前提传递复核

对当前 114 行 Lean 文件逐项核对后，结论边界如下：

| 结论／步骤 | 实际消费的前提 | 本叶没有证明的内容 |
| --- | --- | --- |
| 第 40 行开始的 `front_residual_reduction_attempt`：front 残差等于 `R*u` | 逐项 `R=A-X*S` 恒等式 | R 的 PSD 或正 margin |
| 第 47 行开始的 `tail_residual_zero_attempt`：tail 残差为零 | 每列 `B*S[:,j]=Y[:,j]` | 完整块矩阵 PSD |
| 第 62 行契约的 `margin` 字段 | 外部 `RemainderMargin R mu` 证明项 | 从 `sourceBinding` 自动推出 margin |
| 第 70、77 行两个构造器的 `hmargin` 参数 | 调用者必须显式提供 | 自动选择正 `mu` 或计算 margin 见证 |
| 第 101 行 `exact hc.margin.2.2 u` | 从契约取出给定二次型下界，再按残差等式转移 | 独立证明这个二次型下界 |

因此，`R*u` 和零 tail 残差的等式部分是条件式代数；消费者返回的 PSD／margin 信息完全来自外部 margin 字段。
即使规范 A/X/Y 已取得条件式 source 绑定且 tail 分母严格为正，也不能略去 `hmargin`。
本契约只要求 `mu ≥ 0`，**并不保证 `mu > 0`**；要得到正 margin，调用者还必须选定正 mu 并提供相应 `RemainderMargin` 证明。

## 精确缺失义务与负条件

- **任意候选 A/X/Y**：仍需实际 source 条目绑定；规范符号表的条件式绑定不能认证另一个数值候选。
- **候选 R**：需逐项余项恒等式；没有该字段不能以任意 PSD 矩阵代替真实余项。
- **margin**：没有提供具体 `mu` 或 `∀u` 的余项 margin 证明。这是本轮新增契约的主要外部义务。
- **配置域**：本轮没有提供整个配置域上统一的 margin、区间／覆盖证据或所有 q 上的 margin 家族；单个 q 的条件式接口不能提升为域覆盖。
- **source 与 P4 接口**：CenterOffset、实际权重及导入 Lean 证明的验证继续未闭合；没有提供 P4 特定参数、阈值或 admissibility 的映射证据。

未提供 margin 见证只表示待证明，不表示已经存在反例。
`margin_violation_rejects_attempt` 仅在有明确向量 u 满足
`uᵀRu < mu*||u||²` 的证明时，才推出相应 `RemainderMargin` 不成立。
本叶没有声称已找到这样的 source 反例，也未伪造数值。

## 定向验证与范围

只运行一次小型 Python/SymPy 精确符号残差检查：以自由矩阵 A/X/S/B、任意 u，
在形式条件 `Y=B*S` 下构造 `v=-S*u` 和 `R=A-X*S`，front 的三个差及 tail 的两个差均为精确零。
这是残差代数检查，既不是 source 数值验证，也没有验证或推断 PSD/margin。

静态检查确认直接 import 文件存在，新 sidecar 未见 `sorry`、`admit`、`axiom` 或 `opaque`。
未运行 Lean/Lake、旧数学检查或大回归；未修改共享脚本、既有叶、state 或 registry。

本轮另做定向静态复核：唯一直接 import 为 `NEW_BODY6_SLICE_SELF3MASSBIND20260907`。
检查 SELF3MASSBIND、SOURCEBLOCKBIND、SCHURREMAINDER、TAILSCHUR、TAILINVERSE、TAILMINORS、TAILPSD、MASSTAIL_Source、VGRAM_Source、SELF3_Source 共 10 个相关模块，各自直接 import 对应的本地文件均存在。
这只是限定链上的文件存在性检查，不是完整传递依赖闭包、Mathlib 环境或类型检查。

对当前 SCHURMARGIN 源文件扫描未见 `sorry`、`admit`、`axiom`、`opaque`、`TODO` 或 `FIXME`。
第 99 行存在一个 `refine ... ?_` tactic 子目标，其后第 100–101 行写有对应证明步骤；它没有被当作已验证的内核证明，也没有与 `sorry` 混同。
下划线参数是待 elaborator 推断的项；是否全部成功求解仍需之后真正编译确认。

本轮只补充本 review，Lean 文件字节未改变；未重跑前述符号残差检查。

sidecar 实际字节 SHA-256：
`3e37ec54b791dd7266079d963d7c40a1ff9b2bc635e5564e6cff3b131016fba3`。

完整 `5×5`／6DOF PSD、完整 Schur PSD 定理、Fourier、coverage、Lean 验证与 registry admission 均不在结论范围内。
