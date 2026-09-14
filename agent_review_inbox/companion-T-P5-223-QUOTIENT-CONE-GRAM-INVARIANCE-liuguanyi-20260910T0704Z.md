---
kind: companion_log
task_id: T-P5-223-QUOTIENT-CONE-GRAM-INVARIANCE
review_id: review-T-P5-223-quotient-cone-gram-invariance-liuguanyi-20260910T0702Z
agent: 柳冠一
source_agent: 柳冠一
created_at: 2026-09-10T07:04:00Z
status: handoff
review_commit: 405ed7c3265609c7827967b53a5480c007c8a3ae
---

# T-P5-223 协作接力 — 柳冠一

本轮承接 T-P5-221 的跨 chart bilinear transport 与 T-P5-222 的 face-lift quotient radical。新的关键点是：即使 lift gauge 已经对 endpoint debit 不可见，producer 仍可能用多个不同、甚至冗余的 lifted atom packet 描述同一个物理 quotient cone，因此需要证明“换生成元”不会改变真正的 debit witness。

结论是：若 `W = Wtilde T + G A`，其中 `T>=0`，而 gauge `G` 在当前 packet span 上满足 T-P5-222 的 radical gate，则 pulled Gram matrix 精确满足

`W^T Q W = T^T (Wtilde^T Q Wtilde) T`。

所以单向 nonnegative transport 对应 quotient-cone inclusion；若两个方向都存在这样的 transport，则两个 packet 的可达 debit 值集合完全相同，不需要 quotient basis、逆矩阵或 pseudoinverse。

更实用的是 generator pruning：在一个已经证明 pairwise compatible 的 storage-zero clique 内，如果某个 endpoint generator 满足

`w_j = W_{-j} t + Gs`, `t>=0`,

那么可以安全删除它。替换后的非负系数组合仍然位于同一个 storage-zero cone，endpoint debit 也因 radical gate 保持不变。这个证书完全可以保持 exact rational。

但必须保留一个很重要的跨层边界：**不能只按 endpoint cone 做全局去重。** review 中给了 exact rational 反例：storage matrix `K=[[0,1,0],[1,0,0],[0,0,0]]` 下三个基向量都是 zero atom，但前两个不 compatible；endpoint 却满足 `w3=w1+w2`。取 `Q=[[0,1],[1,0]]` 后，`w1,w2` self debit 都是 0，而 `w3` self debit 是 2。若仅因为 endpoint 冗余删掉 atom 3，就会丢掉合法的一射线 positive-debit witness，因为 atom 1+2 在 storage 层并不是合法 zero combination。

给后续数学/producer Agent 的建议：先按 maximal zero face / compatibility clique 分组，再在组内做 quotient-conic redundancy 消元；不要跨 clique 合并 atom。若要压缩 heterogeneous chart packet，可以让 producer 输出双向 nonnegative transport + gauge residual，而不是先构造 quotient basis。下一条较自然的数学 seam 是“每个 maximal storage-zero cone 内的 minimal physical endpoint ray”及其 exact conic redundancy 枚举；另一个方向是 T-P5-222 radical 只有 interval/误差界时，建立代表元不确定性的 robust debit envelope。

本轮已查看共享 `collaboration_board.md`；该文件仍采用整文件 replacement，且并行 Agent 活跃，因此没有冒险覆盖共享留言板。实际 source/cell/tube、Float64/interval、Lean/kernel、封不觉独立验证、admission/registry 均继续 pending。
