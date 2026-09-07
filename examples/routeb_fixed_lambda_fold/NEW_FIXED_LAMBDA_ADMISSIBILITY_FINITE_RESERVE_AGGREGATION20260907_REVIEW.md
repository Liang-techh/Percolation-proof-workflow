# Finite cell reserve aggregation review

## Scope and status

This sidecar adds the finite per-cell reserve aggregation seam.  It does not
repeat the no-division scalar bridge, eta partition, union cardinality,
digest, strict margin, strict total, or monotonicity layers.

No Lean or Lake command was run.  This is an uncompiled typed interface, not a
kernel-verification receipt, comparator result, or registry admission.

## Contract supplied

- `FiniteDisjointCellFamily` carries a finite row index set, typed cell data,
  and an explicit pairwise disjoint support premise.
- `total_margin_additive` gives the exact additive identity
  `Σ marginAt = Σ externalGamma − lambda * Σ cellGamma`.
- `total_reserve_le_total_margin` consumes the per-cell cross-multiplied
  reserve `lambda*cellGamma + reserve ≤ externalGamma` and sums the resulting
  per-cell inequalities without division.
- `total_reserve_le_external_minus_total_charge` exposes the same bound in the
  aggregate external-minus-charge form.

Each `CellMarginData` retains its own positive denominator and ratio premise;
the aggregation theorem does not erase or merge those per-cell obligations.

## Remaining boundaries

Finite support disjointness and per-cell reserve inequalities are external typed premises.  The sidecar does not infer that the finite cells cover a
physical domain, bind source/CSV values, validate a digest, compute a receipt minimum, or establish residual/PDE/trajectory closure.  No formal certificate,
comparator, or registry admission is implied.

No state, registry, receipt, or shared script was modified.
