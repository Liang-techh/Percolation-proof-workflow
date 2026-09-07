# P3 family-to-point derivative-radius/load bridge

Status: conditional exact-real typed transport candidate, pending independent review.

## Why this leaf is distinct

Earlier leaves package one point at a time or prove scalar order. This leaf
handles the missing dependent-family boundary: `muBar(x)`, component radius,
velocity, weight, and an existing consumer bound are all functions of one
domain point `x` and are specialized together.

`specialize_family_at_point6` requires explicit membership for the common,
machine/lift, central-FD, derivative-hull, and export-center predicates. It
copies the component-radius nonnegativity, weight nonnegativity, and consumer
bound at that same point into `WeightedLoadAtPoint6`.

## Conditional boundary

`componentize` and `consumer_bound` are opaque premises. This sidecar does not
derive a component radius from a concrete derivative tensor, does not prove a
weighted-power inequality, and does not infer domain compatibility from data
equality.

No concrete source, numerical radius, velocity box, rounding fact, coverage,
admission, registry state, or physical interpretation is selected.

No local Lean/Lake command was run. Independent pinned-environment review must
check imports, elaboration, `#print axioms`, and placeholder absence; later
compilation remains candidate evidence only.
