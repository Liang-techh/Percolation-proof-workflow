# T-P5-065 relative remainder absorption — Lean sidecar

Source mathematical review: `agent_review_inbox/review-T-P5-065-relative-remainder-absorption-kuangmanmozun-20260908T0344.md`.

This portable sidecar formalizes only the source-independent kernel seam requested by the mathematical review:

- exact same-monomial factor recombination `g = M*u`, `r = M*e`;
- signed unit-margin absorption under `|sigma| = 1` and `|e| <= eps < m`;
- a higher-order normalized remainder charge from a separately certified monomial envelope;
- the division-free relative remainder sign-stability gate `|r| <= alpha|g|`, `alpha < 1`;
- the sharp `alpha = 1` cancellation boundary and the `z^2 + eps*z = z(z+eps)` lower-order contamination regression;
- additive normalized-remainder difference/Lipschitz budget and a same-domain pointwise adapter.

The monomial-product bound itself is intentionally an interface premise (`|M_S| <= Hcharge`): this sidecar does not duplicate the finite-product transport already handled by T-P5-063/T-P5-064. Likewise it does not bind deployed CSE/source expressions, Float64/libm/FD/controller semantics, reachability/P8 coverage, provenance/admission, or any P5/M4 final conclusion.

Run from the repository checkout:

```bash
bash examples/routeb_p5_relative_remainder_absorption_lean/verify.sh
```

`verify.sh` locates `lake`/`lean` from `PATH`, consumes the repository-pinned `examples/local_fkg/lake-manifest.json`, checks the sidecar toolchain pin, compiles with warnings as errors, and rejects `sorryAx` in the exported theorem audit.
