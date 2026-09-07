# Fixed-lambda index-transport obstruction review

## Scope and status

This sidecar is negative-control tracking for the finite index adapter.  It
does not repeat the positive row-map adapter, reserve aggregation, slack,
strict-margin, digest, or cardinality results.

No Lean or Lake command was run.  This is an uncompiled exact-rational
obstruction file, not a kernel-verification receipt, comparator result, or
registry admission.

## Exact finite obstructions

- In the noninjective example, source rows `{0,1}` both map to target row
  `{0}`.  Unit payloads give source sum `2` and target sum `1`.
- In the nonsurjective example, source `{0}` maps into target `{0,1}` but has no
  preimage for target row `1`.  Unit payloads give sums `1` and `2`.
- In the missing-total-equality example, the map is bijective on singleton
  index sets, but source payload `1` and target payload `2` give unequal sums.

Thus injectivity, surjectivity, and explicit total equalities are independent
transport premises.  A positive reserve/final consumer adapter cannot infer
aggregate equality from a row count or an index map alone.

## Fail-closed boundary

These are abstract finite counterexamples, not claims about the Route-B CSV,
source evaluator, digest, physical coverage, or registry.  They only record
why the corresponding premises must remain explicit in any future adapter.

No state, registry, receipt, or shared script was modified.
