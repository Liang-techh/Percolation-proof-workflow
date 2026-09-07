# Route-B P5 direct residual metric Lean sidecar

This portable sidecar formalizes the source-independent algebra from
`agent_review_inbox/review-T-P5-019-honglianmozun-20260907T0702.md`.

It proves the exact block-(4,5) dissipation lower bound, the direct
`5 ||x+y||^2 <= 17 Q` metric, a square-only residual absorption theorem, and
the improved ISS / quarter-barrier / common-margin integer constants.

It intentionally does **not** prove Julia/DH or Float64 source semantics,
actual-minus-nominal residual bounds, P8 nominal flowpipe coverage,
ODE existence/continuation, or P5/P8/M4 closure.  柳冠一's separate
T-P5-019 FD/runtime source adapter is not claimed by this sidecar.

Run from any environment with the repository's pinned `examples/local_fkg`
Lake environment available:

```bash
./verify.sh
```

`verify.sh` locates `lake` from `PATH`, checks the pinned toolchain and
`lake-manifest.json`, compiles with `-DwarningAsError=true`, and fails on
`sorryAx`, Lean errors, or missing `#print axioms` output.
