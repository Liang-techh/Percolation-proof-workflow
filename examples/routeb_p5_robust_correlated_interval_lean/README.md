# T-P5-045 robust correlated interval Lean sidecar

Agent: `苏梦辰`

This portable sidecar formalizes the source-independent mathematical core of 柳冠一 `T-P5-045`, which bridges signed interval data for the `2x2` residual block into the correlated T-P5-044 Lyapunov gate.

The trusted core keeps the signed symmetric invariant `sigma = k45 + k54` intact. It does **not** replace it by separate absolute bounds on `k45` and `k54`, and it never treats a failed interval lower bound as a physical instability theorem.

Implemented theorem boundary:

- `scaled_correlated_invariants`: exact clearing of the `q=sigma/2`, `Delta` convention.
- `scaled_symmetric_det_lower_of_interval`: `pL>0` and positive `Dmin=4 pL sL-Q^2` imply pointwise positive reserves and `D4>=Dmin`.
- `scaled_adjugate_bias_le_box`: component boxes plus `|sigma|<=Q` bound the correlated adjugate bias.
- `scaled_adjugate_bias_le_cross_cap`: optional tighter direct cross-term cap.
- `correlated_quarter_gate_of_interval_box`: transports `800 Ebox < (109-rU) Dmin` to the pointwise quarter gate.
- `correlated_one_twelfth_parameter_gate_of_interval_box`: analogous `2400` parameter/incremental gate.
- `correlated_quarter_gate_from_cell_box`: end-to-end source-facing composition of determinant and bias certificates.
- global `r<=1` corollaries giving the exact rational checks `200 Ebox < 27 Dmin` and `200 Eg < 9 Dmin`.
- `skew_family_scaled_det_independent`: exact cancellation boundary for `[[0,M],[-M,0]]`.

The sidecar intentionally excludes deployed source binding, Float64/libm/FD/controller/solve semantics, trajectory/first-exit coverage, provenance/admission, registry updates, and any final P5/M4 conclusion.

Run:

```bash
bash examples/routeb_p5_robust_correlated_interval_lean/verify.sh
```

The verifier requires `lake` and `lean` on `PATH`, checks the pinned `examples/local_fkg/lake-manifest.json` environment, compiles with `-DwarningAsError=true`, scans the exported theorem axiom reports, and fails closed on `sorryAx`.

Status after a green focused compile remains `compiled_candidate`: 待封不觉独立验证 / 待梁智炜最终整合。
