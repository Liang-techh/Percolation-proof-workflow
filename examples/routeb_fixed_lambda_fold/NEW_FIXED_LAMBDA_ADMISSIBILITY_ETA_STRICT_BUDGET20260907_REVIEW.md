# Eta-local strict weighted budget review

## Scope and status

This sidecar combines the existing eta sum decomposition and weighted term
lemmas.  It does not repeat the global strict-total theorem, the union sum
decomposition itself, strict-margin derivation, digest, cardinality, or
monotonicity.

No Lean or Lake command was run.  This is an uncompiled typed interface, not a
kernel-verification receipt, comparator result, or registry admission.

## Contract supplied

- `subpartition_strict_load_lt_delta` is a generic finite-subset helper.  It
  consumes subset membership into the union, nonnegative coefficients,
  `0 ≤ load < delta`, an explicit subset nonemptiness premise, and a positive
  coefficient witness.
- `eta27_strict_weighted_load_lt_margin` and
  `eta56_strict_weighted_load_lt_margin` give strict load `<` strict margin for
  each eta subset by combining the helper with the existing eta-local
  delta-to-margin bounds.
- `combine_eta_strict_budgets` uses the already supplied sum-partition
  equalities to add the two strict eta budgets into the union strict budget.
- `EtaStrictBudgetCertificate` preserves both subset nonempty premises and all
  three strict budget conclusions for a later consumer.

The positive coefficient witnesses are kept separately for both eta subsets;
nonnegative coefficients alone would not justify strictness.

## Remaining boundaries

All subset membership, disjointness/sum partition, load, coefficient, delta,
and margin premises remain external typed inputs.  This sidecar does not bind
the load to a source residual, compute a receipt minimum, validate a digest,
prove source/true-DH/physical coverage, or establish PDE/trajectory closure.
No formal certificate, comparator, or registry admission is implied.

No state, registry, receipt, or shared script was modified.
