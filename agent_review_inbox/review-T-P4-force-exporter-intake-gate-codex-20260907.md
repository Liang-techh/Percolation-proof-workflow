---
kind: review_result
task_id: T-P4-KC-COORDINATE-ADAPTER
source_agent: codex-local
created_at: 2026-09-07
integration_status: pending
---

# General-state force exporter：execution-agent receipt intake/hash gate

当前环境仍无 Julia executable。本文件只定义 fresh execution receipt 的
接收门槛；没有 runtime 输出，也不构成任何 PASS 结论。

## Immutable input binding

执行 agent 必须使用当前入库 exporter：

```text
examples/routeb_b45_5_descriptor_terms_adapter_lean/general_state_force_binding_export.jl
exporter_sha256 = 5351110e81327ebc059074a2e445a33e00859320bce37b5b0220bb189f4e46a4
```

并在运行时重新读取、重新计算并记录 deployed source：

```text
C:\Users\z5242\Desktop\重构版\6dof_sos_optimized\6dof_sos_optimized\robot_final\dhport_lib.jl
deployed_source_sha256 = aebe6db09b2d943448c5d701631109dba8f5eeb070cc66593e5dbaca26485936
```

Hash 不匹配、只提交旧 CSV、或只提交旧 verifier 的 hash，均为
`REJECTED_STALE_INPUT`，不能进入 source-binding receipt。

## Required execution record

Receipt 必须包含：

```text
command
worker_host / julia --version
generated_at_utc
exporter_sha256
deployed_source_sha256
csv_sha256
receipt_sha256
seed = 20260907
sample_count = 16
B = [4,5]
D = [1,2,3,6]
mass_regularizer = 1e-6
fd_step = 1e-5
process_exit_code
GENERAL_STATE_FORCE_BINDING_EXPORT_STATUS
max_E1
max_E2
```

推荐命令为：

```text
julia --startup-file=no examples/routeb_b45_5_descriptor_terms_adapter_lean/general_state_force_binding_export.jl
```

## CSV schema gate

CSV 必须包含且按 exporter 顺序保留以下字段，不接受只导出 residual 的
缩减版：

```text
q4,q5,dq4,dq5,w,
CdqB4,CdqB5,GqB4,GqB5,G0B4,G0B5,
tauB4,tauB5,rhsB4,rhsB5,
sourceBlockForce4,sourceBlockForce5,
aB4,aB5,aD1,aD2,aD3,aD6,
MqBB11,MqBB12,MqBB21,MqBB22,
MqBD41,MqBD42,MqBD43,MqBD46,
MqBD51,MqBD52,MqBD53,MqBD56,
sourceDescriptorRhs4,sourceDescriptorRhs5,
E1_4,E1_5,E2_4,E2_5
```

必须有 16 个 data rows；每行的 fields 必须来自同一 `(q,dq,w)` state、同一
`Mq`、同一 `rhs` 和同一 `a = Mq \\ rhs`。B/D 顺序漂移、缺少 `MqBD`、或把
nominal `M0_BB` 放入 `MqBB`，均为 `REJECTED_SCHEMA_OR_BLOCK_BINDING`。

## Residual gate

对每个 data row，intake checker 必须验证有限值并读取 exporter 写出的：

```text
E1 = sourceBlockForce - expectedSourceForce(qB,vB,w,CdqB,GqB,G0B)
E2 = sourceBlockForce - (MqBB*aB + MqBD*aD)
```

只有满足

```text
max(abs(E1_4), abs(E1_5), abs(E2_4), abs(E2_5)) <= 1e-12
```

且 process exit code 为 `0` 时，才可将 exporter 结果标为
`PASS_RUNTIME_FLOAT64_SOURCE_BINDING_CANDIDATE`。否则标为
`REJECTED_RESIDUAL_OR_PROCESS_FAILURE`。

该状态只表示同一运行点上的 source row/solve consistency；不等同于
Float64-to-exact-real Lean theorem，也不等同于 deployed `tau` 等价。

## Receipt status policy

```text
PENDING_JULIA_EXECUTION
PASS_RUNTIME_FLOAT64_SOURCE_BINDING_CANDIDATE
REJECTED_STALE_INPUT
REJECTED_SCHEMA_OR_BLOCK_BINDING
REJECTED_RESIDUAL_OR_PROCESS_FAILURE
```

执行 agent 未同时提供 CSV、receipt、两份输入 hash 和 stdout/stderr/exit
code 时，保持 `PENDING_JULIA_EXECUTION`，不得以 artifact 存在推断 PASS。

## Explicit non-claims

该 intake gate 不检查或关闭：

- deployed `tau` 与 PMI/lifted descriptor 的等价性；
- Float64 运算到 Lean `ℝ` 的语义桥；
- 全域覆盖、DH theorem、residual bound、registry promotion。

当前 codex worker 未执行 Julia，未生成 CSV/receipt，未修改主 state。

