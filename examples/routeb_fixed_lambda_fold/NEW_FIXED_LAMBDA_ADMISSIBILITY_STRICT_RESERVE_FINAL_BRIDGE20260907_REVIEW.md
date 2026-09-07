# Strict reserve to final weighted-budget bridge review

## Scope and status

This sidecar adds the strict finite-reserve parent seam after the existing
finite reserve aggregation and final strict export interfaces.  It does not
repeat total-reserve non-strict aggregation, strict total weighted load,
eta-sum decomposition, strict margin, digest, cardinality, or monotonicity.

No Lean or Lake command was run.  This is an uncompiled proof attempt, not a
kernel-verification receipt, comparator result, or registry admission.

## Contract supplied

- `StrictReserveFamilyPremise` keeps fixed `params.lambda`, finite row
  nonemptiness, per-cell reserve nonnegativity, per-cell cross-multiplied
  reserve bounds, and one strict reserve witness.
- `strict_total_reserve_lt_total_margin` uses finite-sum strictness to prove
  `Σ reserve < Σ marginAt`; the strict witness is essential.
- `ReserveToFinalBudgetAdapter` requires explicit equalities between the
  independently indexed cell-family totals and the existing final weighted
  load/margin totals.  No row/index identity is inferred.
- `strict_reserve_satisfies_final_weighted_budget` transfers the strict reserve
   result to the final consumer's union-budget inequality.
- `build_final_strict_export_from_strict_reserve` conditionally fills the
  existing `FinalStrictConsumerExport`, using the explicit shared-lambda
  equality and the separately supplied two-row premise.

The final budget/export result is conditional: a future caller must still
supply the explicit total equalities, shared-lambda equality, and existing
two-row/fixed-lambda fields required by the final export interface.

## Open conditions and non-claims

If the finite family is empty or no row has a strict reserve inequality, the
strict theorem cannot be constructed and remains open.  Pairwise-disjoint
support, nonnegative coefficients, source bindings, digest bindings, and
physical/domain coverage are not inferred by this sidecar.

No source/CSV, receipt, digest, true-DH/complete coverage, residual/PDE/
trajectory closure, Lean compilation, comparator acceptance, or registry
eligibility is established.  No state, registry, receipt, or shared script was
modified.
