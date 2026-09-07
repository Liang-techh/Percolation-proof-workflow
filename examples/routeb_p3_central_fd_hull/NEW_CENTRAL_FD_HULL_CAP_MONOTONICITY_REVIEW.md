# P3 scalar-cap monotonicity seam

Status: exact-real scalar-budget candidate, pending independent review.

## Scope

`NEW_CENTRAL_FD_HULL_CAP_MONOTONICITY.lean` treats the load coefficient as an
already assembled `Fin 6` vector. It does not repeat how that vector came from
weights, velocities, or component radii.

The budget is

```text
scalarCapLoad(load, cap) = cap * sum_i load[i].
```

## Results

- `totalLoad6_nonneg` derives a nonnegative total coefficient from pointwise
  nonnegative load.
- `scalarCapLoad6_mono` proves `cap1 <= cap2` implies budget monotonicity.
- `scalarCapLoad6_gap_identity` exposes the exact gap formula.
- `scalarCapLoad6_strict_mono` proves strict budget growth when the cap gap and
  total coefficient are both strictly positive.

No component-to-cap theorem, common-domain context, force map, or radius
monotonicity is duplicated.

## Boundary

The load vector, caps, and any upstream consumer budget remain abstract. No
concrete source, numerical constant, velocity box, rounding evidence,
coverage, admission, or registry state is selected or inferred.

No local Lean/Lake command was run. Independent pinned-environment review must
check imports, elaboration, `#print axioms`, and placeholder absence; later
compilation remains candidate evidence only.
