# Verification report

## Scope

This leaf proves only exact algebra over `ℝ`.  The central identity expands

```text
p4(v6) - (50000/50003) cos(y) p6(v6)
 = r4 - (50000/50003) cos(y) r6
   + (m46 - (50000/50003) cos(y) m66) v6.
```

Consequently, the `v6` coefficient vanishes under the displayed coefficient
equation.  The concrete pair `(m46,m66)=(50000*cos(y),50003)` is checked by
exact field arithmetic.

`q6Drive` and `fdDefect` are fields of `OpenInputs`, and
`routeB_residual_retains_open_inputs` proves that the residual minus the
quasi-momentum core is exactly their sum.  They are intentionally open inputs:
no numerical value, sign, bound, finite-difference consistency, source
binding, ODE/PDE semantics, or trajectory property is admitted here.

## Verification boundary

This module does not prove that any physical Route-B system has the affine
profiles used by the interface, does not prove the coefficient equation from
DH/Fourier data, and does not prove cancellation along a real trajectory.  In
particular, it does not establish a Lyapunov inequality, a flowpipe, a defect
budget, or `J <= 1`.

## Focused command

`verify.sh` compiles only `QuasimomentumCancellation.lean` using cached
dependencies and `-DwarningAsError=true`.  It checks Lean 4.33.1 and the exact
cached Mathlib commit, snapshots the local leaf inputs, retains the terminal
log and hashes under `output/run-*`, and checks the printed axiom report for
`sorryAx`.  No full-workspace test suite is run.

## Result

Focused verification succeeded on 2026-09-07T00:07:52Z--00:07:56Z UTC:

- Lean 4.33.1, executable commit `819816b2e0a3bf405af45ae5c7af2491d8f5bee6`;
- cached Mathlib commit `0df444a360eaa60ab8c11dca51a86af692955474`;
- verifier exit code `0` in `output/run-IYRTNFPt`;
- `QuasimomentumCancellation.lean` SHA-256:
  `522d46d111c0fba6f7fe332e6bb44c95ba2853af90fb9b28e14102b678ddfaf2`;
- `QuasimomentumCancellation.olean` SHA-256:
  `29d7e25923982f7f32dda734666adc2bd72801fce37525c91e5c8006d64a4eb7`.

The printed theorem axiom reports contain only `propext`, `Classical.choice`,
and `Quot.sound`; no `sorryAx` was reported.  The focused command compiled
only this module.  The earlier diagnostic attempt `output/run-q7FfrkAj` is
retained, but its verifier checks were later hardened because that environment
did not provide `rg`; it is not the final receipt.
