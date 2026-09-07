# Finite reindex weighted-sum equality review

## Scope and status

This sidecar adds the positive finite reindex equality adapter after the
index-transport obstruction leaf.  It does not repeat reserve aggregation,
strict margin, digest, cardinality, monotonicity, or final-export logic.

No Lean or Lake command was run.  This is an uncompiled proof attempt, not a
kernel-verification receipt, comparator result, or registry admission.

## Contract supplied

- `FiniteReindexWeightAdapter` explicitly requires selected-set membership,
  injectivity, surjectivity, and pointwise weight equality.
- `finite_reindex_weight_sum_eq` uses the finite bijection to prove exact
  equality of source and target weighted sums.
- The cardinality hypothesis in
  `finite_reindex_weight_sum_eq_of_explicit_equiv` is intentionally unused for
  equality: cardinality alone is not a substitute for the map premises.
- `missing_bijection_or_pointwise_equality_has_counterexample` re-exports the
  prior exact finite counterexamples: noninjective collapse, nonsurjective
  omission, and bijective indices with unequal payload values.

## Remaining boundaries

All map and pointwise equality fields are external typed premises.  The lemma
does not bind row payloads to Route-B source/CSV data, prove physical/domain coverage,
validate a digest, compute a receipt, or imply Lean compilation,
formal certificate validity, comparator acceptance, or registry eligibility.

No state, registry, receipt, or shared script was modified.
