---
kind: immutable_remote_runtime_handoff
task_id: T-P4-O2-BB-TRIPLE-EXPORT
source_agent: codex-local
date: 2026-09-07
status: BLOCKED_NO_REMOTE_EXECUTION_ENTRY
---

# O2 remote runtime: minimal executable handoff

## Current blocker

本轮未提交 GitHub workflow，未请求用户确认，也未触发任何远端 job。当前可用 Codex execution host 仍只有 `local`；force workflow 仍未成为 GitHub Actions 可选入口。因此没有 fresh syntax/minimal-run receipt 或 `READY` artifact。

目标 branch driver：

```text
6dof_sos_optimized/routeB_dense_Mq/routeB_interval_branch_bound.jl
```

## Required workflow_dispatch inputs/variables

远端 job 必须固定 Julia `1.10`，并提供：

```text
DEPLOYED_SOURCE_REPOSITORY=<owner>/<deployed-source-repository>
DEPLOYED_SOURCE_REF=<frozen ref containing the driver and premise files>
P3_BB_TRIPLE_CELL_ID=<positive integer; exact requested child id>
```

五类 premise path 与对应 hash 必须成对提供，且 path 指向同一 remote runner workspace 中的实际文件：

```text
P3_BB_SOURCE_RECEIPT_PATH       / P3_BB_SOURCE_RECEIPT_SHA256
P3_BB_GENERATOR_PATH            / P3_BB_GENERATOR_SHA256
P3_BB_INTERVAL_SOURCE_PATH      / P3_BB_INTERVAL_SOURCE_SHA256
P3_BB_MEMBERSHIP_RECEIPT_PATH  / P3_BB_MEMBERSHIP_RECEIPT_SHA256
P3_BB_COVERAGE_JOIN_PATH        / P3_BB_COVERAGE_JOIN_SHA256
```

另需：

```text
P3_BB_INTERVAL_MEMBERSHIP_STATUS=ACCEPTED|PROVEN|SOURCE_INTERVAL_MEMBERSHIP_PROVEN
```

## Minimal remote command

在 clean checkout、已 staging deployed source 与上述五类 premise files 后，只运行：

```bash
julia --startup-file=no --history-file=no --project=. \
  6dof_sos_optimized/routeB_dense_Mq/routeB_interval_branch_bound.jl
```

执行环境必须把 `P3_BB_TRIPLE_CELL_ID` 及上述 variables 注入该进程；不得默认打开其他 branch-and-bound 或全量回归路径。输出应保留：

```text
routeB_theta2_canonical_triple_<P3_BB_TRIPLE_CELL_ID>.json
routeB_interval_branch_bound*.csv
P3_BB_TRIPLE_CELL_ID=<value>
triple_status=PENDING_TRIPLE_NOT_OBSERVED|PENDING_EXTERNAL_PREMISES|READY_STRUCTURAL_CANONICAL_TRIPLE
JULIA_VERSION=<julia --version>
EXIT_CODE=<integer>
STDOUT=<verbatim>
STDERR=<verbatim>
```

`READY_STRUCTURAL_CANONICAL_TRIPLE` 仅在五个 path/hash binding 全部存在且匹配、membership status 合法、parent/child/sibling canonical linkage 成功并且 exit code 为 0 时可接收；否则保留对应 `PENDING_*`，不升级为 READY。

## Required next action

由具备 Julia 1.10 的远端 agent 取得上述 source repo/ref 与五组 premise path/hash 后，按现有未提交 workflow 或等价 isolated runner 执行一次；回传 JSON、CSV、stdout、stderr、exit code 与 hash manifest。workflow 未落地、变量未提供或 Julia 不可用时，本 handoff 保持 blocked；不把 staged workflow、旧输出或静态检查当作 runtime receipt。
