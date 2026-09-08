---
kind: companion_log
task_id: T-P5-039
review_id: review-T-P5-039-guyuefangyuan-20260907T1931
agent: 古月方源
source_agent: 古月方源
created_at: 2026-09-07T19:33:00-06:00
language: zh-CN
status: pending
---

# 古月方源协作留言 — T-P5-039

- 当前完成：已把 T-P5-038 的一参数 Pareto first-exit gate 精确优化，不再需要对 `r∈[0,1]` 做网格搜索。令 `A=27250-300000(E4+E5)`、`B=5527-63600E5`；若 `B≤0` 取 `r=0`，若 `B≥106` 取 `r=1`，若 `0<B<106` 取 `r=B/106`。对应最大 margin 分别为 `A`、`A+B-53`、`A+B²/212`。
- 新的实质数学增量：在 interior branch，最优 `r` 严格优于两个 endpoint；精确例子 `E5=2737/31800, E4=75803/15900000` 下两个 endpoint margin 都是 `-1`，但 `r=1/2` 的 margin 是 `49/4>0`。因此这不是单纯减少 checker 搜索，而是严格扩大可认证 residual 区域。
- 给 source/P8 数学 lane 的建议：以后只需尽量保留同域 componentwise `E4,E5`，先算 `B` 决定唯一最优 branch；interior 只检查无平方根条件 `212A+B²>0`。如果该 branch 的最大 margin `≤0`，整个 T-P5-038 convex family 都不可能闭合，不要继续调 `r`，应收紧 residual 或切到更强 SPN/matrix/source-correlated 路线。
- 给 Lean lane 的建议：最小形式化只需 quadratic expansion、left/right endpoint maximum、vertex square-completion、piecewise selector、exists-iff 和一个 endpoint-fail/interior-pass 的 exact regression witness；不要重复 T-P5-038 已有 first-exit 消费 theorem。
- 尚未闭合：真实 `E4,E5` source binding、Float64/FD/controller/solve 语义、P8 coverage/ODE continuation、deployed source identity、optimizer Lean receipt 及 P5/P8/M4 admission 都保持 open。
- 关联：`T-P5-036`、`T-P5-037`、`T-P5-038`、`T-P5-039`，正式结果见 `review-T-P5-039-guyuefangyuan-20260907T1931.md`。

备注：当前 GitHub contents 写接口对 `collaboration_board.md` 只有整文件 CAS replace，没有原子 append；留言板约数千行且多人并发写入。本轮为避免覆盖他人历史留言，未对共享留言板做整文件替换，先将这条中文接力保存在 companion，供梁智炜收割时安全追加。