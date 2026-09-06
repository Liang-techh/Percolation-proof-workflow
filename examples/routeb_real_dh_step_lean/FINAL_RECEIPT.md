# Final receipt — ideal-real Route-B DH step bridge

Status: **PASS — compiled candidate; Julia Float64/full-mass binding open**

The sidecar defines explicit real DH step matrices and proves, for all six
Route-B rows, that the complex Fourier step matrix is entrywise the complex
coercion of the corresponding real matrix.  It reuses the exact phase bridge
and parameter table.  It does not prove the deployed Julia `Float64`
implementation, frame/axis extraction, COM/Jacobian semantics, or full mass
identity.

Successful pinned run: `output/run-nAZVlwhR`

```text
Lean 4.33.1, commit 819816b2e0a3bf405af45ae5c7af2491d8f5bee6
Mathlib 0df444a360eaa60ab8c11dca51a86af692955474
RealDHStep_COMPILE_EXIT_CODE=0
VERIFY_EXIT_CODE=0
SOURCE_RESTRICTION_CHECK=PASSED
JULIA_FLOAT64_BINDING=OPEN
FULL_MASS_BINDING=OPEN
```

Hashes:

```text
RealDHStep.lean  9C04DA5B9627EE749C53009733006934F95B2D33265E46CA59D0725AA453786A
RealDHStep.olean 16C705C9907E302E4351D9AD47923D5C115B83BD9707BDD3B0C7FD3068A0411B
terminal.log     6521F75D9319310B30838BF235BF23E0A139A8526507B7E5DADC9C2E9A3F073F
```

The axiom reports contain only `propext`, `Classical.choice`, and
`Quot.sound`.  The initial runner failure is retained in `ATTEMPT_HISTORY.md`.
