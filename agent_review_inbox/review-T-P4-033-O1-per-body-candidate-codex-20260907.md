# T-P4-033 O1 — per-body source candidate boundary

## Candidate artifact

`examples/routeb_b45_source_comparator_lean/RouteBO1PerBodyExactSource.lean`
adds a concrete exact-real `sourceBodyMass` expansion through the existing
`sourceContract`, with body and inertia constants, and exposes:

- `sourceBodyMass_eq_bodyMass`;
- `sourceBodyMass_eq_juliaExactBodyMass`;
- `six_per_body_source_expansion`;
- a generic `realFourierAtom_complex_re_target` coefficient-to-real
  cos/sin function-lift lemma.

## Boundary

This file is an **uncompiled candidate**. Its `TypedFourierBodyExport` still
takes `h_body` as a structure field; it does not prove the six exact
`sourceBodyMass = fourierBody` equalities for the current source/state key.
The generic atom lemma also does not instantiate the 610-row aggregate or
prove the finite-key-to-real payload lift. Therefore:

```text
h_body_proven = false
h_aggregate_function_lift_proven = false
source_binding_proven = false
formal_certificate_allowed = false
registry_promoted = false
```

The artifact is retained as a typed starting point for the seven O1 DAG
leaves, not as a verified theorem.
