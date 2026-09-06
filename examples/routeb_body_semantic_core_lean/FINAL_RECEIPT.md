# Final receipt — minimal Route-B body semantic core

Status: **PASS — reusable ideal body semantics; source/Float64 binding open**

This Mathlib-only module kernel-checks midpoint COM, the ancestor cutoff for
translational and angular Jacobian columns, active-column formulas, the
link-mass definition, and the block-(4,5) special cases: zero-based link 4
does not depend on joint 5, while zero-based link 5 does. It is deliberately
independent of frame, DH, and source modules so adapters can be compiled as
small separate leaves.

Successful pinned run: `output/run-6vhFP8Zp`

```text
Lean 4.33.1, commit 819816b2e0a3bf405af45ae5c7af2491d8f5bee6
Mathlib 0df444a360eaa60ab8c11dca51a86af692955474
BodySemanticCore_COMPILE_EXIT_CODE=0
VERIFY_EXIT_CODE=0
SOURCE_RESTRICTION_CHECK=PASSED
JULIA_FLOAT64_BINDING=OPEN
FULL_MASS_BINDING=OPEN
```

Hashes:

```text
BodySemanticCore.lean  fe15f6ca9993f55fc56e6d2c9cca5fa8c7f6e9530b9b900a6f111ed96715149c
BodySemanticCore.olean b9e469fd3e40fe1f8ae09686c1cfee813743fe23fbe0979f9564ab4cc84938a3
terminal.log           c051d5307ba26d56e267e7dab840fdc3d9e02130f81772da4797a8448f9381af
```

The axiom reports contain only `propext`, `Classical.choice`, and
`Quot.sound`. No source equality, Float64 enclosure, or formal certificate is
claimed.
