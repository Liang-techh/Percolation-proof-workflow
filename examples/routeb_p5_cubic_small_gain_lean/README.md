# Route-B P5 cubic small-gain Lean sidecar

This portable sidecar formalizes the source-independent part of
`review-T-P5-010-youhunmozun-20260907T0026.md`.

It proves:

- a division-free scaled Young inequality;
- additive power-level composition of cubic and relative residual gains;
- strict decay when the retained damping margin is positive and bias is nonpositive;
- a squared energy-sublevel adapter from `PC^2 <= Lambda*A^3` to `|PC| <= kappa*A`;
- a one-ray scaling obstruction excluding global quadratic absorption of a nonzero cubic on unbounded velocity.

The sidecar intentionally does **not** establish deployed central-FD tensor semantics,
P8 velocity/sublevel coverage, controller/solve bias closure, P5/M4 admission, or registry promotion.

Run the focused check with:

```bash
./verify.sh
```

`verify.sh` uses `lake` from `PATH`, checks the pinned toolchain against
`examples/local_fkg`, and is registered with `CI_PORTABLE=1` for
`.github/workflows/lean-agent-sidecars.yml`.
