---
kind: review_result
task_id: T-FLT-SPECTRAL-PREDICATE
source_agent: Codex
integration_status: pending
---

# Review Result: T-FLT-SPECTRAL-PREDICATE

## Exact statement

Created a new sidecar theorem in
`examples/anthropic_flt_spectral_predicate_sidecar/AnthropicFLTSpectralPredicateSidecar.lean`
with a concrete operator family and scalar predicate:

- `operatorFamily : Unit → (Fin 2 → ℚ) →ₗ[ℚ] (Fin 2 → ℚ)`
- `scalarPredicate : Unit → ℚ := fun _ => 1`
- `range_eq_eigenspace_of_operatorFamily :
  LinearMap.range f = (operatorFamily ()).eigenspace (scalarPredicate ())`

The theorem is for a finite-dimensional toy model and is explicitly not a direct
proof of any upstream FLT statement.

## Imports

- `Mathlib.LinearAlgebra.Eigenspace.Basic`
- `Mathlib.Data.Matrix.Basic`

## Commands

- `Get-Content examples\\anthropic_flt_spectral_sidecar\\AnthropicFLTSpectralSidecar.lean`
- `rg -n "def eigenspace|theorem .*eigenspace|mem_eigenspace|LinearMap\\.eigenspace" examples\\anthropic_flt_reusable_lean\\.lake\\packages\\mathlib\\Mathlib -g "*.lean"`
- `rg -n "Submodule\\.subtype|range .*subtype|LinearMap\\.range.*subtype" examples\\anthropic_flt_reusable_lean\\.lake\\packages\\mathlib\\Mathlib -g "*.lean"`

## Expected validation

Run from `examples/anthropic_flt_spectral_predicate_sidecar`:

- `lake env lean AnthropicFLTSpectralPredicateSidecar.lean`

and then inspect:

- `#print axioms range_eq_eigenspace_of_operatorFamily`

## Exit codes

- repository/file discovery: `0`
- mathlib API search: `0`
- focused Lean compile: `1`

## Compile result

Attempted:

- `lake env lean AnthropicFLTSpectralPredicateSidecar.lean`

Error:

- `object file 'C:\Users\z5242\Desktop\重构版\工作流\examples\anthropic_flt_reusable_lean\.lake\packages\mathlib\.lake\build\lib\lean\Mathlib\Algebra\Algebra\Equiv.olean' of module Mathlib.Algebra.Algebra.Equiv does not exist`

Because the dependency build is incomplete in the current local environment, I could not reach the theorem body or a `#print axioms` emission in this pass.

## Provenance

- task id: `T-FLT-SPECTRAL-PREDICATE`
- source agent: `Codex`
- scope: new sidecar only, no mutation of `StateStore`, registry, task queue, or existing sidecars
- explicit boundary: concrete finite-dimensional abstraction only; not an upstream FLT theorem

## Blockers

- Need focused Lean compile confirmation for the new sidecar file.
- Need `#print axioms` result captured after compile.
- If the current proof shape fails on local mathlib APIs, the fallback is a
  conditional interface or a slightly simpler concrete statement that still
  keeps the operator family, scalar predicate, and eigenspace predicate visible.
