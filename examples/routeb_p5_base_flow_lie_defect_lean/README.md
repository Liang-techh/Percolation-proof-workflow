# T-P5-093 base-flow Lie-defect Lean sidecar

This sidecar formalizes the exact-real consumer boundary from 红莲魔尊's `T-P5-093-BASE-FLOW-LIE-DEFECT` mathematical review.

It keeps the base-flow perturbation as the signed assembled packet

`S_b = D_x W[b] + (Db)^T W + W(Db)`

before any unsigned bound, proves the rate loss `mu -> mu-rho`, keeps an additional relative variational defect separate so `Db` is not double-counted, and proves the division-free mixed additive tube inequality. It also includes the constant-metric skew cancellation and a scalar regression showing that `Db=0` is insufficient when the metric moves with state.

The calculus/source layer is intentionally external: this file does not construct `Db`, `D_xW[b]`, deployed same-tube coverage, Float64/FD/controller semantics, or P8 ODE/flowpipe evidence.

Run the focused verifier with:

```bash
CI_PORTABLE=1 examples/routeb_p5_base_flow_lie_defect_lean/verify.sh
```

The verifier resolves `lake` and `lean` from `PATH`, checks the sidecar toolchain against `examples/local_fkg/lean-toolchain`, consumes the pinned `examples/local_fkg/lake-manifest.json`, compiles with warnings as errors, scans for `sorry`/`admit`, and audits every exported theorem with `#print axioms`.

Admission boundary: standalone compile success is only `compiled_candidate`; it remains **待封不觉独立验证 / 待梁智炜最终整合**.
