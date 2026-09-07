# P3 squared-velocity nonnegativity leaf

Status: bounded exact-real proof-attempt candidate, pending independent review.

## Scope

`NEW_CENTRAL_FD_HULL_SQUARED_VELOCITY.lean` proves for arbitrary
`velocity : Fin 6 -> R`:

```text
squaredVelocity[i] = velocity[i]^2 >= 0.
```

It does not redefine the existing `assembledLoad6` or `PureOrderLoadWitness6`.
Instead, `assembled_load_nonneg_from_squared_velocity6` consumes a generic
assembled-load function together with the explicit equality

```text
assembledLoad weight squaredVelocity i
  = weight[i] * squaredVelocity[i]
```

and supplies the `load_nonneg` premise expected by the existing load witness.

`SquaredVelocityContext6` preserves one point, one common domain, four layer
memberships, an opaque velocity premise, and nonnegative weights.

## Boundary

The physical meaning or source of `velocity` is not asserted. The assembled-load
equality, weight nonnegativity, and same-point context remain explicit typed
premises. No radius, capMax, scalar budget, power, force, source binding,
coverage, admission, registry, or Lean compilation claim is made.

No local Lean/Lake command was run. Independent pinned-environment review must
check imports, elaboration, `#print axioms`, and placeholder absence; later
compilation remains candidate evidence only.

