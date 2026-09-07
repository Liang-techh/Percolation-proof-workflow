---
kind: review_result
task_id: T-P4-KC-COORDINATE-ADAPTER
source_agent: codex-local
created_at: 2026-09-07
integration_status: pending
---

# Fresh general-state export：execution-agent hand-off

当前 Codex worker 没有 Julia；本文件只交付执行命令和 intake checker，未
生成、读取或伪造 runtime PASS。

## Frozen inputs

```text
exporter:
examples/routeb_b45_5_descriptor_terms_adapter_lean/general_state_force_binding_export.jl
SHA256=5351110e81327ebc059074a2e445a33e00859320bce37b5b0220bb189f4e46a4

deployed source:
C:\Users\z5242\Desktop\重构版\6dof_sos_optimized\6dof_sos_optimized\robot_final\dhport_lib.jl
SHA256=aebe6db09b2d943448c5d701631109dba8f5eeb070cc66593e5dbaca26485936

intake checker:
examples/routeb_b45_5_descriptor_terms_adapter_lean/verify_general_state_force_binding.py
```

## Execution-agent command (PowerShell)

Run from `C:\Users\z5242\Desktop\重构版\工作流`:

```powershell
$exporter = (Resolve-Path 'examples/routeb_b45_5_descriptor_terms_adapter_lean/general_state_force_binding_export.jl').Path
$out = Join-Path (Split-Path $exporter) 'output/general-state-export-20260907'
$stdout = Join-Path $out 'worker.stdout.txt'
$stderr = Join-Path $out 'worker.stderr.txt'
$exitFile = Join-Path $out 'worker.exit-code.txt'
New-Item -ItemType Directory -Force -Path $out | Out-Null
& julia --startup-file=no $exporter 1> $stdout 2> $stderr
$LASTEXITCODE | Set-Content -NoNewline -Encoding utf8 $exitFile
python examples/routeb_b45_5_descriptor_terms_adapter_lean/verify_general_state_force_binding.py `
  --export-dir $out --stdout $stdout --stderr $stderr --exit-code $exitFile
```

The agent must preserve the generated `force_binding_states.csv`,
`FORCE_BINDING_RECEIPT.md`, `worker.stdout.txt`, `worker.stderr.txt`, and
`worker.exit-code.txt`. Do not overwrite an earlier run directory while
collecting the receipt.

## Intake gates

The checker rejects unless all of the following hold:

1. exporter and deployed source hashes equal the frozen values above;
2. process exit code is exactly `0`;
3. stdout contains `GENERAL_STATE_FORCE_BINDING_EXPORT_STATUS=PASS_RUNTIME_FLOAT64`,
   both input hashes, and `MAX_E1`/`MAX_E2`;
4. CSV header/order is the complete exporter schema, including
   `qB,vB,w,CdqB,GqB,G0B,tauB,rhsB,sourceBlockForce,aB,aD,MqBB,MqBD`,
   `sourceDescriptorRhs`, and `E1_4,E1_5,E2_4,E2_5`;
5. exactly 16 data rows are present in sample order;
6. all numeric fields are finite and `max(abs(E1)) <= 1e-12`,
   `max(abs(E2)) <= 1e-12`;
7. generated Markdown receipt repeats the current exporter/source hashes and
   reports `PASS_RUNTIME_FLOAT64`.

On success, the checker prints
`GENERAL_STATE_FORCE_BINDING_INTAKE=PASS_RUNTIME_FLOAT64_SOURCE_BINDING_CANDIDATE`
and prints CSV, runtime-receipt, stdout, and stderr hashes. This is only a
finite-state Float64 source-binding candidate; it is not a Lean exact-real
theorem, not a global source proof, and not deployed `tau` equivalence.

## Current status

```text
JULIA_EXECUTION = NOT RUN (Julia unavailable here)
FRESH_CSV = NOT PRESENT FROM THIS RUN
FRESH_RECEIPT = NOT PRESENT FROM THIS RUN
INTAKE_STATUS = PENDING_JULIA_EXECUTION
DEPLOYED_TAU_EQUIVALENCE = NOT_CLAIMED
MAIN_STATE_MUTATION = false
```

