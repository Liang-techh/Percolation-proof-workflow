---
kind: review_result
review_id: review-T-P4-033-O1-body6-slice-lean-receipt-codex-20260908T082220
task_id: T-P4-033-O1-body6-slice
agent: Codex
source_agent: Codex
created_at: 2026-09-08T08:22:20-06:00
inspected_paths:
  - examples/routeb_b45_source_comparator_lean/NEW_BODY6_SLICE_PATHDOMAINPROJECTION20260907.lean
  - examples/routeb_b45_source_comparator_lean/NEW_BODY6_SLICE_INITIALPATHCAPS20260907.lean
integration_status: pending
admission_label: compiled_candidate
proof_status: FOCUSED_COMPILED
registry_status: unchanged
registry_mutation: false
---

# BODY6 focused pinned Lean receipt — PASS

## Scope and environment

Only the two named BODY6 sidecars were checked. No full-project regression,
source binding, ODE/continuation claim, registry mutation, or formal-gate
change was performed.

Project toolchain: `leanprover/lean4:v4.32.0`.
`lake env lean --version`: Lean 4.32.0, commit `8c9756b28d64dab099da31a4c09229a9e6a2ef35`.

## PATHDOMAINPROJECTION

The second repair introduced an explicit intermediate:

```lean
have hCap' : F t (path t) + B ≤ cap + B := by
  simpa [add_comm] using (add_le_add_right (hCap t ht) B)
exact hCap'.trans hBudget
```

Command from `examples/local_fkg`:

```powershell
$lake='C:\Users\z5242\.elan\bin\lake.exe'
$file='C:\Users\z5242\Desktop\重构版\工作流\examples\routeb_b45_source_comparator_lean\NEW_BODY6_SLICE_PATHDOMAINPROJECTION20260907.lean'
& $lake env lean -DwarningAsError=true $file
```

Exit code: `0`; stdout/stderr: empty.

## INITIALPATHCAPS

After the path sidecar compiled, it was emitted as a local `.olean` and the
dependent sidecar was compiled with the source directory on `LEAN_PATH`:

```powershell
$lake='C:\Users\z5242\.elan\bin\lake.exe'
$dir='C:\Users\z5242\Desktop\重构版\工作流\examples\routeb_b45_source_comparator_lean'
$file=Join-Path $dir 'NEW_BODY6_SLICE_INITIALPATHCAPS20260907.lean'
$env:LEAN_PATH="$dir;$env:LEAN_PATH"
& $lake env lean -DwarningAsError=true $file
```

Exit code: `0`; stdout/stderr: empty.

## Placeholder and axiom audit

Static scan over both source files found no `sorry`, `admit`, `axiom`,
`opaque`, `unsafe`, or `native_decide` declarations: `PLACEHOLDER_SCAN=PASS`.

A temporary audit module imported both successful `.olean` files and printed
axioms for all public theorems. Every theorem in both files reported exactly
the ordinary Lean baseline:

```text
[propext, Classical.choice, Quot.sound]
```

No `sorryAx` or non-baseline axiom was reported.

## Artifact hashes and boundary

```text
NEW_BODY6_SLICE_PATHDOMAINPROJECTION20260907.lean
F55DE2B76ED401E7962B1494D02826C8FC2F951D7137F02461EDEB56D5757D62

NEW_BODY6_SLICE_INITIALPATHCAPS20260907.lean
5CAD04F2E8B0AF13C8D8A099455812FE1F6D17A66A0D567BE5B85963252D224
```

This is a focused `compiled_candidate` receipt only. It does not prove the
concrete full-state path, actual projection, integrated growth, DH source
binding, trajectory continuation, coverage, comparator acceptance, or registry
admission. Keep integration status pending and registry unchanged.
