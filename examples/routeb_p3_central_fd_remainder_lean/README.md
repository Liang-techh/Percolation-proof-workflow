# Route-B P3 centered finite-difference remainder Lean sidecar

Agent: 苏梦辰

Upstream mathematics:
`agent_review_inbox/review-GH-MATH-P3-FD-REMAINDER-honglianmozun-20260908T1507Z.md`

This sidecar formalizes the first checker-facing layer of the centered finite-difference remainder package. It intentionally stops before the analytic/source bridge.

## Kernel statements

`TaylorPair` records two exact symmetric Taylor expansions around the same center, one positive step, one nonnegative third-derivative envelope parameter `M`, and the two one-sided `M*h^3/6` remainder bounds. From only that packet, Lean proves:

- exact centered cancellation `rawDefect = rplus-rminus`;
- `|rawDefect| <= M*h^3/3` and the division-free `3*|rawDefect| <= M*h^3`;
- exact normalized-error identity and `|D_h-d| <= M*h^2/6`;
- interval arithmetic for full shifted-stencil containment;
- a uniform step-cap descendant `M*hmax^2/6`;
- the exact `x^3` sharpness regression and its division-free form;
- the scaled cubic family showing the center two-jet can stay fixed while centered-FD error scales like `A*h^2`;
- a minimal two-term linear residual-budget handoff, conditional on an already source-bound exact decomposition.

## Explicit OPEN interfaces

This sidecar does **not** prove `C^3` implies the `TaylorPair` fields. That analytic Taylor-remainder theorem is the next formal leaf and must quantify the complete shifted stencil. It also does not prove the deployed evaluator is the exact symmetric centered stencil, does not bind the residual coefficients/primitives to source, and says nothing about Float64/libm/rounding, true-DH execution, ODE/flowpipe coverage, registry admission, or the final Route-B conclusion.

The source-facing bridge should therefore expose a theorem of the form `C3OnShiftedStencil -> TaylorPair` (or an equivalent `f''` Lipschitz packet) rather than weakening the present algebraic theorem statements.

## Focused verification

Run from a checkout containing the repository-pinned `examples/local_fkg` Lake environment:

```bash
bash examples/routeb_p3_central_fd_remainder_lean/verify.sh
```

`verify.sh` discovers `lake`/`lean` from `PATH`, checks the sidecar toolchain against `examples/local_fkg/lean-toolchain`, requires the pinned `lake-manifest.json`, rejects `sorry`/`admit`, runs Lean with `-DwarningAsError=true`, checks every exported theorem has an axiom report, and rejects `sorryAx`.

A focused compile PASS is only `compiled_candidate` evidence: 待封不觉独立验证 / 待梁智炜最终整合。
