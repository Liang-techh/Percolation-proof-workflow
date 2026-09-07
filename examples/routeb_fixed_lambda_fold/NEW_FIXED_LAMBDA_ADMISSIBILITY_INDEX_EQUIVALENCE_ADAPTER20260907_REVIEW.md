# Fixed-lambda finite-cell index equivalence adapter review

## Scope and status

This sidecar adds only the explicit transport seam from an independently
indexed finite cell family to the existing tagged final union and strict
export.  It does not repeat reserve aggregation, strict bridges, quantitative
delta/slack, union cardinality, digest, or monotonicity.

No Lean or Lake command was run.  This is an uncompiled typed interface, not a
kernel-verification receipt, comparator result, or registry admission.

## Contract supplied

- `FiniteCellToFinalIndexAdapter` requires an explicit row map with selected-row
  membership, injectivity, and surjectivity onto the final tagged union.
- It separately requires cell-value preservation, `cellLambda = q.lambda`, and
  exact load/margin total equalities.  No row count is used to infer these
  identities.
- `cell_aggregate_strict_budget_of_final_export` rewrites the existing final
  strict weighted budget into the independently indexed cell-family statement
  `totalReserve < totalMargin`.
- `transported_margin_uses_final_lambda` exposes the shared-lambda equality for
  downstream consumers.

The adapter's map is finite only through the supplied `Finset` domains; its
surjectivity is onto the supplied final union, not onto a physical domain.

## Remaining boundaries

All map, value, lambda, and total-equality premises are external typed inputs.
This sidecar does not bind source/CSV values, prove cell/domain coverage,
validate a digest, compute a receipt minimum, or establish residual/PDE/
trajectory closure.  No formal certificate, comparator, or registry admission
is implied.

No state, registry, receipt, or shared script was modified.
