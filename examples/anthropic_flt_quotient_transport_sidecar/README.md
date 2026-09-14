# Anthropic FLT quotient transport sidecar

This is a minimal target-side probe for the highest-value non-number-theoretic
candidate from the FLT scan:

- `Submodule.Quotient.continuousLinearEquiv` (adapted as
  `quotientContinuousLinearEquiv`);
- `Submodule.quotientPiContinuousLinearEquiv` (adapted as
  `quotientPiContinuousLinearEquiv`).

Classification: **directly reusable API candidate**, pending the pinned GitHub
compile and independent admission review.  The finite-index and topological
additive-group assumptions are intentionally unchanged; they are part of the
contract, not an implementation detail.

Potential use in the main system: transport a finite-dimensional quotient of a
constraint/error space to a coordinate-product quotient while keeping the map
continuous.  This can support P3 cell/coordinate adapters or P8 projected
state representations, but it proves neither interval coverage nor flowpipe
containment.

The sidecar is not a Route-B theorem and is not registered as `VERIFIED` merely
because CI compiles it.  Source binding, domain coverage, residual absorption,
and kernel/admission gates remain separate.

Provenance: Anthropic FLT repository commit
`aa2d8b34692b16c70f699536de0d8e75b9a3e9ef`, source
`Definitions/Def_Mathlib_Topology_Algebra_Module_Quotient.lean:5-37`, upstream
Lean `4.33.1`, with Mathlib revision
`db584cd6d46c92f209a44c0f1c829460d327499d` recorded in that repository's
`lake-manifest.json`.

The upstream FLT README explicitly states that its Lean `4.33.1` build has no
matching prebuilt Mathlib cache and that Mathlib is compiled from source.  That
full replay requires resources far beyond this repository's portable GitHub
sidecar lane, so CI must not pretend that `lake exe cache get` at the FLT root
is a valid bootstrap.

Portable CI therefore separates **source provenance** from **compatibility
compilation**.  It checks out the exact FLT commit and verifies its Lean
`4.33.1` toolchain plus pinned Mathlib revision, then independently checks out
that exact Mathlib revision and compiles this extracted API using the Mathlib
revision's own Lean `4.33.0` toolchain and official cache.  `verify.sh` requires
both `SOURCE_ROOT` (the pinned FLT checkout) and `LAKE_ROOT` (the pinned Mathlib
checkout), preserves placeholder and `#print axioms` gates, and prints the two
toolchains separately.

A green portable compile is therefore only a **Mathlib-4.33.0 compatibility
receipt for the extracted theorem statements**, not an exact replay of the
upstream FLT Lean-4.33.1 source-built environment and not a registry admission.
Any claim that specifically depends on the Lean-4.33.1 replay still requires a
separate appropriately resourced source build or equivalent independent
receipt.
