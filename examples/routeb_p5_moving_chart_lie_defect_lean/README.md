# T-P5-095 moving-chart base Lie-defect Lean sidecar

This sidecar formalizes the exact-real algebraic core of 柳冠一's `T-P5-095-MOVING-CHART-BASE-LIE-DEFECT` review.

The trusted core is deliberately split at the calculus/source boundary.  It represents the physical signed defect

`S_b = D_x W[b] + (D_x b)^T W + W D_x b`

and the normalized packet

`S_c = D_z M[c] + (D_z c)^T M + M D_z c`, `M = J^T W J`,

at quadratic-form level in a 2x2 exact-real model.  The theorem `moving_chart_base_lie_defect_quadratic_congruence` proves that the expanded normalized packet equals the physical packet at `J eta` once the differentiated vector covariance

`(D_z J[c]) eta + J (D_z c eta) = (D_x b) (J eta)`

is provided componentwise.  The separate theorem `differentiated_vector_covariance_seam` records the minimum source-side chain-rule plus symmetric-chart-Hessian interface needed to produce that covariance.  `base_lie_defect_rate_pullback` then transports a signed same-metric relative rate bound with exactly the same `rho` and without an inverse or square root.

This sidecar does **not** construct the calculus facts `Jc=b`, `D_z(Jc)`, Hessian symmetry, `D_x W[b]`, or any deployed same-tube source packet.  It also does not bind Float64/FD/controller semantics, P8 ODE coverage, provenance/admission, or the P5/M4 parent.

Run:

```bash
CI_PORTABLE=1 examples/routeb_p5_moving_chart_lie_defect_lean/verify.sh
```

The verifier obtains `lake`/`lean` from `PATH`, checks the sidecar toolchain against `examples/local_fkg/lean-toolchain`, requires the pinned `examples/local_fkg/lake-manifest.json`, compiles with warnings as errors, scans for `sorry`/`admit`, and checks `#print axioms` output for every exported theorem.

Standalone success is only `compiled_candidate`: **待封不觉独立验证 / 待梁智炜（Codex）收割与最终整合**.
