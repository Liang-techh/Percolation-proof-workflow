# Route-B P5 moving-frame source transport Lean sidecar

This portable sidecar formalizes the source-independent algebra in `agent_review_inbox/review-T-P5-028-liuguanyi-20260907T1112.md`.

It proves:

- the exact five-coordinate moving-frame actual-minus-nominal identities;
- exact cancellation of the affine ramp center under a common ramp parameter;
- preservation of the fixed `(t,c)` ramp fiber under straight interpolation;
- finite-time component transport under a controlled parameter mismatch;
- the one-row rank-one correction `K_eff = K0 + kappa ⊗ gamma`;
- the obstruction that a finite four-state homogeneous centered gain across arbitrary parameter pairs forces residual constancy along parameter fibers;
- exact block-(4,5) rational endpoint and `T=1` transport constants.

The sidecar intentionally does **not** source-bind a concrete Julia/Float64 Jacobian envelope, source ordering/hash, certified cell chain, ODE/flowpipe coverage, or any P5/P8/M4 admission/final conclusion.

## Verification

The repository workflow `.github/workflows/lean-agent-sidecars.yml` bootstraps the pinned `examples/local_fkg` Lake environment and runs this directory's `verify.sh` because it contains the marker `CI_PORTABLE=1`.

Locally, with `lake` and `lean` on `PATH` and the repository's `examples/local_fkg` environment present:

```bash
bash examples/routeb_p5_moving_frame_transport_lean/verify.sh
```

The script checks the sidecar toolchain against the pinned Lake environment, runs Lean with `-DwarningAsError=true`, requires an axiom report for each exported theorem, and fails if `sorryAx` appears.
