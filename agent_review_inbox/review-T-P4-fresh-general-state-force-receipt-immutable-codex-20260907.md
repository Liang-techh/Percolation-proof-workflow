---
kind: immutable_receipt
task_id: T-P4-KC-COORDINATE-ADAPTER
source_agent: codex-local
created_at: 2026-09-07
status: PENDING_JULIA_EXECUTION
---

# Fresh general-state force exporter receipt

## Obstruction recorded by this worker

The requested exporter was not executed in this environment.

```text
command: Get-Command julia -ErrorAction SilentlyContinue
result: JULIA_COMMAND_FOUND=False

command: where.exe julia
result: WHERE_JULIA_EXIT_CODE=1
result: WHERE_JULIA_OUTPUT=<empty>
```

Python is available, but that cannot execute the Julia exporter. No runner
invocation was made in this worker. No old CSV or old receipt was consumed as a
fresh result.

## Frozen input identity

```text
exporter:
examples/routeb_b45_5_descriptor_terms_adapter_lean/general_state_force_binding_export.jl
exporter_sha256:
5351110e81327ebc059074a2e445a33e00859320bce37b5b0220bb189f4e46a4

deployed source:
C:\Users\z5242\Desktop\重构版\6dof_sos_optimized\6dof_sos_optimized\robot_final\dhport_lib.jl
deployed_source_sha256:
aebe6db09b2d943448c5d701631109dba8f5eeb070cc66593e5dbaca26485936
```

Both hashes were freshly recomputed before this receipt was written and match
the frozen gate values.

## Required fresh artifact, not produced here

An execution agent with Julia must produce one new output directory containing
the CSV and runtime receipt, with:

```text
sample_count = 16
B = [4,5]
D = [1,2,3,6]
same-state fields = qB,vB,w,CdqB,GqB,G0B,tauB,rhsB,sourceBlockForce,
                    aB,aD,MqBB,MqBD,sourceDescriptorRhs
component residuals = E1_4,E1_5,E2_4,E2_5
max(abs(E1)), max(abs(E2)) <= 1e-12
process exit code = 0
stdout + stderr + exit-code receipt present
CSV SHA and runtime receipt SHA present
```

The existing verifier remains the only acceptance check. This file does not
alter that gate and does not supply any runtime values.

## Negative receipt facts

```text
RUNNER_OUTPUT_EXISTS=False
FRESH_CSV_EXISTS=False
FRESH_RECEIPT_EXISTS=False
runtime_status = NOT_OBTAINED
deployed_tau_equivalence = NOT_CLAIMED
registry_promotion = false
main_state_mutation = false
```

This is an obstruction receipt only; it is not a compiled/runtime PASS and not
a source/DH equivalence claim.

