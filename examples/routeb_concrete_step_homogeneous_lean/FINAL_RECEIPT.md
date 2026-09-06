# Final receipt — concrete Route-B DH step homogeneous decomposition

Status: **PASS — exact-real Route-B DH steps decompose into homogeneous frames**

This Mathlib-only leaf defines the concrete 3x3 rotation block and translation
column extracted from each Route-B real DH step, then proves the full 4x4 step
equals the corresponding homogeneous frame. The theorem is structural and
does not assert Julia Float64 or runtime source equivalence.

Successful pinned run: `output/run-ZBZY9WRv`

```text
Lean 4.33.1, commit 819816b2e0a3bf405af45ae5c7af2491d8f5bee6
Mathlib 0df444a360eaa60ab8c11dca51a86af692955474
ConcreteStepHomogeneous_COMPILE_EXIT_CODE=0
VERIFY_EXIT_CODE=0
SOURCE_RESTRICTION_CHECK=PASSED
JULIA_FLOAT64_BINDING=OPEN
FULL_MASS_BINDING=OPEN
```

Hashes:

```text
ConcreteStepHomogeneous.lean  5da25ba14626338bb82e63b13f2abd4caa4f5bf84d1f5b23ec38731682307499
ConcreteStepHomogeneous.olean 6dd681ce81fdc87d442e5889e1e07c075b637d7fcf70e66db3454a24b4f5988d
```

Only standard logical axioms occur in the axiom reports. This is a compiled
candidate for the proof DAG; no registry promotion is made.
