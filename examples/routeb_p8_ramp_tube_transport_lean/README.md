# Route-B P8 ramp-tube transport Lean sidecar

This portable sidecar formalizes the source-independent part of `T-P8-011`, consuming the mathematics in `agent_review_inbox/review-T-P8-011-guyuefangyuan-20260907T0332.md` and the typed adapter from `examples/routeb_p8_first12_adapter_lean/`.

It proves:

- `proj12_rampLift`: exact recovery of the twelve mechanical coordinates;
- `rampLift_injective_mc`: fixed-time injectivity in `(m,c)`;
- `RampTube` and `rampTube_on_ramp_iff`: exact graph-lift membership;
- `mechanical_coverage_lifts`: pointwise mechanical-tube coverage lifts without independently enclosing `w,c`;
- `PullbackDomain`: the exact source-domain pullback along `w=c*t`;
- `ramp_tail_sq_cap`: the square-only rational tail-domain cap;
- `current_w_box_not_T1`: a rational witness that `|w|<=1/100` cannot cover the full family through `T=1`;
- `ramp_tail_distance` and `explicitMechanical_lipschitz_transport`: the elementary anisotropic Lipschitz substitution identity.

The sidecar deliberately does **not** authenticate Julia `full_rhs!`, prove exact-real/Float64 source regularity, produce interval enclosures, prove ODE existence/continuation, certify a flowpipe, close P8/M4, or mutate the registry.

## Focused verification

From this directory, with the repository-pinned Lean/Lake environment available on `PATH`:

```bash
./verify.sh
```

`verify.sh` is marked `CI_PORTABLE=1` for `.github/workflows/lean-agent-sidecars.yml`. It resolves `lake` from `PATH`, checks this directory's `lean-toolchain` against `examples/local_fkg/lean-toolchain`, then compiles the Picard parent, P8 contract adapter, first-12 adapter, and this child in that order with `-DwarningAsError=true`. It also rejects `sorryAx`, unknown-module, and compiler-error output.

A green focused check is only a compiled formalization candidate. It remains **待封不觉独立验证 / 待梁智炜最终整合**.
