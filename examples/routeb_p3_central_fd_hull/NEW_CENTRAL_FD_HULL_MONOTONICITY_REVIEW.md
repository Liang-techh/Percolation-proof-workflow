# P3 unified-radius monotonicity seam

Status: exact-real finite-sum adapter candidate, pending independent review.

## Purpose

`NEW_CENTRAL_FD_HULL_MONOTONICITY.lean` is the monotonicity layer after the
unified four-layer input. It does not repeat the existing Fin 6 weighted-power
theorem or the force adapter. Instead, it consumes an already established
consumer bound with radius `R` and safely lifts it to a larger `qBar`.

## Closed lemmas

- `gammaRadius6_mono` proves monotonicity of the derivative-first
  three-index Christoffel radius under pointwise `mu <= muBar`.
- `componentQ6_nonneg` and `componentQ6_mono` prove the corresponding
  nonnegativity and monotonicity of the nested velocity-quadratic component
  term.
- `weighted_sum_mono6` and `weightedRadiusSum6_mono` prove finite-sum and
  multiplication monotonicity for nonnegative weights and `|v[i]|` factors.
- `existing_consumer_lift_to_qbar6` lifts an existing consumer result from
  `q` to `qBar` without recomputing the power estimate.
- `existing_consumer_lift_with_error_bound6` retains the explicit premise
  `|error[i]| <= R[i]` while keeping the proof focused on monotonicity.

## Explicit premises

`ConsumerContext6` carries one common domain point, separate membership of all
four remainder layers in that domain, an explicit velocity premise, and a
nonnegative weight vector. The algebra does not infer domain compatibility,
velocity bounds, or weights from radius data.

The intended chain is:

```text
four-layer R/mu input
  -> existing weighted-power consumer gives consumerValue <= W(R)
  -> pointwise R <= q <= qBar and qBar >= 0
  -> existing_consumer_lift_to_qbar6 gives consumerValue <= W(qBar).
```

## Missing obligations and non-claims

No concrete source, `mu`, `qBar`, velocity box, weight vector, or numerical
constant is selected. This leaf does not prove source/export semantics,
rounding, interval coverage, flowpipe inclusion, P3/P4/P5/M4 closure,
admission, or registry promotion. It also does not establish the initial
weighted-power consumer bound; that remains an upstream premise.

No local Lean/Lake command was run. Independent pinned-environment review must
check imports, elaboration, `#print axioms`, and placeholder absence; later
compilation remains candidate evidence only.

