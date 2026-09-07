# P3 common-domain and premise-reuse seam

Status: exact-real predicate-transport candidate, pending independent review.

## Purpose

`NEW_CENTRAL_FD_HULL_COMMON_CONTEXT.lean` supplies the context layer omitted
from the numerical consumers. Four named layers are represented by `Layer6`:

```text
machineLift, centralFD, derivativeHull, exportCenter.
```

`CommonDomainContext6` declares one point, one common-domain predicate, and one
predicate for each layer. `common_to_layer_intersection6` transports the common
membership proof to the universal layer intersection; the point theorem and
the equality transport theorem make reuse explicit.

## Consumer composition

`VelocityWeightPremises6` carries an explicit velocity premise and
nonnegative weight proof. `ExistingWeightedConsumerBound6` carries an already
established consumer inequality abstractly. `ComposedConsumerContext6` packages
the layer intersection, velocity premise, weight nonnegativity, and consumer
bound. The file does not reprove or even specialize the weighted-power
inequality.

`reuse_common_and_velocity_premises6` and
`transport_consumer_context_point6` expose the exact conjunction downstream
adapters may destructure.

## Boundary

The common-domain predicate and velocity premise are intentionally opaque. No
source/export implementation, rounding fact, numerical radius, scalar budget,
interval coverage, flowpipe fact, or admission/registry state is inferred.
The consumer inequality remains an upstream premise.

No local Lean/Lake command was run. Independent pinned-environment review must
check imports, elaboration, `#print axioms`, and placeholder absence; later
compilation remains candidate evidence only.

