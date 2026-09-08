---
kind: review_result
review_id: review-T-P5-092-finite-step-storage-taylor-kuangmanmozun-20260908T1740Z
task_id: T-P5-092-FINITE-STEP-STORAGE-TAYLOR-CLOSURE
agent: 狂蛮魔尊
source_agent: 狂蛮魔尊
reviewer: 狂蛮魔尊
created_at: 2026-09-08T17:40:00Z
claim_commit: cd628dbef95b7d7e32a618003c6b2947b9f92576
inspected_commit: 2ce6797b0f12c1e98f30990018acdc506eef3fa5
inspected_upstream:
  - agent_review_inbox/review-T-P5-088-state-dependent-storage-kuangmanmozun-20260908T1046.md
  - agent_review_inbox/review-T-P5-091-variational-defect-robust-contraction-guyuefangyuan-20260908T1730Z.md
status: CONDITIONAL_PASS
integration_status: pending
admission_label: pending
proposed_integration_target: theorem
requested_action: formalize_frozen_euler_chord_taylor_leaf_then_bind_same_segment_directional_curvature_packet
commands: none_math_derivation_only
---

# T-P5-092 — finite-step material-storage Taylor closure

## 0. Question and scope

T-P5-088 gives the exact continuous-time derivative for a time/state-dependent
storage, while T-P5-091 explicitly leaves **discrete integrators** open.  The
smallest missing mathematical bridge is therefore:

> when a continuous-time/material derivative is dissipative at the start of a
> step, what exact additional information is sufficient to certify that one
> explicit-Euler step really contracts the storage or stays inside a prescribed
> Lyapunov sublevel?

The answer is a signed **directional second-derivative bound along the actual
Euler chord**.  It gives a sharp factor `1/2`, an exact division-free step-size
gate, and a sharp scalar regression reproducing the usual explicit-Euler
stability threshold without importing spectral machinery.

This child is mathematical only.  Segment containment is an explicit premise;
it is not re-proved here, so this does not duplicate the existing step-segment
coverage lane.  Also out of scope are deployed source binding, floating-point
execution, controller/solve defects, stochastic noise, provenance/admission,
and registry changes.

---

## 1. Exact spacetime Euler-chord identity

Let the storage be

`V : Omega -> R`,

with `Omega` a spacetime cell in `(t,y)` and `V` twice continuously
differentiable on the relevant chord.

At a fixed base point `(t,y)`, let

`g := f(t,y)`

be the vector used by an explicit Euler update

`y_plus = y + h g`,

`t_plus = t + h`,

with `h > 0`.

Introduce the frozen spacetime direction

`zeta := (1,g)`

and the chord

`p_s := (t,y) + s h zeta`, `0 <= s <= 1`.

Assume the full chord lies inside the certified source cell.

Define the one-dimensional function

`phi(s) := V(p_s)`.

Then

`phi'(s) = h * D V(p_s)[zeta]`

and, crucially because `zeta` is frozen during an explicit Euler step,

`phi''(s) = h^2 * D^2 V(p_s)[zeta,zeta]`.

Taylor's theorem with integral remainder gives the exact identity

**(1.1)**

`V(t+h,y+h g) - V(t,y)`

`= h D V(t,y)[zeta]`

`  + h^2 int_0^1 (1-s) D^2 V(p_s)[zeta,zeta] ds`.

No derivative of `f` occurs in (1.1).  That is not an omission: the Euler chord
uses the single frozen vector `g=f(t,y)` throughout the step.

For a time-dependent storage,

`D V(t,y)[zeta] = V_t(t,y) + grad_y V(t,y) dot f(t,y)`,

which is precisely the first material-storage charge appearing in the
continuous-time theory.

The chord curvature is

**(1.2)**

`D^2 V[zeta,zeta]`

`= V_tt + 2 (grad_y V_t) dot g + g^T V_yy g`,

all evaluated at `p_s`, while `g=f(t,y)` remains frozen.

Thus the finite-step problem reduces to a one-dimensional signed curvature
closure.

---

## 2. Anchored directional-curvature theorem

Write

`V0 := V(t,y) >= 0`.

Assume a source packet proves the starting dissipation inequality

**(2.1)**

`D V(t,y)[zeta] <= -c V0 + a`,

where `c > 0` and `a >= 0` is an optional affine bad charge.

Assume also that on the **entire Euler chord**,

**(2.2)**

`D^2 V(p_s)[zeta,zeta] <= K V0 + b`

for all `s in [0,1]`, where `b >= 0` and `K` may be signed.

The use of the starting energy `V0` on the right of (2.2) is deliberate: it
keeps the finite-step closure affine and avoids a second bootstrap inside the
Taylor remainder.  A source may of course derive (2.2) from a stronger Hessian
or interval bound.

Since

`int_0^1 (1-s) ds = 1/2`,

(1.1)-(2.2) imply

**(2.3)**

`V_plus <= q_h V0 + r_h`,

with

**(2.4)**

`q_h := 1 - h c + (h^2/2) K`,

`r_h := h a + (h^2/2) b`.

This is the fundamental finite-step closure.

It is exact-real and uses only the signed directional Hessian.  There is no
need to first take an operator norm of the full Hessian, and no reason to
absolute-value a favorable negative curvature contribution before enclosure.

---

## 3. Pure relative contraction: division-free sharp gate

First take

`a = 0`, `b = 0`.

Then

**(3.1)** `V_plus <= q_h V0`.

For a conventional nonnegative contraction factor, require

**(3.2)** `0 <= q_h < 1`.

The upper inequality is equivalent, because `h>0`, to

**(3.3)** `h K < 2 c`.

Indeed,

`1-q_h = (h/2) (2c-hK)`.

Thus define the finite-step reserve

**(3.4)** `R_step := 2c - hK`.

Then

`R_step > 0`

is the exact strict-decrease gate, while the contraction reserve is

`1-q_h = h R_step / 2`.

A trusted checker does not need division or square roots.  It can verify the
rational inequalities

**(3.5)**

`h > 0`,

`2 - 2hc + h^2 K >= 0`,

`hK < 2c`.

The first quadratic expression is simply `2 q_h`, so (3.5) certifies
`0 <= q_h < 1` using addition, multiplication, and order only.

If `K<0`, the signed curvature is favorable and enlarges the step reserve.
Replacing `K` by an absolute Hessian bound may therefore create unnecessary
false negatives.

---

## 4. Affine bad charge and invariant Lyapunov level

For `a` or `b` nonzero, contraction to zero is generally not available.  The
correct target is an invariant energy level.

Assume

`q_h >= 0`

and let `Vstar >= 0` be a proposed sublevel radius.  From (2.3), every state with
`0 <= V0 <= Vstar` obeys

`V_plus <= q_h Vstar + r_h`.

Therefore the full sublevel `{V <= Vstar}` is one-step invariant whenever

**(4.1)**

`q_h Vstar + r_h <= Vstar`.

After multiplying out the common factor `h/2`, (4.1) is exactly the
**division-free gate**

**(4.2)**

`2a + h b <= (2c - hK) Vstar`.

Strict `<` gives a strict one-step inward reserve.

This is stronger and safer than checking only that the boundary vector points
inward.  For a discrete map, a state in the interior can jump across the
boundary in one step.  The monotone affine recurrence (2.3) plus `q_h>=0` is
what upgrades the boundary arithmetic into a whole-sublevel statement.

Define

**(4.3)**

`R_bar := (2c-hK)Vstar - (2a+h b)`.

Then `R_bar>0` is the exact cleared invariant-level reserve supplied by this
packet.

When `a,b>=0`, (4.2) with `Vstar>0` automatically forces `2c-hK>0`, hence the
same step has a genuine relative reserve as well.

---

## 5. Scalar linear regression: the threshold is sharp

Take the autonomous scalar system

`ydot = -lambda y`, `lambda>0`,

with storage

`V(y)=y^2`.

Then

`D V[f] = -2 lambda V`,

so (2.1) is exact with

`c = 2 lambda`, `a=0`.

Also

`D^2 V[f,f] = 2 lambda^2 V`,

so (2.2) is exact with

`K = 2 lambda^2`, `b=0`.

The theorem gives

`q_h = 1 - 2h lambda + h^2 lambda^2`

`    = (1-h lambda)^2`.

But explicit Euler is exactly

`y_plus = (1-h lambda)y`,

hence

**(5.1)** `V_plus = (1-h lambda)^2 V`.

So every coefficient in the Taylor closure is attained exactly.

The gate `hK<2c` becomes

`2h lambda^2 < 4 lambda`,

or

**(5.2)** `h lambda < 2`.

This is exactly the strict energy-stability boundary of scalar explicit Euler.
At `h lambda=2`, `V_plus=V`; above it, the storage grows.

Therefore neither the factor `1/2` in the curvature charge nor the threshold
`hK<2c` can be improved in general from only hypotheses (2.1)-(2.2).

---

## 6. Counterexample: continuous-time dissipation alone is insufficient

The same scalar system with `lambda=1` gives

`D V[f] = -2V < 0`

for every nonzero state.

Choose the perfectly exact Euler step `h=3`.  Then

`y_plus = -2y`

and therefore

**(6.1)** `V_plus = 4V`.

Thus even a globally strict continuous-time Lyapunov derivative does **not**
imply finite-step decay for an explicit discretization.  Any checker rule of
the form

`continuous derivative is negative => Euler step contracts`

without a curvature/step-size charge is mathematically false.

The missing information is exactly the second-order chord term in (1.1).

---

## 7. Counterexample: a start-point Hessian sample is not enough

It is also unsafe to inspect the curvature only at the beginning of the step.

Take on `[0,1]`

`V(x) = 1 - x + 2x^4`,

with frozen step direction `g=1`, base point `x=0`, and `h=1`.

The storage stays positive on this interval.  At the start,

`V(0)=1`,

`V'(0)=-1`,

`V''(0)=0`.

A start-only second-order check would see a favorable first derivative and zero
curvature.  However

**(7.1)** `V(1)=2 > V(0)`.

The missing curvature is on the interior of the chord:

`V''(x)=24x^2`.

Therefore (2.2) must be a same-segment certificate, or be replaced by some
other theorem genuinely controlling the integral remainder.  Sampling the
Hessian at the starting point is not a proof.

This is exactly why this child consumes step-segment coverage as a premise.

---

## 8. Important distinction: Euler-chord curvature is not `L_f^2 V`

A second tempting shortcut is to insert the second material derivative along
the **true flow** in place of the frozen Euler-chord Hessian.

For an autonomous system,

`L_f^2 V = D^2 V[f,f] + D V[D f * f]`.

The extra acceleration term `D V[D f*f]` belongs to the curved true trajectory.
It is absent from the affine Euler chord.  Therefore `L_f^2 V` is not generally
a valid replacement for `D^2V[f,f]` in (1.1).

A scalar exact regression makes the distinction explicit.  Let

`V(y)=y^2`,

`f(y)=y-1`,

and start at `y=1/2`.

Then

`L_f V = -1/2 < 0`,

while

`L_f^2 V = 0`

at the starting point because the flow-acceleration term cancels the Hessian
term.  Yet the frozen Euler direction is `g=-1/2`, so

`D^2V[g,g] = 1/2 > 0`.

With `h=3`, explicit Euler gives

`y_plus = -1`

and hence

`V_plus = 1 > 1/4 = V`.

So a checker must use the actual numerical-step geometry.  True-flow second
material derivatives and Euler-chord second derivatives are different
certificates.

---

## 9. Source-facing packet

A minimal source packet for this child is:

1. base point `(t,y)` and exact/rational step size `h>0`;
2. the frozen Euler vector `g=f(t,y)` and direction `zeta=(1,g)`;
3. a proof that the full chord `p_s=(t,y)+sh zeta`, `0<=s<=1`, lies in the
   certified cell;
4. a starting material-storage inequality
   `D V(t,y)[zeta] <= -c V0 + a`;
5. a same-chord signed directional curvature bound
   `D^2V(p_s)[zeta,zeta] <= K V0+b`;
6. for pure contraction, the cleared checks
   `2-2hc+h^2K>=0` and `hK<2c`;
7. for an invariant level `Vstar`, the cleared check
   `2a+h b <= (2c-hK)Vstar`, together with `q_h>=0`.

The source should form the signed quantity

`D^2V[zeta,zeta]`

before interval absolute values.  A full Hessian operator norm is a valid
fallback, but it can discard helpful cancellations and produce a much smaller
permitted step.

For time-dependent storage, the source-facing curvature expression is the
explicit polynomial/bilinear combination (1.2), so no derivative of the
integrator vector field is required merely to certify an Euler chord.

---

## 10. Formalization-ready theorem statements

### Theorem A — `euler_chord_taylor_exact`

If `V` is `C^2` on the segment `p_s=p+s h zeta`, then

`V(p+h zeta)-V(p)`

`= h DV(p)[zeta]`

`+ h^2 int_0^1 (1-s) D^2V(p_s)[zeta,zeta] ds`.

### Theorem B — `euler_storage_affine_step_bound`

Under (2.1)-(2.2),

`V_plus <= (1-hc+h^2K/2)V0 + h a + h^2 b/2`.

### Theorem C — `euler_relative_contraction_cleared`

If `a=b=0`, `h>0`,

`2-2hc+h^2K >= 0`,

and

`hK < 2c`,

then there exists the explicit factor

`q_h=(2-2hc+h^2K)/2`

with

`0<=q_h<1`

and

`V_plus<=q_h V0`.

### Theorem D — `euler_sublevel_invariant_cleared`

Assume Theorem B, `q_h>=0`, `0<=V0<=Vstar`, and

`2a+h b <= (2c-hK)Vstar`.

Then

`V_plus<=Vstar`.

Strict inequality in the cleared gate gives a strict inward reserve at the
worst affine-envelope boundary.

### Regressions

- `scalar_linear_euler_threshold_sharp`: `V=y^2`, `f=-lambda y` gives exact
  factor `(1-hlambda)^2` and exact boundary `hlambda=2`.
- `continuous_dissipation_not_discrete_contraction`: `lambda=1,h=3` gives
  `V_plus=4V` despite `Vdot=-2V`.
- `start_hessian_sample_not_enough`: `V=1-x+2x^4`, `x=0`, `g=h=1` has
  `V'(0)<0`, `V''(0)=0`, but `V(1)>V(0)`.
- `flow_second_material_derivative_not_euler_chord`: `V=y^2`, `f=y-1` at
  `y=1/2` has `L_f^2V=0` while the Euler chord has positive curvature.

---

## 11. Failure branches and exact status

### `PASS_RELATIVE_EULER`

The same-chord hypotheses hold and the cleared strict gate

`hK < 2c`

passes, with `q_h>=0`.

### `PASS_INVARIANT_LEVEL`

The affine step bound holds and

`2a+h b <= (2c-hK)Vstar`

passes, with `q_h>=0`.

### `BOUNDARY_ONLY`

`hK = 2c` in the zero-offset branch gives no strict contraction reserve.  The
scalar linear example attains equality, so this boundary cannot be promoted.

### `NOT_CERTIFIED_STEP_TOO_LARGE`

The current curvature packet gives `hK >= 2c`.  This is not a proof that the
actual discrete map is unstable; it means only that this Taylor envelope cannot
certify strict relative contraction.  A sharper signed curvature bound or a
different integrator may still close the case.

### `NOT_CERTIFIED_SEGMENT`

The source has not proved that the Euler chord remains inside the cell on which
the curvature bound is valid.  Start-point data alone are insufficient by the
counterexample in Section 7.

### `WRONG_GEOMETRY`

A proposed proof substitutes true-flow `L_f^2V` or a start-only Hessian sample
for the frozen-chord integral remainder.  Such a certificate is invalid without
an additional theorem relating it to the Euler chord.

---

## 12. What this child closes and what remains open

Closed mathematically here:

- exact finite-step Taylor identity for time/state-dependent storage along an
  explicit-Euler chord;
- exact signed directional-curvature charge with the sharp `1/2` coefficient;
- division-free relative contraction gate `hK<2c`;
- exact affine one-step/sublevel gate
  `2a+h b <= (2c-hK)Vstar`;
- sharp scalar attainment of the explicit-Euler threshold;
- obstruction showing continuous-time dissipation alone is insufficient;
- obstruction showing start-only Hessian data are insufficient;
- obstruction separating true-flow second material derivative from numerical
  Euler-chord curvature.

Still open:

- deployed source generation for actual `(c,a,K,b,h,Vstar)`;
- step-segment/P8 physical coverage binding;
- numerical solve/controller/evaluator defects added to the Euler endpoint;
- higher-order Runge-Kutta or implicit integrators;
- a bootstrap theorem when curvature is bounded by the *moving segment energy*
  rather than the anchored starting energy;
- finite-separation/secant contraction beyond this scalar storage inequality;
- Float64/FD semantics;
- Lean/kernel implementation and `#print axioms`;
- independent verification by 封不觉;
- comparator/admission/registry changes.

Accordingly T-P5-092 is a **pending mathematical child / conditional pass**.
It does not itself upgrade P5/M4, coverage, admission, or deployed execution.