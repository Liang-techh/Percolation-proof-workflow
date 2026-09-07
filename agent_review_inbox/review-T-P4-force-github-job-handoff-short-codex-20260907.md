---
kind: execution_handoff
task_id: T-P4-KC-COORDINATE-ADAPTER
source_agent: codex-local
date: 2026-09-07
status: PENDING_RUNTIME_JULIA
---

# Force runtime: shortest GitHub Actions handoff

本机没有 Julia，未执行 exporter，未产生 runtime PASS。连接任务中没有可直接使用的 Julia-capable host；本文件只提供可复制的 runner job，不改变 strict gate。

## One-time repository variables

在仓库 Settings -> Variables 中设置：

```text
DEPLOYED_SOURCE_REPOSITORY=<owner>/<deployed-dhport-source-repository>
DEPLOYED_SOURCE_REF=<pinned-ref-containing-the-frozen-dhport_lib.jl>
```

`DEPLOYED_SOURCE_REF` 必须解析到已约定的 deployed source snapshot；job 若未设置变量会在 source staging 处失败，不得回退到其他 source。

## Copyable job

将以下内容作为 `.github/workflows/force-general-state-export.yml`，手动 `workflow_dispatch`：

```yaml
name: force-general-state-export

on:
  workflow_dispatch:

jobs:
  force-runtime:
    runs-on: ubuntu-latest
    timeout-minutes: 15
    steps:
      - uses: actions/checkout@v4
        with:
          path: workflow

      - uses: actions/checkout@v4
        with:
          repository: ${{ vars.DEPLOYED_SOURCE_REPOSITORY }}
          ref: ${{ vars.DEPLOYED_SOURCE_REF }}
          path: deployed-source

      - uses: julia-actions/setup-julia@v2
        with:
          version: '1.10'

      - name: Stage deployed source and run strict exporter gate
        shell: pwsh
        working-directory: workflow
        run: |
          if ([string]::IsNullOrWhiteSpace($env:DEPLOYED_SOURCE_REPOSITORY) -or
              [string]::IsNullOrWhiteSpace($env:DEPLOYED_SOURCE_REF)) {
            throw 'DEPLOYED_SOURCE_REPOSITORY/DEPLOYED_SOURCE_REF are required'
          }
          $target = Join-Path $env:GITHUB_WORKSPACE '..\6dof_sos_optimized\6dof_sos_optimized'
          New-Item -ItemType Directory -Force -Path $target | Out-Null
          Copy-Item (Join-Path $env:GITHUB_WORKSPACE 'deployed-source\6dof_sos_optimized\robot_final') `
            (Join-Path $target 'robot_final') -Recurse -Force
          & pwsh -NoLogo -NoProfile -File `
            'examples/routeb_b45_5_descriptor_terms_adapter_lean/run_general_state_force_binding.ps1'
          if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
        env:
          DEPLOYED_SOURCE_REPOSITORY: ${{ vars.DEPLOYED_SOURCE_REPOSITORY }}
          DEPLOYED_SOURCE_REF: ${{ vars.DEPLOYED_SOURCE_REF }}

      - name: Upload complete force receipt
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: force-general-state-export-20260907-${{ github.run_id }}
          path: |
            workflow/examples/routeb_b45_5_descriptor_terms_adapter_lean/output/general-state-export-20260907/
            workflow/**/worker.stdout.txt
            workflow/**/worker.stderr.txt
            workflow/**/worker.exit-code.txt
          if-no-files-found: error
```

## Acceptance intake

仅当 runner/verifier 输出并上传下列字段时才可进入 receipt intake：

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

同时必须满足：`force_binding_states.csv` 恰为 16 rows，`B=[4,5]`、`D=[1,2,3,6]`，完整 schema，所有字段 finite，worker/verifier exit code 为 0，并保留 stdout/stderr/exit receipt。缺文件、hash drift、非零退出、schema/row/residual 失败均保持 pending/rejected；不得把 runner 或旧 CSV 当作 PASS。

本 handoff 不声称 runtime 已执行，不修改主 state，不推出 deployed tau 等价。
