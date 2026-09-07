# T-P5-023 piecewise path transport Lean sidecar

This sidecar formalizes the finite algebraic layer of `review-T-P5-023-liuguanyi-20260907T0916.md`.

It proves: (1) a scalar finite telescoping identity; (2) the triangle bound for a force map applied to a sum of certified residual increments; (3) composition of per-segment state-coordinate and residual-increment bounds into a single path coefficient `pathK`; (4) the Frobenius-style squared centered-gain bound consumed by P5; and (5) a minimal counterexample theorem showing that an unbridged endpoint jump is unconstrained by zero local budgets.

The sidecar intentionally starts after the source checker has certified a connecting chain. It does not prove that a Julia/Float64 Jacobian interval is correct, that any concrete P8 boxes form such a chain, that the ODE stays in those cells, or that P5/P8/M4 is closed. Raw-PMI to generalized-force normalization, when needed, is represented by the single force map `A` in `piecewise_force_centered_gain`; callers must not normalize the same residual a second time.

Run with a PATH containing the repository-pinned Lean/Lake environment:

```bash
./verify.sh
```

`verify.sh` is marked `CI_PORTABLE=1` and is discovered by `.github/workflows/lean-agent-sidecars.yml`. It compares this sidecar's `lean-toolchain` with `examples/local_fkg/lean-toolchain`, invokes `lake env lean -DwarningAsError=true`, requires an axiom report for every exported theorem, and rejects `sorryAx`.

Status after authoring: candidate only. A successful focused compile is still **待封不觉独立验证 / 待梁智炜最终整合**.
