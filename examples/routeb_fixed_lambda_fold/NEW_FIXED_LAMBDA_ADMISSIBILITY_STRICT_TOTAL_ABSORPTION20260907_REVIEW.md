# Strict total absorption bridge review

## Scope and status

This sidecar adds the strict finite-sum step after the weighted absorption
budget.  It does not repeat strict margin, digest, union cardinality,
monotonicity, or the non-strict weighted budget lemmas.

No Lean or Lake command was run.  This is an uncompiled typed interface, not a
kernel-verification receipt, comparator result, or registry admission.

## Contract supplied

- `strict_total_weighted_load_lt_delta` consumes nonnegative coefficients,
  `0 ≤ load < delta` on every selected row, an explicit union nonemptiness
  premise, and a witness row with `0 < coefficient`.  The witness supplies the
  strict summand needed by `Finset.sum_lt_sum`.
- `strict_total_weighted_load_lt_margin` transfers the strict total delta bound
  through the existing non-strict delta-to-margin sum bound.
- `StrictTotalAbsorptionCertificate` and
  `build_strict_total_absorption_certificate` preserve the nonempty-union
  premise and both strict total conclusions for a later absorption consumer.

The positive coefficient witness is essential: if every coefficient is zero,
all weighted totals are zero and no strict total inequality follows, even when
every row load is strictly below delta.

## Remaining boundaries

The result consumes only finite typed load, coefficient, delta, and margin
premises.  It does not identify the load with a source residual, prove a
physical/PDE absorption theorem, compute a receipt minimum, validate a digest,
or establish source/coverage/trajectory closure.  No formal certificate,
comparator, or registry admission is implied.

No state, registry, receipt, or shared script was modified.
