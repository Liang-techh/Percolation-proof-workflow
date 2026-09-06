# DH force mismatch → mechanical power → conditional finite-time budget

This is a mathematical proof-composition checkpoint. It does not certify the
entire robot, and no theorem here has been admitted through the final statement
comparator. The original target and its historical reports are unchanged.

## What is made explicit

`DHPowerBinding.lean` defines the real residual of the actual returned
acceleration, rather than assuming that a floating solve is exact:

    rsolve = Mi*a - (tauI - cI - gI)
    e = (Ma-Mi)*a + (tauI-tauA) + (cA-cI) + (gA-gI) + rsolve.

It proves the resulting force identity, reuses the existing controller-power
cancellation, and derives

    dE <= (631227/1086800)*w^2 + sum_i eps_i^2/(2*D_i)

from explicit mechanical derivative and component enclosure hypotheses.
The final rounded RHS assembly error is included in rsolve as defined above;
if a backend instead defines its residual relative to the actual rounded RHS,
that backend must add the RHS assembly discrepancy too. Do not omit or count it
twice. All vectors and matrices here are interpreted real values, not a formal
semantics of Julia or IEEE arithmetic.

## Reused and newly closed mathematical premises

- `ControllerPowerCore.lean` contains the unchanged declaration
  `RobotFormalEnergy.closed_loop_power_identity` extracted from the target.
  The frozen full source is `ExistingEnergyCore.lean`, SHA-256
  `56341d50f43e9fdca79ab3a947712ce63bdb7f61be2261a769e7030e3bc5da96`.
  Its unrelated later calculus declarations fail under the current pin; the
  full source was **not** repaired or declared compiled. The failure is retained
  in `output/run-uaJqj9FL/`. The extracted declaration and new power bridge
  compile in `output/run-5RHBCcg9/`.
- The independent `routeb_christoffel_power/ChristoffelPower.lean` proves the
  Christoffel/metric-rate power cancellation for any finite real tensor, without
  a tensor symmetry hypothesis. `MechanicalAssembly.lean` composes it with the
  new force-error bound, removing the formerly supplied hC equality. Actual
  derivative identification and the kinetic/potential chain rules remain.
- `FDForceBudget.lean` independently proves the exact rational polynomial
  identity for the six component envelopes obtained by the coefficient audit,
  and its upper bound `(3103*cap^2+152*cap+4)/10^21` for cap>=0. The premise
  that the FD errors obey these component envelopes is explicit, not an axiom.
- It also composes FD and runtime errors while preserving cross terms:
  the budget is `sum (epsFD_i+epsRuntime_i)^2/(2D_i)`, not the sum of their
  separately squared budgets.
- `EnergyTube.lean` proves a one-sided derivative comparison and the resulting
  T=1 terminal energy budget for the source's ramp input `w(t)=c*t`, c^2<=3.
  This is an energy bound, not terminal block-set inclusion. It does not replace
  a broader disturbance class if the final target requires one.

## Remaining mathematical obligations

1. Prove that the actual DH derivatives instantiate the tensor, mass, potential
   and controller objects in these declarations.
2. Admit the Fourier coefficients and their centered-difference remainder
   bounds into Lean, not merely their final rational arithmetic.
3. Replace the invalid unshifted-storage lower-bound premise. The exact Fourier
   storage is negative arbitrarily close to the origin along joint 2 (see
   below). Prove an adequate shifted or direct block comparison and an
   all-six-velocity cap. A p45 bound controls only v4 and v5.
4. Enclose the Float64 parameter, trig/FK, FD evaluation, mass, RHS assembly and
   solve errors. Their contribution is not included in the tiny exact-real FD
   truncation budget.
5. Close original initial-set, domain first-exit/continuation, storage-to-block
   and terminal-set comparisons. The independent P8 probe still uses a different
   tiny horizon/domain and a constant disturbance state.

## Storage obstruction changes the proof frontier

The independent exact coefficient audit gives

    W(0,t,0,0,0,0) = (2029689/400000)*(cos(t)-1) + (2/5)*t^2.

`StorageObstruction.lean` proves this scalar expression is at most
`-(749689/3200000)*t^2` for `|t|<=1`, hence negative when `t!=0`. It also
transfers the obstruction to a general W **given the explicit slice identity**.
The proof compiles in `output/tube-RWfVZNvn/`; no new axiom or `sorry` is used.
`../routeb_potential_slice/PotentialSlice.lean` now closes the coefficient-to-slice
seam for the full encoded 17-row potential; `output/run-SuGxG04V/` there records
the successful compilation and exact source-field/Kp audit. Physical-DH
identification remains a separate seam.

Thus the shortcut `E >= 9401/2000000 * sum(v_i^2)` is false for this unshifted
energy: set v=0 at a negative configuration. This does **not** refute the
original tube/terminal theorem. The previous FD budget remains correct under
its explicitly stated cap premise; that premise must now be established with
a different comparison.

An algebraically valid coarse shift is `B=4079979/400000`. The exact coefficient
composition is now proved in `../routeb_shifted_storage/ActualShift.lean`:
`W+B >= sum(q_i^2)/5`, without extra assumptions on the encoded W. Constant
row 8 is removed before summing positive coefficients because it cancels from
U-U0. Compilation succeeded in `output/actual-GqBg6J4g/` there; the preceding
finite-index reduction failure is retained. It shifts initial budgets too.
The resulting global block comparison is too loose to establish eta=5.6 by
itself. `ShiftBudgetObstruction.lean` strengthens this: any C making the same
W+C globally nonnegative must have `C>=749689/3200000` by the t=1 slice. For
any nonnegative unshifted energy cap, the coarse budget
`(1600000/9401)*(Ecap+C)` is then strictly greater than `28/5`. This compiles
in `output/tube-DRiLEgLi/`. Merely optimizing C cannot rescue this comparison
factor; a sharper/different block comparison is required. This does not rule
out other comparisons or the original dynamics theorem.
Neither shrinking the goal to a coordinate slice nor changing Kp is
part of this work. The v2 proposed DAG records this obstruction and separates
conditional domain estimates from their first-exit closure.

## Verification scope

Use the existing WSL Lean 4.33.1 / Mathlib
`0df444a360eaa60ab8c11dca51a86af692955474` cache:

    bash examples/routeb_dh_power_binding/verify.sh
    bash examples/routeb_dh_power_binding/verify_tube.sh

The second command reuses the explicitly named previously compiled power and
Christoffel objects. Their hashes are logged. The original failed full-file
compile and derivative/linter repair logs are retained. No regression campaign,
remote CI, dependency download or comparator tool rebuild was performed.
