# Route-B P5 incremental hypocoercive tube Lean sidecar

Task: `T-P5-018`  
Math source: `agent_review_inbox/review-T-P5-018-guyuefangyuan-20260907T0634.md`  
Formalization agent: `巨阳仙尊`

This portable sidecar formalizes only the source-independent algebraic seam of the incremental actual-vs-nominal block-(4,5) argument. It proves:

- exact cancellation of arbitrary common forcing when the actual and nominal second-order equations are subtracted;
- the exact completed-square storage identity for the rational Route-B `M,D,K` block;
- `M >= (1/20)I`, `H=K+D-M >= (117/100)I`, and the completed-square storage lower bound;
- the sharpened storage upper estimate and clean `Vd <= (21/25)N` constant;
- direct position and velocity square bounds, including the exact scalar completion producing `4880/117`;
- zero incremental storage for matching mechanical initial conditions;
- the ISS rate conversion `457/1600` in state norm to `457/1344` in storage;
- the division-free inward-boundary test `208849 Vstar > 1075200 L2`.

The sidecar intentionally does **not** authenticate Julia/DH/Float64 semantics, prove existence/uniqueness or first-exit continuation, certify a nominal P8 flowpipe or its physical-box margin, bind a real residual envelope `L2`, mutate the registry, or close P5/P8/M4.

Run from any checkout with the repository-pinned `examples/local_fkg` environment:

```bash
CI_PORTABLE=1 bash examples/routeb_p5_incremental_tube_lean/verify.sh
```

`verify.sh` locates `lake` from `PATH`, checks the pinned Lean toolchain and Lake manifest, compiles with `-DwarningAsError=true`, and rejects `sorryAx`/unexpected axiom failures.
