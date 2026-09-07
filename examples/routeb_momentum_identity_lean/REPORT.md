# Verification report

## Scope

The leaf treats every sine/cosine slot as an arbitrary real input and keeps
all coefficients exact.  The common remote-velocity combination is

```text
V = v2 + v3
```

and the two cross-row corrections are

```text
sigma4 = k*sinY^2*v4 + F*v1 + f*V + delta4*v2 + J*cosY*v6
sigma5 = h*v1 + g*V + delta5*v2.
```

The exact rational values are defined in the Lean source.  The kernel checks
the two subtraction identities, the reference-plus-sigma rearrangements,
and the separated/recombined forms of both sigma expressions.

## Verification boundary

No theorem here identifies `TrigInputs` with evaluated trigonometric
functions, a DH mass matrix, a Julia implementation, or a Float64 execution.
There is no acceleration, force, ODE, trajectory, source-comparator, residual,
interval, or terminal-bound statement.  In particular, a compiled OLean file
is only evidence for this algebraic seam.

## Focused command

`verify.sh` snapshots the local inputs into an isolated run directory and
compiles only `RouteBMomentumIdentity.lean` with `-DwarningAsError=true`.
It uses the pinned Lean 4.33.1 executable and the cached Mathlib revision
`0df444a360eaa60ab8c11dca51a86af692955474`.  No full-workspace test suite is
run.

## Result

Focused verification succeeded on 2026-09-07T00:16:17Z--00:17:01Z UTC in
`output/run-SOJZfdgY`:

- Lean 4.33.1, Mathlib `0df444a360eaa60ab8c11dca51a86af692955474`;
- `RouteBMomentumIdentity_COMPILE_EXIT_CODE=0`;
- no forbidden source markers and no `sorryAx` dependency;
- source SHA-256: `a784b4fe8b0985d025ef61ffd2f9ac9f64bcc1ad8c20cf329caa2a534988bd3a`;
- OLean SHA-256: `b7486b1e63cddef6af9e816cea322a38fbcd45eeaafd819d0be0cfeb0d385fc1`.
