# T-P5-115 root-free second-jet Lean sidecar

This sidecar formalizes the kernel-facing part of `T-P5-115-ROOT-FREE-SECOND-JET-INDEPENDENT-ENERGY` from 狂蛮魔尊.  It is intentionally source-independent: it does **not** prove that the deployed P5 producer supplies `r,m,c`, the physical quadratic metric, same-segment coverage, or the numerical caps.

## Trusted interface

`P5RootFreeSecondJet.lean` defines a minimal `PSDQuadraticKernel` carrying only:

- nonnegativity of `Q`;
- the PSD cross-square inequality `B(x,y)^2 <= Q(x)Q(y)`;
- exact add/sub quadratic expansions.

From that interface it proves:

- cap-level cross-square transport;
- guarded, square-root-free two-channel discriminant envelopes for both `x+y` and `x-y`;
- the nested `J2 = r-m-c` independent-energy certificate using the four scalar gates from T-P5-115;
- the homogeneous common-scale specialization;
- endpoint and rational regressions;
- fail-closed counterexamples showing that the nonnegative branch guard and cross allowance cannot be dropped.

The sharp square-root infimum and weighted three-block identity remain mathematical review facts; they are not needed by the trusted checker and are deliberately omitted here.

## Portable verification

Run from any checkout whose `examples/local_fkg/` environment contains the pinned `lake-manifest.json` and matching Lean toolchain:

```bash
CI_PORTABLE=1 bash examples/routeb_p5_root_free_second_jet_lean/verify.sh
```

`verify.sh` finds `lake` and `lean` from `PATH`, checks the pinned toolchain, rejects `sorry`/`admit`, compiles with `-DwarningAsError=true`, and requires an axiom report for every public theorem.

## Explicitly open

- actual `D2M/D2R/J2` source extraction;
- actual P5 metric/source identity and same-segment coverage;
- numerical `U_r,U_m,U_c` or homogeneous coefficient production;
- T-P5-112/T-P5-113 downstream source/power binding;
- Float64/FD/controller equivalence and P8 flowpipe coverage;
- independent validation, admission, registry, and final P5/M4 closure.

Status after a successful focused compile remains `compiled_candidate`: 待封不觉独立验证 / 待梁智炜（Codex）收割与最终整合。
