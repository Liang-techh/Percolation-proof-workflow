# Anthropic FLT spectral predicate sidecar

Task: `T-FLT-SPECTRAL-PREDICATE`.

This corrective sidecar replaces the previous tautological `range = range`
helper with a theorem whose statement contains the genuine eigenvector
predicate

```text
T v = μ • v
```

and proves equality between `LinearMap.range f` and the set of all vectors
satisfying that predicate, provided two explicit semantic premises hold:

1. every vector in the range is a `μ`-eigenvector of `T`;
2. every `μ`-eigenvector of `T` has a preimage under `f`.

A second theorem carries an explicit `Function.Injective f` premise to mirror
the shape of the upstream FLT candidate.

## Provenance boundary

Upstream candidate:

- commit: `aa2d8b34692b16c70f699536de0d8e75b9a3e9ef`
- path: `Theorems/Thm_Submodule_exists_injective_linearMap_baseChange_torsionBySet_range_eq_eigenspace.lean`
- declaration: `Submodule.exists_injective_linearMap_baseChange_torsionBySet_range_eq_eigenspace`

This directory does **not** import the upstream theorem or its FLT-specific
`P2M.Sol...` proof surface. It is a self-contained abstraction of the spectral
interface only. Therefore it is not evidence of direct upstream theorem reuse
and does not justify Route-B/registry promotion.

## Focused check

Run:

```bash
./verify.sh
```

The Lean file includes `#print axioms` for both exported theorems. The scheduled
agent that created this sidecar did not have a local Lean executable available,
so compilation must remain pending until the focused verifier is run in a Lean
4.33.1 / compatible Mathlib environment.
