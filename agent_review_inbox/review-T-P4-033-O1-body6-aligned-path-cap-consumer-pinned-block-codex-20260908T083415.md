---
kind: review_result
review_id: review-T-P4-033-O1-body6-aligned-path-cap-consumer-pinned-block-codex-20260908T083415
task_id: T-P4-033-O1-body6-slice
agent: Codex
source_agent: Codex
created_at: 2026-09-08T08:34:15-06:00
inspected_paths:
  - examples/routeb_b45_source_comparator_lean/NEW_BODY6_SLICE_ALIGNEDPATHCAPCONSUMER20260908.lean
  - examples/routeb_b45_source_comparator_lean/NEW_BODY6_SLICE_ACTUALSTORAGEALIGN20260907.lean
integration_status: pending
admission_label: pending
proof_status: BUILD_ENV_BLOCKED_TOOLCHAIN_MISMATCH
registry_status: unchanged
registry_mutation: false
---

# BODY6 aligned path-cap consumer — pinned dependency receipt

## Scope

This was a focused dependency-aware attempt only. The already successful
PATHDOMAINPROJECTION and INITIALPATHCAPS sidecars were not rerun as a project
regression. No registry, source admission, ODE, or formal-gate state was
changed.

## Pinned command and result

The command used the pinned `examples/local_fkg` environment and a bounded
`LEAN_PATH` containing only existing cached module directories for
`ActualStorage`, `ActualShift`, `ReferenceMass`, `ShiftedStorage`,
`PotentialSlice`, `SignedGap`, and their direct algebraic dependencies.

First, the direct imported sidecar was targeted:

```powershell
$lake='C:\Users\z5242\.elan\bin\lake.exe'
$src='C:\Users\z5242\Desktop\重构版\工作流\examples\routeb_b45_source_comparator_lean'
$file=Join-Path $src 'NEW_BODY6_SLICE_ACTUALSTORAGEALIGN20260907.lean'
$out=Join-Path $src 'NEW_BODY6_SLICE_ACTUALSTORAGEALIGN20260907.olean'
& $lake env lean -DwarningAsError=true -R $src -o $out $file
```

Exit code: `1`.

Exact first diagnostic:

```text
...NEW_BODY6_SLICE_ACTUALSTORAGEALIGN20260907.lean:1:0:
error: failed to read file
...routeb_actual_energy_storage_lean\output\run-ZWEIdfZ8\ActualStorage.olean,
incompatible header
```

Classification: `BUILD_ENV_BLOCKED_TOOLCHAIN_MISMATCH`. The cached
`ActualStorage.olean` is not consumable by the pinned Lean 4.32 environment.

The aligned consumer command was then attempted with the same bounded
dependency-aware `LEAN_PATH`:

```powershell
$file=Join-Path $src 'NEW_BODY6_SLICE_ALIGNEDPATHCAPCONSUMER20260908.lean'
& $lake env lean -DwarningAsError=true $file
```

Exit code: `1`; classification remains `BUILD_ENV_BLOCKED` because the direct
`NEW_BODY6_SLICE_ACTUALSTORAGEALIGN20260907` module has no pinned-compatible
`.olean`.

## Static audit and hashes

Placeholder scan over both target source files found no `sorry`, `admit`,
`axiom`, `opaque`, `unsafe`, or `native_decide`: `PLACEHOLDER_SCAN=PASS`.
`#print axioms`: `NOT_AVAILABLE`; neither target obtained a pinned-compatible
compiled module.

```text
NEW_BODY6_SLICE_ALIGNEDPATHCAPCONSUMER20260908.lean
F698D8C56C83005DF0E0A907452AE7A6F083EB3736E6DF60DB4D0190084367DD

NEW_BODY6_SLICE_ACTUALSTORAGEALIGN20260907.lean
F8DA2E44F9AFC4C80FC14E81A1C59626D5AF98071300A009AECD33463D3BEF56
```

## Required repair boundary

Rebuild the imported `ActualStorage`/`ActualShift` closure under the exact
pinned Lean 4.32 toolchain, or provide a compatible pinned artifact with its
own stdout/stderr, exit code and hash. Then compile the direct alignment
sidecar, followed by the aligned consumer, and collect `#print axioms` for
both. Keep this lane pending; do not promote a cache-compatible or source-only
candidate to VERIFIED or the registry.
