---
kind: companion_log
task_id: T-P5-169-SHARP-FLOOR-CONTACT-LOCALIZATION
agent: 狂蛮魔尊
source_agent: 狂蛮魔尊
created_at: 2026-09-09T16:41:00Z
review_commit: 300fec2e52d7a3a78107110f25df0ab016dc81d2
status: mathematical_child_pending
---

# T-P5-169 中文协作摘要

本轮把 T-P5-159 的“sharp floor 必有 zero contact”与 T-P5-165 的“strict-negative graph 分量分解”真正接上了零水平。

核心结论如下。

1. 若固定 `D` 时 `M_D` 已 copositive，而 `x>=0` 满足 `x^T M_D x=0`，则把 `x` 按 `M_D` 的严格负边图连通分量拆开后，每个非零分量限制本身都必须精确满足零二次型；不同活跃分量之间的所有 cross charge 也必须为零。原因是整个分解只含非负项，总和为零只能逐项归零。

2. 因此若 `D_*>0` 是全局 sharp floor，则任意 sharp contact 的每个活跃负边分量 `C` 都单独拥有同一个 sharp floor：`D_C^*=D_*`。在 `D_*` 处该分量有零 contact；对任意 `D<D_*`，同一个局部向量直接给出

`q_D(x_C)=-(D_*-D)(sum x_C)(sum g_i x_i)<0`。

所以一个单独分量就足以证明整个 sharp threshold，且同一个 witness 对所有更小 floor 都是严格 FAIL witness。

3. 还能做更强的静态分解：直接在 `D=0` 用 `K_ij<0` 建负边图。不同初始分量之间有 `K_ij>=0`，而加入任何 `D>=0` 后 cross entry 只会继续增加。因此整个一参数 floor 问题从一开始就精确分解，得到

`D_* = max_C D_C^*`。

这意味着 T-P5-159 的 rational bracket 可以按 `D=0` 的负边分量并行独立求，再取最大值；不需要任何跨分量 support/KKT 搜索。

4. sharp principal-kernel/root candidate 也可以局部化到一个 winning component。以后 determinant/kernel 枚举没有必要跨越候选 `D` 下已经分离的严格负边分量。

两个边界已经钉死：第一，winning component 不一定唯一。构造 `D_*=1`、两个 `[[1,-1],[-1,1]]` 块且跨块在 `D=1` 精确为零时，`(1,1,1,1)` 是跨两个分量的 global zero contact，但任意一个 pair 都已单独 sharp；所以只能说“可局部化”，不能说“所有 contact 天然只在一个分量”。第二，`D_*=0` 时 singleton zero contact 完全可能，因此“winning component 至少两个顶点”必须保留 `D_*>0` 假设。

本轮没有升级真实 `{g_i,K_ij}` source、simplex/coverage、Float64、Lean/kernel、封不觉独立验证、registry/admission 或 P5/P8/M4 parent closure。当前只应视为 `CONDITIONAL_PASS_MATHEMATICAL_CHILD / pending source binding`。
