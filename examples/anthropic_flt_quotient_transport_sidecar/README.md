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
`Definitions/Def_Mathlib_Topology_Algebra_Module_Quotient.lean:5-37`, Lean
`4.33.1`, Mathlib revision
`db584cd6d46c92f209a44c0f1c829460d327499d`.  The upstream staging and Apache
attribution boundaries are recorded in the repository's FLT intake reports.
