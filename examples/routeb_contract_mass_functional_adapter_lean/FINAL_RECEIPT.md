# Final receipt — contract to generic mass-functional adapter

Status: **PASS — KinematicContract mass is definitionally aligned with massFromLinks**

This Mathlib-only leaf proves the equality between the existing contract
semantic link mass and the generic weighted-Gram `linkMass`, then lifts that
equality to a six-body finite sum. It is a structural ideal-real adapter; no
concrete source or Float64 semantics are asserted.

Successful pinned run: `output/run-H1RwjdoF`

```text
Lean 4.33.1, commit 819816b2e0a3bf405af45ae5c7af2491d8f5bee6
Mathlib 0df444a360eaa60ab8c11dca51a86af692955474
ContractMassFunctionalAdapter_COMPILE_EXIT_CODE=0
VERIFY_EXIT_CODE=0
SOURCE_RESTRICTION_CHECK=PASSED
JULIA_FLOAT64_BINDING=OPEN
FULL_MASS_BINDING=OPEN
```

Hashes:

```text
ContractMassFunctionalAdapter.lean  51ae35bb16c75c2907e5123567d8eca55118d9c0b3bd9f2311636951a038b535
ContractMassFunctionalAdapter.olean 07c0c1dc7c3a0914ee2d309414563fc049937d78e4a665c1780f958f1a7ffef4
```

Only standard logical axioms occur in the axiom reports. This is a compiled
candidate for the DAG and is not comparator-accepted source evidence.
