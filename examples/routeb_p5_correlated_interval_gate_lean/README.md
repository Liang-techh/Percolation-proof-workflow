# T-P5-045 signed-sum interval transport companion — Lean sidecar

Formalization agent: **巨阳仙尊**.

Mathematical intake: `agent_review_inbox/review-T-P5-045-liuguanyi-20260907T2108.md`.

During this round, 苏梦辰 concurrently submitted the main T-P5-045 formalization at `examples/routeb_p5_robust_correlated_interval_lean/`. To avoid duplicate ownership, this sidecar is deliberately narrowed to one complementary interface seam that the main sidecar does not directly encode:

- from signed entry intervals for `k45` and `k54`, plus endpoint sum caps, prove the pointwise interval for `sigma = k45+k54`;
- derive exactly the `|sigma| <= Q` premise consumed by the robust correlated determinant/bias theorem;
- freeze the skew-family cancellation `M+(-M)=0` before absolute scalarization.

No determinant, bias, quarter-barrier, parameter gate, source Jacobian, Float64, P8 coverage, provenance/admission, registry, or final integration claim is duplicated here.

Run in the pinned repository Lake environment:

```bash
CI_PORTABLE=1 bash examples/routeb_p5_correlated_interval_gate_lean/verify.sh
```

A green compile remains a `compiled_candidate`: **待封不觉独立验证 / 待梁智炜（Codex）收割与最终整合**。
