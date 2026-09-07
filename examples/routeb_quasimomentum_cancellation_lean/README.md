# Route-B quasi-momentum cancellation Lean leaf

This directory is a strict, kernel-checked algebraic leaf for the exact-real
Route-B expression

```text
pi4 = p4 - (50000/50003) * cos(y) * p6.
```

`QuasimomentumCancellation.lean` models the `v6` dependence of `p4` and `p6`
as affine profiles.  It proves both:

- the finite-difference `v6` coefficient of `pi4` is zero when
  `m46 = (50000/50003) * cos(y) * m66`; and
- the concrete coefficient pair `m46 = 50000*cos(y)`, `m66 = 50003`
  satisfies that condition exactly.

The `OpenInputs` structure keeps `q6Drive` and `fdDefect` explicit.  The
residual theorem shows that both terms remain additively present; neither is
assumed zero, bounded, identified with a source, or related to a trajectory.
This is an interface for later work, not a trajectory or stability theorem.

The leaf has no `sorry`, `admit`, custom axiom, or `unsafe` declaration.  The
focused verifier compiles only this module with warnings-as-errors, checks the
Lean toolchain and cached Mathlib revision, rejects forbidden proof markers,
and rejects a `sorryAx` dependency in the printed kernel axiom report.  It does
not run a repository-wide regression or mutate Lake state.

Run from WSL at the workspace root:

```text
wsl -d Ubuntu -- bash examples/routeb_quasimomentum_cancellation_lean/verify.sh
```

Pins:

- Lean: `leanprover/lean4:v4.33.1`
- Mathlib cache commit: `0df444a360eaa60ab8c11dca51a86af692955474`
