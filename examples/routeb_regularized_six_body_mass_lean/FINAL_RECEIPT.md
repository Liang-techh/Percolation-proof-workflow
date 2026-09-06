# Final receipt — regularized six-body isotropic mass adapter

Status: **PASS — exact rational regularizer composed with six-body mass reduction**

This Mathlib-only leaf proves the entrywise regularized six-body mass formula:
the scalar-isotropic six-link Gram sum plus the exact diagonal
`1/1000000` term. It is an ideal-real adapter and does not bind Julia
Float64 execution or the Fourier coefficient table.

Successful pinned run: `output/run-2UEw1Rrk`

```text
Lean 4.33.1, commit 819816b2e0a3bf405af45ae5c7af2491d8f5bee6
Mathlib 0df444a360eaa60ab8c11dca51a86af692955474
RegularizedSixBodyMass_COMPILE_EXIT_CODE=0
VERIFY_EXIT_CODE=0
SOURCE_RESTRICTION_CHECK=PASSED
JULIA_FLOAT64_BINDING=OPEN
FULL_MASS_BINDING=OPEN
```

Hashes:

```text
RegularizedSixBodyMass.lean  7eb82a98479517602af1ce5015073a177d50cf28fc0fa539d17295dcbe63a76c
RegularizedSixBodyMass.olean 62d6d1d9e4127959af48535bd8a93626419674bbfb3dfd3b872ecf9dd6697f72
```

Only standard logical axioms occur in the axiom reports. Comparator and
source-semantic acceptance remain open.
