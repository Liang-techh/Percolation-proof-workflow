# Route-B exact rational momentum identity seam

This directory is a small, self-contained Lean 4 algebra leaf for the
block-(4,5) momentum decomposition.  It defines

```text
V = v2 + v3
p4 = R4*v4 + sigma4
p5 = R5*v5 + sigma5
```

with the exact rational constants and the explicit `F, f, h, g, delta4,
delta5` coefficient expressions from the block crossing rows.  The eight
sine/cosine slots are fields of `TrigInputs`, but are retained as
unconstrained real variables.  No trigonometric identity is needed by the
kernel proof.

The checked theorems prove `p4 - R4*v4 = sigma4` and
`p5 - R5*v5 = sigma5`, the equivalent reference-plus-sigma forms, and the
linear regrouping of the shared `v2+v3` coefficient.  The separated and
recombined sigma formulas are both exposed, so the `V` correlation is not
discarded.

This is only a pure algebra kernel proof.  It does not bind the formulas to
Julia or DH source, establish a trajectory or ODE, prove a residual identity
or residual bound, or establish any Lyapunov/flowpipe/terminal claim.

The focused verifier compiles only `RouteBMomentumIdentity.lean` with
warnings-as-errors, checks the pinned Lean/Mathlib versions, rejects
`sorry`/`admit`/`axiom`/`unsafe` markers and `sorryAx` dependencies, and does
not run a repository-wide regression.

Run from WSL at the workspace root:

```text
wsl -d Ubuntu -- bash examples/routeb_momentum_identity_lean/verify.sh
```

Pins:

- Lean: `leanprover/lean4:v4.33.1`
- Mathlib cache commit: `0df444a360eaa60ab8c11dca51a86af692955474`
