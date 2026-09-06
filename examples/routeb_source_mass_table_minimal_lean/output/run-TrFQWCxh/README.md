# Minimal exact source mass-table Lean sidecar

This sidecar is deliberately independent of the historical Route-B `.olean`
chain. It imports only `Mathlib` and defines the six exact rational source
mass values and the exact isotropic inertia scalars `I_val / 3`:

```text
mass    = [1, 4/5, 3/5, 2/5, 3/10, 3/20]
I_val/3 = [1/3, 1/5, 7/60, 1/15, 1/30, 1/60]
```

The main reusable theorem is
`linkMass_entry_scalarIdentity`: for arbitrary real Jacobian entries, an
isotropic inertia matrix reduces the generic mass entry to the translational
Gram term plus the rotational Gram term. No CSV, `Float64`, source-runtime
assumption, axiom, `sorry`, or `admit` is used.

This is an isolated compiled candidate, not a source-semantics or Fourier
evaluator binding.
