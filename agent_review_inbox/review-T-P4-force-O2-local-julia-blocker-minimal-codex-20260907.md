---
kind: immutable_execution_blocker
task_id: T-P4-O2-BB-TRIPLE-EXPORT
source_agent: codex-local
date: 2026-09-07
status: BLOCKED_LOCAL_JULIA_MISSING
---

# Local-first Julia syntax/minimal-runner blocker

本轮不提交、不确认 GitHub staged workflow，也不发布远端变更。目标 branch driver 仍为：

```text
C:\Users\z5242\Desktop\重构版\6dof_sos_optimized\6dof_sos_optimized\routeB_dense_Mq\routeB_interval_branch_bound.jl
```

本地唯一执行探测结果：

```text
Get-Command julia -> no result
JULIA_FOUND=False
```

因此没有 Julia syntax/minimal-path 结果，没有 fresh stdout/stderr/exit receipt，也没有 `P3_BB_TRIPLE_STATUS=READY`。branch driver 与 GitHub staged workflow 均未修改。

## Minimal handoff blocker

下一步只需由用户或已具备 Julia 1.10 的远端执行 agent 提供：

```text
DEPLOYED_SOURCE_REPOSITORY=<owner>/<deployed-dhport-source-repository>
DEPLOYED_SOURCE_REF=<frozen deployed-source ref>
P3_BB_TRIPLE_CELL_ID=<exact cell id>
EXTERNAL_PREMISE_HASH_<name>=<hash for every declared premise>
```

然后仅执行 parse-only 与 source-defined opt-in O2 triple path，回传 `JULIA_VERSION`、driver/backup hashes、`PENDING|READY`、exit code、verbatim stdout/stderr。缺 Julia、缺变量、缺 premise hash 或 selector 不明确时保持 pending；不得把 staged workflow、旧 CSV 或静态检查当作 runtime receipt。

本记录不改变任何 gate 或主 state，不作物理或 deployed-tau 等价声明。
