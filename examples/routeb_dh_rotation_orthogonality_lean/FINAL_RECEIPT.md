# Final receipt — exact DH rotation orthogonality

Status: **PASS — generic exact-real DH rotation orthogonality**

This Mathlib-only leaf defines the 3x3 rotation block of a standard DH
transform and proves row orthogonality from the two scalar identities
`ct*ct + st*st = 1` and `ca*ca + sa*sa = 1`. It is independent of Julia
Float64 and source evaluation; the Route-B specialization of these identities
is a separate obligation.

Successful pinned run: `output/run-u9aZXWdK`

```text
Lean 4.33.1, commit 819816b2e0a3bf405af45ae5c7af2491d8f5bee6
Mathlib 0df444a360eaa60ab8c11dca51a86af692955474
DHRotationOrthogonality_COMPILE_EXIT_CODE=0
VERIFY_EXIT_CODE=0
SOURCE_RESTRICTION_CHECK=PASSED
JULIA_FLOAT64_BINDING=OPEN
FULL_MASS_BINDING=OPEN
```

Hashes:

```text
DHRotationOrthogonality.lean  2c02c6e139dc7353335a4e2aae6b88582465c7073bfab820dc78dd52cf4f0155
DHRotationOrthogonality.olean 8658e553683a9afef09e7c9039805d8f66c13bd6ff1231f29f06ac64f4eeb01d
```

Only standard logical axioms occur in the axiom report.
