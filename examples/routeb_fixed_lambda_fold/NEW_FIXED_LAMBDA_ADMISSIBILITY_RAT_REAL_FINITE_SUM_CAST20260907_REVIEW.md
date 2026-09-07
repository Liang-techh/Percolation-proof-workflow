# Rational-to-real finite-sum cast adapter review

## Scope and status

This sidecar adds only the ℚ→ℝ finite `Finset.sum` cast seam.  It does not
repeat the finite reindex theorem, composed slack, reserve aggregation,
strict-margin, digest, or cardinality layers.

No Lean or Lake command was run.  This is an uncompiled typed proof attempt,
not a kernel-verification receipt, comparator result, or registry admission.

## Contract supplied

- `cast_finset_sum_rat_to_real` proves explicitly that casting a finite
  rational sum to `ℝ` equals the sum of the cast summands.
- `sourceRealSum` and `targetRealSum` expose the real weighted sums attached to
  the existing rational `FiniteReindexWeightAdapter`.
- `finite_reindex_weight_sum_eq_after_rat_real_cast` applies the existing
  rational reindex equality through the canonical ℚ→ℝ cast.
- `finite_reindex_cast_chain` records the complete source-cast-target chain
  for a downstream typed consumer.

The finite `Finset` domain and canonical ring-compatible cast are explicit
requirements.  If either is unavailable, the cast/reindex seam remains open;
no Float or untyped numeric conversion is substituted.

## Remaining boundaries

This adapter does not bind rational values to Route-B source/CSV data, validate
a digest or receipt, prove physical/domain coverage, or imply Lean
compilation, formal certificate validity, comparator acceptance, or registry eligibility.

No state, registry, receipt, or shared script was modified.
