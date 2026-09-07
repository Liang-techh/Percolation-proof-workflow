# Periodic review-agent roster and GitHub dispatch roles

This roster is the user-provided pool for the research roundtable. The names
and minute slots are scheduling labels; the inbox remains the durable source
of truth for task claims and results.

## Current scheduled GitHub-agent pool

The following nine entries are the only currently scheduled GitHub agents
shown by the user. New releases must use this pool. A role is a routing
boundary, not evidence that its agent has proved a theorem.

| agent label | canonical responsibility |
|---|---|
| 柳冠一 | Inbox 协作 / 结果回收、任务去重 |
| 苏梦辰 | Inbox 协作 / theorem decomposition 任务协调 |
| 幽魂魔尊 | 数学突破 / 主数学瓶颈 |
| 大爱仙尊 | 数学突破 / 主数学瓶颈 |
| 古月方源 | Inbox 协作 / 主路线与任务协调 |
| Percolation 最终验证 | 唯一验证 Agent / axioms、provenance、receipt、admission、最终 gate |
| 巨阳仙尊 | Lean 形式化 / 编译修复、typed interface、sidecar |
| 狂蛮魔尊 | Inbox 协作 / 不等式与强攻难点结果协调 |
| 红莲魔尊 | Inbox 协作 / 能量法与 Lyapunov 结果协调 |

The former `星宿仙尊`、`臭屁猪`、`封不觉`、`狂弓魔尊`、`奥尼洛` and
`占月方源` labels are no longer in the current scheduled pool. Existing
historical claims and review files retain their original author labels and are
not rewritten.

## Periodic polling slots

The user-facing schedule is hourly per agent; exact next-run offsets are held
by the Codex scheduler, not inferred from this repository file:

| agent label | nominal slot |
|---|---:|
| 柳冠一 | hourly |
| 苏梦辰 | hourly |
| 幽魂魔尊 | hourly |
| 大爱仙尊 | hourly |
| 古月方源 | hourly |
| Percolation 最终验证 | hourly |
| 巨阳仙尊 | hourly |
| 狂蛮魔尊 | hourly |
| 红莲魔尊 | hourly |

## Assignment and harvest protocol

梁智炜 assigns independent, bounded bottlenecks by adding or updating an
entry in `task_queue.md`, using the canonical role matrix for all new GitHub
releases. Each agent should claim one disjoint task, write an immutable
`review_result` file, include exact paths/commits/commands and evidence
boundaries, and avoid modifying StateStore, the verified registry, or another
agent's files.

The roundtable harvest runs every 20 minutes. A harvest runs the idempotent
inbox integrator, records pending provenance or an event-only external catalog
event, preserves all failed attempts, and pushes meaningful changes. It does
not infer completion from a review's prose, compile artifact, badge, or solver
status. Unknown tasks remain in the inbox for explicit triage.

The harvest updates the local workspace first. It must not routinely fetch,
merge, or push to GitHub; remote synchronization is reserved for a major
mathematical breakthrough, a verified architecture milestone, or an explicit
user request, to avoid competing with scheduled GitHub agents.
