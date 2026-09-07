# Final fixed-lambda strict export review

## Scope and status

This sidecar is the final typed consumer seam for the current finite lane.  It
does not repeat eta partition, strict-total, strict-margin, digest,
cardinality, or monotonicity proofs.

No Lean or Lake command was run.  This is an uncompiled typed interface, not a
kernel-verification receipt, comparator result, or registry admission.

## Contract supplied

- `TwoRowMarginDenominatorPremise` accepts two `Fin 2` rows whose
  `CellMarginData` carries positive denominator, ratio, and declared margin
  fields; it additionally accepts the strict upper premise `lambdaUpper > 2`.
- `two_row_positive_margin_of_upper` and
  `two_row_admissible_of_upper` expose the final two-row positive-margin and
  fixed-`lambda=2` admissibility results using the existing bridge.
- `FinalStrictConsumerExport` combines those two-row results with the already
  completed `EtaStrictBudgetCertificate.union_load_lt_margin`.
- `build_final_strict_consumer_export` is the reusable export theorem.  The
  type `UniformMarginLowerBound f q.lambda` forces the global budget and the
  two-row consumer to share the same fixed lambda.

The only minimal additional premise is the explicit two-row strict-upper
condition; denominator/ratio/margin data remain in the typed row records.

## Remaining boundaries

This export consumes declared finite evidence only.  It does not establish
source/CSV binding, receipt or digest validity, complete/true-DH coverage,
residual/PDE/trajectory closure, formal certificate validity, Lean
compilation, comparator acceptance, or registry eligibility.

No state, registry, receipt, or shared script was modified.
