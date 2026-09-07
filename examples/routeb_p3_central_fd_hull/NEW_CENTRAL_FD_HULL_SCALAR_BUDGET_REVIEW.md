# P3 scalar budget seam

Status: exact-real finite-sum budget candidate, pending independent review.

## Purpose

`NEW_CENTRAL_FD_HULL_SCALAR_BUDGET.lean` compresses the component-radius
output of the existing unified derivative-radius/weighted-power chain into a
downstream scalar load budget. It does not repeat the force adapter, radius
monotonicity, or weighted-power inequality.

The load coefficient is explicit:

```text
loadCoeff[i] = weight[i] * |velocity[i]|.
```

The compression chain is:

```text
weightedLoad(weight, velocity, q)
  <= capLoad(weight, velocity, qCap)
  <= scalarCap * sum_i loadCoeff[i].
```

`existing_consumer_to_scalar_cap6` composes this chain with an already supplied
consumer bound. Thus the upstream unified `muBar` only needs to provide the
component radius `q`, component caps `qCap`, and their pointwise order.

## Explicit premises

- `weight_nonneg` makes multiplication monotone;
- `q >= 0` and `qCap >= 0` preserve radius semantics;
- `q <= qCap` is the component-to-cap premise;
- `qCap[i] <= scalarCap` is the scalar-collapse premise;
- `ScalarBudgetContext6` carries one common domain point, all four layer
  memberships, and an explicit velocity premise;
- `hConsumer` is the existing weighted-power consumer bound and remains an
  external upstream premise.

No velocity box, weight choice, scalar cap, source evaluator, or numerical
constant is selected here.

## Missing obligations and non-claims

This leaf does not prove how `q` or `qCap` were obtained from a concrete source,
does not establish source/export semantics or rounding, and does not prove
interval coverage, flowpipe inclusion, P3/P4/P5/M4 closure, admission, or
registry promotion. The scalar budget is only as sound as the upstream
consumer bound and component-cap premises.

No local Lean/Lake command was run. Independent pinned-environment review must
check imports, elaboration, `#print axioms`, and placeholder absence; later
compilation remains candidate evidence only.

