# Final receipt — homogeneous frame rotation projection

Status: **PASS — 4x4 homogeneous product to 3x3 rotation projection**

This Mathlib-only leaf defines standard homogeneous 4x4 frames and proves that
the top-left 3x3 block of a product is the product of the two top-left
rotation blocks. It is the exact structural bridge from 4x4 DH frame recursion
to the cumulative 3x3 rotation prefix.

Successful pinned run: `output/run-O33agpqU`

```text
Lean 4.33.1, commit 819816b2e0a3bf405af45ae5c7af2491d8f5bee6
Mathlib 0df444a360eaa60ab8c11dca51a86af692955474
HomogeneousRotationProjection_COMPILE_EXIT_CODE=0
VERIFY_EXIT_CODE=0
SOURCE_RESTRICTION_CHECK=PASSED
JULIA_FLOAT64_BINDING=OPEN
FULL_MASS_BINDING=OPEN
```

Hashes:

```text
HomogeneousRotationProjection.lean  a3a6ead7d060729cbcb10ea89122c02fde4c6986474792e369708ff367e8fa8b
HomogeneousRotationProjection.olean df79c634d37249485ed95efaef8d90b71a8119a5dd401f97efaabe00ffcf1b32
```

Only standard logical axioms occur in the axiom reports.
