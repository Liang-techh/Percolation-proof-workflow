# Verification report

## Scope

The leaf formalizes an abstract joint `p`/`sigma` interface for M4.  It proves
the algebraic propagation from explicit budget premises to

```text
V(t) <= V(0) + B,
B = forcingCap / (4 * lambda) + sigmaCap,
v(t)^2 <= 4 * (V(0) + B) + 2 * sigmaCap / m^2.
```

The state hypotheses explicitly contain `p = m*v + sigma` and
`x = (q,p/m)`.  The filter calculation and the velocity decomposition use
only elementary real algebra and nonnegativity of squares.

## Conditional boundary

`IntegratedEnergySeam` is an intentional open premise:

```text
V(t) - V(0) <= accumulatedForcing / (4*lambda) + sigmaTerminal^2.
```

It is the admission point for a future rigorous integration, telescoping, or
flowpipe proof.  No Bochner integral is hidden in the definition, and no
pointwise differential inequality is silently upgraded into an integrated
claim.  `ForcingBudget` and `SigmaTerminalBound` then replace the seam's
quantities by their explicit caps.

No theorem in this directory claims real DH source binding, exact DH dynamics,
compiled-candidate acceptance, or a verified physical trajectory.

## Focused verifier

The intended command is `bash verify.sh`.  It checks the pinned Lean
4.33.1 toolchain and Mathlib revision, compiles only `JointPSigmaBudget.lean`
with `warningAsError=true`, rejects `sorry`, `admit`, custom `axiom`, and
`unsafe`, and checks the ten printed theorem axiom reports for unexpected
axioms.  It does not run full-repository regression.

## Result

Focused verification passed on 2026-09-07 UTC via:

```text
bash verify.sh
LEAN_COMPILE_EXIT_CODE=0
Axiom audit: 10 declarations; unexpected axioms: 0
PASS: 10 theorem axiom reports; zero proof holes; no custom axioms.
```

Every printed theorem report contains only Lean's standard
`propext`, `Classical.choice`, and `Quot.sound` foundations.  In particular,
there is no `sorryAx`; the verifier also rejects `sorry`, `admit`, custom
`axiom`, and `unsafe` tokens before compilation.  No repository-wide
regression was run.
