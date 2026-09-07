# P3 derivative-first four-layer force adapter

Status: exact-real typed proof skeleton, pending independent review.

## Purpose

`NEW_CENTRAL_FD_HULL_FORCE_ADAPTER.lean` is the boundary adapter from a
derivative-first Christoffel contraction to a source-force output. It does not
reprove the existing Fin 6 weighted power inequality. Instead, it exposes the
error vector in exactly the form that the prior power seam can consume.

The fixed tensor order is:

```text
T[k,i,j] = differentiated-coordinate, mass-row, mass-column.
```

## Four-layer decomposition

`FourLayerRemainders6` names four independent exact-real tensors:

1. `machineLift`;
2. `centralFD`;
3. `derivativeHull`;
4. `exportCenter`.

`christoffelContraction6_add4` proves linearity of the same contraction map,
and `four_layer_contraction_split` applies it to their sum. The source-force
equality itself is retained as `SourceForceContract6.source_force_eq`, an
explicit premise rather than a theorem inferred from names or data.

`source_force_error_power_input` and
`source_force_error_vector_eq` then identify

```text
sourceForce(v) - referenceForce(v)
```

with the sum of the four contraction errors. This vector is the direct input
to the existing `weighted_power_error6` consumer; no second power bound is
duplicated here.

## Radius side

`four_layer_radius_contract` separately proves the pointwise triangle bound

```text
|R₀ + R₁ + R₂ + R₃| <= mu₀ + mu₁ + mu₂ + mu₃,
```

with each layer counted once. The radius proof is independent of the
source-force equality and therefore cannot turn a radius premise into source
semantics.

## Explicit external premises

`BoundaryPremises6` carries separate proof fields for:

- source binding;
- rounding/lift contract;
- export-center contract;
- same-domain coverage contract.

They are intentionally not consumed by the algebraic split. A future adapter
must instantiate them with independently checked evidence and also supply
the four pointwise radius hypotheses. No concrete source, radius, velocity
box, or export payload is selected here.

## Missing obligations and non-claims

This skeleton does not prove the deployed source force equals the declared
contraction, does not prove Float64/libm rounding, and does not establish
source/export consistency or coverage. It also does not prove a numerical
`mu`, a velocity-domain bound, flowpipe inclusion, P3/P4/P5/M4 closure,
admission, or registry promotion.

No local Lean/Lake command was run. Independent pinned-environment review must
check elaboration, imports, `#print axioms`, and placeholder absence. A later
compile would remain candidate evidence only.

