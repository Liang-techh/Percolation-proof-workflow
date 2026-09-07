# P3 assembled load-coefficient witness

Status: bounded exact-real proof-attempt candidate, pending independent review.

## Scope

`NEW_CENTRAL_FD_HULL_LOAD_WITNESS.lean` proves the smallest missing premise for
the pure order consumer: an assembled six-component load vector is pointwise
nonnegative when it is formed as

```text
load[i] = weight[i] * squaredVelocity[i],
weight[i] >= 0,
squaredVelocity[i] >= 0.
```

`PureOrderLoadWitness6` is the minimal `load/load_nonneg` record expected by the
order bridge. `context_pure_order_load_witness6` connects the same witness to a
common point/domain context and an explicit velocity premise.

## Boundary

The squared-velocity vector is an external typed premise; this leaf does not
prove how it was formed from a velocity, nor does it select weights or a
domain. It does not rebuild radius payloads, capMax, scalar budgets, weighted
power, force maps, or any physical/source semantics.

No numerical value, rounding evidence, coverage, admission, or registry state
is selected or inferred. No local Lean/Lake command was run. Independent
pinned-environment review must check imports, elaboration, `#print axioms`, and
placeholder absence; later compilation remains candidate evidence only.

