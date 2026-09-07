# Strict margin consumer review

## Scope and status

This sidecar consumes the revised explicit delta contract and adds only the
strictness layer.  It does not repeat digest, union cardinality, monotonicity,
selected-box, fixed-2 feasibility, or receipt-minimum logic.

No Lean or Lake command was run.  This is an uncompiled typed interface, not a
kernel-verification receipt, comparator result, or registry admission.

## Contract supplied

- `gap_contract_gives_strict_upper` turns `gap > 0` and
  `gap ≤ lambdaUpper - lambda` into the strict upper inequality
  `lambda < lambdaUpper` for each selected union row.
- `gap_contract_gives_strict_margin` combines `delta > 0` with the revised
  rowwise lower bound `delta ≤ marginAt` to obtain `marginAt > 0`.
- `gap_contract_gives_row_strict_feasibility` packages those two conclusions
  with an explicit lower premise `1 < lambda`.
- `strict_load_is_strictly_below_row_margin` propagates the strict downstream
  load condition `0 ≤ load < delta` to `0 ≤ load < marginAt` rowwise.

All conclusions are over the supplied finite tagged union and consume the
revised contract's explicit ratio, upper-gap, and cell-lower premises.

## Remaining boundaries

The sidecar does not establish any gap, coefficient, ratio, or load premise;
those remain external inputs.  It does not bind source/CSV values, validate a
digest, prove complete or true-DH coverage, establish residual/PDE/trajectory
closure, or imply Lean compilation, comparator acceptance, registry
eligibility, or formal certificate admission.

No state, registry, receipt, or shared script was modified.
