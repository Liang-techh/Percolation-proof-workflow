# Final receipt — Route-B source rotation block bridge

Status: **PASS — exact-real source top-left rotation block**

This leaf proves that the top-left 3x3 block of every exact-real Route-B 4x4
DH step is the specialized `dhRotation` matrix, and lifts the previously
proved row-orthogonality to that source block. It does not claim Julia
Float64 matrix multiplication or source runtime equivalence.

Successful pinned run: `output/run-Qk8Gg5d9`

```text
Lean 4.33.1, commit 819816b2e0a3bf405af45ae5c7af2491d8f5bee6
Mathlib 0df444a360eaa60ab8c11dca51a86af692955474
SourceRotationBlock_COMPILE_EXIT_CODE=0
VERIFY_EXIT_CODE=0
SOURCE_RESTRICTION_CHECK=PASSED
JULIA_FLOAT64_BINDING=OPEN
FULL_MASS_BINDING=OPEN
```

Hashes:

```text
SourceRotationBlock.lean  59ba41ff224b235423874ece002689367c9a61be1d78790eac1e753dd5e1f289
SourceRotationBlock.olean efcb3f55c391bac1d16594a35b61ed905063a4797baa10bc293572cba5c8745f
```

Only standard logical axioms occur in the axiom reports.
