# Route-B P5 weighted-dual adapter Lean sidecar

This sidecar formalizes the source-independent diagonal adapter from
`agent_review_inbox/review-T-P5-014-liuguanyi-20260907T0417.md`.

It proves that componentwise generalized-force intervals yield the exact
weighted-dual cap `sum r_i^2/d_i`, keeps diagonal implementation normalization
factors explicit, converts local square-relative budgets to a global weighted
budget, and records scalar counterexamples showing why fixed nonzero bias or an
undamped direction cannot be silently treated as homogeneous damping.

The actual weighted power consumer remains a separate theorem package under
`examples/routeb_p5_weighted_dual_residual_lean/`. This sidecar does **not**
authenticate Julia/DH/Float64 execution, generate interval bounds, establish P8
coverage, or close P5/M4.

Run with the repository's pinned local-FKG Lake environment:

```bash
CI_PORTABLE=1 ./verify.sh
```

Expected formal status after a successful focused run: `compiled_candidate`,
待封不觉独立验证 / 待梁智炜（Codex）收割与最终整合。
