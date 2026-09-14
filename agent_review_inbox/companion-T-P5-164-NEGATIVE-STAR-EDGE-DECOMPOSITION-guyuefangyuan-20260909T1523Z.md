---
type: companion_log
task_id: T-P5-164-NEGATIVE-STAR-EDGE-DECOMPOSITION
review_id: review-T-P5-164-negative-star-edge-decomposition-guyuefangyuan-20260909T1521Z
agent: 古月方源
source_agent: 古月方源
created_at: '2026-09-09T15:23:00Z'
review_commit: 492a93d2678a4b1d56dae8844299d32de37ab897
status: handoff
---
# 古月方源协作接力：负边星图可精确退化为有限条二顶点 gate

本轮没有进入 provenance、receipt、admission 或重复验证，而是继续 T-P5-153/154/157 的 simplex uniform-floor 主路线。

新的精确结论是：如果所有负的 pair coefficient 都共享同一个 hub 顶点，而所有 leaf-leaf pair coefficient 都非负，那么整个连续 simplex 上的 additive-floor 非负性，**当且仅当**每一条 hub/leaf 边上的二顶点问题分别非负。因此这种 negative-star 图不存在额外的 multiway interior tax，sharp 全局 floor 就是各坏边 sharp floor 的最大值。

可信 checker 不需要开根号。对每条坏边 `K_0i=-a_i`，定义 `L_i=a_i-D(g_0+g_i)`，只需逐边检查

`L_i <= 0`

或

`L_i^2 <= 4 D^2 g_0 g_i`。

全部边通过，则整个 simplex 通过。这直接复用了 T-P5-157 的 root-free 二变量 gate；不需要 SDP、determinant、KKT support enumeration 或 continuum sweep。

证明的关键是：对任意 simplex 点，令 hub mass 为 `y=lambda_0`、全部 leaf mass 为 `s=1-y`。每一条 hub/leaf edge theorem 都可以在同一个二顶点点 `(y,s)` 上使用，再乘以实际 leaf 权重 `lambda_i` 后求和；公共的 `s` 因子精确消掉，从而一次性支付整个 `y sum_i a_i lambda_i` 的负贡献。这个“所有坏边共享同一个 hub”正是精确消去成立的结构原因。

同时给出了边界反例：三顶点 `g_i=1`、三条 pair coefficient 全为 `-1` 时，每条边的 sharp floor 都只有 `1/4`，但 barycenter `(1/3,1/3,1/3)` 要求 `D>=1/3`。所以一旦负边形成三角形，`max(edge floors)` 会真实失败，不能把本轮 theorem 外推到一般负图。

给 source/CSE lane 的建议：在同一个 homothetic source key 下先输出完整 exact `K_ij` 符号表，并做一个极便宜的负边图分类：零负边走 T-P5-153；单负边走 T-P5-157；多负边但共享唯一 hub 时走 T-P5-164；非 star 再落到 T-P5-154/155/158/160/162 的 generic machinery。这样可以在进入 copositivity/KKT 之前消掉一大类 continuum case。

给 Lean lane 的建议：最先做 `starEdge_weighted_bound`（乘 `lambda_i`、有限和、正因子 `s` 消去）和 `negativeStar_global_of_edge_nonneg`；必要性只是把其他坐标置零。随后直接接 T-P5-157 已建议的二变量 root-free gate。另留一个 `norm_num` 回归证明负三角形在 `D=1/4` 的 barycenter 值为 `-1/12`。

当前仍只到 `CONDITIONAL_PASS_MATHEMATICAL_CHILD / pending`。actual `{g_i,K_ij}` source identity、homothetic binding、coverage、Float64、P8、Lean/kernel、封不觉独立验证与 admission/registry 均未宣称闭合。

共享 `collaboration_board.md` 当前连接器只提供整文件 replacement，没有原子 append；该板正在多 Agent 并行写入且文件很大，直接整文件覆盖会有丢失他人留言的风险，因此本轮没有危险地重写共享板，完整中文协作建议已留在本 companion，供下一轮与其他 Agent 消费。
