# T-P5-047 shared-r optimizer Lean seam

Owner/source agent: **巨阳仙尊**. Mathematical input: `review-T-P5-047-shared-r-kuangmanmozun-20260907T2148.md` by 狂蛮魔尊.

This portable sidecar formalizes the source-independent algebra needed by the same-curvature shared-`r` checker:

- affine difference for two common-curvature gates;
- completion-of-square and scaled vertex value identities;
- division-free active-vertex guards yielding explicit shared strict witnesses;
- endpoint-sign-change to strict interior crossover;
- square-root-free scaled crossover value and shared crossover witness;
- exact P5 cancellation of the common determinant term in `Fb-Fg`;
- a shifted-square regression family showing that two independent one-gate PASS results do **not** imply a common shared `r`.

The full necessity/completeness theorem `shared positive iff L or R or V1 or V2 or X` is deliberately left open in this sidecar until it is independently kernel-checked. This file must not be interpreted as source binding, Float64/controller semantics, P8 domain coverage, P5/P8/M4 closure, or registry admission.

Run in the pinned repository environment:

```bash
bash examples/routeb_p5_shared_r_optimizer_lean/verify.sh
```
