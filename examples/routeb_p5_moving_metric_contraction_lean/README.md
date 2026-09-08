# T-P5-090 moving-metric contraction Lean sidecar

Agent: 苏梦辰  
Math source: `agent_review_inbox/review-T-P5-090-moving-metric-contraction-congruence-liuguanyi-20260908T1710Z.md` (柳冠一)

This portable sidecar kernelizes the source-independent 2x2 exact-real algebraic core of T-P5-090. It keeps the differential/source layer outside the trusted statement and consumes only the pointwise moving-frame connection action

`K η = J(B η) - A(J η)`

plus the material-metric quadratic packet. The main theorem proves, at quadratic-form level,

`C_z(η) = C_x(Jη)`

for the complete normalized tensor `BᵀM + MB - L_G M`, where `M=JᵀWJ`. A separate theorem transports `C_x >= 2 μ W` to the pulled-back form with the **same** `μ`, without inverse, square root, determinant division, or eigenvalue API.

The sidecar also freezes two checker regressions from the mathematical review: dropping the material metric derivative changes the true contraction scalar from `0` to `-1` in the zero-system example, and a moving affine chart with denominator-cleared `(1+t)B=1` has exact cancellation `2 B (1+t)^2 - 2(1+t)=0`.

## Exported theorem boundary

- `pullback_quadratic_eq_bilinear`
- `physical_variation_rate_identity`
- `moving_metric_contraction_tensor_congruence`
- `contraction_rate_pullback`
- `normalized_rate_of_congruence`
- `dropping_material_metric_derivative_counterexample`
- `moving_affine_chart_material_cancellation`

## Intentionally open

This sidecar does **not** derive the Fréchet/`HasDeriv` covariance identity from `JG=F∘T+T_t`; it takes the resulting connection action as a typed algebraic premise. Also open are symmetry/differentiability source certificates, deployed true-DH binding, Float64/libm/FD/controller/solve semantics, same-tube domain coverage, finite-step/secant consequences, P8 ODE/flowpipe coverage, comparator admission, registry mutation, and the final P5/M4 conclusion.

Run from the repository with the pinned `examples/local_fkg` environment:

```bash
CI_PORTABLE=1 bash examples/routeb_p5_moving_metric_contraction_lean/verify.sh
```

A focused compile/axiom PASS remains only `compiled_candidate`: 待封不觉独立验证 / 待梁智炜最终整合。
