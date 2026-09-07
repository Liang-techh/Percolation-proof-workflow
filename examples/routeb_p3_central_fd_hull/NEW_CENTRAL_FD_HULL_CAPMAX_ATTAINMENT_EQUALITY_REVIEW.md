# P3 capMax attainment equality seam

Status: exact-real finite-sum candidate, pending independent review.

## Scope

`NEW_CENTRAL_FD_HULL_CAPMAX_ATTAINMENT_EQUALITY.lean` handles the sharp case
left open by the general capMax inequality. It uses an explicit attained index
`iStar : Fin 6` and a support premise:

```text
qCap[iStar] = capMax
load[iStar] > 0
load[i] = 0 for every i != iStar.
```

## Results

- `single_support_term_eq6` proves the per-index equality by an explicit
  attained/off-support case split.
- `single_support_budget_equality6` proves

  ```text
  sum_i load[i] * qCap[i]
    = capMax * sum_i load[i].
  ```

- `single_support_positive_mass_equality6` retains the positive-mass premise
  alongside the equality result.
- `equality_refines_order_boundary6` records that exact equality implies the
  ordinary `<=` order boundary; the general inequality for arbitrary support
  remains supplied by the prior capMax budget leaf.

No support or maximum API is inferred, and no load budget is recomputed beyond
this exact equality case.

## Boundary

No concrete source, numerical cap, velocity box, rounding evidence, coverage,
admission, or registry state is selected. The equality depends on the explicit
attainment and support premises.

No local Lean/Lake command was run. Independent pinned-environment review must
check imports, elaboration, `#print axioms`, and placeholder absence; later
compilation remains candidate evidence only.

