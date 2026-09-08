# 3D → 2D principal-row restriction

状态：`OPEN_UNCOMPILED / pending`。未运行本机或远程 Lean/Lake；没有 compiled、
VERIFIED、kernel_checked 或依赖公理审计结论。

新增 `NEW_PRINCIPAL_RESTRICTION_20260908.lean`，3 个 theorem 候选；只按请求中
明确给出的 T*a=g 构建 source-independent 接口，不认证 revision 785 的来源。

## 精确接口

T : Fin 3 → Fin 3 → Real，a,g : Fin 3 → Real。
用 Fin.castSucc 将两个保留坐标嵌入前三维的槽 0、1：

```text
A_ij = T_(castSucc i),(castSucc j)
u_j = a_(castSucc j)
p_i = g_(castSucc i)
h_i = T_(castSucc i),2
v = a_2

T*a=g  ⇒  A*u = p-h*v.
```

候选名 a6 表示预期的第三个 block 分量；只有额外的 joint/source 映射才能把
局部槽 2 认作物理 joint 6。候选未自动绑定物理质量矩阵、加速度或残差。

`split_three` 展开有限求和；`principal_rows` 只使用前两行。
没有消元第三行，没有假设 a6=0、h=0、T 对称、PSD 或 A 可逆。
`principal_rows_of_zero_coupling` 仅在显式 ∀i,h_i*v=0 时允许丢掉耦合项。
一般情况下，A*u=p 不成立。例如 T 第一行为 (1,0,1)、a=(0,0,1)、
g=T*a，则第一行左侧 A*u=0，但 p_0=1；保留 -h*v 后等式正确。
这是纸面精确例子，不是物理 DH 反例或本轮运行的 Lean 例子。

前两行不是完整 3D 系统的等价替代：第三行必须独立保留，不能由 principal
restriction 反推 T*a=g。若未来采用第三行 k*u+d*v=r 消元，必须显式给 d≠0，
才可写 v=(r-k*u)/d、(A-h*k/d)u=p-h*r/d。本轮没有实现或调用该 Schur 路线，
因此主 lemma 不需要 d≠0，也不把 A 与 Schur complement 混为一谈。

## import / tactic 与 admission 风险

直接 imports：Mathlib.Data.Real.Basic、Mathlib.Algebra.BigOperators.Fin、
Mathlib.Tactic.Linarith。使用 Fin.castSucc、Fin.sum_univ_succ、simp、rw、linarith；
没有完整 Mathlib import、matrix inverse 或 source adapter import。
后续优先检查固定 Fin 求和的 castSucc 归约与 split_three rewrite 匹配；这是
未测试的最小化候选依赖集，不是已确认的编译接口。无需 nlinarith 或数值判定。

只新增本候选与本 REVIEW.md，不修改 state/registry/shared scripts，不产生
构建配置或 OLean。即使后续通过编译，也只提供代数投影；source mapping、路径
覆盖、port metric 转换与 admission 仍属独立义务。
