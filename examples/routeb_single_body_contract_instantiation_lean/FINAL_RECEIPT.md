# Final receipt — Route-B single-body contract instantiation

Status: **PASS — block-(4,5) single-body contract leaves; full mass binding
remains open**

The sidecar specializes the verified source/frame contract to body indices 3
and 4. It kernel-checks the link-4/joint-5 inactive cutoff, the link-5/joint-5
active translational formula, and source/frame body-mass equality separately
for both bodies.

Successful pinned run: `output/run-XSWyT6w1`

```text
Lean 4.33.1, commit 819816b2e0a3bf405af45ae5c7af2491d8f5bee6
Mathlib 0df444a360eaa60ab8c11dca51a86af692955474
SingleBodyContractInstantiation_COMPILE_EXIT_CODE=0
VERIFY_EXIT_CODE=0
SOURCE_RESTRICTION_CHECK=PASSED
JULIA_FLOAT64_BINDING=OPEN
FULL_MASS_BINDING=OPEN
```

Hashes:

```text
SingleBodyContractInstantiation.lean  3d38adef4396a5db0b01c3b85102b29c2c4f2f1bf9e8b3cc2e12ea31877b7f95
SingleBodyContractInstantiation.olean e14eb735fa0bf9f9aef78928fe696bd2bcd08d0856468c801277fdd2c8dcb609
```

Only `propext`, `Classical.choice`, and `Quot.sound` occur in the axiom
reports. No Julia `Float64`, full six-body mass, or comparator admission is
claimed.
