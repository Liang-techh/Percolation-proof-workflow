# Final receipt — Route-B six-body mass sum

Status: **PASS — six-body finite contract sum; source evaluator and Fourier
binding remain open**

The sidecar defines the finite sum of all six per-body contract mass
contributions and proves source/frame equality by `Finset.sum_congr`, reusing
the verified per-body source contract equality.

Successful pinned run: `output/run-SxiOkB3F`

```text
Lean 4.33.1, commit 819816b2e0a3bf405af45ae5c7af2491d8f5bee6
Mathlib 0df444a360eaa60ab8c11dca51a86af692955474
SixBodyMassSum_COMPILE_EXIT_CODE=0
VERIFY_EXIT_CODE=0
SOURCE_RESTRICTION_CHECK=PASSED
JULIA_FLOAT64_BINDING=OPEN
FULL_MASS_BINDING=OPEN
```

Hashes:

```text
SixBodyMassSum.lean  cf3f3a01ab20a14a265171b5b66806c4e59305f8b69ab2b740e05a938ce5967b
SixBodyMassSum.olean 38a2bb16a39540610360836c034ace104cb89dc05bf10ac09f11e5d77230a65f
```

Only standard logical axioms occur in the axiom reports. No Julia machine
equality, regularizer identity, Fourier normalization, or comparator admission
is claimed.
