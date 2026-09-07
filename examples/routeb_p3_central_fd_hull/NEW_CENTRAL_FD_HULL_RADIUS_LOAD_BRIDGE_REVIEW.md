# P3 derivative-radius to weighted-load payload bridge

Status: conditional exact-real typed payload candidate, pending independent review.

## Why this leaf is separate

The preceding leaves prove radius order, force decomposition, weighted-power
bounds, scalar budgets, and cap interfaces. This leaf adds only the missing
same-point payload boundary: a derivative radius `muBar`, its component radius,
one velocity/weight pair, four layer memberships, and an existing consumer
bound are carried in one typed record.

## Interface

`RadiusLoadContext6` requires:

- one `point` and one common-domain predicate, with membership for all four
  layers;
- an opaque `componentize` map and the equality
  `componentRadius = componentize muBar velocity`;
- nonnegative component radius and weight premises;
- an explicit velocity premise;
- an already established bound
  `consumerValue <= downstreamWeightedLoad6 weight velocity componentRadius`.

`compose_downstream_weighted_load6` copies these facts into
`DownstreamWeightedLoadInput6`. `reuse_downstream_weighted_load_premises6`
exposes the conjunction downstream adapters may destructure.

The componentization and consumer inequality remain conditional premises. No
new radius, force, monotonicity, scalar budget, or power estimate is hidden in
the constructor.

## Boundary

No concrete evaluator, numerical radius, velocity box, rounding fact, domain
partition, physical semantic binding, admission, or registry state is inferred.
The record only makes unresolved premises explicit and keeps all four layers at
the same declared point.

No local Lean/Lake command was run. Independent pinned-environment review must
check imports, elaboration, `#print axioms`, and placeholder absence; later
compilation remains candidate evidence only.

