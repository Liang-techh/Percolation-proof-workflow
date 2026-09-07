---
kind: review_result
task_id: T-P0-001
source_agent: Codex
created_at: 2026-09-06T21:00:00-06:00
integration_status: pending
---

# T-P0-001：Route-B reproducibility baseline 只读复核

## Scope and mutation boundary

本次只读取当前工作流 checkpoint、既有 attempt/receipt/event 记录，以及外部项目的文件元数据和 SHA-256。没有运行长回归，没有修改外部项目，没有修改 `state.json`、registry、frontier 或 queue。

Inspected:

- `artifacts/routeb_6dof/state.json`（当前 revision `332`）
- 外部项目 `C:\Users\z5242\Desktop\重构版\6dof_sos_optimized\6dof_sos_optimized`
- 外部 `robot_final/verify_all.py`
- P0 节点 `527611b83f6a49dda06a0d4eb711f129`

## Existing P0 attempts

P0 仍为 `open`，没有 `verified_artifact`，registry 为空。

| attempt | recorded status | command | exit code | source hash fields |
|---|---|---|---:|---|
| `f28416d2ebac43e59cbd4636af72d183` | `passed` | `python robot_final/verify_all.py` | 0 | receipt contains six source hashes and `source_unchanged=true` |
| `7f0c218aacb5463eb910f117d99823c8` | `external_gate_error` | `python robot_final/verify_all.py` | 1 | no attached receipt/source hash set |

The state history explicitly records the later failure as reopening P0 and identifies these unresolved issues: current delivery source differs from the historical manifest, authoritative and delivery interval sources differ, the target artifact index is stale, and the current delivery checker failed. It also retracts the reproducibility claim based on relabelled historical source hashes.

## Hash audit

The historical successful receipt records:

- `robot_final/verify_all.py`: `982efd4b21b1a390e425fc49103bc675efd71d08bc168076352ff752d6b39a6f`
- `robot_final/routeB_certificate_manifest.toml`: `45dedbd700aa012b356e84a146407b5a92c96266a3f6549198b406f10eef5716`
- `PROJECT_REFORM_AUDIT.md`: `a64c6a63c21e72adf233fe12ffd3cc4ed03bd3f26c54a6f496cf6a553b4ca342`
- `PROJECT_REFORM_TARGET.md`: `439a7378bdbf8950445b91a66d917535ede341065ced8a548a176517d679138c`
- `robot_formal_v1/README.md`: `41e82581c476a3ec94faf6e374c2605c215df36dc3b4b430cde029fb24a572c0`
- `robot_formal_v1/manifest.json`: `951f263780cc0fb9e35b54d119eed91289de45eb02da75b3bcf3a70aca600ae3`

The current external `verify_all.py` hash still matches the historical value:

`982EFD4B21B1A390E425FC49103BC675EFD71D08BC168076352FF752D6B39A6F`

However, the current external `routeB_certificate_manifest.toml` hash is:

`D9AE90AF1860364EAE950649B3FFBF1810D78583383781EC9FA6949FDD24F495`

which does **not** match the historical successful receipt (`45ded...`). Additional current hashes read for context were:

- `robot_final/routeB_export_manifest.toml`: `5B61D624F4F6060DA8C33A51FA7982BEF8206D2C3924BABB512440DEFAD89187`
- `robot_final/routeB_certificate_status.csv`: `DE59F7B7FD284B5E7182ACF2A9A3DECE8647B8102B92E9ED585ECA77657C29D6`
- `robot_final/routeB_partition_coverage.json`: `E2051669922B1213162CFEC4F82EF21E5B5B0DE951AD6CCDF176E972905B713A`

This is sufficient to invalidate direct reuse of the old successful receipt as a current baseline. It is not evidence that `verify_all.py` itself changed; it is evidence of source/manifest drift.

## P0 gate decision

`P0.reproducibility_baseline` is **not eligible for `evidence_complete`**.

The prior exit-code-zero run is historical engineering evidence only. The later exit-code-one run, the manifest hash mismatch, and the state event `current_baseline_complete=false` prevent closure. The P0 node must remain `open`; `integration_status` remains `pending`.

## Minimum gates still missing

1. Restore or explicitly version the authoritative/delivery source relationship; identify the exact manifest intended for the current checkout.
2. Produce a fresh receipt from the current external project with command, cwd, stdout/stderr, exit code, complete source hash map, and before/after snapshot hashes.
3. Resolve the stale artifact index and prove that every required P0 artifact is present and bound to the same snapshot.
4. Reconcile the current delivery interval source with the authoritative interval source; a passing checker alone is insufficient while they differ.
5. Re-run only the approved reproducibility checker after the above reconciliation. Do not promote the result to Lean registry: P0 is an external engineering gate.

The global fail-closed conditions remain unchanged: no registry promotion and `formal_certificate_allowed=false` (as recorded by the existing state history and target gate snapshot).

