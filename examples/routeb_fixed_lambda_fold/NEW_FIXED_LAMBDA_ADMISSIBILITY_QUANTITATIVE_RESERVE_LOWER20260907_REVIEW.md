# Quantitative aggregate reserve lower-bound review

## Scope and status

This sidecar adds only the quantitative lower-bound leaf after finite reserve
aggregation.  It does not repeat total-reserve aggregation, the existing
one-strict-witness bridge, eta partition, digest, cardinality, monotonicity,
or final export construction.

No Lean or Lake command was run.  This is an uncompiled bounded proof attempt,
not a kernel-verification receipt, comparator result, or registry admission.

## Contract supplied

- `QuantitativeReserveLowerPremise` keeps fixed lambda, finite nonemptiness,
  per-cell `delta ≥ 0`, `delta ≤ reserve`, and an explicit positive delta
  witness.  The underlying family retains pairwise-disjoint support and each
  cell's denominator/ratio fields.
- `total_delta_positive` uses the finite-sum positivity library lemma rather
  than duplicating the prior strict-witness bridge.
- `total_delta_le_total_reserve` gives the computable aggregate lower bound,
  and `StrictAggregateReserveLowerBound` packages
  `0 < Σ delta ≤ Σ reserve`.
- `quantitative_lower_bound_to_final_budget` uses explicit total equality and
  shared-lambda adapter premises to place `Σ delta` below the final weighted
  load while retaining the already supplied final strict load `<` margin.

## Open conditions and non-claims

If the finite family is empty, deltas are not nonnegative, or no positive
delta witness is supplied, the strict lower-bound certificate remains open.
No cell coverage, digest, source/CSV binding, receipt, Lean compilation,
residual/PDE/trajectory closure, comparator acceptance, or registry eligibility
is inferred.

No state, registry, receipt, or shared script was modified.
