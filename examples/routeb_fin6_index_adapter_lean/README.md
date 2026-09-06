# Route-B Fin 6 / Julia index adapter

This sidecar is the minimal strict source-order adapter for B45-1.

It defines and proves:

- a bijection from Lean's zero-based `Fin 6` indices to Julia's one-based
  indices `1 ≤ n ≤ 6`;
- the exact offset relation `julia = zero + 1` and its inverse;
- the source-order list `[0, 1, 2, 3, 4, 5]` and its one-based image
  `[1, 2, 3, 4, 5, 6]`;
- the block mappings, interpreting the source labels as Julia 1-based:
  `B = (4,5)` becomes zero-based `(3,4)`, and
  `D = (1,2,3,6)` becomes zero-based `(0,1,2,5)`.

The list/block statements are exact finite adapter facts.  They are not a
claim that Lean has been bound to Julia `Float64`, the Julia DH function, the
COM/Jacobian implementation, the mass function, or any full Route-B
certificate.  Function-level frame/mass binding remains **OPEN**.

## Verification

Run `bash verify.sh` from this directory.  The script uses the pinned
Lean 4.33.1 executable and the pinned Mathlib checkout already used by the
other Route-B sidecars.  It compiles the source with warnings treated as
errors, checks the expected source restrictions, and records a receipt under
`output/run-*`.

The successful result is an exact compiled candidate, not a promotion into
the shared theorem registry.  This sidecar intentionally does not modify
`state.json`, the original 6-DOF directory, or any existing sidecar.

## Evidence level

`COMPILED_CANDIDATE_COMPARATOR_PENDING`.

The remaining B45-1 obligation is function-level binding of the six concrete
source steps (including frame/axis semantics) and then the mass/COM/Jacobian
functions.  Those obligations remain OPEN/UNKNOWN here.
