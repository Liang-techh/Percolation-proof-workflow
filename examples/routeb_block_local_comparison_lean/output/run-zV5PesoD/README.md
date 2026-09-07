# Minimal block-(4,5) local storage comparison

This directory contains one new Lean leaf.  It imports the already compiled
`examples/routeb_local_energy_budget/LocalEnergyBudget.lean` result and proves
the reusable comparison

```text
p45(q4,q5,v4,v5) <= Lambda * VB(q4,q5,v4,v5)
Lambda = 6400000 / 200739
```

for arbitrary real block coordinates.  Thus the comparison is a pure
quadratic/algebraic interface: it has no domain, trajectory, differentiability,
or residual-size premise.

The theorem p45_le_mul_VB_of_Lambda_ge exposes the monotone downstream form:
any supplied constant Lambda' larger than the exact constant is also accepted,
using only the already verified nonnegativity of VB.

`derivative_budget_and_storage_comparison` is the downstream seam.  It accepts
the block equations and the derivative expression as explicit premises and
returns both the existing derivative budget and the independent storage
comparison.  The residuals `e4,e5` are explicit total mismatch variables and
are not bounded by this leaf.

## Local verification

From the workspace root, run:

```powershell
wsl -d Ubuntu -- bash '/mnt/c/Users/z5242/Desktop/重构版/工作流/examples/routeb_block_local_comparison_lean/verify.sh'
```

The verifier copies the pinned `LocalEnergyBudget.olean` from its successful
run, checks its source and artifact hashes, and compiles only this new source
with Lean 4.33.1, cached Mathlib, and `-DwarningAsError=true`.  It also checks
the source for `sorry`, `admit`, and source-level `axiom` declarations.

## Real binding still open

This leaf does not establish any of the following physical facts:

- the executed DH/controller equations imply `blockEquation` for the actual
  trajectory, including remote coupling, gravity, mass mismatch, and the
  finite-difference/Float64/linear-solve defects;
- the supplied `dVB` is the derivative of the actual trajectory storage, with
  `qdot = v`, regularity, chain rule, and time integration;
- `VB` is the exact storage used by the real implementation rather than the
  constant-reference mass plus local PD expression imported here;
- a uniform pointwise or integrated bound for the total residual energy, or
  the required disturbance/input budget;
- domain coverage/first-exit, continuation, full-horizon tube containment, or
  terminal transfer;
- statement-level equivalence between this local `p45` and the final external
  comparator target.

Consequently this is a `LEAN_VERIFIED` algebraic leaf and an explicit adapter
interface, not a real-dynamics or full Route-B certificate.
