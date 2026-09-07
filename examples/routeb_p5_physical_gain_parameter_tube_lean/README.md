# Route-B P5 physical-gain parameter-tube Lean sidecar

This portable sidecar formalizes the source-independent algebraic child from `agent_review_inbox/review-T-P5-031-guyuefangyuan-20260907T1224.md`.

It checks:

- exact `0 <= t <= 1` moving-frame endpoint bounds for block coordinates 4 and 5;
- physical component-gain transport into a centered state part plus deterministic `|dc|` gain;
- four-term centered square aggregation;
- two-channel Cauchy and square-only product-slack cross-term consumption;
- the resulting `||Dl||^2 <= (U+p)V + (W+q)dc^2` envelope;
- the exact `11424/137088/2285` checker-facing parameter-tube gate;
- the necessity diagnostic `R^2 > 6264373248 U W` for any nonnegative slack pair.

The artifact deliberately does **not** provide the physical gain table, Float64/linear-solve/controller incremental semantics, P8 same-domain coverage, center trajectory binding, ODE first-exit continuation, provenance/admission, registry mutation, or final P5/P8/M4 integration.

Run from any environment with the repository-pinned Lean/Lake toolchain on `PATH`:

```bash
CI_PORTABLE=1 bash examples/routeb_p5_physical_gain_parameter_tube_lean/verify.sh
```

Status after compilation must remain `compiled_candidate`: 待封不觉独立验证 / 待梁智炜（Codex）收割与最终整合。
