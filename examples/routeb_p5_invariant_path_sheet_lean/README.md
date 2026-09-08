# T-P5-096 invariant path-sheet coverage Lean sidecar

Agent/source_agent: **巨阳仙尊**.

This sidecar formalizes the smallest kernel-facing leaves extracted from 古月方源's `T-P5-096-INVARIANT-PATH-SHEET-COVERAGE` review.

## Trusted-core statements

`P5InvariantPathSheetCoverage.lean` proves:

- exact affine re-centering and coordinatewise convexity of an axis-aligned inner box;
- the Route-A exact margin consumer: `|x0-c|<=r`, `|xt-x0|<=t*B`, `t<=h`, `B>=0`, `r+h*B<=H` imply `|xt-c|<=H`;
- the corresponding pointwise typed-box consumer;
- square-only/radical-free speed-cap production from `v^2<=S<=B^2`, `B>=0`;
- the logically tiny full-sheet lifting theorem from pointwise forward invariance;
- the Route-B division-free differential algebra `E<=nu^2 Rin` plus `nu*dU<=-nu^2 U+E` implies `nu*dU<=-nu^2(U-Rin)`;
- the strict inner/outer collar and shifted-sublevel equivalence;
- exact algebraic regressions showing endpoint trajectories do not certify the whole flowed sheet and zero tangent energy does not certify a base-state tube.

## Deliberately not formalized here

The sidecar does **not** claim the analytic scalar integration theorem, first-exit/bootstrap continuation, integrating-factor/Gronwall invariance, existence/uniqueness of the deployed flow, actual source-tube binding, evaluator/controller/Float64/FD semantics, P8 coverage, registry admission, or final P5/M4 closure. In particular, the Route-A displacement premise must still come from a separate calculus/ODE theorem, and Route-B still needs the analytic comparison leaf plus a separately typed **base-state** storage source.

The semantic distinction between `U_base(t,x)` and a variational/tangent energy is intentional and regression-tested.

## Portable verification

Run from any environment in which `lake` and `lean` are on `PATH`:

```bash
CI_PORTABLE=1 examples/routeb_p5_invariant_path_sheet_lean/verify.sh
```

The verifier uses the repository `examples/local_fkg/lake-manifest.json` and checks that its `lean-toolchain` agrees with this sidecar's pinned `leanprover/lean4:v4.32.0`. It compiles with `-DwarningAsError=true`, scans for `sorry`/`admit`, requires every public theorem to emit a `#print axioms` report, and fails on `sorryAx`.

Status after a green focused compile is only `compiled_candidate`: **待封不觉独立验证 / 待梁智炜（Codex）收割与最终整合**。
