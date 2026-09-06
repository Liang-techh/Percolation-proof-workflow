# Final receipt — isotropic inertia rotation bridge

Status: **PASS — exact isotropic rotation identity; orthogonality/source
binding remains an obligation**

This Mathlib-only leaf proves that if the rows of a 3x3 real matrix are
orthonormal, then `R * (s I) * Rᵀ = s I`. It is the algebraic bridge needed to
replace Julia's rotated isotropic inertia term with the fixed inertia matrix
used by the contract mass core. The source-specific proof that each DH
rotation has orthonormal rows is intentionally separate.

Successful pinned run: `output/run-KWENke5I`

```text
Lean 4.33.1, commit 819816b2e0a3bf405af45ae5c7af2491d8f5bee6
Mathlib 0df444a360eaa60ab8c11dca51a86af692955474
IsotropicInertia_COMPILE_EXIT_CODE=0
VERIFY_EXIT_CODE=0
SOURCE_RESTRICTION_CHECK=PASSED
JULIA_FLOAT64_BINDING=OPEN
FULL_MASS_BINDING=OPEN
```

Hashes:

```text
IsotropicInertia.lean  4072f7097745e23f51bbfe063e6b689dc2d76e5092ade1d0589ae58ff1d41294
IsotropicInertia.olean e1bc6b4866f5e1cb25ee831885db3388b1255c7ef7b8faba7b300fa51f1ebebc
```

Only `propext`, `Classical.choice`, and `Quot.sound` occur in the axiom
report. No DH orthogonality, Julia Float64 semantics, or comparator admission
is claimed here.
