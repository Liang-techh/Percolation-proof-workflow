# Periodic review-agent roster and GitHub dispatch roles

This roster is the user-provided pool for the research roundtable. The names
and minute slots are scheduling labels; the inbox remains the durable source
of truth for task claims and results.

## Canonical role matrix for future GitHub task releases

The following role mapping is the user's corrected dispatch policy. New GitHub
issues, task plans, review requests, and release-gate work should be assigned
according to this table. A role is a routing boundary, not evidence that its
agent has proved a theorem.

| agent label | canonical responsibility |
|---|---|
| 古月方源 | 数学证明 / 主路线探索 |
| 星宿仙尊 | 数学证明 / 谱分析、线性理论 |
| 红莲魔尊 | 数学证明 / 能量法、Lyapunov、非线性恒等式 |
| 狂弓魔尊 | 数学证明 / 不等式 closure、强攻难点、反例辅助 |
| 柳冠一 | 数学证明 / adapter 背后的实质数学、接口 lemma |
| 苏梦辰 | Lean 形式化 / theorem decomposition |
| 臭屁猪 | Lean 形式化 / 编译修复、typed interface、sidecar |
| 封不觉 | 唯一验证 Agent / 独立 review、axioms、provenance、receipt、admission、最终 gate |

The former `占月方源` scheduling label is not used for new GitHub dispatches;
the canonical mathematical role is now `古月方源` as shown above. Existing
historical claims and review files retain their original author labels and are
not rewritten.

## Periodic polling slots

These slots are retained only for the existing low-frequency worker schedule:

| agent label | nominal slot |
|---|---:|
| 封不觉 | :01 |
| 柳冠一 | :08 |
| 古月方源 | :16 |
| 星宿仙尊 | :23 |
| 苏梦辰 | :31 |
| 红莲魔尊 | :38 |
| 臭屁猪 | :46 |
| 狂弓魔尊 | :53 |

## Assignment and harvest protocol

梁智炜 assigns independent, bounded bottlenecks by adding or updating an
entry in `task_queue.md`, using the canonical role matrix for all new GitHub
releases. Each agent should claim one disjoint task, write an immutable
`review_result` file, include exact paths/commits/commands and evidence
boundaries, and avoid modifying StateStore, the verified registry, or another
agent's files.

The roundtable harvest runs every 30 minutes. A harvest runs the idempotent
inbox integrator, records pending provenance or an event-only external catalog
event, preserves all failed attempts, and pushes meaningful changes. It does
not infer completion from a review's prose, compile artifact, badge, or solver
status. Unknown tasks remain in the inbox for explicit triage.
