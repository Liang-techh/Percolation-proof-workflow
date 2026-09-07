---
kind: immutable_execution_review
task_id: T-P4-O2-BB-TRIPLE-EXPORT
source_agent: codex-local
date: 2026-09-07
status: BLOCKED_NO_JULIA_RUNTIME
---

# O2 canonical parent/child/sibling triple exporter — runtime obstruction

## Scope

只允许检查并运行真实 branch driver 的 opt-in canonical O2 parent/child/sibling triple exporter：

```text
C:\Users\z5242\Desktop\重构版\6dof_sos_optimized\6dof_sos_optimized\routeB_dense_Mq\routeB_interval_branch_bound.jl
```

目标是 Julia 语法检查及最小 O2 路径，必须显式保留：

```text
P3_BB_TRIPLE_CELL_ID
external premise hashes
PENDING / READY
```

禁止全量 branch-and-bound、全仓库回归或把旧输出当作 fresh runtime evidence。

## Observed blocker

本机执行环境探测结果：

```text
Get-Command julia -> no result
JULIA_FOUND=False
```

因此本轮没有 Julia parse、include、最小路径、stdout/stderr 或 exit-code receipt；未验证用户所述“同 hash 备份”，未修改 branch driver，也未将任何 `PENDING` 升级为 `READY`。

## Direct runner intake contract

有 Julia 1.10 的执行 agent 接手后，只运行该文件的 opt-in O2 exporter 路径，并保存：

```text
P3_BB_TRIPLE_CELL_ID=<exact non-empty cell id>
P3_BB_TRIPLE_STATUS=PENDING|READY
EXTERNAL_PREMISE_HASH_<name>=<exact hash for every declared premise>
DRIVER_SOURCE_HASH=<fresh hash of routeB_interval_branch_bound.jl>
BACKUP_SOURCE_HASH=<hash of the pre-edit backup>
JULIA_VERSION=<julia --version>
EXIT_CODE=<integer>
STDOUT=<verbatim captured stdout>
STDERR=<verbatim captured stderr>
```

`READY` 只能在 opt-in O2 path 实际完成且所有 external premise hashes 非空、匹配其声明 source、exit code 为 0 时使用；语法失败、缺 premise、hash mismatch、selector 缺失或最小路径异常均保持 `PENDING`/失败，不得修饰为 READY。

语法检查可独立使用 Julia 的 parse-only 命令；它不能替代 O2 runtime receipt：

```text
julia --startup-file=no --history-file=no -e "Meta.parseall(read(ARGS[1], String)); println(\"JULIA_PARSE=PASS\")" "routeB_dense_Mq/routeB_interval_branch_bound.jl"
```

随后必须使用该 source 已定义的 opt-in selector 运行最小 O2 triple path；不得猜测、重命名或默认开启 selector。输出应直接归档为 immutable receipt，并关联上述字段。

本 review 仅记录 runtime obstruction；不声称编译、语法通过、O2 READY、物理等价或 deployed tau 等价。
