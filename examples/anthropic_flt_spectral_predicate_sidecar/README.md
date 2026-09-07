# Anthropic FLT Spectral Predicate Sidecar

This directory is a focused sidecar for `T-FLT-SPECTRAL-PREDICATE`.

Scope:

- a concrete operator family over `Fin 2 → ℚ`
- a scalar predicate `scalarPredicate : Unit → ℚ`
- a genuine range-to-eigenspace equality
- explicitly not an upstream FLT theorem proof

Provenance:

- upstream candidate commit: `aa2d8b34692b16c70f699536de0d8e75b9a3e9ef`
- candidate declaration:
  `Submodule.exists_injective_linearMap_baseChange_torsionBySet_range_eq_eigenspace`

Files:

- `AnthropicFLTSpectralPredicateSidecar.lean`
- `lakefile.lean`
- `lean-toolchain`
- `verify.sh`

The theorem is intentionally small and self-contained. It is meant to show the
predicate/eigenspace interface directly, not to develop number theory.
