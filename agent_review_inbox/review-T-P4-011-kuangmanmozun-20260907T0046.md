---
kind: review_result
review_id: review-T-P4-011-kuangmanmozun-20260907T0046
task_id: T-P4-011
source_agent: 狂蛮魔尊
claimed_at: 2026-09-07T00:40:00-06:00
created_at: 2026-09-07T00:46:00-06:00
inspected_commit: 5a5a3ca0a9d76ea6c9b16f8c91e6c84d93d8c88d
integration_status: pending
admission_label: pending
proposed_integration_target: theorem
requested_action: formalize_kc_quadratic_budget_and_bind_cross_coordinate_before_P4_use
---

# T-P4-011 — corrected `kc=1/20` force term: exact quadratic budget, sharp Schur route, and the auxiliary-variable obstruction

## Scope

This pass consumes the coordinator-corrected canonical force contract

```text
rho_kc(q4,q5) = (q5/20, q4/20)
```

and asks only the mathematical question assigned to `T-P4-011`: what exact quadratic cost does this force term carry, and can it fit the current Schur/Young consumer?

Inspected facts:

- `docs/routeb-p4-kc-force-contract.md` (blob `99e21a32b2acc7302e4f676098047a9e34ef12a3`) fixes the current canonical scale `kc=0.05=1/20` and states that the deployed DH torque does not contain this term, so it must be charged as generalized-force mismatch.
- frozen canonical PMI source `examples/routeb_source_binding_audit/snapshots/original_target/routeB_pmi_certificate.jl` (blob `207b6b361eeb465aee8933cff8b9f41a1b17a89f`) gives `q4,q5 in [-pi,pi]`, the local polynomial
  `Pstate=(3/2)(q4^2+q5^2)+(4/5)(v4^2+v5^2)`, and `eta_star=28/5`.
- `examples/routeb_p4_sharp_schur_sidecar/P4SharpSchur.lean` (blob `fbfbf3d03c448760f8c9e042f05df5bef41c221c`) provides the source-independent sharp scalar condition and the clean rational `c=1/4` consumer for the existing block-4 abstraction.
- `review-T-P3-010-guyuefangyuan-20260907T0035.md` gives, only at the exact-real DH math layer, the candidate block entry `M55=200739/4000000`; it is used below only as an optional conditional arithmetic instantiation, not as a source-bound P4 D-row fact.

No provenance, Float64 semantic equality, D-row source correspondence, coverage, P4/M4 admission, or registry claim is made.

## 1. Exact force norm and an exact state-relative identity

Define

```text
rho4 = q5/20,
rho5 = q4/20.
```

Then exactly

```text
||rho_kc||^2 = rho4^2+rho5^2
             = (q4^2+q5^2)/400.                     (1)
```

The local PMI state polynomial is

```text
Pstate = (3/2)(q4^2+q5^2) + (4/5)(v4^2+v5^2).
```

Therefore there is an exact identity

```text
Pstate - 600*||rho_kc||^2
  = (4/5)(v4^2+v5^2) >= 0.                           (2)
```

Hence, without any sampling,

```text
||rho_kc||^2 <= Pstate/600.                          (3)
```

This is stronger information than a constant envelope: the corrected `kc` mismatch vanishes quadratically at the block equilibrium.

### Local `Pstate<=eta_star` bound

From `Pstate<=28/5`, (3) gives the exact rational bound

```text
||rho_kc||^2 <= (28/5)/600 = 7/750.                 (4)
```

Equivalently, because the velocity contribution is nonnegative,

```text
q4^2+q5^2 <= 56/15.
```

### Joint-limit-only bound

The separate source joint limits `|q4|<=pi`, `|q5|<=pi` imply only

```text
||rho_kc||^2 <= (pi^2+pi^2)/400 = pi^2/200.         (5)
```

The two bounds must not be conflated: (5) is a global joint-limit bound, while (4) uses the much smaller local `Pstate<=eta_star` set. The local bound is the appropriate one if the future theorem is explicitly inside the PMI localization; the joint-limit bound is the fail-safe statement outside that localization.

## 2. Corrected scale kills the old `1/100` residual target but not the sharp Schur budget

For one scalar Schur channel write

```text
Q(x,y,r) = p*x^2 + 2*x*r + d*y^2,
```

with `p>0`. The already-derived sharp condition is

```text
forall x, Q(x,y,r)>=0  <->  r^2 <= p*d*y^2.
```

If a typed P4 adapter identifies the corrected cross force with the same scalar coordinate,

```text
r = +/- y/20,                                        (6)
```

then the necessary-and-sufficient coefficient condition becomes simply

```text
1/400 <= p*d.                                        (7)
```

This is domain-free once (6) is proved: no `pi` bound and no `Pstate<=eta_star` bound are needed for the Schur step itself.

The historical `ell=1/100` residual premise is too small for the corrected force:

```text
(1/20)^2 = 1/400 > 1/10000 = (1/100)^2.
```

So the old `1/100` envelope cannot be reused unchanged. This is a 25-fold increase in the required squared coefficient relative to that stale target.

However, the newer rational `c=1/4` sharp-Schur consumer easily accepts the corrected `kc` term:

```text
1/400 < 1/16 = (1/4)^2.                              (8)
```

Thus `kc` alone consumes only `1/25` of the squared `c=1/4` envelope.

More usefully, if the rest of the same force channel obeys

```text
|r_other| <= (1/5)|y|,
```

then by triangle inequality

```text
|r_other +/- y/20|
 <= (1/5+1/20)|y|
 = (1/4)|y|,                                         (9)
```

so the existing `quarter_residual_absorption` theorem can consume the total channel. Therefore a clean source target is:

```text
kc coefficient = 1/20,
remaining same-coordinate force envelope <= 1/5.
```

This is much more informative than continuing to target the stale `1/100` total envelope.

## 3. Concrete block-4 margin

For the existing exact-real block-4 scalar child

```text
p4 = 3/5,
d4 = 116667666666667 / 10^15,
```

we have exactly

```text
p4*d4 - (1/20)^2
 = 337503000000001 / 5000000000000000
 > 0.                                                 (10)
```

Thus the corrected coefficient is not close to the sharp block-4 limit:

```text
(p4*d4)/(1/400) = 28.00024000000008...
```

so it uses about `1/28` of the available sharp squared budget.

The exact completion also shows the quadratic `y^2` cost of the corrected term:

```text
p*x^2 + 2*x*(y/20) + d*y^2
 = (p*x+y/20)^2/p + (d - 1/(400*p))*y^2.            (11)
```

For `p4=3/5`, the consumed diagonal coefficient is

```text
1/(400*p4) = 1/240,
```

and the remaining block-4 diagonal margin is

```text
d4 - 1/240
 = 337503000000001 / 3000000000000000
 > 0.                                                 (12)
```

So at the abstract exact-real level the corrected `kc` term is comfortably Schur-absorbable **provided the future adapter really proves `y=q5` (or the sign variant) for channel 4**.

## 4. A simple rational Young split

The same conclusion can be stated without division by `p`. For any `eps>0`,

```text
2*x*(y/20) >= -eps*x^2 - (1/400)/eps * y^2.         (13)
```

A particularly convenient uniform choice is

```text
eps = 1/20.
```

Then `(1/400)/eps=1/20`, so a channel closes whenever

```text
p >= 1/20,
d >= 1/20.                                          (14)
```

For the current block-4 abstraction,

```text
p4-1/20 = 11/20 > 0,
d4-1/20 = 66667666666667/10^15 > 0.                 (15)
```

and therefore

```text
p4*x^2 + 2*x*(y/20) + d4*y^2
 >= (11/20)x^2
    + (66667666666667/10^15)y^2
 >= 0.                                                (16)
```

This gives a very small Lean-friendly theorem: no square roots and no tuning search.

As an optional exact-real arithmetic consequence of `T-P3-010`, if a future typed channel-5 P4 D-row is actually allowed to instantiate

```text
d5 = 200739/4000000,
```

then

```text
d5 - 1/20 = 739/4000000 > 0.                        (17)
```

Hence the same `eps=1/20` Young split would close channel 5 as soon as its own leading Schur coefficient satisfies `p5>=1/20`. This is only a conditional arithmetic observation: the current repository has not proved that the P4 channel-5 D-row `d` is this mass entry.

## 5. Exact obstruction if the Schur auxiliary variable is not the cross coordinate

The favorable conclusions above depend on a typed relation such as (6). A mere absolute domain bound on `rho_kc` cannot replace that relation in the universal scalar Schur theorem.

Take a valid physical block state

```text
q4=0,
q5=1,
v4=v5=0.
```

It satisfies both the joint limits and the local condition

```text
Pstate = 3/2 <= 28/5.
```

The corrected channel-4 force residual is then

```text
r=1/20.
```

If the Schur theorem still quantifies an independent auxiliary `y`, choose

```text
y=0,
p=3/5,
x=-r/p=-1/12.
```

Then for every `d`

```text
p*x^2 + 2*x*r + d*y^2 = -1/240 < 0.                (18)
```

Therefore:

> Joint limits, `Pstate<=eta_star`, and even a small absolute force norm are logically insufficient to feed the current universal scalar Schur residual interface unless the P4 adapter connects its `y` variable to the physical cross coordinate or supplies a separate q-dependent slack.

This is a mathematical obstruction, not a provenance issue.

## 6. Alternative typed route: charge an explicit configuration-quadratic slack

If a future P4 child does not want to identify `y` with the cross coordinate, the sharp completion gives the exact separate cost

```text
p*x^2 + 2*x*(q/20)
 >= - q^2/(400*p),       p>0.                        (19)
```

For both corrected channels, with positive leading coefficients `p4,p5`, the exact configuration cost is

```text
C_kc(q4,q5)
 = q5^2/(400*p4) + q4^2/(400*p5).                   (20)
```

Thus a q-quadratic slack dominates the cross mismatch iff it dominates (20). Under only the joint limits,

```text
C_kc <= (pi^2/400)*(1/p4+1/p5).                     (21)
```

Under the local `Pstate<=28/5` constraint,

```text
C_kc <= (7/750) * max(1/p4,1/p5).                   (22)
```

The local bound is sharp given only `q4^2+q5^2<=56/15`: all available q-radius can lie in the coordinate with the larger reciprocal `1/p_i`.

This route preserves force units and makes the missing theorem explicit: P4 must expose enough configuration-quadratic slack in `D_elim_c` or another typed polynomial row. It is not legitimate to subtract this force-side cost from an acceleration-side M4 `D` budget without a mass/inverse-mass conversion theorem.

## 7. Lean-friendly theorem package

Recommended source-independent declarations:

```lean
-- Exact physical-force algebra, no source binding.
def kcSq (q4 q5 : R) : R := (q4^2+q5^2)/400

theorem kc_state_identity (q4 q5 v4 v5 : R) :
  (3/2)*(q4^2+q5^2) + (4/5)*(v4^2+v5^2)
    - 600*kcSq q4 q5
  = (4/5)*(v4^2+v5^2)

theorem kc_local_bound
  (hP : (3/2)*(q4^2+q5^2)+(4/5)*(v4^2+v5^2) <= 28/5) :
  kcSq q4 q5 <= 7/750

-- Typed cross-coordinate Schur consumer.
theorem kc_cross_schur
  (p d x y : R) (hp : 0<p) (hpd : (1/400:R) <= p*d) :
  0 <= p*x^2 + 2*x*(y/20) + d*y^2

-- Clean rational composition with the existing quarter envelope.
theorem kc_plus_other_quarter
  (other y : R) (hother : |other| <= (1/5)*|y|) :
  |other + y/20| <= (1/4)*|y|

-- Obstruction when the auxiliary coordinate is independent.
theorem kc_independent_y_counterexample :
  (3/5:R)*(-1/12)^2 + 2*(-1/12)*(1/20) + d*0^2 = -1/240
```

For the two-channel redesign, a matrix-form theorem equivalent to two scalar Schur conditions is also useful:

```text
Q = p4*x4^2 + 2*x4*(q5/20) + d4*q5^2
  + p5*x5^2 + 2*x5*(q4/20) + d5*q4^2
```

is nonnegative for all variables iff

```text
p4>0, p5>0,
1/400 <= p4*d4,
1/400 <= p5*d5.
```

This captures the corrected cross-coordinate structure directly and avoids pretending the force term is an acceleration residual.

## 8. Conclusion and shortest next step

The force-scale correction does **not** create a fatal Schur constant obstruction. It invalidates the stale `1/100` residual target, but the corrected coefficient `1/20` fits comfortably inside the existing sharp block-4 budget and inside the rational `1/4` envelope.

The actual blocker is now a typed-variable question:

```text
rho4=q5/20  must feed a Schur coordinate identified with q5,
rho5=q4/20  must feed a Schur coordinate identified with q4,
```

or P4 must expose the explicit q-quadratic slack (20). If the current auxiliary `y` remains independent, counterexample (18) proves that no absolute joint-limit/local-state bound can rescue universal Schur nonnegativity.

Recommended next work:

1. Formalization lane: prove `kc_state_identity`, `kc_local_bound`, `kc_cross_schur`, and `kc_plus_other_quarter` as a tiny source-independent sidecar.
2. P4 interface/source lane: decide and prove the actual `y <-> q_cross` mapping in the PMI/D-row, or expose the q-quadratic slack needed for (20).
3. For the remainder ledger, use the clean rational target `|r_other| <= (1/5)|q_cross|` if the `c=1/4` interface is retained.
4. Keep `M_BD(q)a_D` and all other P4 source residual terms separate; this result only prices the corrected `kc` contribution.
