---
kind: review_result
review_id: review-T-P5-005-kuangmanmozun-20260906T2307
task_id: T-P5-005
source_agent: 狂蛮魔尊
claimed_at: 2026-09-06T23:02:00-06:00
created_at: 2026-09-06T23:07:00-06:00
integration_status: pending
admission_label: pending
proposed_integration_target: theorem
requested_action: formalize_relative_residual_closure_and_preserve_obstruction
---

# T-P5-005 — relative residual strict-decay closure and the current-interface obstruction

## Scope

This review answers the newly released P5 mathematical frontier:

```text
||r|| <= rho ||v||,  rho < delta
    ==> E_dot <= -(delta-rho)||v||^2,
```

but does so in the units actually used by the repository. It derives a sharper
diagonal/weighted version, gives exact component-wise premises that are easy to
bind to force residuals, and then tests those premises against the current
`DHPowerBinding.forceError` and `FDForceBudget.envelope` interfaces.

Inspected mathematical objects:

- `examples/routeb_p5_residual_power_lean/DissipativeResidualPower.lean`
  - blob `e2dee5128d3ac6e9738d94f6ee7908ea909df2a3`
  - already proves the scalar relative-residual consequence after the norm
    reduction has been supplied.
- `examples/routeb_dh_power_binding/DHPowerBinding.lean`
  - blob `5e440147a2428262d1beea31ccb56c27d2818b07`
  - defines the actual abstract force-error decomposition consumed by the
    energy identity.
- `examples/routeb_dh_power_binding/FDForceBudget.lean`
  - blob `4e3a3ae56b5ec2708d0deeec2de786d0a0218e36`
  - current FD component envelope has nonzero additive offsets.
- `examples/routeb_supply_core/RouteBSupplyCore.lean`
  - blob `90e5f0d66c002655e89087c0f71f088b44401891`
  - exact diagonal damping values
    `[13/10,11/10,19/20,4/5,13/20,1/2]`.

No source binding, sampling, receipt, provenance, or admission claim is made.

## 1. The correct force/velocity weighted norm

Let the six positive damping coefficients be `d_i>0` and define

```text
A(v) := sum_i d_i * v_i^2.
```

A force residual `r` pairs with velocity through mechanical power

```text
<r,v> = sum_i r_i v_i.
```

The unit-consistent dual quadratic residual is therefore

```text
B(r) := sum_i r_i^2 / d_i.
```

A natural relative residual hypothesis is not just a dimensionless Euclidean
statement but

```text
B(r) <= kappa^2 * A(v),      0 <= kappa < 1.        (R)
```

Here `kappa` is dimensionless because `B` and `A` have the same power-scaled
quadratic units.

### Weighted Young closure without square roots

For `kappa>0`, each component satisfies the exact square identity

```text
0 <= (kappa*d_i*v_i-r_i)^2 / d_i,
```

hence

```text
2*kappa*r_i*v_i
 <= kappa^2*d_i*v_i^2 + r_i^2/d_i.
```

Summing and using (R):

```text
2*kappa*<r,v>
 <= kappa^2*A(v) + B(r)
 <= 2*kappa^2*A(v).
```

Therefore

```text
<r,v> <= kappa*A(v),
```

and any zero-input energy identity of the form

```text
E_dot <= -A(v) + <r,v>
```

closes as

```text
E_dot <= -(1-kappa)*A(v).                            (1)
```

If `v != 0`, positivity of all `d_i` and `kappa<1` gives strict negativity.
The `kappa=0` case is the exact-residual case `B(r)=0`, hence `r=0`.

This is strictly more natural than first collapsing to a Euclidean
`delta=min_i d_i` and losing the diagonal damping structure.

## 2. Component-wise sufficient condition

A more source-friendly but stronger premise is

```text
|r_i| <= rho_i * |v_i|,
0 <= rho_i < d_i.                                    (C)
```

Then

```text
r_i*v_i <= |r_i|*|v_i| <= rho_i*v_i^2,
```

so directly

```text
E_dot
 <= -sum_i d_i*v_i^2 + sum_i r_i*v_i
 <= -sum_i (d_i-rho_i)*v_i^2.                       (2)
```

This is sharp at the component level: if `r_i=rho_i*v_i`, the contribution of
that channel is exactly `-(d_i-rho_i)v_i^2`.

If one wants a single Euclidean rate, define

```text
lambda := min_i (d_i-rho_i) > 0.
```

Then

```text
E_dot <= -lambda * sum_i v_i^2.                     (3)
```

For the repository's exact damping coefficients,

```text
min_i d_i = 1/2.
```

Thus the coarse scalar theorem can use `delta=1/2`. For example, the simple
uniform requirement

```text
rho_i <= d_i/2  for every i
```

gives

```text
E_dot <= -(1/2) A(v) <= -(1/4) * sum_i v_i^2.       (4)
```

The diagonal statement (2) should be preferred whenever actual component
budgets are available.

## 3. Exact decomposition requirements for the current `forceError`

The current force error is

```text
e_i = mass_i + tau_i + coriolis_i + gravity_i + solve_i,
```

where, exactly as encoded in `DHPowerBinding.forceError`,

```text
mass_i     = ((Ma-Mi)a)_i,
tau_i      = (tauI-tauA)_i,
coriolis_i = (cA-cI)_i,
gravity_i  = (gA-gI)_i,
solve_i    = solveResidual_i.
```

A sufficient same-component relative interface is therefore to prove, on the
**same covered domain**,

```text
|mass_i|     <= alphaM_i |v_i|,
|tau_i|      <= alphaT_i |v_i|,
|coriolis_i| <= alphaC_i |v_i|,
|gravity_i|  <= alphaG_i |v_i|,
|solve_i|    <= alphaS_i |v_i|,

alphaM_i+alphaT_i+alphaC_i+alphaG_i+alphaS_i < d_i. (5)
```

Then triangle inequality yields (C) with

```text
rho_i = alphaM_i+alphaT_i+alphaC_i+alphaG_i+alphaS_i.
```

This precisely identifies what true-DH/FD/solve mathematics would have to
supply for the strongest component-wise version.

A less restrictive cross-component alternative is to bound each physical
piece in the dual damping norm and require the sum of its dimensionless gains
to be below one:

```text
sqrt(B(mass))     <= kM sqrt(A(v)),
sqrt(B(tau))      <= kT sqrt(A(v)),
...
sqrt(B(solve))    <= kS sqrt(A(v)),

kM+kT+kC+kG+kS < 1.                                  (6)
```

For formalization, (6) can be stated without square roots by supplying the
already-composed `B(e) <= kappa^2 A(v)` theorem; the physical adapter can prove
it by whatever matrix/operator estimates are most natural.

## 4. Structural counterexample: the generic `forceError` interface cannot imply a velocity-relative bound

The variables in `DHPowerBinding.forceError` are intentionally abstract real
inputs. From that definition alone there is an immediate counterexample to any
unconditional theorem

```text
|forceError_i| <= rho*|v_i|.
```

Fix any channel `i` and choose

```text
Ma = Mi = 0,
a = 0,
tauA = tauI = 0,
cA = cI = 0,
gI = 0,
gA_i = 1,
v = 0.
```

Then `solveResidual_i=0` and the definition gives

```text
forceError_i = 1,
```

while

```text
rho*|v_i| = 0
```

for every finite `rho`.

Therefore **no purely algebraic theorem over the current generic
`DHPowerBinding` inputs can produce the required relative residual estimate**.
New source/domain hypotheses must force all velocity-independent mismatch terms
to vanish or be absorbed elsewhere.

This is a counterexample to the current abstract inference, not a claim that
the deployed DH trajectory actually realizes these arbitrary inputs.

## 5. Stronger obstruction from the current FD envelope shape

`FDForceBudget.envelope cap i` is

```text
slope_i * cap + offset_i.
```

The exact offsets are

```text
index 0: 0
index 1: 68343 / 800000000000000
index 2: 21909 / 1000000000000000
index 3: 6867  / 8000000000000000
index 4: 6867  / 4000000000000000
index 5: 0.
```

So channels 1--4 have strictly positive additive offsets even at `cap=0`.
The current theorem premise is only

```text
|efd_i| <= envelope cap i.
```

At `cap=0` and `v_i=0`, choose for example

```text
efd_i = offset_i/2
```

on any positive-offset channel. This satisfies the existing FD enclosure but
violates every finite relative bound

```text
|efd_i| <= rho_i |v_i| = 0.
```

Hence the **current FD envelope theorem is logically insufficient** to derive
T-P5-005, even before true-DH provenance is discussed. The positive offset does
not prove the actual FD error is nonzero at `v=0`; it proves only that the
present envelope is too inhomogeneous to establish relative scaling.

Even on channels with zero offset, a positive `slope_i*cap` is not relative to
`v_i` unless one also proves `cap <= C|v_i|` or replaces `cap` by a state norm
that vanishes with the equilibrium.

## 6. Consequence: pure velocity-relative strict decay is not currently available

The current error ledger contains terms that are naturally functions of
configuration, acceleration, disturbance, finite-difference truncation and
floating execution, not only velocity. Therefore the best mathematically
honest architecture is a split

```text
e = e_rel + e_bias,
```

where

```text
B(e_rel) <= kappa^2 A(v),   kappa<1,                 (7)
```

and `e_bias` is charged separately.

Then

```text
E_dot
 <= -(1-kappa)A(v) + <e_bias,v> + input_supply.      (8)
```

If `e_bias` has only an absolute norm bound, the P5-004 Young/ultimate-bound
result is the correct consumer. To obtain genuine strict zero-input decay, one
must additionally prove `e_bias=0` (or a state-relative storage bound that also
vanishes at the equilibrium).

For nonzero ramp disturbance `w`, the exact supply already contains input
power; one should not demand unconditional `E_dot<0` for all states. The strict
relative-residual theorem is naturally a zero-input/local-stability child or a
child after the input supply has been separately accounted for.

## 7. Lean-friendly theorem decomposition

Recommended source-independent formalization targets:

```lean
-- Componentwise diagonal closure.
theorem component_relative_residual_decay
    (d rho v r : Fin 6 -> ℝ)
    (hd : ∀ i, 0 < d i)
    (hrho : ∀ i, 0 <= rho i ∧ rho i < d i)
    (hrel : ∀ i, |r i| <= rho i * |v i|) :
    -(∑ i, d i * v i^2) + ∑ i, r i * v i
      <= -(∑ i, (d i-rho i) * v i^2)
```

and a concrete supply-core corollary with `d=RouteBSupplyCore.damping`.

A very small obstruction theorem can also be formalized directly from the
existing interface:

```lean
theorem generic_forceError_not_velocity_relative
    (rho : ℝ) :
    ∃ Ma Mi a tauA tauI cA cI gA gI v i,
      v i = 0 ∧
      |forceError Ma Mi a tauA tauI cA cI gA gI i| > rho * |v i|
```

with the explicit gravity-mismatch witness above (for nonnegative `rho`; the
right side is zero regardless).

For the weighted norm, define

```text
dampedSq v := sum_i d_i*v_i^2
dualSq r   := sum_i r_i^2/d_i
```

and formalize the no-square-root implication

```text
0 < kappa < 1,
dualSq r <= kappa^2*dampedSq v
--------------------------------
-sampedSq v + dot r v <= -(1-kappa)*dampedSq v.
```

The proof is componentwise weighted Young plus finite summation; no spectral
machinery is needed.

## 8. What is proved / what remains open

Mathematically proved in this review:

- the unit-consistent weighted relative-residual condition that yields strict
  damping retention;
- a sharper component-wise condition preserving every diagonal damping margin;
- exact premises needed for the five-term `forceError` decomposition;
- a concrete counterexample showing the generic force-error interface cannot
  imply velocity-relative scaling without new hypotheses;
- a second counterexample showing the current positive-offset FD envelope
  cannot imply relative scaling by itself.

Still open:

- whether the **actual deployed** mass/controller/C/G/solve residual pieces
  vanish sufficiently at the equilibrium or satisfy (5)/(7) on a covered
  domain;
- a true-DH same-domain proof of any relative gain;
- any full-state relative storage estimate involving `q,w,a` rather than only
  `v`;
- flowpipe/domain coverage and M4 admission.

## Recommended next action

1. Formalization agents: implement the component-wise and weighted source-
   independent lemmas; preserve the explicit generic/FD obstruction theorem.
2. Physical math/source lane: split `forceError` into terms that genuinely
   vanish with velocity/state and terms that carry additive bias. Do **not** try
   to algebraically convert the current FD envelope into `rho|v|`.
3. If strict zero-input decay is required, prove the bias part vanishes at the
   equilibrium. If it does not, stop pursuing a pure velocity-relative theorem
   and use the mixed `e_rel+e_bias` architecture with P5-004 for the bias.

No Lean/checker command was run in this mathematical pass; compilation belongs
to the designated formalization agents and final validation to 封不觉.
