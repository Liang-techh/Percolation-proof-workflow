# Composed reindex and positive-slack adapter review

## Scope and status

This sidecar composes the existing finite reindex weighted-sum equality with
the existing aggregate positive-slack certificate.  It does not repeat
reindex equality, reserve aggregation, quantitative delta, aggregate slack,
strict margin, digest, or cardinality proofs.

No Lean or Lake command was run.  This is an uncompiled typed proof attempt,
not a kernel-verification receipt, comparator result, or registry admission.

## Contract supplied

- `ComposedReindexSlackAdapter` retains the finite reindex adapter itself,
  explicit source-reserve and target-load total equalities, final-margin total
  equality, and shared-lambda equality.
- `composed_reindex_and_slack_give_final_strict_budget` consumes those explicit
  equalities together with `AggregateSlackCertificate` and outputs
  `0 < sigma ≤ finalMargin − finalLoad`, hence finalLoad `<` finalMargin.
- No cardinality premise is used as a substitute for the reindex map's
  membership, injectivity, surjectivity, or pointwise equality fields.

## Remaining boundaries

The row map, pointwise weights, total equalities, aggregate slack, and fixed
lambda are all external typed premises.  The adapter does not prove source or
physical/domain coverage, validate a digest, compute a receipt, or imply Lean
compilation, formal certificate validity, comparator acceptance, or registry eligibility.

No state, registry, receipt, or shared script was modified.
