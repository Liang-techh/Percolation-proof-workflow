# P3 Fin 6 weighted central-FD power seam

Status: exact-real typed consumer candidate, pending independent review.

## What this adds

`NEW_CENTRAL_FD_HULL_POWER_SEAM.lean` completes the next consumer layer after
the slot adapter and the unweighted Fin 6 consumer. It keeps the convention

```text
T[k,i,j] = derivative-first tensor
```

and provides:

- `gammaRadius6`: the three-index Christoffel radius;
- `componentBound6`: the explicit nested `(j,k)` velocity-quadratic sum;
- `weighted_power_error6`: a nonnegative-weight consumer for
  `sum_i w[i] * v[i] * e[i]`;
- `four_term_telescoping6`: the exact tensor identity for four consecutive
  remainder differences;
- `four_term_remainder_bound6`: a four-term telescoping radius contract;
- `four_term_to_weighted_power6`: direct composition of the four-term tensor
  remainder with the weighted cubic power consumer.

## Exact sum bookkeeping

The sidecar keeps the index roles visible:

```text
gammaRadius6 mu i j k
  = (mu[k,i,j] + mu[j,i,k] + mu[i,j,k]) / 2

componentBound6 mu v i
  = sum j,k, gammaRadius6 mu i j k * |v[j] * v[k]|

weightedPowerBound6 w mu v
  = sum i, w[i] * |v[i]| * componentBound6 mu v i.
```

`zero_velocity_term6` records that a term vanishes when either velocity factor
is zero. `diagonal_velocity_term6` records the `j=k` diagonal as
`|v[j]|^2`, while `zero_radius_term6` records the exact zero-radius case. The
remaining `(j,k)` terms stay in the same ordered nested sum; no symmetry or
factor-of-two shortcut is introduced.

The weighted lemma requires only `w[i] >= 0`. It therefore preserves the
direction of the component inequality and does not silently use signed
weights.

## Four-term remainder contract

`four_term_telescoping6` first identifies four consecutive differences with
their endpoint difference. `tensorAdd4 R₀ R₁ R₂ R₃` is then the exact
pointwise sum of four remainder layers. `four_term_remainder_bound6` proves
that their absolute value is bounded by
the pointwise sum of `mu₀`, `mu₁`, `mu₂`, and `mu₃`, each exactly once.
`four_term_to_weighted_power6` feeds that sum to the derivative-first
Christoffel consumer and then to the weighted power lemma.

The four layers are intentionally unlabeled at the algebraic level. A later
adapter may assign them to machine/lift, central-FD, derivative-hull, and
export-center discrepancies, but this file does not assert any such external
semantics.

## Non-claims and missing evidence

No concrete source, `mu`, velocity box, weight vector, or numerical constant is
chosen. This leaf does not establish source/DH semantics, Float64 or libm
rounding, exported-payload correctness, interval coverage, flowpipe inclusion,
P3/P4/P5/M4 closure, admission, or registry promotion.

The true source/export obligations remain: a typed source-to-`T[k,i,j]`
binding, independently checked four remainder radii, a proof that the same
domain is used by all layers, and any downstream velocity/weight hypotheses.

No local Lean/Lake command was run. Independent pinned-environment review must
check elaboration, imports, `#print axioms`, and placeholder absence; a later
compile would remain only candidate evidence.
