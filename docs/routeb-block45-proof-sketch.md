# Route-B block-(4,5): proposed proof decomposition

Status: research proposal, not a checked Lean reduction. The P0–P9 stage order
is an operational plan, not a theorem-dependency proof. None of the edges below
can discharge a parent until its formal statement and reduction are checked.

## Fixed objective and scope gaps

The target remains the original block-(4,5) finite-time tube and terminal
containment under the implemented true-DH dynamics. The delivery manifest
records horizon `T=1`, initial radius `0.15`, `eta=5.6`, and joint block `4,5`.
These numbers do not by themselves define X0, W, the six-state domain, or the
disturbance regularity. Extract their exact definitions before formalizing M4.
In particular, do not infer a time-varying disturbance theorem from an ODE
adapter that treats w as a constant thirteenth state.

The successful P8 local probe requests only T=0.001, with state and disturbance
radii 0.001. It reports 35 reachsets and explicitly retains coverage=false.
It is not the requested T=1, radius=0.15 certificate.

## Analytic power route, with all seams explicit

1. Bind the DH kinematics and controller to an exact-real model. Keep the
   decimal-rational analytic model distinct from Float64 parameters, central
   finite differences (h=1e-5), regularization (mu=1e-6), and the linear solve.
2. Prove the Newton–Euler lift equations and the energy derivative identity.
   The Julia zero-polynomial audit is evidence to translate, not an assumed
   physical power identity. The current constant-multiplier cancellation alone
   does not prove that the lift variables describe the executed dynamics.
3. Reuse the isolated exact six-dimensional supply theorem:
   `gamma*w^2 - P(v,w) = sum_i D_i*(v_i-c_i*w)^2`,
   gamma=631227/2173600, with its explicit rational D and G definitions.
   This theorem has no q-domain restriction and no physical dynamics premise.
4. On a candidate domain, enclose every component of the real force mismatch
   e, including the actual returned acceleration's solve residual. The compiled
   quadratic theorem gives `P(v,w)+dot(e,v) <= (631227/1086800)*w^2 +
   sum(e_i^2/(2D_i))`. Combine FD and runtime envelopes before squaring; retain
   cross terms. Domain closure is a later first-exit obligation, not assumed.
5. With a proved derivative identity, integrate this error-inclusive budget.
   Establish ODE/chain-rule and integration hypotheses separately. If a proof
   needs the stronger `dE<=w^2`, it must separately absorb the actual signed
   remainder into `(1-gamma)*w^2+completion(v,w)`. A positive absolute-error
   bound cannot satisfy a zero-input zero-budget shortcut merely by being small.
6. Prove the actual X0 energy budget and the storage-to-block comparison.
   An energy derivative upper bound alone is not positive definiteness or
   domination of the requested block tube.
7. Close domain containment and solution continuation together using a valid
   barrier/first-exit argument. Do not assume the trajectory remains in D in
   order to prove the premise needed for remaining in D.
8. Derive terminal transfer from the same storage, disturbance budget, horizon,
   and block comparison. Check the target statement independently.
9. Produce an independent flowpipe for the same model, X0, W and horizon.
   Retain it as separate cross-validation rather than kernel theorem evidence.

The fallback is the original partitioned Schur/PMI route if storage comparison
or remainder absorption is not feasible; no automatic switch to a different
mathematical objective is authorized by this sketch. P7 remains conditional.

## Reusable local sources to inspect before duplicating a lemma

Target `robot_formal_v1/energy_invariant_formal_core.lean` already contains
generic diagonal Young, descriptor power/remainder, chain-rule, energy tube,
barrier, and terminal arithmetic lemmas. Their names alone do not establish
applicability. Each reused declaration needs exact type, dependency audit,
pinned compilation and the appropriate source/target comparison.

The new `examples/routeb_supply_core/RouteBSupplyCore.lean` specializes the
quadratic core and proves attainment and coefficient minimality. Its sharpness
is over all real (v,w), not over dynamically attainable DH trajectories.

## Next useful leaves

- Resolve the storage-to-block bottleneck described below and the exact original
  target-domain/disturbance definitions.
- Bind the now compiled mechanical-power and error-budget lemmas to actual DH
  derivatives and the implementation's force residuals.
- Establish all-coordinate domain coverage by first exit, not by assuming a
  velocity cap obtained from the requested block bound.
- Keep final statement comparison and P0 provenance open; defer broad regression
  and exporter rebuilds while the mathematical frontier is unresolved.

## Mathematical checkpoint: unshifted storage obstruction

The v2 proposed graph supersedes the initial operational decomposition. Exact
Fourier coefficients and actual Kp yield
`W(t e2)=(2029689/400000)*(cos t-1)+(2/5)*t^2`. A compiled Lean scalar proof
shows this is negative for every `0<|t|<=1`. The exact coefficient audit also
gives the actual Hessian entry `d22 W(0)=-1709689/400000`; full source-to-DH
formal identification remains open.

Therefore unshifted E cannot dominate the all-six kinetic lower bound, even
locally around the origin. The provisional FD cap premise cannot be obtained
from that E, and a block-(4,5) bound never bounds the four other velocities.
This is a refuted proof shortcut, not a refuted original theorem.

The force-error composition, Christoffel cancellation, mechanical assembly,
exact rational FD-budget arithmetic, and a conditional T=1 ramp energy tube
now have compiled Lean sources. They retain physical derivative, component
enclosure, initial-set and disturbance assumptions. Runtime errors are separate
from exact-real centered-difference truncation errors; their cross terms remain
in the final square budget.

A shift `B=4079979/400000` yields the coarse comparison
`W+B>=sum(q_i^2)/5` by exact coefficient arithmetic. This also shifts the
initial budget and does not by itself meet eta=5.6. Prioritize a sharper
block comparison or the original partitioned Schur/PMI route with the same
controller and full domain. Preserve the negative result in persistent state
so a later agent does not retry the invalid nonnegativity shortcut.

Subsequent compiled leaves refine this checkpoint without rewriting the saved
v2 DAG receipt: `PotentialSlice.lean` proves the full encoded coefficient-to-slice
identity, and `ActualShift.lean` proves the exact global shifted bound with
constant row 8 canceled. `ShiftBudgetObstruction.lean` proves that **optimizing
the scalar shift alone cannot fix the same coarse block factor**. Any globally
nonnegative W+C has `C>=749689/3200000`; with Ecap>=0,
`(1600000/9401)*(Ecap+C) >= 749689/18802 > 28/5`. Do not spend further search
budget tuning C while retaining this comparison coefficient. Prioritize a
different, tighter block storage comparison or the original port/Schur route.

Full M4 remains open. `formal_certificate_allowed` remains false.
