# Fixed-lambda eta sum decomposition review

## Scope and status

This sidecar adds only the weighted load/margin additive decomposition by eta
partition.  It does not repeat union cardinality, digest, strict margin,
strict total, or monotonicity results.

No Lean or Lake command was run.  This is an uncompiled typed interface, not a
kernel-verification receipt, comparator result, or registry admission.

## Contract supplied

- `ExplicitEtaSumPartition` explicitly accepts two tagged finite subsets, a
  finite union equality, disjointness, and a `Finset` sum-partition premise.
- `weighted_load_union_eq_eta_sum` and
  `weighted_margin_union_eq_eta_sum` decompose the union totals into the
  eta=2.7 and eta=5.6 sub-budget sums.
- `eta27_weighted_load_nonnegative` and
  `eta56_weighted_load_nonnegative` transfer rowwise nonnegativity to each
  sub-budget.
- The four eta-specific budget lemmas transfer weighted load to delta and delta
  to margin separately for each subcollection, using the existing rowwise
  budget terms and the explicit finite-subset membership premises.

The decomposition is combinatorial over supplied tagged finite subsets.  The
finite union equality is not a physical-domain or source-coverage theorem.

## Remaining boundaries

Subset membership, disjointness, sum partition, coefficient nonnegativity,
load bounds, and delta/margin bounds are all supplied typed premises.  This
sidecar does not validate a digest, bind CSV/source values, compute a receipt
minimum, prove true-DH or complete coverage, establish residual/PDE/trajectory
closure, or imply formal certificate, comparator, or registry admission.

No state, registry, receipt, or shared script was modified.
