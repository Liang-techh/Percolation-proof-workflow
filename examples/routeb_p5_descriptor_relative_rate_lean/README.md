# T-P5-085 descriptor-relative Lyapunov rate sidecar

This portable Lean sidecar formalizes the source-independent theorem decomposition from 红莲魔尊's `T-P5-085-DESCRIPTOR-RELATIVE-RATE` review.

It proves only the algebraic/ordered-field layer:

- descriptor/full-state squared estimate + same-cell relative-plus-additive RHS packet -> squared port packet;
- division-free relative/additive power absorption via a positive `d * mu^2` cancellation;
- Lyapunov rate/bias ledger consumption;
- homogeneous pure-relative corollary and first-exit inward condition;
- exact zero-storage obstruction for the pure-relative branch;
- the factor-4 equality regression;
- the upstream exact `1402217/12000000` producer-metric constant remains nonnegative.

The theorem statements intentionally do **not** assert any deployed `Hrel/Habs`, descriptor source equality, true-DH cell coverage, Float64/libm/FD/controller/solve semantics, trajectory continuation, P8 flowpipe coverage, or registry/admission result. Those remain external typed premises.

## Focused verification

Run from a checkout containing the repository-local `examples/local_fkg` environment:

```bash
CI_PORTABLE=1 examples/routeb_p5_descriptor_relative_rate_lean/verify.sh
```

`verify.sh` resolves `lake` and `lean` from `PATH`, checks the pinned Lean toolchain against `examples/local_fkg/lean-toolchain`, uses the repository-pinned `lake-manifest.json`, rejects `sorry`/`admit`, compiles with `-DwarningAsError=true`, and requires an axiom report for every exported theorem.

Admission boundary: a focused compile is at most `compiled_candidate`; final independent validation belongs to 封不觉 and final integration belongs to 梁智炜.
