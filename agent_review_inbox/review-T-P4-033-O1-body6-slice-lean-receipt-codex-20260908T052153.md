---
kind: review_result
review_id: review-T-P4-033-O1-body6-slice-lean-receipt-codex-20260908T052153
task_id: T-P4-033-O1-body6-slice
agent: Codex
source_agent: Codex
created_at: 2026-09-08T05:21:53-06:00
inspected_paths:
  - examples/routeb_b45_source_comparator_lean/NEW_BODY6_SLICE_PATHDOMAINPROJECTION20260907.lean
  - examples/routeb_b45_source_comparator_lean/NEW_BODY6_SLICE_INITIALPATHCAPS20260907.lean
  - examples/routeb_b45_source_comparator_lean/NEW_BODY6_SLICE_PATHDOMAINPROJECTION20260907.review.md
  - examples/routeb_b45_source_comparator_lean/NEW_BODY6_SLICE_INITIALPATHCAPS20260907.review.md
integration_status: pending
admission_label: pending
proof_status: LEAN_ELAB_ERROR; BUILD_ENV_BLOCKED_DEPENDENCY
registry_status: unchanged
registry_mutation: false
---

# BODY6 focused Lean receipt — path/domain and initial/full-path caps

## Scope

This was a two-file focused check only. No full-project regression, registry
mutation, source binding, ODE claim, or formal-gate change was performed.

The pinned project toolchain is `leanprover/lean4:v4.32.0`; `lake env lean
--version` reports Lean 4.32.0. The standalone `lake.exe --version` shim may
report the host default 4.33.1, so the receipt uses the project environment and
records the pinned `lake env lean` result.

## Placeholder scan

Static scan over both source files returned no `sorry`, `admit`, `axiom`,
`opaque`, `unsafe`, or `native_decide` matches. This is only a source scan;
it is not a kernel or axiom receipt.

## PATHDOMAINPROJECTION

Command, from `examples/local_fkg`:

```powershell
$lake='C:\Users\z5242\.elan\bin\lake.exe'
$file='C:\Users\z5242\Desktop\重构版\工作流\examples\routeb_b45_source_comparator_lean\NEW_BODY6_SLICE_PATHDOMAINPROJECTION20260907.lean'
& $lake env lean -DwarningAsError=true $file
```

Exit code: `1`.

Classification: `LEAN_ELAB_ERROR`.

Exact diagnostic:

```text
...NEW_BODY6_SLICE_PATHDOMAINPROJECTION20260907.lean:53:47: error:
Application type mismatch: The argument hBudget has type
cap + B ≤ bar but is expected to have type B + cap ≤ ?m.54
in the application
LE.le.trans (add_le_add_right (hCap t ht) B) hBudget
```

The failing proof is `projected_shift_cap_transfer_attempt`. The smallest
repair is to normalize the commutative sum before consuming the budget, for
example:

```lean
have hBudget' : B + cap ≤ bar := by simpa [add_comm] using hBudget
exact (add_le_add_right (hCap t ht) B).trans hBudget'
```

No `#print axioms` output is admissible for this file because compilation did
not complete and no successful sidecar environment was produced. Treat the
axiom receipt as `NOT_AVAILABLE`, not as PASS.

## INITIALPATHCAPS

The first attempted `-I` command was rejected by Lean 4.32 itself (`unknown
option -- I`), so it is not used as a source failure. The valid dependency-aware
attempt used the source directory in `LEAN_PATH`:

```powershell
$lake='C:\Users\z5242\.elan\bin\lake.exe'
$root='C:\Users\z5242\Desktop\重构版\工作流\examples\routeb_b45_source_comparator_lean'
$file=Join-Path $root 'NEW_BODY6_SLICE_INITIALPATHCAPS20260907.lean'
$env:LEAN_PATH="$root;$env:LEAN_PATH"
& $lake env lean -DwarningAsError=true $file
```

Exit code: `1`.

Classification: `BUILD_ENV_BLOCKED_DEPENDENCY`.

Exact diagnostic: unknown module prefix
`NEW_BODY6_SLICE_PATHDOMAINPROJECTION20260907`; no source/olean for that
module was present in the search path. This is a consequence of the imported
PATHDOMAINPROJECTION file not producing a successful `.olean`, not evidence
that INITIALPATHCAPS itself elaborates.

No `#print axioms` output is admissible for INITIALPATHCAPS either;
`#print axioms = NOT_AVAILABLE` pending a successful dependency build.

## Hashes and admission boundary

```text
NEW_BODY6_SLICE_PATHDOMAINPROJECTION20260907.lean
C3D0432FB2B53815BB9E23271ECADFA871E5526A96B9BF7B533EFE392D2AA6AC

NEW_BODY6_SLICE_INITIALPATHCAPS20260907.lean
5CAD04F2E8B0AF13C8D8A099455812FE1F6D17A66A0D567BE5B85963252D224
```

Keep both leaves `OPEN_UNCOMPILED/pending`. After the one-line commutativity
repair, rerun PATHDOMAINPROJECTION first, emit its complete stdout/stderr and
`#print axioms`, then compile INITIALPATHCAPS against the resulting module.
Neither result may be promoted to VERIFIED or written to the registry from
this receipt.
