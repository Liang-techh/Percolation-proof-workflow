# Final receipt — six-body isotropic mass reduction

Status: **PASS — scalar-isotropic link reduction lifts to six-body mass**

This Mathlib-only leaf lifts the isotropic `linkMass` entry identity through
the finite six-link `massFromLinks` sum. It exposes the exact sum of
translational and rotational Jacobian row Grams required by the source mass
adapter.

Successful pinned run: `output/run-ialqen55`

```text
Lean 4.33.1, commit 819816b2e0a3bf405af45ae5c7af2491d8f5bee6
Mathlib 0df444a360eaa60ab8c11dca51a86af692955474
SixBodyIsotropicMass_COMPILE_EXIT_CODE=0
VERIFY_EXIT_CODE=0
SOURCE_RESTRICTION_CHECK=PASSED
JULIA_FLOAT64_BINDING=OPEN
FULL_MASS_BINDING=OPEN
```

Hashes:

```text
SixBodyIsotropicMass.lean  6b918d4d01569c346d713887e6e2467337a6ced133c7abbe5afae3bb6194fd77
SixBodyIsotropicMass.olean 58f3da5b1be9ab053512b73216ebff0d2d04504852706a29e5d7aad0b3cb8cef
```

Only standard logical axioms occur in the axiom reports. No concrete source,
Float64, comparator, or final-certificate claim is made.
