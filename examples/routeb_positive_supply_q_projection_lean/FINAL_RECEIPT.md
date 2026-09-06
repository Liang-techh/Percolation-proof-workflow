# Physical Q-norm projection leaf receipt

Status: PASS — exact compiled candidate, absolute physical projection only.

Successful run: `output/run-TQRk7uuS`

Pinned environment:

- Lean 4.33.1, commit `819816b2e0a3bf405af45ae5c7af2491d8f5bee6`
- Mathlib commit `0df444a360eaa60ab8c11dca51a86af692955474`
- `-DwarningAsError=true`
- cached dependencies only

Compiler result:

```text
QProjection_COMPILE_EXIT_CODE=0
VERIFY_EXIT_CODE=0
SNAPSHOT_HASHES_UNCHANGED=true
```

The successful leaf proves, for the exact expanded current Q,

```text
eta' Q eta <= epsilon_Q^2, epsilon_Q >= 0
  => |(e4+e5)' eta| <= sqrt(32/495) * epsilon_Q.
```

It also proves the selected-coordinate constant is sharp using
`eta=(0,0,0,21s,11s,0)`.

The exported theorem reports contain only the standard axioms `propext`,
`Classical.choice`, and `Quot.sound`.  The source contains no `sorry` or
`admit`.

| Artifact | SHA-256 |
|---|---|
| `QProjection.lean` | `3482783b07b44768c05f46df27788079dd57b918e93d48bba9e84ec966eed282` |
| `QProjection.olean` | `e3fadb3850a681f5e4d094bc380c0439d155233b49383427ef55b6f4e3522eba` |
| `terminal.log` | `b2a5a98c8f69fd0142705eb47ee962b78f8c0b87e7fb32f6b18f0621a1c58438` |

## Scope boundary

This is an absolute Q-norm projection theorem.  It does **not** prove
`|etaU| <= kappa*rho` unless a separate source theorem supplies equilibrium
vanishing or a state-relative scaling such as `epsilon_Q <= c*rho`.  It does
not prove the Float64-to-real source bridge, uniform feasibility,
continuation, reachability, `J <= 1`, or registry promotion.  The global
state must remain `formal_certificate_allowed=false`.

Failed attempts remain in `ATTEMPT_HISTORY.md` and their output directories.
