# Periodic review-agent roster

This roster is the user-provided pool for the research roundtable. The names
and minute slots are scheduling labels; the inbox remains the durable source
of truth for task claims and results.

| agent label | nominal slot |
|---|---:|
| 封不觉 | :01 |
| 柳冠一 | :08 |
| 占月方源 | :16 |
| 星宿仙尊 | :23 |
| 苏梦辰 | :31 |
| 红莲魔尊 | :38 |
| 奥尼洛 | :46 |
| 狂弓魔尊 | :53 |

## Assignment and harvest protocol

梁智炜 assigns independent, bounded bottlenecks by adding or updating an
entry in `task_queue.md`. Each agent should claim one disjoint task, write an
immutable `review_result` file, include exact paths/commits/commands and
evidence boundaries, and avoid modifying StateStore, the verified registry,
or another agent's files.

The roundtable harvest runs every 30 minutes. A harvest runs the idempotent
inbox integrator, records pending provenance or an event-only external catalog
event, preserves all failed attempts, and pushes meaningful changes. It does
not infer completion from a review's prose, compile artifact, badge, or solver
status. Unknown tasks remain in the inbox for explicit triage.
