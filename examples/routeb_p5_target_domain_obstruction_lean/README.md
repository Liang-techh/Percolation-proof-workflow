# P5-099 target-domain obstruction Lean sidecar

This sidecar consumes the mathematical review `agent_review_inbox/review-P5-099-TARGET-DOMAIN-DECISION-kuangmanmozun-20260908T2041Z.md` and exposes only a kernel-facing algebraic seam.

It formalizes a typed state with six q coordinates, six v coordinates and one disturbance coordinate; the displayed broad ellipsoid/cap predicate; the exact witness `q=0, v=0, w=1`; strict reserve of that witness inside the displayed bounds; the algebraic ramp realization `1*1=1`; the exact rational gap `gapG` and `gapG>11/100`; the sharp pointwise beta-increment iff; the equivalent target-floor weakening; the division-free coefficient half-space; vanishing of q/v beta weights at the witness; the fixed `lambda=2` linear debit; and the final conditional theorem that any universal nonnegative target over the broad algebraic domain is false once a separate source theorem supplies `P witness = -gapG`.

This sidecar intentionally does **not** prove the deployed DH/source equality behind `gapG`, a physical/reachable-domain predicate, path/FD/graph coverage, full-cell sufficiency after changing beta, Float64/controller semantics, P8 ODE coverage, registry admission, or P5/M4 closure. The `TargetState`, `BroadTarget`, and `betaAt` objects are a minimal typed theorem interface, not a claim that they are definitionally identical to the deployed evaluator objects.

Run from a checkout with the repository's pinned `examples/local_fkg` environment available:

```bash
CI_PORTABLE=1 ./verify.sh
```

The verifier discovers `lake` and `lean` from `PATH`, checks the sidecar toolchain against `examples/local_fkg/lean-toolchain`, requires `examples/local_fkg/lake-manifest.json`, compiles with `-DwarningAsError=true`, scans for `sorry`/`admit`, and checks all public theorem axiom reports for `sorryAx`.
