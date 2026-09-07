# P3 pure order consumer bridge

Status: conditional exact-real order candidate, pending independent review.

## Scope

`NEW_CENTRAL_FD_HULL_ORDER_CONSUMER.lean` intentionally abstracts the already
assembled load coefficient as `load : Fin 6 -> R`. It does not rebuild the
weight/velocity load expression or any radius payload.

## Closed order steps

- `weightedLoad6_mono_component_cap` proves

  ```text
  q[i] <= qCap[i] and load[i] >= 0
    => sum_i load[i] * q[i]
       <= sum_i load[i] * qCap[i].
  ```

- `capLoad6_le_capMaxLoad6` proves the conditional scalar capMax upper bound
  from `qCap[i] <= capMax`.
- `capMax_consumer_order_bridge6` composes an existing consumer inequality with
  both order steps and outputs the capMax scalar budget bound.

The context keeps one point, one common domain, four layer memberships, an
explicit velocity premise, and nonnegative weights visible. The order proof
uses only the already assembled nonnegative load premise.

## Boundary

The consumer bound, component cap inequalities, load nonnegativity, and scalar
cap upper bound are explicit premises. No source or physical semantics,
rounding fact, numerical value, coverage, admission, or registry state is
inferred. No component-to-cap construction, scalar-cap monotonicity, capMax
minimality, attainment equality, or force theorem is repeated.

No local Lean/Lake command was run. Independent pinned-environment review must
check imports, elaboration, `#print axioms`, and placeholder absence; later
compilation remains candidate evidence only.

