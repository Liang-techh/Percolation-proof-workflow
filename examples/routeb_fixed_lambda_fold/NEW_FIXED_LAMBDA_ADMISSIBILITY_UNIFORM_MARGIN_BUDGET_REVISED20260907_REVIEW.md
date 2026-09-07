# Revised uniform margin budget bridge review

## Scope and status

This revision narrows and makes explicit the lower-bound seam requested for
downstream use.  It does not repeat monotonicity, digest, union cardinality,
selected-box, or fixed-2 feasibility results, and it does not compute a receipt minimum.

No Lean or Lake command was run.  This is an uncompiled typed interface, not
a kernel-verification receipt, comparator result, or registry admission.

## Exact bridge

- `ExplicitUpperGapCellLowerContract` exposes only the premises needed by the
  downstream margin estimate: `gap > 0`, `cellLower > 0`, rowwise
  `gap ≤ lambdaUpper - lambda`, rowwise `cellLower ≤ cellGamma`, and the
  rowwise ratio equality `lambdaUpper = externalGamma / cellGamma`.
- `marginAt_eq_upper_gap_mul_cell` proves the exact affine factorization
  `marginAt lambda row = (lambdaUpper - lambda) * cellGamma`, using the typed
  positive denominator.
- `explicit_delta_le_marginAt` then proves rowwise
  `gap * cellLower ≤ marginAt lambda row` by monotone multiplication.
- `revised_uniform_margin_lower_bound` packages `delta = gap * cellLower`
  into the existing lower-bound record, and `revised_budget_consumes_load`
  provides the pointwise downstream load consumer.

The ratio is an explicit contract field in this revision, even though the
existing cell record also carries a ratio field.  This prevents a later
adapter from accidentally mixing metrics or ledgers without stating the
binding premise.

## Remaining boundaries

All gap, coefficient, ratio, and finite-union premises are external inputs.
No finite minimum is inferred from `RECEIPT.json`, and no decimal or SHA
evidence is converted into a Lean fact.  The bridge does not establish source binding,
true-DH/complete coverage, residual/PDE/trajectory closure, Lean
compilation, comparator acceptance, or registry eligibility.

No state, registry, receipt, or shared script was modified.
