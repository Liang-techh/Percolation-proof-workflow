# Anthropic FLT spectral predicate sidecar

Task: `T-FLT-SPECTRAL-PREDICATE`.

This corrective sidecar replaces the previous tautological `range = range`
helper with a theorem whose statement contains a genuine eigenvector predicate
and proves a concrete range-to-eigenspace equality over `Fin 2 → ℚ`.

The upstream candidate is retained as provenance only:

- commit: `aa2d8b34692b16c70f699536de0d8e75b9a3e9ef`
- path: `Theorems/Thm_Submodule_exists_injective_linearMap_baseChange_torsionBySet_range_eq_eigenspace.lean`
- declaration: `Submodule.exists_injective_linearMap_baseChange_torsionBySet_range_eq_eigenspace`

This directory does not import the upstream theorem or its FLT-specific
`P2M.Sol...` proof. It is a self-contained abstraction, not direct upstream
reuse and not a Route-B/registry admission.

## Focused check

Run `lake env lean AnthropicFLTSpectralPredicateSidecar.lean` through
`verify.sh`. The Lean file includes `#print axioms` for the exported theorem.
