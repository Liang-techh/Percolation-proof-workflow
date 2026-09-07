# Periodic review-agent roster and GitHub dispatch roles

This roster is the user-provided pool for the research roundtable. The names
and minute slots are scheduling labels; the inbox remains the durable source
of truth for task claims and results.

## Current scheduled GitHub-agent pool

The following six entries are the only currently scheduled GitHub agents
shown by the user. New releases must use this pool. A role is a routing
boundary, not evidence that its agent has proved a theorem.

| agent label | canonical responsibility |
|---|---|
| 柳冠一 | 数学证明 / adapter 背后的实质数学与主路线瓶颈 |
| 苏梦辰 | Lean 形式化 / theorem decomposition、编译与 sidecar |
| 古月方源 | 数学证明 / 主路线探索与数学瓶颈 |
| 狂蛮魔尊 | 数学证明 / 不等式 closure、强攻难点与反例辅助 |
| 巨阳仙尊 | Lean 形式化 / 编译修复、typed interface、sidecar |
| 红莲魔尊 | 数学证明 / 能量法、Lyapunov 与非线性恒等式 |

The former `幽魂魔尊`、`大爱仙尊`、`Percolation 最终验证`、`星宿仙尊`、
`臭屁猪`、`封不觉`、`狂弓魔尊`、`奥尼洛` and `占月方源` labels are no longer
in the current scheduled pool. Existing
historical claims and review files retain their original author labels and are
not rewritten.

## Periodic polling slots

The user-facing schedule is an hourly six-agent ring with the following offsets;
the two Lean slots are deliberately reserved for pinned-environment validation
and repair, while the other four slots are mathematical work:

| agent label | nominal slot |
|---|---:|
| 柳冠一 | :00 — mathematics |
| 苏梦辰 | :10 — Lean |
| 古月方源 | :20 — mathematics |
| 狂蛮魔尊 | :30 — mathematics |
| 巨阳仙尊 | :40 — Lean |
| 红莲魔尊 | :50 — mathematics |

## Assignment and harvest protocol

梁智炜 assigns independent, bounded bottlenecks by adding or updating an
entry in `task_queue.md`, using the canonical role matrix and six-slot ring for
all new GitHub releases. Mathematical tasks go to 柳冠一、古月方源、狂蛮魔尊、
红莲魔尊; Lean compilation, pinned-environment validation, and repair tasks go
to 苏梦辰、巨阳仙尊. Each agent should claim one disjoint task, write an
immutable `review_result` file, include exact paths/commits/commands and
evidence boundaries, and avoid modifying StateStore, the verified registry, or
another agent's files.

The roundtable harvest runs hourly. A harvest runs the idempotent
inbox integrator, records pending provenance or an event-only external catalog
event, preserves all failed attempts, and pushes meaningful changes. It does
not infer completion from a review's prose, compile artifact, badge, or solver
status. Unknown tasks remain in the inbox for explicit triage.

The harvest updates the local workspace first. It must not routinely fetch,
merge, or push to GitHub; remote synchronization is reserved for a major
mathematical breakthrough, a verified architecture milestone, or an explicit
user request, to avoid competing with scheduled GitHub agents.
