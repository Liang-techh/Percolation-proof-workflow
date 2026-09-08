# T-P5-050 singular PSD classifier Lean sidecar

Agent: 巨阳仙尊

This focused sidecar formalizes the source-independent algebraic core of 狂蛮魔尊's `T-P5-050` review for a singular positive-semidefinite symmetric `2x2` quadratic block.

It contains:

- the two adjugate/kernel identities;
- the exact incompatibility-norm identity;
- the pivot-free trace completion identity;
- the compatible nonzero-rank global completion bound;
- the adjugate defect kernel ray and its unboundedness obstruction;
- the `trace = 0` zero-matrix branch;
- a complete `iff` classifier for existence of a finite global upper bound under `p >= 0`, `s >= 0`, `det H = 0`.

The sidecar deliberately does **not** claim deployed P5 coefficient/source binding, Float64/controller semantics, P8 same-domain trajectory coverage, ODE continuation, P5/M4 closure, provenance/admission, or registry mutation. It also does not replace the positive-definite T-P5-044 lane.

Run from this directory or through the repository GitHub Actions sidecar runner:

```bash
CI_PORTABLE=1 ./verify.sh
```

`verify.sh` resolves `lake`/`lean` from `PATH`, reuses the repository-pinned `examples/local_fkg/lake-manifest.json`, enforces the matching Lean toolchain, compiles with `-DwarningAsError=true`, checks all public theorem axiom reports, and rejects `sorryAx`.

Status after a green focused run: `compiled_candidate` only — 待封不觉独立验证 / 待梁智炜（Codex）收割与最终整合。
