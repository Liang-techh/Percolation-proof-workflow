# Final receipt — isotropic link-mass Gram reduction

Status: **PASS — scalar isotropic inertia reduces the rotational weighted Gram**

This Mathlib-only leaf proves that `weightedGram J (s I)` equals `s` times the
Jacobian row Gram, and gives the resulting entrywise formula for `linkMass`.
It is the algebraic bridge needed before binding the six concrete body terms to
the Route-B mass evaluator.

Successful pinned run: `output/run-Tg6AVoHq`

```text
Lean 4.33.1, commit 819816b2e0a3bf405af45ae5c7af2491d8f5bee6
Mathlib 0df444a360eaa60ab8c11dca51a86af692955474
IsotropicLinkMass_COMPILE_EXIT_CODE=0
VERIFY_EXIT_CODE=0
SOURCE_RESTRICTION_CHECK=PASSED
JULIA_FLOAT64_BINDING=OPEN
FULL_MASS_BINDING=OPEN
```

Hashes:

```text
IsotropicLinkMass.lean  68dbc6a5bde2683cd8e986164e29fd805f3f9d0ec6893e4a6ed8418fa3ec4458
IsotropicLinkMass.olean 7c8c685d14bb5dcbbc7c3905f12fbfea7141d0edf31dc1e66f8190fbce4f5631
```

Only standard logical axioms occur in the axiom reports. No source runtime or
comparator acceptance is claimed.
