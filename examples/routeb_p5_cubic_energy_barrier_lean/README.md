# Route-B P5 cubic-energy barrier Lean sidecar

This portable sidecar formalizes the source-independent algebra from
`agent_review_inbox/review-T-P5-011-honglianmozun-20260907T0155.md`.

It proves the square-only cubic absorption theorem

`PC^2 <= Lambda*A^3`, `A <= K*Z`, `Lambda*K*Z <= g^2`
`=> |PC| <= g*A`,

its strict variant, the corresponding Lyapunov-ledger nonincrease/strict-decay
consumers, the scalar regularizer bridge yielding `K = 2600000`, and the exact
Fourier specialization

`fdLambda(SF)*2600000 = 13*SF/72000000000000000`.

The final theorem consumes the division-free barrier

`13*SF*Z <= 72000000000000000*g^2`

without square roots.

## Focused check

From the repository root, run:

```bash
CI_PORTABLE=1 examples/routeb_p5_cubic_energy_barrier_lean/verify.sh
```

`verify.sh` resolves `lake` from `PATH`, checks that the local Lake root uses the
same pinned `lean-toolchain`, compiles with warnings as errors, and requires an
axiom report for every theorem.

## Boundary

This sidecar does **not** compute or source-bind `S_F`, prove the modified
non-kinetic storage lower bound `W_min`, bound the Float64 `dM/cijk/accumulation`
remainder, close controller/solve bias, prove first-exit/ODE coverage, or change
P5/M4/registry admission. Those remain explicit downstream premises.
