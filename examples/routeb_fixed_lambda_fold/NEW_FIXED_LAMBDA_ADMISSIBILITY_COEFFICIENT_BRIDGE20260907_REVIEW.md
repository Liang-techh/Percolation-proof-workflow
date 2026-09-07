# Fixed-lambda coefficient identity and strict-margin bridge review

## Scope and status

This sidecar imports and reuses the earlier typed consumer.  It adds no new
parameter or row structure.  Its scope is the coefficient algebra connecting
the supplied fields

`candidateMargin = externalGamma - lambda * cellGamma`

and

`lambdaUpper = externalGamma / cellGamma`,

under the explicit premise `cellGamma > 0` and the fixed-parameter equality
`lambda = 2`.

No Lean or Lake command was run.  The file is therefore an uncompiled,
reviewable interface with no kernel-verification, comparator, or registry
status.  It contains no `sorry` declaration by construction, but that textual
fact is not a substitute for the required pinned build receipt.

## Reusable bridge

- `coefficient_identity` rewrites the supplied margin equation into
  `externalGamma = lambda * cellGamma + candidateMargin`.
- `strict_upper_iff_positive_margin` proves the exact equivalence
  `lambda < lambdaUpper ↔ 0 < candidateMargin`, using the positive denominator
  and the fixed `lambda = 2` carried by `FixedLambdaParameters`.
- `finset_strict_upper_iff_positive_margin` lifts that equivalence pointwise
  over an arbitrary finite `Finset Nat`; it does not reinterpret labels as a
  dense ordinal.
- `two_row_strict_upper_iff_positive_margin` provides the same bridge for the
  existing `Fin 2` consumer.
- `fixed_two_strict_upper_consumes_margin` is the direct `lambdaUpper > 2`
  consumer requested by the fixed-lambda lane.

## External premises still required

The `CellMarginData` equalities and positivity field are assumptions supplied
by a future adapter.  This sidecar does not establish that they were computed
by the Route-B source evaluator, that decimal ledger text denotes the stated
exact values, or that any declared row is present in the source artifact.

The finite quantifiers cover only the supplied row function and index set.
They do not prove all-cell/true-DH interval coverage, partition completeness,
missing-cell exclusion, residual absorption, trajectory/PDE validity, or
parent-node closure.  `Fin 2` remains interface arity, not physical coverage.

The candidate must remain pending until the pinned Lean build, axiom/`sorry`
audit, source/coverage bridges, and exact comparator/admission workflow are
completed separately.  No state, registry, receipt, or shared script was
modified by this sidecar.
