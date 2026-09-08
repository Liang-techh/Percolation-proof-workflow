# T-P5-045 signed-symmetric correlated interval gate — Lean sidecar

Formalization agent: **巨阳仙尊**.

Mathematical intake: `agent_review_inbox/review-T-P5-045-liuguanyi-20260907T2108.md`.

This sidecar freezes only the source-independent algebraic/interface layer:

- exact scaled invariants `D4 = 4*p*s-sigma^2` and the scaled adjugate bias;
- signed entry-interval addition before absolute scalarization;
- strict determinant lower transport from `pL`, `sL`, `Q`, `Dmin`;
- independent component-box adjugate-bias bound;
- optional direct correlated cross-cap bound;
- strict quarter-barrier and one-twelfth parameter gate transport;
- exact whole-`r in [0,1]` integer simplifications.

The formalization exposes one useful typed boundary: the bias lemmas need nonnegative diagonal coefficients (`p,s >= 0`) in addition to upper coefficient bounds when transporting `|b_i|` caps through square terms. In the intended composition these are supplied by `scaled_symmetric_det_lower_of_interval`.

It does **not** certify source Jacobian identity, signed interval exporter correctness, actual `b/g` enclosures, Float64/libm/FD/controller/solve semantics, same-P8 trajectory/domain coverage, provenance/admission, registry mutation, or final P5/P8/M4 integration.

Run in the pinned repository Lake environment:

```bash
CI_PORTABLE=1 bash examples/routeb_p5_correlated_interval_gate_lean/verify.sh
```

Status after a green focused compile remains `compiled_candidate`: **待封不觉独立验证 / 待梁智炜（Codex）收割与最终整合**。
