---
kind: execution_handoff
task_id: T-P4-KC-COORDINATE-ADAPTER
source_agent: codex-local
created_at: 2026-09-07
status: PENDING_JULIA_EXECUTION
---

# Short GitHub-runner handoff: fresh force export

本机探测：`JULIA_FOUND=False`。本文件不包含本机运行结果；不改变 gate。

## Required staging

在 clean GitHub checkout 中保留 workflow repo 为：

```text
$GITHUB_WORKSPACE
```

将 canonical deployed source snapshot 放在 exporter 预期的 sibling path：

```text
$GITHUB_WORKSPACE/../6dof_sos_optimized/6dof_sos_optimized/robot_final/dhport_lib.jl
```

固定输入：

```text
exporter = examples/routeb_b45_5_descriptor_terms_adapter_lean/general_state_force_binding_export.jl
exporter_sha256 = 5351110e81327ebc059074a2e445a33e00859320bce37b5b0220bb189f4e46a4
deployed_source_sha256 = aebe6db09b2d943448c5d701631109dba8f5eeb070cc66593e5dbaca26485936
runner = examples/routeb_b45_5_descriptor_terms_adapter_lean/run_general_state_force_binding.ps1
verifier = examples/routeb_b45_5_descriptor_terms_adapter_lean/verify_general_state_force_binding.py
```

## Short execution command

On a clean GitHub runner with Julia and Python available, run from
`$GITHUB_WORKSPACE`:

```bash
pwsh -NoLogo -NoProfile -File \
  examples/routeb_b45_5_descriptor_terms_adapter_lean/run_general_state_force_binding.ps1
```

The runner itself checks both frozen hashes, refuses an existing output
directory, executes Julia, captures stdout/stderr/exit code, and invokes the
existing strict verifier. Do not replace it with a direct exporter invocation.

## Required uploaded output

Upload this entire directory as one artifact:

```text
examples/routeb_b45_5_descriptor_terms_adapter_lean/output/general-state-export-20260907/
```

It must contain:

```text
force_binding_states.csv
FORCE_BINDING_RECEIPT.md
worker.stdout.txt
worker.stderr.txt
worker.exit-code.txt
```

Also retain the verifier/job stdout, including the final intake line and all
reported hashes.

## Acceptance fields

The execution receipt is admissible only if it records:

```text
GENERAL_STATE_FORCE_BINDING_INTAKE=PASS_RUNTIME_FLOAT64_SOURCE_BINDING_CANDIDATE
SOURCE_SHA256=aebe6db09b2d943448c5d701631109dba8f5eeb070cc66593e5dbaca26485936
EXPORTER_SHA256=5351110e81327ebc059074a2e445a33e00859320bce37b5b0220bb189f4e46a4
CSV_SHA256=<fresh value>
RUNTIME_RECEIPT_SHA256=<fresh value>
STDOUT_SHA256=<fresh value>
STDERR_SHA256=<fresh value>
MAX_E1=<value <= 1e-12>
MAX_E2=<value <= 1e-12>
```

The verifier additionally requires exact B/D order `B=[4,5]`, `D=[1,2,3,6]`,
16 data rows, complete schema, finite numeric fields, and process exit code `0`.

Any missing artifact, hash drift, nonzero exit, schema mismatch, or residual
failure remains `PENDING`/`REJECTED`; it must not be relabeled PASS. This
finite-state runtime candidate does not assert a Lean exact-real theorem or
deployed `tau` equivalence.

