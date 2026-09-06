# Real compilation evidence

Final status: **PASS**, 2026-09-05T18:21:53Z.

- [Current Lean source](LocalEnergyBudget.lean)
- [Successful compiler log](output/run-37fVwazf/compile.log)
- [Successful full verification log](output/run-37fVwazf/verify.log)
- [Exact compiled source snapshot](output/run-37fVwazf/LocalEnergyBudget.lean)
- [Compiled artifact](output/run-37fVwazf/LocalEnergyBudget.olean)
- [Direct cached verifier](verify.sh)

The successful log records `LEAN_COMPILE_EXIT_CODE=0` and `VERIFY_EXIT_CODE=0`.
All 13 printed theorem dependency reports contain only `propext`,
`Classical.choice`, and `Quot.sound`; none contains `sorryAx` or a model axiom.

Environment:

```text
Lean 4.33.1 (819816b2e0a3bf405af45ae5c7af2491d8f5bee6)
Mathlib 0df444a360eaa60ab8c11dca51a86af692955474
/home/z5242/.elan/toolchains/leanprover--lean4---v4.33.1/bin/lean
Cached package libraries under /home/z5242/sos_lean
-DwarningAsError=true
```

Final SHA-256 values:

```text
LocalEnergyBudget.lean
6ed571661f816473120b69e1550627cf5f16ae0ef68df6ffd22dd77f00dac23f
verify.sh
cbd98a957c7b9f7284e731b6053d3e0664b3733378f80b3ee3202d05113261cc
LocalEnergyBudget.olean
058fe6692deca45f4c66142cc63898c98b5d0bbe402dbedbf86885f85fdefe91
```

## Failed attempts retained without alteration

| Run | Exit | Compiler finding | Logs |
| --- | --- | --- | --- |
| `run-ChNcsQ7L` | 1 | The four-index finite sum did not simplify to the block expression before arithmetic. | [compile](output/run-ChNcsQ7L/compile.log), [verify](output/run-ChNcsQ7L/verify.log) |
| `run-R2XPgS0V` | 1 | Adding membership simplifications still left that sum unexpanded. | [compile](output/run-R2XPgS0V/compile.log), [verify](output/run-R2XPgS0V/verify.log) |
| `run-2EZ4eqRJ` | 1 | Full-sum expansion left nested `Fin.succ` indices syntactically different from numeral indices. | [compile](output/run-2EZ4eqRJ/compile.log), [verify](output/run-2EZ4eqRJ/verify.log) |

The final proof uses the four-index subset and `norm_num [Fin.ext_iff] at hs`,
as suggested by the main task, to normalize the numeric-index disequalities.
The full12-ball premise and all theorem statements are preserved. The prior
successful full-sum proof remains recorded in
[run-pbaO1lFk](output/run-pbaO1lFk/verify.log).
The derivative,
half-damping, storage comparisons, cap arithmetic, and conditional ledger proofs
already elaborated in the first run. Failed runs contain error-recovery
`sorryAx` reports for the failed projection and its dependent initial-bound
theorem; they are not accepted proof artifacts.

No broad test suite, solver, Julia model, optional EnergyTube dependency, or Lake
build was run. The new source and its verifier are the only compiled leaf inputs.

## What remains conditional

To apply the result to the model, identify the supplied derivative expression
and dynamics with the actual trajectory, and prove the integrated energy ledger.
In particular, prove the intended uniform bound

```text
integral_0^t [(5/8)*e4(s)^2 + (10/13)*e5(s)^2] ds <= 1/10,
for the relevant trajectories and 0 <= t <= 1.
```

Here `e` is the TOTAL reference-block force mismatch, including mass error,
remote acceleration coupling, gravity, and FD/Float64 effects. This residual
bound is an explicit next obligation, not a conclusion of this leaf. The
input-energy bound and requisite regularity/domain premises also remain external.
