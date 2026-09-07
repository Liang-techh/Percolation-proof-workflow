# Body-6：九项系数下界见证与零构型严格 margin 障碍

状态：**OPEN_UNCOMPILED**。未运行 Lean/Lake，未取得内核验证或 registry admission。

新增 `NEW_BODY6_SLICE_ENTRYMARGIN20260907.lean`（133 行）及本定向 review。
直接导入 `TAILSOLVECERT20260907`，继承实际 source 系数、SELF3/mixed 绑定及余项接口。
本叶给出明确的系数不等式充分条件，并发现规范公式在零构型有精确零方向；没有从 sampled PSD 或 uniform 命名推出正 margin。

## 最小系数下界见证

`NineEntryLowerBound R mu beta` 显式保存：

- `Rij=Rji`；
- `mu>0`、`beta≥0`；
- 三项对角不等式：`mu+2*beta ≤ Rii`；
- 六项有序非对角不等式：`|Rij|≤beta`，`i≠j`。

这里的“九项”按九个矩阵条目计数；对称性使成对非对角条件重复，但 typed 接口保留全部有序条目。
这是共同 off-diagonal bound 的对角占优充分条件，不是正 margin 的必要条件。
不能仅因这套条件失败，就断言 R 不正定。

核心二元不等式是

\[
|r|\le\beta\quad\Longrightarrow\quad
2rxy\ge-\beta(x^2+y^2).
\]

代码按 r 的符号使用以下非负分解：

\[
\beta(x^2+y^2)+2rxy=
\begin{cases}
r(x+y)^2+(\beta-r)(x^2+y^2),&r\ge0,\\
-r(x-y)^2+(\beta+r)(x^2+y^2),&r\le0.
\end{cases}
\]

将三对交叉项下界与三项对角下界合并后得到

\[
u^TRu\ge\mu(u_0^2+u_1^2+u_2^2).
\]

`nine_entries_to_margin_attempt` 因而尝试从这些系数证据推出 `RemainderMargin R mu`，不把该 margin 作为输入直接重述。

## 实际 source 与 domain uniformity

`source_entry_envelope_attempt` 将 R 取为实际条目表达 `sourceCoefficient q m kappa`。
其对称性复用 exact-source 接口中实际质量对称性与 mixed 转置关系；三项对角和六项 off-diagonal 不等式仍是独立外部证明参数。

`exact_source_margin_from_entries_attempt` 另消费 `ExactSchurCoefficientContract`，将上述实际系数下界转移到已绑定的候选 R。
该契约仍包含 source A/X/Y 绑定及实际 tail 的正分母／逆／求解接口，没有从 SELF3 的 A 绑定单独生成 margin。

`uniform_source_entry_margin_attempt` 要求明确的共同 `mu>0`，以及
`∀q∈D, NineEntryLowerBound (sourceCoefficient q ...) mu (beta q)`。
允许 beta 随 q 改变，但 mu 必须相同；结果才是严格正的共同 margin 与 `UniformMargin D ... mu`。
有限样本上的不等式、逐点各自正 mu 或名称中出现 uniform，都不能代替域内这个全称家族。

## 精确零构型检查：当前规范公式有零方向

本次做了一次针对性精确有理检查，使用继承的规范 SELF3/mixed/tail 公式，取

\[
q=(0,0,0,0,0,0),\quad m=3/20,\quad\kappa=1/60,\quad h=offset=7/200.
\]

这里使用的是现有公式规定的实际标量权重，不是另造 cross-block 数据。
SELF3 几何系数在该点为 `a=1/20,b=2/25,p=87/200,r=0,u=9/40,v=0`。
将规范加权 A 与 mixed X、`Y=Xᵀ`、tail 对角逆组合得到

\[
R_0=\begin{pmatrix}
168198/126378125&-120/40441&-57/40441\\
-120/40441&960/40441&456/40441\\
-57/40441&456/40441&1083/202205
\end{pmatrix}.
\]

精确非零向量

\[
u_*=(0,-19,40),\qquad \|u_*\|^2=1961
\]

满足 `R0*u* = (0,0,0)`。这是一条有理恒等式，不是浮点特征值接近零的判断，也不是有限 sampled PSD 被提升为全域结论。

`canonical_zero_null_attempt` 在 Lean proof attempt 中直接展开既有有限表，尝试证明同一零方向。
`source_zero_null_attempt` 再通过 `explicit_A_mixed_source_binding_attempt` 与实际条目余项公式，把它条件式转移至 `sourceCoefficient`。
此 source 转移明确要求 `CenterOffsetTarget` 和实际固定权重绑定，所有导入及新增 Lean 脚本仍未编译。

## 严格正 margin 的精确 obstruction

`source_zero_no_positive_margin_attempt` 在上述 source 前提下，对任意 `mu>0` 拒绝
`RemainderMargin (sourceCoefficient 0 (3/20) (1/60)) mu`。
理由是将 margin 条件应用于 u* 会要求 `mu*1961≤0`，与 `mu>0` 矛盾。

`domain_contains_zero_obstruction_attempt` 进一步说明：若域 D 包含零构型，在同样前提下不可能有该 source 余项族的统一严格正 margin。
这不否定 PSD 或零 margin，也不声称完整 `5×5`／6DOF 矩阵的 PSD 性质。
排除零构型只是寻找正 margin 的必要限制之一，不能据此保证其余配置均有正 margin。

该反证比“目前尚缺 margin 见证”更具体，但实际 source 结论仍经过未编译的条件式 source 链，不能报告为内核已验证的机器人定理。

## 仍需独立提供的内容

1. 待研究的明确配置域 D，以及其是否排除上述零构型和其他潜在零方向。
2. 该域上的共同正 mu 与全部九项系数不等式证明；这套充分条件过强时，也可另用严谨的 margin 证明，不得将条件失败等同于非 PSD。
3. 独立候选 A/X/Y/R 的完整实际 source 绑定、中心偏移与权重见证。
4. 连续域覆盖／余项界及 Lean 编译验证。没有提供这些证据时不能从有限检查推广至 uniform margin。

## 本次验证范围

仅执行两项定向精确检查：规范零构型的有理 A/X/tail 组合及零方向核对；二元不等式的两条代数分解展开差为零。
没有搜索大配置网格、计算浮点 PSD 判据、重跑旧 Fourier/Gram 检查或做宽回归。

静态检查确认直接 import 文件存在，新 sidecar 未见 `sorry`、`admit`、`axiom` 或 `opaque`。
未运行 Lean/Lake，未验证完整依赖闭包或内核证明。

sidecar 实际字节 SHA-256：
`cd76aff5988dc684f86fa67fa38b975ebf812cac22c6997589f66b16d95e5ae4`。

本次只新增上述两文件，未修改既有叶、共享脚本、StateStore 或 registry。
完整矩阵 PSD、实际域内正 margin、Fourier、coverage、Lean 验证与 registry admission 均未被宣称完成。
