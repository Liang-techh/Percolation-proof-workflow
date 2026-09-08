# T-P5-076 weighted Gram Lipschitz Lean sidecar

Agent/source_agent: **苏梦辰**.

This portable sidecar formalizes the first algebraic leaves requested by 柳冠一's `T-P5-076-WEIGHTED-GRAM-LIPSCHITZ` mathematics. It deliberately stops before segment integration, deployed Jacobian/source binding, numerical evaluator semantics, ODE coverage, admission, or registry mutation.

Kernel-facing statements:

- `signed_cross_term_le`: one signed Gram cross term is bounded by `c (x^2+y^2)` from `|h| <= c`.
- `weighted_gram_row_upper_2x2`: exact two-row Gershgorin/Young-style weighted Gram upper certificate.
- `weighted_jacobian_pointwise_sq_le_2x2`: consumes signed weighted Gram entries formed *after* summation and returns the pointwise squared-Lipschitz quadratic bound.
- `cleared_implicit_weighted_gram_term_identity`: scalar denominator-clearing identity `A=dJ`, `Delta=eta d^2`.
- `cleared_implicit_weighted_gram_sum_identity`: finite signed sum version; no absolute value is moved inside the Gram sum.
- two exact cancellation regressions for `J=[[1,1],[1,-1]]`.

The first sidecar intentionally uses a 2x2 pointwise Jacobian theorem as the minimal kernel-checkable SCC block. The general finite-dimensional row-sum theorem and convex-segment integration theorem remain separate follow-up obligations; this avoids mixing the source-independent finite algebra with Mathlib integration/differentiability APIs in the first receipt.

Run from this directory or through `.github/workflows/lean-agent-sidecars.yml`:

```bash
CI_PORTABLE=1 bash verify.sh
```

`verify.sh` resolves `lake` and `lean` from `PATH`, reuses the repository's pinned `examples/local_fkg` Lake environment, requires the same `lean-toolchain`, scans for `sorry`/`admit`, compiles with warnings as errors, and checks that every exported theorem emitted an axiom report with no `sorryAx`.

Passing this sidecar means only `compiled_candidate`: **待封不觉独立验证 / 待梁智炜最终整合**.
