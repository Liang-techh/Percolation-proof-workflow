# Route-B P4 strict common-lambda boundary Lean sidecar

This portable sidecar formalizes the checker-facing algebraic core of
`T-P4-041-STRICT-COMMON-LAMBDA-BOUNDARY` from 狂蛮魔尊's review.

It proves:

- square-root-free weak, strict, and exact-boundary pair predicates;
- under `U,V >= 0`, `weak PASS ∧ strict FAIL` iff the exact polynomial boundary holds;
- the rational touching pair `(C,U,V)=(4,1,1)` is weak-but-not-strict;
- the two Young rows `t^2-3t+2` and `t^2-5t+6` have the unique common weak witness `t=2`, where both saturate and no positive common reserve exists;
- the exact perturbation identity
  `4UV-(C-U-V)^2 = 32 e (1-e)`;
- `0<e<1` is strict, `e=0` is boundary-only, and `e<0` fails even the weak gate;
- the exact `e=1/10, t=39/20` reserve witness from the mathematical review.

The sidecar deliberately does **not** claim the finite-family open-interval Helly theorem, a concrete P4 cell/source coefficient binding, Float64 realization, P8 domain/trajectory coverage, P4/M4 closure, or registry admission. Those remain separate obligations.

## Portable verification

The sidecar is pinned to the repository's Lean 4.32.0 environment and reuses the pinned `examples/local_fkg` Lake project. `verify.sh` discovers `lake` and `lean` from `PATH`, performs a placeholder scan, compiles with warnings as errors, and checks every public theorem's `#print axioms` output for `sorryAx`.

```bash
CI_PORTABLE=1 bash examples/routeb_p4_strict_lambda_boundary_lean/verify.sh
```

A successful focused compile is only `compiled_candidate` evidence. It remains **待封不觉独立验证 / 待梁智炜（Codex）收割与最终整合**.
