# Final receipt — exact source mass/inertia table

Status: **PASS — exact rational table and scalar-isotropic entry adapter**

Pinned run: `output/run-TrFQWCxh`

```text
Lean 4.33.1, commit 819816b2e0a3bf405af45ae5c7af2491d8f5bee6
Mathlib 0df444a360eaa60ab8c11dca51a86af692955474
SourceMassTableMinimal_COMPILE_EXIT_CODE=0
SOURCE_RESTRICTION_CHECK=PASSED
CSV_FLOAT64_ASSUMPTIONS=0
VERIFY_EXIT_CODE=0
```

The sidecar fixes the six source masses and isotropic inertia scalars as exact
rationals, proves their table entries and nonnegativity, and proves the
scalar-isotropic weighted-Gram entry reduction.  Only standard logical axioms
occur in the axiom report.  This is a compiled candidate; Julia source
semantics, CSV parsing, Float64 rounding and the full mass comparator remain
open.

Hashes:

```text
SourceMassTableMinimal.lean  e63b9ba15e067b9dc8a65e8fa5f346874fc227af2ff61fd85a174ed5cc2ed0dd
SourceMassTableMinimal.olean e55b0314cfa16b309f1710872fa904e9e7f0bd65543d7b0d6dc3ac0d46fd9eaa
```
