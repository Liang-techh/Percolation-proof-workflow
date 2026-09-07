# Route-B M4 cross-branch budget transfer

Task: `T-M4-007`.

This sidecar formalizes only the exact arithmetic child extracted from
`review-T-M4-006-daai-xianzun-20260906T2346.md`:

```text
D_old = 4483/2000
D_new = 1401/625
D_new - D_old = 1/10000

D_base <= D_old, rho_bar <= 16,
D_tail <= rho_bar/160000,
D_total <= D_base + D_tail
------------------------------------------------
D_total <= D_new.
```

It also provides the general slack form
`rho_bar <= 160000 * (D_new - D_base)`.

This is a conditional arithmetic theorem. It does not prove the P7
integral/ramp estimate, identify variables with deployed DH dynamics, prove
flowpipe coverage, or alter the authoritative M4 gate. A remote pinned Lean
run and independent axiom/admission review are still required.
