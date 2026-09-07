# Weighted residual absorption budget review

## Scope and status

This sidecar adds only the finite weighted-sum consumer after the strict
margin layer.  It does not repeat strict-margin derivation, digest, union
cardinality, monotonicity, or fixed-λ feasibility.

No Lean or Lake command was run.  This is an uncompiled typed interface, not a
kernel-verification receipt, comparator result, or registry admission.

## Contract supplied

- `StrictLoadBelowDelta` accepts exactly `0 ≤ load < delta` on every selected
  union row, while `UniformMarginLowerBound` supplies `delta ≤ marginAt`.
- `NonnegativeCoefficient` is an explicit finite-union premise for the load
  coefficients.
- `weighted_load_term_le_delta_term` proves the rowwise coefficient-weighted
  budget inequality; with a positive coefficient,
  `weighted_load_term_lt_delta_term_of_positive_coefficient` gives the strict
  version from `load < delta`.
- `total_weighted_load_le_total_delta` and
  `total_delta_le_total_weighted_margin` combine by finite `Finset` summation
  to yield `total_weighted_load_le_total_weighted_margin`.

The result is a budget bridge for a later residual absorption proof.  A strict total inequality is not claimed from nonnegative coefficients alone, because
all coefficients could be zero; a positive selected coefficient remains an
explicit future premise.

## Remaining boundaries

The load, coefficient, delta, and row-margin premises are external typed
inputs.  This sidecar does not identify them with a source residual, compute a
receipt minimum, validate a digest, or prove source/coverage/PDE/trajectory
closure.  It does not imply formal certificate validity, comparator
acceptance, or registry eligibility.

No state, registry, receipt, or shared script was modified.
