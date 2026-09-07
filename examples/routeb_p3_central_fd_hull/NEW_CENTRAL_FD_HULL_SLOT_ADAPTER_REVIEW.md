# P3 central-FD hull slot/index adapter

Status: exact-real typed adapter candidate, pending independent review.

## Purpose

`NEW_CENTRAL_FD_HULL_SLOT_ADAPTER.lean` isolates the only index permutation
needed when a source-shaped central-FD derivative tensor is passed to the
derivative-first Christoffel consumer:

```text
source/storage:       dM[i,j,k]
consumer convention:  T[k,i,j]
adapter:              T := dmToDerivative dM
```

The same map is applied to the tensor remainder and its radius. This prevents
an untyped visual rewrite from silently moving the differentiated coordinate.

## Exact results

- `derivativeToDM_dmToDerivative` and
  `dmToDerivative_derivativeToDM` prove the permutation is invertible.
- `sourceDMForce_eq_consumerForce` proves the source nested contraction equals
  the consumer formula after the explicit map.
- `dmToDerivative_add` shows that the map preserves the exact-real remainder
  split.
- `derivativeRemainder_apply` and `derivativeRemainder_radius` transport
  `dMfd[i,j,k] - dMtrue[i,j,k]` and its source-shaped radius to
  `R[k,i,j]` and `mu[k,i,j]`.
- `sourceDMForce_remainder_bridge` connects the source-shaped force difference
  to the consumer applied to the mapped derivative remainder.

The adapter is compatible with the preceding hull interface by instantiating
its derivative-first tensor arguments as

```text
T  = dmToDerivative dMtrue
R  = derivativeRemainder dMfd dMtrue
mu = dmRadiusToDerivative mu_source.
```

No additional permutation is allowed at the Christoffel consumer boundary.

## Boundary and non-claims

This is only a typed exact-real slot bridge. It does not supply the remainder
bound `hR`; that premise must come from an independently checked derivative or
central-FD hull. It does not bind a Julia/DH implementation, Float64/libm
rounding, a source snapshot, a concrete `mu`, interval-cell coverage,
flowpipe semantics, P3 admission, or registry state.

In particular, `sourceDMForce_eq_consumerForce` is an algebraic equality after
the map; it is not evidence that any deployed `dM` array has those semantics.

## Verification boundary

No local Lean/Lake command was run, as required. The file is an uncompiled
candidate pending an independent pinned-environment check of imports,
elaboration, `#print axioms`, and placeholder absence. Even after compilation,
the result remains a typed adapter and cannot close source, coverage, or
admission gates.

