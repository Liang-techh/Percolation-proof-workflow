---
kind: review_result
review_id: review-T-P5-081-moving-affine-chart-kuangmanmozun-20260908T0842
task_id: T-P5-081-MOVING-AFFINE-CHART
agent: 狂蛮魔尊
source_agent: 狂蛮魔尊
created_at: 2026-09-08T08:42:00-06:00
claim_commit: 61dc6639c45bfa558305974e153340b2a27758f1
inspected_commits:
  - 8b36d94936707744a1c477696d406bff5bac536e
  - d56e196ca5833aa4db830984beb657f6739afd96
  - f0d1df5605088ee79b7416d61af04cf78c2d2f65
  - 91b6d1064d8f63a9ce8374006815cb39e07ccc8a
inspected_paths:
  - agent_review_inbox/review-T-P5-079-similarity-normalization-liuguanyi-20260908T0806.md
  - agent_review_inbox/review-T-P5-078-mixed-relative-additive-corrector-kuangmanmozun-20260908T0752.md
  - agent_review_inbox/review-T-P5-080-correlation-aware-mixed-defect-kuangmanmozun-20260908T0822.md
integration_status: pending
admission_label: pending
proposed_integration_target: theorem
requested_action: >-
  Insert this as the moving-chart extension of T-P5-079. A time/iteration-varying
  invertible scale is not itself an energy defect when the quadratic metric is
  transported by the same congruence. The only new additive term is the failure
  of the moving center/reference to follow the same physical flow/corrector.
  Feed that exact center-mismatch packet into T-P5-078/T-P5-080 rather than
  charging arbitrary scale-motion penalties. Keep source equality, deployed
  normalization, Float64/controller, coverage and admission open.
---

# T-P5-081 — moving affine chart: exact connection cancellation and center-mismatch gate

## 0. Result in one line

T-P5-079 proves that a **fixed** affine normalization

`x = c + S z`

preserves the weighted SCC certificate exactly when the residual and metric are
transported covariantly. It deliberately leaves moving/time-dependent `S` open.
The missing fact is sharper than a generic perturbation estimate:

> **A moving invertible scale costs exactly zero quadratic-energy reserve if the
> metric is co-moved by the same congruence. The only unavoidable chart-motion
> defect is the mismatch of the moving center/reference from the same physical
> flow or corrector map.**

This holds both for one-step correctors and continuous-time dynamics.

For the discrete corrector, let

`x = c + S z`,

`x_plus = x - h F_x(x)`,

and let the next chart be arbitrary

`x_plus = c_plus + S_plus z_plus`,

with `S,S_plus` invertible. Define the incremental normalized residual `G` by

**(0.1)** `F_x(c+Sz) - F_x(c) = S G(z)`.

Define the exact center-following corrector and the center mismatch

**(0.2)** `c_ref_plus = c - h F_x(c)`,

**(0.3)** `m = c_plus - c_ref_plus`.

Then the exact cleared identity is

**(0.4)**
`S_plus z_plus = S (z - h G(z)) - m`.

Let a fixed physical SPD weight be `W_x`, and co-move the chart metrics by

`W = S^T W_x S`,

`W_plus = S_plus^T W_x S_plus`.

Then

**(0.5)**
`Q_{W_plus}(z_plus)`
` = Q_{W_x}(S(z-hG)-m)`.

In particular, if the center follows the same exact corrector (`m=0`),

**(0.6)** `Q_{W_plus}(z_plus) = Q_W(z-hG)`

for **every** invertible `S_plus`. Thus an arbitrary change of scale between
steps has zero effect on the Lyapunov factor. There is no condition-number,
`||S_plus-S||`, derivative-of-scale, or small-gain penalty to pay.

If `m != 0`, it enters as one ordinary additive defect in the physical metric.
Suppose

`Q_W(z-hG) <= q V`,

`Q_{W_x}(m) <= D`,

where `V=Q_W(z)`, `q>=0`, `D>=0`. Then on a candidate barrier `Vstar>0`, the
independent-envelope robust gate is the exact radical-free condition

**(0.7)** `R = (1-q)Vstar - D > 0`,

**(0.8)** `4 q Vstar D < R^2`.

This is equivalent to

`sqrt(q Vstar) + sqrt(D) < sqrt(Vstar)`

and is sharp for the uncertainty class. Signed center/corrector correlation can
instead be consumed by T-P5-080.

The continuous-time analogue is equally clean. For

`x_dot = -F_x(t,x)`,

`x = c(t)+S(t)z`,

set

`r_c = c_dot + F_x(t,c)`

and require the incremental covariance

**(0.9)** `F_x(t,c+Sz)-F_x(t,c)=S G(t,z)`.

If `S A = S_dot` and `S b = r_c`, then

**(0.10)** `z_dot = -G - A z - b`.

With the co-moving metric

`W_z(t)=S(t)^T W_x S(t)`,

the connection term `A z` cancels **exactly** against `W_z_dot`:

**(0.11)**
`V_dot = -2 <G,z>_{W_z} - 2 <b,z>_{W_z}`,

where `V=Q_{W_z}(z)=Q_{W_x}(x-c)`.

Thus `S_dot` creates no Lyapunov penalty. If the center is an actual reference
trajectory of the same flow, `c_dot=-F_x(t,c)`, then `r_c=0`, `b=0`, and

**(0.12)** `V_dot = -2 <G,z>_{W_z}`.

The same strong-monotonicity rate therefore survives an arbitrary moving
invertible scale exactly.

If instead

`<G,z>_{W_z} >= mu V`, `mu>0`,

and

`Q_{W_z}(b)=Q_{W_x}(r_c) <= B`,

then any candidate level `Vstar>0` has strict inward vector field whenever

**(0.13)** `B < mu^2 Vstar`.

This gate is division-free and sharp. Equality is boundary-only, not strict.

The important distinction is therefore:

- **scale motion** `S -> S_plus` or `S_dot`: exact gauge/connection effect,
  cancelled by co-moving congruence metric;
- **center mismatch** from the same map/flow: a real additive forcing that must
  consume contraction reserve.

This is a mathematics/interface child only. It does not bind any deployed SCC,
source normalization, evaluator, Float64/FD/controller, root tracker, P8/ODE
coverage, Lean/kernel receipt, provenance, admission, registry state, or parent
closure.

---

## 1. Discrete moving-chart identity

Let the physical one-step map be

`x_plus = x - h F_x(x)`

with scalar `h>=0`. Write the current state as

`x=c+Sz`.

Subtract the same-map center update

`c_ref_plus=c-hF_x(c)`:

`x_plus-c_ref_plus`
` = x-c - h(F_x(x)-F_x(c))`
` = Sz - h S G(z)`
` = S(z-hG(z))`,

using (0.1).

Now allow the deployed next center `c_plus` to differ from the same-map center
by

`m=c_plus-c_ref_plus`.

Then

`x_plus-c_plus`
` = x_plus-c_ref_plus - m`
` = S(z-hG)-m`.

Because the next chart satisfies

`x_plus-c_plus=S_plus z_plus`,

we obtain the multiplication-only identity

### Theorem 1.1 — moving affine corrector transport

**(1.1)** `S_plus z_plus = S(z-hG)-m`.

No inverse is required in the trusted statement. Analytically one may solve for
`z_plus`, but a checker can remain entirely on the cleared equality.

### Exact energy transport

Let

`W=S^T W_x S`,

`W_plus=S_plus^T W_x S_plus`.

Then by T-P5-079's congruence identity,

`Q_{W_plus}(z_plus)`
` = Q_{W_x}(S_plus z_plus)`
` = Q_{W_x}(S(z-hG)-m)`.

If `m=0`,

`Q_{W_plus}(z_plus)`
` = Q_{W_x}(S(z-hG))`
` = Q_W(z-hG)`.

The matrix `S_plus` has disappeared completely.

### Corollary 1.2 — exact factor invariance under arbitrary scale update

If

`Q_W(z-hG) <= q Q_W(z)`,

then for `m=0`,

`Q_{W_plus}(z_plus) <= q Q_W(z)`

with exactly the same numerical `q`, for every invertible `S_plus`.

Thus a changing normalization is harmless at theorem level if the next metric
is transported with it.

---

## 2. Why freezing the metric fabricates fake contraction or expansion

A moving chart without the co-moving metric is not merely conservative; it can
produce completely fictitious energy behavior.

Take one physical dimension, `W_x=1`, no physical dynamics, and fixed center
`c=0`. Let

`x_plus=x=1`.

At the current step choose `S=1`, hence `z=1` and `W=1`. At the next step choose

`S_plus=2`.

Then `z_plus=1/2`.

If one incorrectly keeps the old normalized metric `1`, the reported energy is

`z_plus^2=1/4`,

which looks like a factor-four contraction despite the physical state being
unchanged.

But the correct transported metric is

`W_plus=S_plus^2=4`,

so

`Q_{W_plus}(z_plus)=4*(1/2)^2=1`,

exactly the unchanged physical energy.

Reverse the scale and take `S_plus=1/2`. The same frozen-metric mistake reports
`z_plus^2=4`, a factor-four expansion. Therefore chart-scale motion can fake
arbitrarily strong contraction or expansion unless the metric moves by the same
congruence.

This is a structural counterexample: no amount of tighter scalar estimation can
repair a metric/chart mismatch.

---

## 3. Discrete center mismatch is exactly an additive defect

Set

`a_phys := S(z-hG)`.

Then (0.5) is simply

`V_plus = Q_{W_x}(a_phys-m)`.

Assume on the barrier `V<=Vstar` that

`Q_{W_x}(a_phys) <= q Vstar`,

`Q_{W_x}(m) <= D`.

The worst independent-envelope value is

`(sqrt(q Vstar)+sqrt(D))^2`.

Rather than forming radicals, define

`R=(1-q)Vstar-D`.

For nonnegative `q,D,Vstar`,

`(sqrt(qVstar)+sqrt(D))^2 < Vstar`

is equivalent to

`R>0`

and

`4qVstar D < R^2`.

Hence:

### Theorem 3.1 — moving-center barrier gate

Assume

- `q>=0`, `D>=0`, `Vstar>0`;
- `Q_W(z-hG)<=qVstar` on `Q_W(z)<=Vstar`;
- `Q_{W_x}(m)<=D`;
- `R=(1-q)Vstar-D>0`;
- `4qVstar D<R^2`.

Then

`Q_{W_plus}(z_plus)<Vstar`.

This is exactly the T-P5-078/T-P5-075 additive-error geometry with the
**center-tracking error** as the additive packet. It must not be charged once as
"chart motion" and again as evaluator error if they are the same physical
quantity.

### Sharpness

In one dimension take `W_x=1`, choose admissible vectors with

`a_phys=-sqrt(qVstar)`, `m=+sqrt(D)`.

Then

`|a_phys-m|=sqrt(qVstar)+sqrt(D)`,

so the bound is attained. Without signed correlation information, no smaller
uniform barrier can follow from the two norm envelopes.

If a source theorem proves the sign/correlation of `<a_phys,m>`, use T-P5-080
instead of this independent-envelope gate.

---

## 4. Same-map center update is the exact discrete cancellation condition

The condition `m=0` has a direct operational meaning:

`c_plus = c - h F_x(c)`.

The moving center need not be a fixed equilibrium. It only needs to be advanced
by the **same exact corrector map** as the state reference.

Then

`x_plus-c_plus`
` = (x-c)-h(F_x(x)-F_x(c))`,

so all translation disappears from the difference dynamics.

This matters when a source pipeline tracks a moving nominal state rather than a
static root. Requiring `F_x(c)=0` is unnecessarily restrictive; what matters for
incremental contraction is same-map transport of the reference.

Conversely, being an instantaneous root is not enough if the center is moved by
some external rule.

### Counterexample — instantaneous root path still injects bias

Take the scalar nonautonomous field

`F_x(t,x)=x-c(t)`

with `c(t)=t` and physical flow

`x_dot=-F_x(t,x)=-(x-t)`.

For every time `t`, `c(t)` is an exact instantaneous root because

`F_x(t,c(t))=0`.

But the centered variable `y=x-c(t)` satisfies

`y_dot=-y-1`.

Thus the moving root contributes the persistent bias `-1`. The fact
`F_x(t,c(t))=0` does **not** cancel `c_dot`.

The exact cancellation condition is instead

`c_dot=-F_x(t,c)`,

i.e. the reference is itself a trajectory of the same physical flow.

---

## 5. Continuous-time moving chart and exact connection cancellation

Let

`x_dot=-F_x(t,x)`

and introduce a differentiable moving affine chart

`x=c(t)+S(t)z`,

where every `S(t)` is invertible.

Differentiate:

`x_dot=c_dot+S_dot z+S z_dot`.

Subtract and add `F_x(t,c)`:

`c_dot+S_dot z+S z_dot`
` = -[F_x(t,c+Sz)-F_x(t,c)] - F_x(t,c)`.

Assume the incremental covariance

`F_x(t,c+Sz)-F_x(t,c)=S G(t,z)`.

Define the center mismatch

`r_c=c_dot+F_x(t,c)`.

Then

**(5.1)**
`S z_dot = -S G - S_dot z - r_c`.

A trusted checker can stop here. If one additionally names `A,b` by the cleared
relations

`S A=S_dot`,

`S b=r_c`,

then

`z_dot=-G-Az-b`.

Now define the co-moving metric

`W_z=S^T W_x S`.

Its derivative is

`W_z_dot=S_dot^T W_x S + S^T W_x S_dot`.

Set

`V=z^T W_z z`.

Then

`V_dot`
` = 2<z_dot,z>_{W_z} + z^T W_z_dot z`
` = -2<G,z>_{W_z}`
`   -2<Az,z>_{W_z}`
`   -2<b,z>_{W_z}`
`   +2<S_dot z,Sz>_{W_x}`.

Because `S A=S_dot`,

`<Az,z>_{W_z}`
` = <S A z,Sz>_{W_x}`
` = <S_dot z,Sz>_{W_x}`.

Therefore the two scale-motion terms cancel exactly:

### Theorem 5.1 — moving-scale connection cancellation

**(5.2)**
`V_dot=-2<G,z>_{W_z}-2<b,z>_{W_z}`.

Equivalently, without introducing `A,b`,

`V=Q_{W_x}(x-c)`

and

`V_dot`
` = -2 <F_x(t,x)-F_x(t,c),x-c>_{W_x}`
`   -2 <r_c,x-c>_{W_x}`.

No `S_dot` term survives.

### Corollary 5.2 — moving reference trajectory preserves the rate exactly

If

`c_dot=-F_x(t,c)`,

then `r_c=0` and

`V_dot=-2<G,z>_{W_z}`.

If additionally

`<G,z>_{W_z}>=mu V`,

then

`V_dot<=-2mu V`

with the same `mu` as in the fixed chart. Arbitrarily fast but differentiable
scale motion does not alter the rate, provided the congruence metric is moved
exactly with the chart.

---

## 6. Continuous center-mismatch barrier and sharp floor

Assume

`<G,z>_{W_z}>=mu V`, `mu>0`,

and

`Q_{W_z}(b)=Q_{W_x}(r_c)<=B`.

By weighted Cauchy,

`-<b,z>_{W_z} <= sqrt(BV)`.

Hence

**(6.1)** `V_dot <= -2mu V + 2sqrt(BV)`.

On the boundary `V=Vstar>0`, strict inward pointing follows from

`mu Vstar > sqrt(BVstar)`.

Because all quantities are nonnegative, this is equivalent to the square-only
gate

### Theorem 6.1 — division-free moving-center invariant level

**(6.2)** `B < mu^2 Vstar`.

No division or square root is needed by the trusted arithmetic layer.

Likewise a proposed non-strict asymptotic floor `Vfloor>0` is certified by

**(6.3)** `B <= mu^2 Vfloor`.

The familiar analytic floor `B/mu^2` need never be formed in the checker.

### Sharpness

Consider one dimension with

`y_dot=-mu y-r`,

`V=y^2`,

and `B=r^2`.

At the adverse boundary point

`y=-sign(r) sqrt(Vstar)`,

one has exactly

`V_dot=-2mu Vstar+2|r|sqrt(Vstar)`.

Therefore:

- if `B<mu^2Vstar`, the boundary is strictly inward;
- if `B=mu^2Vstar`, the adverse boundary has `V_dot=0` exactly;
- if `B>mu^2Vstar`, that boundary point is outward.

So (6.2) is sharp for the independent norm-envelope uncertainty class.

Example: `mu=1`, `r=1`, `Vstar=1` is exactly boundary-only. At `y=-1`,
`V_dot=0`. For `Vstar=1/4`, at `y=-1/2`,

`V_dot=-1/2+1=1/2>0`,

so the smaller level is not invariant.

---

## 7. Optional signed refinement

The norm-only mismatch bound is not always optimal. If the source can prove a
signed relative cross theorem

`<b,z>_{W_z} >= -eta V`

on the same cell, then Theorem 5.1 gives directly

`V_dot <= -2(mu-eta)V`.

Thus `eta<mu` restores pure exponential decay without a positive floor.

This is the continuous-time analogue of T-P5-080's correlation-aware branch.
As there, sampled/favorable signs are not enough: the lower bound must be proved
on the full source cell in the same weight.

---

## 8. Counterexample to a generic "scale-velocity penalty"

A common safe-looking but mathematically wasteful route would bound

`||S^{-1}S_dot||`

and subtract a generic penalty from `mu`.

That can be arbitrarily pessimistic. Take a constant physical deviation
`y=x-c`, no residual dynamics, and any differentiable invertible `S(t)` with
`y=S(t)z(t)`. Then the normalized state obeys exactly the connection equation

`z_dot=-S^{-1}S_dot z`.

The connection norm can be arbitrarily large. Nevertheless the physical energy

`Q_{W_x}(y)`

is exactly constant, and the co-moving normalized energy

`Q_{S^T W_x S}(z)`

is the same constant. The apparent connection growth/decay cancels with metric
motion identically.

Therefore a theorem that pays an unsigned `||S^{-1}S_dot||` tax while also
using the exact co-moving metric is strictly weaker than necessary. Such a tax
is justified only if the metric itself is frozen/approximated or if the chart
transport identity is defective.

---

## 9. Exact interface to T-P5-078 and T-P5-080

The discrete center mismatch

`m=c_plus-[c-hF_x(c)]`

is not a new error species. After exact moving-chart transport it is simply the
additive vector in

`S_plus z_plus = a_phys-m`.

Therefore:

1. if only `Q(m)<=D` is known, use T-P5-078/T-P5-075's independent-envelope
   additive barrier with this exact `D`;
2. if source analysis proves `<a_phys,m>` or a normalized equivalent, use
   T-P5-080's signed correlation gate;
3. do not add a separate `||S_plus-S||` fee when `W_plus=S_plus^T W_x S_plus`
   is exact;
4. do not double-charge `m` if the same center-tracking error is already present
   in an evaluator/controller defect packet.

For continuous time the analogous source quantity is

`r_c=c_dot+F_x(t,c)`.

The scale derivative `S_dot` is structural and cancels; `r_c` is the genuine
bias packet.

---

## 10. Minimal checker-facing contract

A moving discrete chart needs only:

1. current exact chart `x=c+Sz`;
2. next exact chart `x_plus=c_plus+S_plus z_plus`;
3. invertibility of `S,S_plus` (or a source proof that both charts are valid);
4. incremental covariance
   `F_x(c+Sz)-F_x(c)=S G(z)`;
5. same physical fixed weight `W_x`;
6. congruence metrics
   `W=S^T W_x S`, `W_plus=S_plus^T W_x S_plus`;
7. exact center mismatch
   `m=c_plus-[c-hF_x(c)]`.

The principal theorem can be checked from the multiplication-only equality

`S_plus z_plus=S(z-hG)-m`.

For continuous time add:

8. differentiability of `c,S`;
9. `r_c=c_dot+F_x(t,c)`;
10. optionally cleared factors `S A=S_dot`, `S b=r_c`.

No inverse, condition number, spectral recomputation, or square root is needed
for the exact transport. Scalar strictness gates use only multiplication,
squares, addition, and order.

---

## 11. Suggested formalization leaves

Small theorem candidates:

1. `moving_affine_corrector_cleared`
   - derive `Splus*zplus=S*(z-h*G)-m`.

2. `moving_affine_energy_transport`
   - congruence turns the cleared state identity into (0.5).

3. `moving_scale_zero_cost_of_center_exact`
   - `m=0` implies exact factor invariance independent of `Splus`.

4. `moving_center_barrier_sq_gate`
   - prove the radical-free discrete gate (0.7)-(0.8).

5. `moving_chart_differential_cleared`
   - derive `S*zdot=-S*G-Sdot*z-r_c`.

6. `moving_metric_connection_cancel`
   - prove (5.2) from `Wz=S^T*Wx*S`, `S*A=Sdot`, `S*b=r_c`.

7. `reference_trajectory_exact_decay`
   - `r_c=0` preserves the original strong-monotonicity rate.

8. `moving_center_invariant_level_sq_gate`
   - from `B<mu^2*Vstar`, derive strict inward boundary.

9. `instantaneous_root_not_reference_trajectory_regression`
   - `F(t,x)=x-t`, `c=t` yields `y_dot=-y-1`.

10. `frozen_metric_fake_contraction_regression`
    - `S=1`, `Splus=2`, physical identity map: frozen metric reports `1/4`,
      congruence metric reports `1`.

---

## 12. Boundaries deliberately left open

This review does not prove:

- that deployed P5 uses a moving affine chart at all;
- exact source identities for `c,S,S_plus,c_dot,S_dot`;
- that an implementation updates its reference by the same corrector/flow;
- a concrete bound on center mismatch `m` or `r_c`;
- chart approximation or metric approximation errors;
- nonlinear/state-dependent charts `x=T(t,z)` whose Jacobian depends on `z`;
- state-dependent physical metrics `W_x(x,t)`;
- Float64/outward rounding, FD, controller, linear solve, or evaluator errors;
- root existence/uniqueness, source-domain coverage, P8/ODE first-exit coverage;
- Lean/kernel compilation, provenance, admission, registry mutation, or P5/M4
  closure.

Nonlinear charts remain genuinely different: the state-dependent Jacobian and
its derivatives cannot in general be removed by one constant congruence. This
review only closes the **moving affine** case.

---

## 13. Proposed downstream route

The safe moving-chart chain is

`physical corrector/flow`
` -> current/next affine charts`
` -> incremental residual covariance`
` -> co-moving congruence metrics`
` -> exact cancellation of scale motion`
` -> isolate center mismatch only`
` -> T-P5-078 independent additive gate OR T-P5-080 signed correlation gate`
` -> invariant-ball / contraction consumer`.

The main mathematical rule is:

**Do not pay for coordinate motion twice. Co-move the metric, cancel the scale
connection exactly, and spend reserve only on the reference-center mismatch
that remains after subtracting the same physical map.**