# Final receipt — Route-B kinematic contract core

Status: **PASS — Mathlib-only contract congruence core; source and Float64
binding remain open**

This sidecar defines a one-way `KinematicContract` containing only seven frame
origins and six joint axes. It kernel-checks congruence lifting from pointwise
origin/axis equality to translational Jacobians, angular Jacobians, and body
mass, and proves the block-(4,5) inactive/active cutoffs. A future source
adapter only needs to establish the two function equalities; it does not need
to import frame recursion or DH matrix definitions into this core.

Successful pinned run: `output/run-0FvNkLzz`

```text
Lean 4.33.1, commit 819816b2e0a3bf405af45ae5c7af2491d8f5bee6
Mathlib 0df444a360eaa60ab8c11dca51a86af692955474
BodyContractCore_COMPILE_EXIT_CODE=0
VERIFY_EXIT_CODE=0
SOURCE_RESTRICTION_CHECK=PASSED
JULIA_FLOAT64_BINDING=OPEN
FULL_MASS_BINDING=OPEN
```

Hashes:

```text
BodyContractCore.lean  525e564bdbb57976f0c8a119a6e4bf9294d979dbfcc35ca705bf12a7ad95a4db
BodyContractCore.olean eab31f6595659adeae9a743a9ace57ee2e388334a41f90e7cbc49cf0996e65f7
terminal.log           ca940b0b15c38059ca2795ef1a4f10360266cc670c7851650a7745759810de8c
```

The axiom reports contain only `propext`, `Classical.choice`, and
`Quot.sound`. This is a compiled candidate, not a registry admission: the
comparator still must connect the contract to the concrete Julia/Float64
source functions.
