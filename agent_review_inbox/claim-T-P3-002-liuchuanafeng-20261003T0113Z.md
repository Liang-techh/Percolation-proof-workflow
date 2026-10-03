---
kind: task_claim
agent: 流川枫
task_id: T-P3-002
claimed_at: 2026-10-03T01:13:00Z
status: claimed
inspected_commit: ffded83ad2eaade9863b95025018b24e8502e4fb
---

# Claim T-P3-002

流川枫认领 `T-P3-002` 的只读审计：检查当前仓库是否已经能对一个固定 q-box（优先 `q=0`）和一个质量元 `M[i,j]` 交出可回放的 Float64 运算/舍入 trace，还是只能给出缺失 witness 的精确原因。

边界：

- 只写本 claim 与同一轮 `review_result`；不改 `task_queue.md`、registry、state 或正式证明。
- 不从单点相等 bit、十进制打印或历史 smoke 推全局 interval soundness。
- 不把条件 Lean sidecar 或历史 compile receipt 当作运算级 trace。
- 不覆盖 Codex 历史 review `review-T-P3-002-ieee-trace.md` 的 provenance。
- 本轮不跑 Julia、不重编 Lean。
