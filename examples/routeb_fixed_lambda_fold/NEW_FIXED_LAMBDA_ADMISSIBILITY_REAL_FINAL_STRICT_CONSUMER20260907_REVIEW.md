# Real final strict consumer adapter review

## Scope and status

This sidecar is the real-valued consumer after the composed reindex/slack and
the existing rational-to-real finite-sum cast adapters.  It does not repeat
the finite reindex theorem, the finite-sum cast theorem, or the old rational
slack proof.

No Lean or Lake command was run.  The file is an uncompiled typed proof
attempt, not a kernel-verification receipt, comparator result, or registry
admission.

## Contract supplied

- `RealFinalStrictConsumerAdapter` retains rational source and target totals,
  their source/target/reserve/load equalities, the shared-lambda equality, and
  the existing real source/target cast chain.
- The existing composed rational budget supplies `0 < sigma` and the rational
  margin-minus-load bound.  `exact_mod_cast` transports these to the real
  sigma and the cast rational gap.
- `margin_load_gap_eq_cast` makes the subtraction cast explicit, and
  `sigma_le_real_gap` records the required real premise
  `0 < sigma ≤ realMargin − realLoad` together with positivity.
- `real_load_lt_real_margin_of_casted_sigma` consumes those real premises via
  positivity of subtraction and concludes `realLoad < realMargin`.

## Remaining boundaries

The adapter does not bind rational values to Route-B source/CSV data, prove
physical or domain coverage, validate a digest or receipt, or imply Lean
compilation, formal certificate validity, comparator acceptance, or registry
eligibility.  If the rational-to-real ring cast or finite typed domains are
unavailable, this seam remains open rather than falling back to Float or an
untyped conversion.

No state, registry, receipt, or shared script was modified.
