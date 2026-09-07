---
kind: review_result
review_id: review-T-P5-013-honglianmozun-20260907T0358
task_id: T-P5-013
source_agent: 红莲魔尊
claimed_at: 2026-09-07T03:51:00-06:00
created_at: 2026-09-07T03:58:00-06:00
inspected_commit: 0a4882c859691c200c3e71b670476efd457283e9
integration_status: pending
admission_label: pending
proposed_integration_target: theorem
requested_action: formalize_pointwise_mixed_energy_budget_then_first_exit_barrier_and_bind_source_ramp_work_weighted_dual_remainder
---

# T-P5-013 — finite-horizon Lyapunov barrier with ramp work and genuine nonconservative remainder

## Scope

This child combines two already-derived P5 structures without changing either one:

- `T-P5-011`: inside an energy sublevel, the central-FD cubic power can be absorbed by a chosen damping margin using the square-only condition `Lambda*K*Z <= g_C^2`;
- `T-P5-012`: parameter-dependent conservative extraction leaves the exact ramp-work term `-c * partial_w Phi`, while a genuinely nonconservative force remainder must be charged through a dual dissipation norm rather than falsely declared conservative.

The missing mathematics is a **finite-horizon self-bootstrap**: additive ramp work and nonconservative work may prevent monotone Lyapunov decay, but they can still be admitted if their accumulated energy cost cannot reach the cubic barrier before the target time.

I also inspected `T-P8-011`. Its ramp-graph/domain result is kept strictly separate: the energy theorem below does not repair the currently documented narrow `w` source box and does not claim P8 coverage.

No source/IEEE numerical bound, ODE/source semantic equality, flowpipe certificate, provenance, admission, P5/M4 closure, or registry update is claimed.

## 1. Energy ledger after conservative extraction

Let

```text
A(t) >= 0
```

be the dissipation quadratic form. Let `Z(t) >= 0` be the shifted modified storage from `T-P5-011/012`, so the central-FD cubic power `P_C` satisfies on the relevant domain

```text
P_C(t)^2 <= Lambda * A(t)^3,
A(t) <= K * Z(t).                                           (1)
```

Let `g0 > 0` denote the damping margin **after** any already-certified relative residuals have been deducted. Split it as

```text
g0 = g_C + g_R,
g_C >= 0,
g_R > 0.                                                   (2)
```

Here `g_C` is reserved for the cubic term and `g_R` for a genuine nonconservative force remainder `r(t)`.

After the parameter-dependent conservative part has been moved into storage, the pointwise ledger has the form

```text
Zdot <= -g0*A + P_C + <r,v> + h_ramp,                       (3)
```

where

```text
h_ramp = -c * partial_w Phi(q,w).                            (4)
```

A one-sided bound `h_ramp <= Hbar` is enough; the stronger source contract `|h_ramp| <= Hbar` is sufficient but not necessary.

## 2. Sharp nonconservative charging

Assume the dissipation matrix `D` is positive definite and

```text
A = v^T D v,
R = r^T D^{-1} r.                                           (5)
```

For every `g_R>0`, exact completion of the square gives

```text
-g_R*A + r^T v
 = -g_R * ||D^(1/2)v - (1/(2g_R))D^(-1/2)r||^2
   + R/(4g_R).                                              (6)
```

Therefore, if

```text
R(t) <= Rbar,                                               (7)
```

then

```text
-g_R*A + r^T v <= Rbar/(4g_R).                              (8)
```

The coefficient `1/(4g_R)` is sharp under only (5)-(7): equality is attained at `v=(1/(2g_R))D^{-1}r` when the bound in (7) is saturated.

For a division-free consumer, introduce an explicit nonnegative energy-rate budget `B_R` and require

```text
Rbar <= 4*g_R*B_R.                                         (9)
```

Then simply

```text
-g_R*A + r^T v <= B_R.                                     (10)
```

This is the preferred formal interface because a source/checker can return an exact rational `Rbar` and the theorem need not divide inside the main ledger.

## 3. Cubic absorption on a candidate energy barrier

Choose a barrier `Zstar>=0` satisfying

```text
Lambda*K*Zstar <= g_C^2.                                   (11)
```

Whenever

```text
0 <= Z(t) <= Zstar,                                        (12)
```

(1) and (11) imply the existing `T-P5-011` square-only absorption

```text
|P_C(t)| <= g_C*A(t).                                      (13)
```

Substituting (13) into (3) and using (2),

```text
Zdot <= -g_R*A + r^T v + h_ramp.                           (14)
```

Hence from (9)-(10) and `h_ramp<=Hbar`,

```text
Zdot <= B_R + Hbar =: B.                                   (15)
```

This is the key point: additive execution/ramp effects no longer need to be incorrectly forced into a velocity-relative bound. They are allowed to spend a finite amount of the energy-barrier headroom.

## 4. Finite-horizon first-exit closure

Assume `Z` is continuous on `[0,T]`, differentiable on `(0,T)` (or absolutely continuous with the derivative inequality almost everywhere), and that the pointwise ledger above is valid whenever `Z<=Zstar` and the trajectory stays in the typed source/domain contract.

Suppose

```text
T >= 0,
B >= 0,
Z(0) + T*B < Zstar.                                        (16)
```

Then

```text
Z(t) < Zstar for every 0 <= t <= T.                         (17)
```

### Proof

Assume a first exit exists and let `t*` be the first time with `Z(t*)=Zstar`. On `[0,t*)` one has `Z<Zstar`, so the cubic absorption and therefore (15) are valid. Integrating gives

```text
Z(t*) <= Z(0) + t*B <= Z(0) + T*B < Zstar,                 (18)
```

contradicting `Z(t*)=Zstar`. Thus the sublevel cannot be exited before `T`.

Consequently the cubic small-gain premise is self-maintained over the entire finite horizon even though `Z` need not be monotone.

A non-strict version with `Z(0)+T*B <= Zstar` gives a closed-sublevel bound if the derivative hypothesis is available on the closed sublevel, but the strict form (16) is the cleaner first-exit contract and avoids boundary tangency bookkeeping.

## 5. Combined source-facing theorem

The source-independent P5 consumer can therefore be summarized as follows.

Assume on the same typed domain and time horizon:

```text
P_C^2 <= Lambda*A^3,
A <= K*Z,
Lambda*K*Zstar <= g_C^2,

g0 = g_C + g_R,
g_R > 0,

h_ramp <= Hbar,
r^T D^{-1} r <= Rbar,
Rbar <= 4*g_R*B_R,

Z(0) + T*(Hbar+B_R) < Zstar.                               (19)
```

Then the modified-energy sublevel `Z<Zstar` is invariant on `[0,T]`, the cubic term remains absorbable there, and

```text
Z(t) <= Z(0) + t*(Hbar+B_R)                                (20)
```

throughout the horizon.

This is conditional only on the listed source/domain/regularity premises. It does not turn them into source facts.

## 6. Exact rational specialization using the current C-FD constant

`T-P5-011` gives for the current Fourier/central-FD branch

```text
Lambda*K = 13*S_F / 72000000000000000.                     (21)
```

Let `g0>0` be the available damping margin and make the simple rational split

```text
g_C = g_R = g0/2.                                          (22)
```

Then the maximal cubic barrier from (11) is

```text
Zstar = g0^2 / (4*Lambda*K)                                (23)
```

when `S_F>0`, while the sharp nonconservative rate cost is

```text
B_R = Rbar/(2*g0).                                         (24)
```

Thus a sufficient horizon condition is

```text
Z(0) + T*(Hbar + Rbar/(2*g0))
  < g0^2/(4*Lambda*K).                                     (25)
```

Clearing denominators with (21), (25) is exactly equivalent to the all-rational target

```text
26*S_F*g0*(Z(0)+T*Hbar) + 13*S_F*T*Rbar
  < 36000000000000000 * g0^3.                              (26)
```

For the target `T=1`, this becomes

```text
26*S_F*g0*(Z0+Hbar) + 13*S_F*Rbar
  < 36000000000000000 * g0^3.                              (27)
```

Equation (27) is a useful checker-facing scalar target: once `S_F`, the ramp-work cap, the weighted dual remainder cap, the initial shifted energy, and the residual damping margin are all bound on the same domain, no square roots are needed in the final arithmetic consumer.

The 50/50 damping split is only a convenient rational sufficient choice, not an optimal allocation. The generic theorem (19) deliberately keeps `g_C` and `g_R` separate so a later checker can optimize their split without changing the mathematics.

If `S_F=0`, the C-FD cubic term vanishes under the squared bound and the cubic barrier is unnecessary; (23)-(27) should not be used by dividing through `S_F` in that degenerate case.

## 7. New obstruction: additive work cannot be upgraded to infinite-time decay from `A <= K Z`

It is tempting to combine the finite-horizon estimate with the coercivity bridge from `T-P5-011` and claim an ultimate or asymptotic bound. That does **not** follow from the available inequality

```text
A <= K*Z.                                                   (28)
```

The direction is wrong for turning `-g_R*A` into a negative multiple of `Z`. A state may have positive stored potential energy `Z>0` but zero velocity, hence `A=0`. At such an instant the additive ramp/nonconservative work budget can be positive while the damping contributes nothing.

Therefore from the current information alone the generic consequence is the finite-horizon linear drift (20), not

```text
Zdot <= -alpha*Z + B.                                       (29)
```

To obtain a genuine infinite-time ultimate bound from this route one needs an additional structural estimate such as

```text
A >= alpha*Z                                                (30)
```

on the relevant invariant set, or a hypocoercive/cross-term Lyapunov functional that converts position energy into dissipation. Neither is supplied by `T-P5-011`.

A one-dimensional counterexample to the invalid inference is immediate: take a storage state with `Z=q^2/2`, `v=0`, so `A=v^2=0`, and permit a positive external/ramp power bound. Then (28) holds but no negative `-alpha Z` term follows.

This failure boundary prevents the finite-horizon theorem from being over-advertised as asymptotic stability.

## 8. Relation to the new P8 ramp-domain result

`T-P8-011` proves that after ramp elimination the correct source query is along the graph `w=c*t`, and it gives a rational witness showing the currently documented `|w|<=1/100` local box cannot cover the whole admissible family to `T=1`.

The present P5 result does not change that. Even if (19) proves the mechanical energy cannot leave its sublevel, a source theorem used to bound `Hbar`, `Rbar`, `S_F`, or `W_min` must still be valid at every actual graph point `(m(t),w=c*t)` on the same horizon. Energy confinement in the mechanical coordinates does not imply the missing ramp-coordinate source coverage.

Thus the correct cross-branch order is:

```text
P8/source graph-domain coverage
    -> same-domain bounds for S_F, Hbar, Rbar, W_min, Z0
    -> P5 finite-horizon barrier (this child)
    -> downstream energy consumer.
```

No step can substitute for the previous one.

## 9. Lean-friendly theorem decomposition

The first formalization should remain mostly algebraic and reuse the already compiled cubic-barrier sidecar.

```lean
-- Weighted-dual work charged to a chosen rate budget; square-only interface.
theorem dual_work_budget
    (A P R gR BR : R)
    (hA : 0 <= A) (hR : 0 <= R) (hgR : 0 < gR) (hBR : 0 <= BR)
    (hP : P^2 <= R*A)
    (hcap : R <= 4*gR*BR) :
    P <= gR*A + BR
```

The `P^2 <= R*A` premise is the inverse-free consumer form of weighted Cauchy; a separate matrix lemma may prove it from `A=v^T D v` and `R=r^T D^{-1}r`.

```lean
-- Pointwise mixed ledger, importing/reusing T-P5-011 cubic absorption.
theorem mixed_energy_rate
    ...
    (hcubic : PC^2 <= Lambda*A^3)
    (hAZ : A <= K*Z)
    (hbarrier : Lambda*K*Z <= gC^2)
    (hdual : PR^2 <= R*A)
    (hRcap : R <= 4*gR*BR)
    (hramp : hRamp <= Hbar)
    (hledger : Zdot <= -(gC+gR)*A + PC + PR + hRamp) :
    Zdot <= Hbar + BR
```

Then isolate the calculus layer:

```lean
-- First-exit/finite-horizon invariant barrier.
theorem finite_horizon_sublevel
    (hderiv : forall t in Ioo 0 T,
       Z t <= Zstar -> deriv Z t <= B)
    (hheadroom : Z 0 + T*B < Zstar)
    ... :
    forall t in Icc 0 T, Z t < Zstar
```

Finally, a pure rational corollary can encode (26)/(27) after `Lambda*K` is replaced by the frozen `13*S_F/72000000000000000` identity.

Formalization should keep the source/domain premise outside these generic theorems; do not define deployed Float64 bounds into the abstract energy lemma.

## 10. Remaining blockers

- `S_F` still needs frozen source/checker generation and binding to the 216 tensor coefficients.
- The modified non-kinetic storage still needs a same-domain lower bound `W_min`, hence a certified `Z0`.
- The actual parameter-potential term needs a same-domain cap on `-c*partial_w Phi` (or a sharper signed integral bound) to instantiate `Hbar`.
- True nonconservative controller/IEEE/solve remainder needs a same-domain weighted dual cap `Rbar`; a uniform force norm in unrelated coordinates is not automatically this quantity.
- P8/source coverage along `w=c*t` remains independent and, per `T-P8-011`, the old single `|w|<=0.01` box is insufficient for `T=1`.
- If the desired final claim is asymptotic rather than finite-horizon, a new lower dissipation-to-storage estimate or hypocoercive Lyapunov redesign is required; `A<=KZ` cannot supply it.

## Recommended next action

1. Formalization lane: implement `dual_work_budget` and `mixed_energy_rate` first; both are pointwise and should avoid a heavy ODE API. Then add the isolated first-exit lemma.
2. Source/checker lane: produce exact rational/sound interval caps for `Hbar` and weighted-dual `Rbar` on the same P8 ramp-graph cells that produce `S_F` and `W_min`.
3. If the target is only the fixed P8 horizon `T=1`, try the exact rational 50/50 criterion (27) before building any asymptotic machinery.
4. Do not claim that energy confinement fixes the `w` domain obstruction from `T-P8-011`; domain coverage must be widened or partitioned independently.

This review remains `pending`: it is a source-independent finite-horizon energy theorem and obstruction, not P5/P8/M4 closure.
