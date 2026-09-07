# Route-B P5 parameter-tube gain Lean sidecar

This sidecar formalizes the source-independent algebra from
`agent_review_inbox/review-T-P5-030-honglianmozun-20260907T1205.md`.

It proves the exact outer-product increment identity, anisotropic and isotropic
entrywise bounds, the two-component row-sum force estimate with the current
`k_E = 1/10` specialization, homogeneous centered-force gain inflation, and the
pure algebraic finite-cover target step.  A square-root-free unit-radius
reduction for the quadratic tube cost is also included for later rational-cover
construction.

The sidecar intentionally does **not** certify source coefficients, source
hashes, checker-generated anchor cells, a concrete finite cover, ODE/flowpipe
coverage, P5/P8/M4 closure, provenance/admission, or final integration.

Run from any checkout with `lake` and `lean` on `PATH`:

```bash
CI_PORTABLE=1 bash examples/routeb_p5_parameter_tube_gain_lean/verify.sh
```

The script reuses the repository-pinned `examples/local_fkg` Lake environment
and checks that its toolchain matches this sidecar's `lean-toolchain` before
compiling with `-DwarningAsError=true`.  It also requires an axiom report for
every exported theorem and rejects `sorryAx`.
