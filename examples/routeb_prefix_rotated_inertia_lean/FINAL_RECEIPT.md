# Final receipt — cumulative-prefix isotropic inertia bridge

Status: **PASS — cumulative orthogonal prefixes preserve isotropic inertia**

This Mathlib-only leaf composes the seven-slot cumulative rotation
orthogonality theorem with the isotropic inertia identity. For every prefix and
scalar inertia `s`, it proves `R * (s I) * Rᵀ = s I`, including the entrywise
form needed by the link-mass functional.

Successful pinned run: `output/run-pxP29rsU`

```text
Lean 4.33.1, commit 819816b2e0a3bf405af45ae5c7af2491d8f5bee6
Mathlib 0df444a360eaa60ab8c11dca51a86af692955474
PrefixRotatedInertia_COMPILE_EXIT_CODE=0
VERIFY_EXIT_CODE=0
SOURCE_RESTRICTION_CHECK=PASSED
JULIA_FLOAT64_BINDING=OPEN
FULL_MASS_BINDING=OPEN
```

Hashes:

```text
PrefixRotatedInertia.lean  64e1505038bb57c15380a0783983ac1cf1a4b16e6cbc32c846cc5b9d96f1c575
PrefixRotatedInertia.olean 2f3f9d8367d0e2d635a79fc9739546922a38835f8b193a992953cd27c7aeb6db
```

Only standard logical axioms occur in the axiom reports. This is a compiled
candidate for the Route-B proof DAG, not comparator-accepted source evidence.
