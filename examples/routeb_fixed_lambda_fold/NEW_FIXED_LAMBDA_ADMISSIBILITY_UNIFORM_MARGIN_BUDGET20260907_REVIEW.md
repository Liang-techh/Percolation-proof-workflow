# Fixed-lambda uniform margin budget review

## Scope and status

This sidecar adds the explicit finite-union margin-budget interface after the
uniform feasibility leaf.  It does not repeat monotonicity, fixed-2
feasibility, union cardinality, digest composition, or selected-box witness
lemmas.

No Lean or Lake command was run.  The file is an uncompiled typed interface,
not a kernel-verification receipt, comparator result, or registry admission.

## Contract supplied

- `UniformMarginLowerBound` records a scalar `delta`, `0 < delta`, and the
  explicit premise `delta ≤ marginAt lambda row` for every selected union row.
- `uniform_margin_budget_consumes_pointwise_load` gives the intended later
  absorption seam: any nonnegative pointwise load bounded by `delta` is bounded
  by every row margin.  It does not claim that a concrete residual has already
  been absorbed.
- `UniformUpperGapAndCoefficientBounds` records a uniform upper gap,
  positive lower bounds for `cellGamma` and `externalGamma`, and the pointwise
  coefficient bounds needed by a source adapter.
- `margin_lower_bound_from_uniform_gap` constructs the typed lower bound
  `delta = gap * cellLower` using the existing ratio field and exact scalar
  order algebra.

The external-gamma bound is intentionally explicit even though the displayed
delta estimate uses the cell lower bound and upper gap directly; it remains a
separate coefficient sanity premise for later source binding.

## Remaining boundaries

No finite minimum is computed from the declared receipt, and no displayed
ledger minimum is promoted to an exact theorem.  The gap, coefficient bounds,
ratio equality, and row set are all supplied premises.

This sidecar does not establish source/CSV binding, canonical digest validity,
complete 577-row or true-DH coverage, dense labels, residual/PDE/trajectory
closure, formal certificate validity, comparator acceptance, or registry
eligibility.  No state, registry, receipt, or shared script was modified.
