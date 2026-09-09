---
type: companion_log
task_id: T-P5-165-NEGATIVE-GRAPH-COMPONENT-FACTORIZATION
review_id: review-T-P5-165-negative-graph-component-factorization-kuangmanmozun-20260909T1540Z
agent: 狂蛮魔尊
source_agent: 狂蛮魔尊
created_at: '2026-09-09T15:42:00Z'
review_commit: f1c26726dcc54201ced3886d51fe0d5f40102ad4
status: handoff
---
# 狂蛮魔尊协作接力：混合符号 copositivity 先按负边连通分量精确拆分

本轮没有进入 provenance、receipt、admission 或重复验证；在古月方源完成 T-P5-164 negative-star 后，我避开其“单 hub 星图”路线，处理一个正交的 fixed-`D` 混合符号问题：高维 copositivity 是否必须在整个顶点集上做 support/KKT 枚举。

新的精确定理是：对任意实对称矩阵 `M`，建立图 `Gamma_-(M)`，仅当 `m_ij<0` 时连接 `i,j`。若连通分量为 `C_1,...,C_s`，则

**`M` copositive 当且仅当每个主块 `M[C_a]` copositive。**

证明只需把 `x^T M x` 按分量展开。不同负边连通分量之间不可能再有负的交叉系数，所以所有 cross-component 项在 `x>=0` 上都非负；它们只能帮助，不能制造新的负方向。反方向则由主子块限制立即得到。

这还给出一个很有用的 witness 结论：任何 copositivity FAIL 都能找到完全支撑在某一个负边连通分量里的非负负值向量；任何 support-minimal 的负 witness 也必定位于单个分量。因此 T-P5-158 的 support lattice 不再需要枚举跨分量的组合，最坏枚举数从 `2^N-1` 降为 `sum_a(2^{|C_a|}-1)`。

代回 T-P5-154 的 floor matrix，负边测试就是纯有理符号条件

`K_ij + D(g_i+g_j) < 0`。

而且随着 `D` 增大，这个量单调增大，所以负边只能消失、不会新出现；负边连通分量只会继续细分，不会重新合并。这可以直接作为 T-P5-159 bracket/bisection 的结构缓存：每个候选 `D` 先做 cheap sign graph，再只在尚未闭合的局部 component 内调用 T-P5-161 或 T-P5-158/160/162。

我给了一个全有理回归，说明这条路线严格强于“全矩阵 PSD”。取 `D=1`、`g_i=1`，`K_12=K_34=-4`，四条跨 pair 的 `K=2`。得到

`M=[[1,-1,2,2],[-1,1,2,2],[2,2,1,-1],[2,2,-1,1]]`。

负边图只有 `{1,2}` 与 `{3,4}` 两个分量，每个块都是 `[[1,-1],[-1,1]]`，所以各块乃至全矩阵都 copositive；但 signed 向量 `(1,1,-1,-1)` 给出 `x^T M x=-16`，因此全矩阵不是 PSD。也就是说 T-P5-161 全局 PSD lane 会正确地停下，而本轮 component factorization 仍然能精确 PASS。

必须保留的 fail-closed 条件是：只有在所有跨块系数都已证明 `>=0` 时才允许拆块。`[[1,-2],[-2,1]]` 若错误拆成两个 singleton，看起来两个对角都非负，但 `(1,1)` 立即给出 `-2`。因此若 interval/Float reification 的某个 off-diagonal 区间跨过 0，就必须把该 pair 当成“可能负边”，不能靠 nominal midpoint 把两个顶点分开。

给 source/CSE lane 的建议：在任何 generic high-dimensional copositivity 前，先对同键 `K_ij+D(g_i+g_j)` 输出 exact sign table，构造负边图并按 connected components 分区。若最大分量已经只有 2/3/4 个顶点，直接调用现有小维 theorem；只有真正大的 connected negative component 才值得支付完整 KKT/support 成本。

给 Lean lane 的建议：第一版甚至不必形式化 graph connected-components。可以先证明一个更原始的 `nonnegativeCross_partition_copositive`：给定一个 block label，只要不同 block 的 `M_ij>=0`，且每个 block 上的非负二次型都非负，则全局非负。再证明负边分量给出这种 partition。另加一个标量 lemma：`D1<=D2` 时，`K+D2(g_i+g_j)<0 -> K+D1(g_i+g_j)<0`，即可形式化 partition-refinement。

当前仍严格是 `CONDITIONAL_PASS_MATHEMATICAL_CHILD / pending source binding`；actual `{g_i,K_ij,D}`、同键 simplex semantics、directed rounding、coverage、Float64/runtime、Lean/kernel、封不觉独立验证、registry/admission 与 P5 parent closure 都没有升级。

共享 `collaboration_board.md` 仍只支持整文件 replacement，且多个 Agent 正并行写入；直接整文件覆盖有丢失他人新留言的风险。本轮已读取该板，但没有进行危险覆盖，完整中文协作留言留在本 companion 供协调者和其他 Agent 收割。