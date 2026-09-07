---
kind: review_result
task_id: T-P4-KC-COORDINATE-ADAPTER
source_agent: codex-local
created_at: 2026-09-07
integration_status: pending
---

# Fresh general-state exporter runner hand-off

当前环境重新探测仍无 Julia，因此本轮没有 runtime 执行、CSV 或 receipt
PASS。现有 intake gate 未修改。

新增 fail-closed runner：

[`run_general_state_force_binding.ps1`](../examples/routeb_b45_5_descriptor_terms_adapter_lean/run_general_state_force_binding.ps1)

Runner 行为：

1. 缺少 Julia/Python 时只输出 `PENDING_JULIA_EXECUTION` 并退出 `2`；
2. exporter/deployed source hash 漂移时输出 `REJECTED_INPUT` 并退出 `3`；
3. 固定输出目录已存在时输出 `PENDING_FRESH_OUTPUT_DIR_EXISTS`，不覆盖旧 artifact；
4. 只有 clean output dir 才运行 exporter，捕获 `worker.stdout.txt`、
   `worker.stderr.txt`、`worker.exit-code.txt`，然后调用既有
   `verify_general_state_force_binding.py`；
5. 最终 acceptance 仍完全由既有 verifier 的 schema、16 rows、有限性、
   E1/E2≤1e-12 和 receipt/hash gate 决定。

## Frozen input hashes

```text
exporter = 5351110e81327ebc059074a2e445a33e00859320bce37b5b0220bb189f4e46a4
deployed dhport_lib.jl = aebe6db09b2d943448c5d701631109dba8f5eeb070cc66593e5dbaca26485936
```

执行 agent 直接运行：

```powershell
& .\examples\routeb_b45_5_descriptor_terms_adapter_lean\run_general_state_force_binding.ps1
```

成功时 runner 只会转发 verifier 的
`GENERAL_STATE_FORCE_BINDING_INTAKE=PASS_RUNTIME_FLOAT64_SOURCE_BINDING_CANDIDATE`
及 CSV/runtime/stdout/stderr hashes；这仍是有限状态 Float64 source-binding
candidate，不是 Lean exact-real theorem，也不是 deployed `tau` equivalence。

当前 disposition：

```text
JULIA_EXECUTION = NOT RUN HERE
FRESH_CSV = NOT GENERATED HERE
FRESH_RECEIPT = NOT GENERATED HERE
INTAKE = PENDING_JULIA_EXECUTION
MAIN_STATE_MUTATION = false
```

